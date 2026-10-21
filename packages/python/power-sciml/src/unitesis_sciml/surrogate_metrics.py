"""Evaluation of power-flow surrogates against solver labels (spec 029, AC-029-S02/03/06).

Any surrogate (physics baseline, GNN, PINN) is scored with the same function so results are
comparable. Gate AC-029-S02: p95 absolute voltage error <= 0.005 pu and recall >= 0.99 for
under-voltage violations; with too few true violations in the evaluated set the gate is
reported as ``insufficient_violations`` instead of passing.
"""

from __future__ import annotations

from typing import Any

import numpy as np

P95_LIMIT_PU = 0.005
RECALL_MIN = 0.99
MIN_VIOLATIONS = 20


def score_voltages(vm_true: np.ndarray, vm_pred: np.ndarray, *, v_min_pu: float = 0.95
                   ) -> dict[str, Any]:
    t = np.asarray(vm_true, dtype=float).ravel()
    p = np.asarray(vm_pred, dtype=float).ravel()
    if t.shape != p.shape or t.size == 0:
        raise ValueError("vm_true and vm_pred must be non-empty and the same shape")
    if not (np.all(np.isfinite(t)) and np.all(np.isfinite(p))):
        raise ValueError("non-finite voltages cannot be scored")
    err = np.abs(p - t)
    true_v = t < v_min_pu
    pred_v = p < v_min_pu
    n_true = int(true_v.sum())
    recall = float((true_v & pred_v).sum() / n_true) if n_true else None
    precision = float((true_v & pred_v).sum() / pred_v.sum()) if pred_v.sum() else None
    p95 = float(np.percentile(err, 95))
    if n_true < MIN_VIOLATIONS:
        gate = "insufficient_violations" if p95 <= P95_LIMIT_PU else "failed"
    else:
        gate = "passed" if p95 <= P95_LIMIT_PU and recall >= RECALL_MIN else "failed"
    return {"nodes_scored": int(t.size), "mae_pu": float(err.mean()), "p95_abs_error_pu": p95,
            "max_abs_error_pu": float(err.max()), "true_violations": n_true,
            "violation_recall": recall, "violation_precision": precision,
            "v_min_pu": v_min_pu, "gate_ac_006_02": gate}
