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
                        *, select: bool = False, cv_folds: int | None = None,
                        **spec_overrides: Any) -> dict[str, Any]:
    import torch  # optional dependency: imported only when distillation is requested
    from unitesis_sciml.distillation import (
        DistillationSpec,
        TeacherProvenance,
        cross_validate,
        load_feeder_graphs,
        merge_validation_into_training,
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
    criterion = "lowest validation p95; test never consulted"
    if cv_folds:
        candidates = [DistillationSpec(**{**spec_overrides, **c}) for c in SELECTION_GRID]
        spec, selection = cross_validate(graphs, candidates, k=cv_folds)
        graphs = merge_validation_into_training(graphs)
        criterion = (f"group {cv_folds}-fold cross-validation over non-test feeders, lowest "
                     "mean p95; epochs = median early-stopping epoch; final fit on all "
                     "non-test feeders; test evaluated once")
    elif select:
        candidates = [DistillationSpec(**{**spec_overrides, **c}) for c in SELECTION_GRID]
        spec, selection = select_by_validation(graphs, candidates)
    report, models = run_distillation(graphs, spec, physics)
    report["selection"] = {"criterion": criterion,
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


def evaluate_in_domain(dataset_dir: str | Path, distillation_evidence: str | Path,
                       models_dir: str | Path, output: str | Path, *, v_min_pu: float,
                       margin_pu: float = 0.10) -> dict[str, Any]:
    """Re-score saved surrogates inside the declared domain ``V_prior >= v_min - margin``.

    The threshold comes from the case planning criterion, fixed before looking at results.
    """
    import torch
    from unitesis_sciml.distillation import (
        applicability_report,
        load_feeder_graphs,
        make_model,
    )

    raw = json.loads(Path(distillation_evidence).read_text(encoding="utf-8"))
    report = raw.get("payload", raw)["report"]
    spec = report["spec"]
    graphs, _ = load_feeder_graphs(dataset_dir)
    features = graphs[0].features.shape[-1]
    sizes = {"teacher": (spec["teacher_hidden"], spec["teacher_layers"]),
             "student": (spec["student_hidden"], spec["student_layers"]),
             "baseline_student": (spec["student_hidden"], spec["student_layers"])}
    threshold = v_min_pu - margin_pu
    results = {}
    for name, (hidden, layers) in sizes.items():
        model = make_model(spec["architecture"], features, hidden, layers)
        model.load_state_dict(torch.load(Path(models_dir) / f"{name}.pt", weights_only=True))
        model.eval()
        results[name] = applicability_report(model, graphs, "test", defer_below_pu=threshold,
                                             v_min_pu=v_min_pu)
    payload = {
        "schema": "unitesis.surrogate-domain-evaluation/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "distillation_evidence": str(distillation_evidence),
        "domain_rule": f"surrogate answers only when the linear prior min V >= {threshold:.3f} "
                       f"p.u. (planning v_min {v_min_pu} - margin {margin_pu}); otherwise the "
                       "own solver computes",
        "results": results,
        "technical_acceptance": False,
    }
    return publish_evidence(output, payload)


def run_screening_benchmark(dataset_dir: str | Path, distillation_evidence: str | Path,
                            models_dir: str | Path, output: str | Path, *,
                            split: str = "test",
                            iterations: tuple[int, ...] = (1, 2, 3, 5)) -> dict[str, Any]:
    """AC-029-S06: learned surrogate vs truncated physics, alone and as a warm start."""
    import time

    import numpy as np
    import torch
    from unitesis_sciml.distillation import load_feeder_graphs, make_model, predict
    from unitesis_sciml.physics_screening import FixedPointScreener
    from unitesis_sciml.surrogate_metrics import score_voltages

    raw = json.loads(Path(distillation_evidence).read_text(encoding="utf-8"))
    spec = raw.get("payload", raw)["report"]["spec"]
    graphs = [g for g in load_feeder_graphs(dataset_dir)[0] if g.split == split]
    model = make_model(spec["architecture"], graphs[0].features.shape[-1],
                       spec["teacher_hidden"], spec["teacher_layers"])
    model.load_state_dict(torch.load(Path(models_dir) / "teacher.pt", weights_only=True))
    model.eval()
    screeners = {g.network_id: FixedPointScreener(g.ybus.numpy()) for g in graphs}
    n_scen = sum(g.vm.shape[0] for g in graphs)

    def run(name: str, k: int, warm: bool) -> dict[str, Any]:
        true, pred, mismatch = [], [], []
        t0 = time.perf_counter()
        for g in graphs:
            p, q = g.features[..., 0].numpy(), g.features[..., 1].numpy()
            v0 = None
            if warm:
                with torch.no_grad():
                    out = predict(model, g.features, g).numpy()
                v0 = out[..., 0] * np.exp(1j * out[..., 1])
            res = screeners[g.network_id].refine(p, q, k, v0=v0)
            true.append(g.vm.numpy().ravel())
            pred.append(np.abs(res.v).ravel())
            mismatch.append(res.mismatch_pu)
        row = score_voltages(np.concatenate(true), np.concatenate(pred))
        row.update(method=name, physics_iterations=k, learned_warm_start=warm,
                   ms_per_scenario=(time.perf_counter() - t0) * 1e3 / n_scen,
                   max_mismatch_pu=float(np.concatenate(mismatch).max()))
        return row

    rows = [run(f"physics-k{k}", k, False) for k in iterations]
    rows += [run("learned", 0, True)]
    rows += [run(f"learned+physics-k{k}", k, True) for k in iterations if k <= 2]
    passing = [r for r in rows if r["gate_ac_006_02"] == "passed"]
    fastest = min(passing, key=lambda r: r["ms_per_scenario"]) if passing else None
    payload = {
        "schema": "unitesis.screening-benchmark/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "split": split, "feeders": sorted(g.network_id for g in graphs),
        "scenarios": n_scen, "learned_model": {"architecture": spec["architecture"],
                                               "hidden": spec["teacher_hidden"],
                                               "layers": spec["teacher_layers"]},
        "results": rows,
        "fastest_passing": fastest["method"] if fastest else None,
        "learned_alone_beats_physics": any(
            r["method"] == "learned" and r["gate_ac_006_02"] == "passed" for r in rows),
        "note": "physics = truncated Z-bus fixed point on the solver Y-bus, slack held; "
                "timings are single-thread CPU and include the learned inference",
        "technical_acceptance": False,
    }
    return publish_evidence(output, payload)
