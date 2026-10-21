"""Use case: distil a power-flow surrogate from a solver-labelled dataset (spec 029, ADR-0011).

The physics teacher is the own solver recorded in the dataset manifest (engine, version and
the manifest digest); model weights are written outside Git (``local-data``) and identified
by their SHA-256 in the evidence. Technical acceptance stays ``False``.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from unitesis_evidence.store import publish_evidence

# Declared candidate grid for model selection on the validation split (T029-K06).
SELECTION_GRID: tuple[dict[str, Any], ...] = (
    {"architecture": "graphsage", "teacher_hidden": 64, "teacher_layers": 4},
    {"architecture": "impedance", "teacher_hidden": 32, "teacher_layers": 6},
    {"architecture": "impedance", "teacher_hidden": 64, "teacher_layers": 8},
)


def run_pf_distillation(dataset_dir: str | Path, output: str | Path, models_dir: str | Path,
                        *, select: bool = False, **spec_overrides: Any) -> dict[str, Any]:
    import torch  # optional dependency: imported only when distillation is requested
    from unitesis_sciml.distillation import (
        DistillationSpec,
        TeacherProvenance,
        load_feeder_graphs,
        run_distillation,
        select_by_validation,
    )

    dataset = Path(dataset_dir)
    raw = json.loads((dataset / "manifest.json").read_text(encoding="utf-8"))
    manifest = raw.get("payload", raw)
    manifest_sha = raw.get("payload_sha256")
    if not manifest_sha:
        raise ValueError("dataset manifest is not verified evidence (payload_sha256 missing)")
    engine = manifest["engine"]
    physics = TeacherProvenance(engine["name"], "own_physics_solver", engine["version"],
                                manifest_sha)
    graphs, _ = load_feeder_graphs(dataset)
    if not any(g.split == "train" for g in graphs):
        raise ValueError("dataset has no training feeders")
    spec = DistillationSpec(**spec_overrides)
    selection = None
    if select:
        candidates = [DistillationSpec(**{**spec_overrides, **c}) for c in SELECTION_GRID]
        spec, selection = select_by_validation(graphs, candidates)
    report, models = run_distillation(graphs, spec, physics)
    report["selection"] = {"criterion": "lowest validation p95; test never consulted",
                           "candidates": selection} if selection else None
    out_models = Path(models_dir)
    out_models.mkdir(parents=True, exist_ok=True)
    for name, model in models.items():
        torch.save(model.state_dict(), out_models / f"{name}.pt")
    payload = {
        "schema": "unitesis.distillation-evidence/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "case_id": manifest.get("case_id"),
        "dataset_id": manifest.get("dataset_id"),
        "dataset_manifest_sha256": manifest_sha,
        "report": report,
        "models_dir": str(out_models),
        "technical_acceptance": False,
        "limitations": [
            "surrogates prioritise scenarios; every decision is confirmed by the own solver",
            "balanced positive-sequence labels; phase-frame labels (008-C) not yet distilled",
            "teachers restricted to the own solver and own models (ADR-0011)",
        ],
    }
    return publish_evidence(output, payload)
