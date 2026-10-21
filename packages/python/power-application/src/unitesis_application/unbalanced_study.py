"""Use case: phase-frame study (spec 008-C) -> verified evidence.

The own three-phase engine computes; there is no installed independent engine for
arbitrary unbalanced snapshots yet, so the comparison is ``unavailable`` with the reason,
never a faked pass. The engine itself is validated by
``benchmarks/power-flow/unbalanced-results.json`` (IEEE 13 published voltages and
equivalence with the balanced Newton-Raphson).
"""

from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from unitesis_adapters.neutral_json import ingest_file
from unitesis_domain import SolverSettings, StudyRequest
from unitesis_evidence.store import canonical, publish_evidence
from unitesis_simulation import ThreePhaseEngine

from .study import code_manifest

LIMITATIONS = [
    "phase frame: Kron-reduced line matrices, YNyn0 transformers, fixed-tap ideal regulators, "
    "ZIP loads (wye/delta)",
    "no automatic regulator control (line-drop compensation) and no Dyn transformers yet",
    "no independent phase-frame reference engine installed: comparison unavailable per study; "
    "engine validated by the unbalanced benchmark",
    "source parameters are explicit but not externally certified",
    "technical and regulatory acceptance require human review",
]
NO_REFERENCE = ("no independent phase-frame reference engine installed; see "
                "benchmarks/power-flow/unbalanced-results.json for the engine validation")


def run_unbalanced_study(source: str | Path, output: str | Path, *, scenario_id: str = "base",
                         positive_sequence_lines: bool = False,
                         settings: SolverSettings | None = None) -> dict[str, Any]:
    """Raises ``IngestionError`` when the source is quarantined."""
    ingestion = ingest_file(source)
    snapshot = ingestion.require_snapshot()
    engine = ThreePhaseEngine(positive_sequence_lines=positive_sequence_lines)
    request = StudyRequest(snapshot.content_sha256, scenario_id, engine.name,
                           settings or SolverSettings())
    result = engine.solve(snapshot, request)
    payload = {
        "schema": "unitesis.unbalanced-study-evidence/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "scenario_id": scenario_id,
        "snapshot_sha256": snapshot.content_sha256,
        "snapshot": snapshot.canonical(),
        "source_manifest": ingestion.manifest,
        "code_tree_sha256": sha256(canonical(code_manifest())).hexdigest(),
        "status": result.status,
        "candidate": result.as_dict() | {"result_sha256": result.result_sha256},
        "reference": None,
        "comparison": {"status": "unavailable", "reason": NO_REFERENCE},
        "technical_acceptance": False,
        "regulatory_acceptance": False,
        "limitations": LIMITATIONS,
    }
    return publish_evidence(output, payload)
