"""Use cases: source -> snapshot -> study -> independent comparison -> verified evidence.

Composition lives here; no electrical equations and no engine internals. A missing
reference engine yields comparison ``unavailable``, never a faked pass. Technical and
regulatory acceptance stay ``False`` until human review (constitution V).
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from unitesis_adapters.neutral_json import IngestionResult, ingest_file
from unitesis_domain import ElectricalSnapshot, Load, SolverSettings, StudyRequest, StudyResult
from unitesis_evidence.store import canonical, publish_evidence
from unitesis_ports import EngineUnavailable, PowerFlowEngine
from unitesis_simulation import PandapowerEngine, RadialBFSEngine, compare_results

LIMITATIONS = [
    "balanced radial positive-sequence scope: one slack, PQ loads, series lines, ideal switches",
    "source parameters are explicit but not externally certified",
    "no SCADA, no native CYME/PowerFactory persistence",
    "technical and regulatory acceptance require human review",
]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[5]


def code_manifest(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    files = sorted((root / "packages/python").glob("*/src/**/*.py"))
    return {str(p.relative_to(root)).replace("\\", "/"): sha256(p.read_bytes()).hexdigest()
            for p in files}


def solve_and_compare(snapshot: ElectricalSnapshot, scenario_id: str, *,
                      candidate: PowerFlowEngine | None = None,
                      reference: PowerFlowEngine | None = None,
                      settings: SolverSettings | None = None) -> dict[str, Any]:
    candidate = candidate or RadialBFSEngine()
    reference = reference if reference is not None else PandapowerEngine()
    settings = settings or SolverSettings()
    req_c = StudyRequest(snapshot.content_sha256, scenario_id, candidate.name, settings)
    cand_result = candidate.solve(snapshot, req_c)
    ref_result: StudyResult | None = None
    try:
        req_r = StudyRequest(snapshot.content_sha256, scenario_id, reference.name, settings)
        ref_result = reference.solve(snapshot, req_r)
        if cand_result.status == "computed" and ref_result.status == "computed":
            comparison = compare_results(ref_result, cand_result, snapshot)
        else:
            comparison = {"status": "failed", "issues": [
                {"metric": "status", "detail": f"candidate={cand_result.status} "
                                               f"reference={ref_result.status}"}]}
    except EngineUnavailable as exc:
        comparison = {"status": "unavailable", "reason": str(exc)}
    return {"candidate": cand_result, "reference": ref_result, "comparison": comparison}


def _payload(snapshot: ElectricalSnapshot, manifest: dict[str, Any], run: dict[str, Any],
             scenario_id: str) -> dict[str, Any]:
    cm = code_manifest()
    cand: StudyResult = run["candidate"]
    ref: StudyResult | None = run["reference"]
    return {
        "schema": "unitesis.study-evidence/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "scenario_id": scenario_id,
        "snapshot_sha256": snapshot.content_sha256,
        "snapshot": snapshot.canonical(),
        "source_manifest": manifest,
        "code_tree_sha256": sha256(canonical(cm)).hexdigest(),
        "status": cand.status,
        "candidate": cand.as_dict() | {"result_sha256": cand.result_sha256},
        "reference": (ref.as_dict() | {"result_sha256": ref.result_sha256}) if ref else None,
        "comparison": run["comparison"],
        "technical_acceptance": False,
        "regulatory_acceptance": False,
        "limitations": LIMITATIONS,
    }


def run_study(source: str | Path, output: str | Path, *, scenario_id: str = "base",
              reference: PowerFlowEngine | None = None) -> dict[str, Any]:
    """Full vertical; raises ``IngestionError`` when the source is quarantined."""
    ingestion: IngestionResult = ingest_file(source)
    snapshot = ingestion.require_snapshot()
    run = solve_and_compare(snapshot, scenario_id, reference=reference)
    return publish_evidence(output, _payload(snapshot, ingestion.manifest, run, scenario_id))


# --- Scenario: new customer connection (spec 002, cloned scenario only) ---------------

def with_new_load(snapshot: ElectricalSnapshot, load_id: str, bus: str,
                  p_mw: float, q_mvar: float) -> ElectricalSnapshot:
    """Return a cloned snapshot with an added load; the source snapshot is untouched."""
    snapshot.bus(bus)  # KeyError if absent: never attach to an inferred bus
    return replace(snapshot, loads=(*snapshot.loads, Load(load_id, bus, p_mw, q_mvar, True)))


def run_new_load_study(source: str | Path, output: str | Path, *, load_id: str, bus: str,
                       p_mw: float, q_mvar: float,
                       v_min_pu: float = 0.95, max_loading_percent: float = 100.0,
                       reference: PowerFlowEngine | None = None) -> dict[str, Any]:
    ingestion = ingest_file(source)
    before_snap = ingestion.require_snapshot()
    after_snap = with_new_load(before_snap, load_id, bus, p_mw, q_mvar)
    before = solve_and_compare(before_snap, "before", reference=reference)
    after = solve_and_compare(after_snap, f"after:{load_id}", reference=reference)

    def summary(res: StudyResult) -> dict[str, Any]:
        if res.status != "computed":
            return {"status": res.status, "messages": list(res.messages)}
        loadings = [b.loading_percent for b in res.branches if b.loading_percent is not None]
        return {"status": res.status,
                "min_vm_pu": min(b.vm_pu for b in res.buses),
                "max_loading_percent": max(loadings) if loadings else None,
                "loss_p_mw": res.total_loss_p_mw,
                "slack_p_mw": res.slack_p_mw}

    sb, sa = summary(before["candidate"]), summary(after["candidate"])
    violations: list[str] = []
    if sa["status"] == "computed":
        if sa["min_vm_pu"] < v_min_pu:
            violations.append(f"min voltage {sa['min_vm_pu']:.4f} pu < {v_min_pu}")
        loading = sa["max_loading_percent"]
        if loading is not None and loading > max_loading_percent:
            violations.append(f"loading {loading:.1f}% > {max_loading_percent}%")
    payload = {
        "schema": "unitesis.new-load-evidence/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source_manifest": ingestion.manifest,
        "request": {"load_id": load_id, "bus": bus, "p_mw": p_mw, "q_mvar": q_mvar,
                    "criteria": {"v_min_pu": v_min_pu,
                                 "max_loading_percent": max_loading_percent}},
        "before": {"snapshot_sha256": before_snap.content_sha256, "summary": sb,
                   "comparison": before["comparison"]},
        "after": {"snapshot_sha256": after_snap.content_sha256, "summary": sa,
                  "comparison": after["comparison"],
                  "result": after["candidate"].as_dict()},
        "screening": ("violations" if violations else "no_violation_detected")
        if sa["status"] == "computed" else "not_computed",
        "violations": violations,
        "technical_acceptance": False,
        "limitations": LIMITATIONS,
    }
    return publish_evidence(output, payload)
