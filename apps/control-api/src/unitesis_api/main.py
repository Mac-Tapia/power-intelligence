"""Thin HTTP boundary over the application use cases (BACKEND-FRONTEND-BLUEPRINT contracts, subset).

No electrical computation in handlers: studies are queued as jobs and executed outside the
request (FastAPI background task for the local profile; a worker queue in production).
Jobs are persisted in the selected SQLite file; single API process only.
Authentication/tenant isolation are NOT implemented yet: the app refuses to start unless
``UNITESIS_LOCAL_ONLY=1`` is set, so it can never be exposed by accident.

  UNITESIS_LOCAL_ONLY=1 uvicorn unitesis_api.main:app --app-dir apps/control-api/src

The workstation UI (``apps/workstation-web/public``) is served at ``/`` by the same process.
"""

from __future__ import annotations

import json
import os
import uuid
from contextlib import asynccontextmanager
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from unitesis_adapters.job_repository import SqliteJobRepository
from unitesis_adapters.neutral_json import IngestionError, build_snapshot, parse_payload
from unitesis_adapters.sql_repository import SqliteRepository
from unitesis_application.job_execution import execute_persisted_job
from unitesis_economics import parse_basis
from unitesis_optimization import SizingCriteria, load_catalog
from unitesis_ports.protocols import JobRepository

from .telemetry import AuditMiddleware, RequestMetrics

API_VERSION = "0.2.0"
ROOT = Path(__file__).resolve().parents[4]
CATALOG_DIR = ROOT / "config/catalogs/conductors"
EXAMPLES_DIR = ROOT / "fixtures/networks"
BASIS_EXAMPLE = ROOT / "fixtures/economics/conductor_alternatives_synthetic.json"
UI_DIR = ROOT / "apps/workstation-web/public"


class StudyIn(BaseModel):
    snapshot_sha256: str = Field(min_length=64, max_length=64)
    scenario_id: str = Field(default="base", min_length=1, max_length=120)
    engine: Literal["bfs", "nr"] = "nr"


class NewLoadIn(StudyIn):
    load_id: str = Field(min_length=1, max_length=120)
    bus: str = Field(min_length=1)
    p_mw: float = Field(allow_inf_nan=False)
    q_mvar: float = Field(allow_inf_nan=False)


class AlternativesIn(StudyIn):
    line_id: str = Field(min_length=1, max_length=120)
    catalog_id: str = Field(min_length=1, max_length=120)
    operating_temperature_c: float
    phase_gmd_m: float
    v_min_pu: float = 0.95
    max_loading_percent: float = 100.0
    economic_basis: dict[str, Any]


def _json_files(folder: Path) -> dict[str, Path]:
    return {p.stem: p for p in sorted(folder.glob("*.json"))} if folder.is_dir() else {}


