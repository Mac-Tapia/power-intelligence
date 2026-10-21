"""Read-only API over imported real networks and their source geometry (spec 003).

Independent ``APIRouter`` so the platform owner wires it with one line and its own
authentication dependencies:

    app.include_router(create_networks_router(ROOT / "local-data/networks"),
                       dependencies=[...])

Only ids listed in a verified import report are served (no path traversal), the report is
re-read with its digest, and per-load customer attributes are never exposed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from unitesis_evidence.store import EvidenceError, read_evidence

_ID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.")


def _safe_id(value: str) -> str:
    if not value or not set(value) <= _ID_CHARS or ".." in value:
        raise HTTPException(404, "not found")
    return value


def create_networks_router(networks_root: str | Path) -> APIRouter:
    root = Path(networks_root)
    router = APIRouter(prefix="/api/v1/networks", tags=["networks"])

    def report(case_id: str) -> dict[str, Any]:
        path = root / _safe_id(case_id) / "import_report.json"
        if not path.is_file():
            raise HTTPException(404, "case has no imported network")
        try:
            return read_evidence(path)
        except EvidenceError as exc:
            raise HTTPException(409, "import report failed integrity check") from exc

    def feeder_row(case_id: str, network_id: str) -> dict[str, Any]:
        rows = {r["network_id"]: r for r in report(case_id)["feeders"]}
        row = rows.get(_safe_id(network_id))
        if row is None or not row.get("snapshot_file"):
            raise HTTPException(404, "feeder not validated in this import")
        return row

    @router.get("")
    def list_cases() -> list[dict[str, Any]]:
        out = []
        if root.is_dir():
            for d in sorted(p for p in root.iterdir() if (p / "import_report.json").is_file()):
                try:
                    rep = read_evidence(d / "import_report.json")
                except EvidenceError:
                    continue
                out.append({"case_id": rep["case_id"], "parser": rep.get("parser"),
                            "summary": rep.get("summary")})
        return out

    @router.get("/{case_id}/feeders")
    def list_feeders(case_id: str) -> list[dict[str, Any]]:
        return [{k: r.get(k) for k in ("network_id", "state", "nominal_kv", "counts",
                                       "non_three_phase_sections", "quarantine_reasons",
                                       "snapshot_sha256", "geometry_extent")}
                for r in report(case_id)["feeders"]]

    @router.get("/{case_id}/feeders/{network_id}")
    def get_feeder(case_id: str, network_id: str) -> dict[str, Any]:
        row = feeder_row(case_id, network_id)
        return json.loads((root / case_id / row["snapshot_file"]).read_text(encoding="utf-8"))

    @router.get("/{case_id}/feeders/{network_id}/geometry")
    def get_geometry(case_id: str, network_id: str) -> dict[str, Any]:
        row = feeder_row(case_id, network_id)
        if not row.get("geometry_file"):
            raise HTTPException(404, "no source geometry for this feeder")
        return json.loads((root / case_id / row["geometry_file"]).read_text(encoding="utf-8"))

    return router
