"""Spec 004: the API and independent workers execute the same persisted request."""

from __future__ import annotations

from pathlib import Path

from unitesis_economics import parse_basis
from unitesis_optimization import SizingCriteria, load_catalog

from .alternatives import evaluate_conductor_alternatives
from .study import engine_by_name, solve_and_compare, with_new_load


def execute_persisted_job(repository, jobs, job_id: str, *, catalogs: Path) -> dict:
    if not jobs.claim(job_id):
        return jobs.get(job_id)
    try:
        job = jobs.get(job_id)
        request = job["request"]
        snapshot = repository.load_snapshot(request["snapshot_sha256"])
        if job["kind"] == "alternatives":
            # Resolve only a registered catalog, not an arbitrary path from the request.
            available = {p.stem: p for p in catalogs.glob("*.json")}
            catalog = load_catalog(available[request["catalog_id"]])
            if catalog.sha256 != request["catalog_sha256"]:
                raise ValueError("catalog changed since enqueue")
            criteria = SizingCriteria(request["operating_temperature_c"], request["phase_gmd_m"],
                                      request["v_min_pu"], request["max_loading_percent"])
            report = evaluate_conductor_alternatives(snapshot, line_id=request["line_id"],
                catalog=catalog, criteria=criteria, basis=parse_basis(request["economic_basis"]))
            return jobs.finish(job_id, {"study_status": "computed", "report": report})
        if job["kind"] == "new_load":
            snapshot = with_new_load(snapshot, **{k: request[k] for k in
                                     ("load_id", "bus", "p_mw", "q_mvar")})
            repository.save_snapshot(snapshot, {})
        # Legacy queued requests used BFS. New requests persist an explicit engine.
        run = solve_and_compare(snapshot, request["scenario_id"],
                                candidate=engine_by_name(request.get("engine", "bfs")))
        ids = [repository.save_result(run["candidate"])]
        if run["reference"] is not None:
            ids.append(repository.save_result(run["reference"]))
        return jobs.finish(job_id, {"scenario_snapshot_sha256": snapshot.content_sha256,
            "result_sha256": ids, "study_status": run["candidate"].status,
            "comparison": run["comparison"]["status"]})
    except Exception:
        return jobs.fail(job_id, "execution_failed")