def _create_local_app(db_path: str | Path | None = None) -> FastAPI:
    if os.environ.get("UNITESIS_LOCAL_ONLY") != "1":
        raise RuntimeError("control-api has no auth yet; set UNITESIS_LOCAL_ONLY=1 for local use")
    database = db_path or os.environ.get("UNITESIS_DB", ":memory:")
    dsn = os.environ.get("UNITESIS_POSTGRES_DSN")
    if dsn:
        from unitesis_adapters.postgres_repository import PostgresJobRepository, PostgresRepository

        namespace = os.environ.get("UNITESIS_POSTGRES_NAMESPACE", "unitesis")
        if os.environ.get("UNITESIS_CREDENTIALS_FILE"):
            namespace = "tenant_" + sha256(str(Path(database).absolute()).encode()).hexdigest()[:24]
        repo = PostgresRepository(dsn, namespace=namespace)
        jobs: JobRepository = PostgresJobRepository(dsn, namespace=namespace)
    else:
        repo = SqliteRepository(database)
        jobs = SqliteJobRepository(database)
        jobs.recover_interrupted()
    execution_mode = os.environ.get("UNITESIS_EXECUTION_MODE", "background")
    if execution_mode not in {"background", "worker"}:
        repo.close()
        jobs.close()
        raise ValueError("invalid execution mode")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            yield
        finally:
            jobs.close()
            repo.close()

    app = FastAPI(title="UNITESIS control-api", version=API_VERSION, lifespan=lifespan)
    app.state.repository = repo
    app.state.jobs = jobs
    metrics = RequestMetrics()
    app.add_middleware(AuditMiddleware, metrics=metrics)

    @app.get("/api/v1/metrics")
    def request_metrics() -> dict[str, Any]:
        return metrics.snapshot()

    @app.exception_handler(RequestValidationError)
    async def invalid_request(_request: Request, exc: RequestValidationError) -> JSONResponse:
        # Pydantic error inputs may contain secrets or non-finite values that JSON
        # cannot encode. Return field locations and stable types, never input/ctx.
        return JSONResponse(status_code=422, content={"detail": [
            {"loc": list(error["loc"]), "type": error["type"], "msg": "Invalid request field"}
            for error in exc.errors()]})

    @app.get("/api/v1/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "version": API_VERSION, "auth": "local_only_not_implemented"}

    @app.get("/api/v1/snapshots")
    def list_snapshots() -> list[dict[str, Any]]:
        return repo.list_snapshots()

    @app.get("/api/v1/examples")
    def list_examples() -> list[str]:
        return list(_json_files(EXAMPLES_DIR))

    @app.get("/api/v1/examples/{name}")
    def get_example(name: str) -> dict[str, Any]:
        files = _json_files(EXAMPLES_DIR)
        if name not in files:
            raise HTTPException(404, "example not found")
        return json.loads(files[name].read_text(encoding="utf-8"))

    @app.get("/api/v1/economic-basis/example")
    def get_basis_example() -> dict[str, Any]:
        return json.loads(BASIS_EXAMPLE.read_text(encoding="utf-8"))

    @app.get("/api/v1/catalogs/conductors")
    def list_catalogs() -> list[dict[str, Any]]:
        out = []
        for cid, path in _json_files(CATALOG_DIR).items():
            cat = load_catalog(path)
            out.append({"catalog_id": cid, "name": cat.name, "sha256": cat.sha256,
                        "source_url": cat.source_url,
                        "conductors": [{"id": c.conductor_id, "section_mm2": c.section_mm2,
                                        "ampacity_a": c.ampacity_a}
                                       for c in cat.ordered_by_section()]})
        return out

    @app.post("/api/v1/snapshots", status_code=201)
    def import_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        try:
            parsed = parse_payload(raw)
        except IngestionError as exc:
            raise HTTPException(422, {"state": "rejected", "reason": str(exc)}) from exc
        result = build_snapshot(parsed, "api-upload")
        result.manifest.update(source_sha256=sha256(raw).hexdigest(), file_name=None)
        repo.save_source(result.manifest, result.quarantine)
        if result.snapshot is None:
            raise HTTPException(422, {"state": result.state,
                                      "quarantine": [q.as_dict() for q in result.quarantine]})
        key = repo.save_snapshot(result.snapshot, result.manifest)
        return {"state": result.state, "snapshot_sha256": key, "manifest": result.manifest}

    @app.get("/api/v1/snapshots/{snapshot_sha256}")
    def get_snapshot(snapshot_sha256: str) -> dict[str, Any]:
        try:
            snap = repo.load_snapshot(snapshot_sha256)
        except KeyError as exc:
            raise HTTPException(404, "snapshot not found") from exc
        return {"snapshot_sha256": snapshot_sha256, "snapshot": snap.canonical(),
                "results": repo.results_for_snapshot(snapshot_sha256)}

    def _enqueue(body: StudyIn, tasks: BackgroundTasks,
                 new_load: dict[str, Any] | None = None,
                 alternatives: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            repo.load_snapshot(body.snapshot_sha256)
        except KeyError as exc:
            raise HTTPException(404, "snapshot not found") from exc
        job_id = uuid.uuid4().hex
        kind = "alternatives" if alternatives else "new_load" if new_load else "study"
        request = body.model_dump()
        if alternatives:
            request["catalog_sha256"] = alternatives["catalog"].sha256
        job = jobs.enqueue(job_id, kind, request)
        if execution_mode == "background":
            tasks.add_task(execute_persisted_job, repo, jobs, job_id, catalogs=CATALOG_DIR)
        return job

    @app.post("/api/v1/studies", status_code=202)
    def create_study(body: StudyIn, tasks: BackgroundTasks) -> dict[str, Any]:
        return _enqueue(body, tasks)

    @app.post("/api/v1/studies/new-load", status_code=202)
    def create_new_load_study(body: NewLoadIn, tasks: BackgroundTasks) -> dict[str, Any]:
        return _enqueue(body, tasks, {"load_id": body.load_id, "bus": body.bus,
                                      "p_mw": body.p_mw, "q_mvar": body.q_mvar})

    @app.post("/api/v1/studies/conductor-alternatives", status_code=202)
    def create_alternatives_study(body: AlternativesIn,
                                  tasks: BackgroundTasks) -> dict[str, Any]:
        catalogs = _json_files(CATALOG_DIR)
        if body.catalog_id not in catalogs:
            raise HTTPException(404, "catalog not found")
        try:
            basis = parse_basis(body.economic_basis)
            criteria = SizingCriteria(body.operating_temperature_c, body.phase_gmd_m,
                                      body.v_min_pu, body.max_loading_percent)
        except ValueError as exc:
            raise HTTPException(422, {"state": "rejected", "reason": str(exc)}) from exc
        return _enqueue(body, tasks, alternatives={
            "line_id": body.line_id, "catalog": load_catalog(catalogs[body.catalog_id]),
            "criteria": criteria, "basis": basis})

    @app.get("/api/v1/jobs/{job_id}")
    def get_job(job_id: str) -> dict[str, Any]:
        try:
            return jobs.get(job_id)
        except KeyError as exc:
            raise HTTPException(404, "job not found") from exc

    @app.get("/api/v1/results/{result_sha256}")
    def get_result(result_sha256: str) -> dict[str, Any]:
        try:
            return repo.get_result(result_sha256)
        except KeyError as exc:
            raise HTTPException(404, "result not found") from exc

    if UI_DIR.is_dir():
        app.mount("/", StaticFiles(directory=UI_DIR, html=True), name="workstation")
    return app


def create_app(db_path: str | Path | None = None) -> FastAPI:
    if os.environ.get("UNITESIS_LOCAL_ONLY") != "1":
        raise RuntimeError("set UNITESIS_LOCAL_ONLY=1; external service deployment is disabled")
    credentials = os.environ.get("UNITESIS_CREDENTIALS_FILE")
    if credentials:
        from .security import create_secure_app

        default_db = str(ROOT / "local-data/unitesis.sqlite")
        database = db_path or os.environ.get("UNITESIS_DB", default_db)
        return create_secure_app(database, Path(credentials), _create_local_app, UI_DIR)
    return _create_local_app(db_path)


app = create_app() if os.environ.get("UNITESIS_LOCAL_ONLY") == "1" else None
