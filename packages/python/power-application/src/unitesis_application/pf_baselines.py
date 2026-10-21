"""Physics baseline for the power-flow surrogate (spec 006, AC-006-06), no training needed.

First-order linearisation on the shared Y-bus around the no-load profile V0:
``V ≈ V0 + Y_bb^-1 conj(S_b / V0)`` for non-slack nodes (valid for radial and meshed
feeders). Every learned surrogate must beat this baseline on the same test feeders to be
worth its complexity; both are scored with ``unitesis_sciml.surrogate_metrics``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

import numpy as np
from scipy.sparse.linalg import splu
from unitesis_adapters.neutral_json import ingest_file
from unitesis_evidence.store import canonical, publish_evidence, read_evidence
from unitesis_sciml.surrogate_metrics import score_voltages
from unitesis_simulation import build_ybus
from unitesis_topology import build_energized_network

BASELINE = "linearised-ybus-first-order"


def linear_voltages(snapshot, p_node: np.ndarray, q_node: np.ndarray) -> np.ndarray:
    """Voltage magnitudes (scenarios x nodes) from node injections given as loads (MW/MVAr)."""
    model = build_ybus(snapshot, build_energized_network(snapshot))
    n = len(model.index)
    v0_slack = snapshot.slacks[0].vm_pu * np.exp(1j * np.radians(snapshot.slacks[0].angle_deg))
    if n == 1:
        return np.full((p_node.shape[0], 1), abs(v0_slack))
    ybb = model.ybus[1:, 1:].tocsc()
    yb0 = model.ybus[1:, [0]].toarray().ravel()
    lu = splu(ybb)
    v0 = lu.solve(-yb0 * v0_slack)                              # no-load profile
    s = -(p_node[:, 1:] + 1j * q_node[:, 1:]) / model.base_mva  # injections, per unit
    dv = lu.solve(np.conj(s / v0).T).T
    vm = np.abs(v0 + dv)
    return np.column_stack([np.full(vm.shape[0], abs(v0_slack)), vm])


def evaluate_baseline(networks_dir: str | Path, dataset_dir: str | Path, output: str | Path,
                      *, split: str = "test", v_min_pu: float = 0.95) -> dict[str, Any]:
    networks = Path(networks_dir)
    data = Path(dataset_dir)
    manifest = read_evidence(data / "manifest.json")
    report = read_evidence(networks / "import_report.json")
    files = {r["network_id"]: r["snapshot_file"] for r in report["feeders"]
             if r.get("snapshot_file")}
    trues, preds, per_feeder = [], [], []
    for f in manifest["feeders"]:
        if f["split"] != split or not f["kept"]:
            continue
        with np.load(data / f["file"]) as arrays:              # close the file (Windows)
            p_mw, q_mvar, true = arrays["p_mw"], arrays["q_mvar"], arrays["vm_pu"]
        snap = ingest_file(networks / files[f["network_id"]]).require_snapshot()
        if snap.content_sha256 != f["snapshot_sha256"]:
            raise ValueError(f"{f['network_id']}: snapshot differs from dataset manifest")
        pred = linear_voltages(snap, p_mw, q_mvar)
        trues.append(true.ravel())
        preds.append(pred.ravel())
        per_feeder.append({"network_id": f["network_id"],
                           **score_voltages(true, pred, v_min_pu=v_min_pu)})
    if not trues:
        raise ValueError(f"no feeders with samples in split {split!r}")
    payload = {
        "schema": "unitesis.surrogate-evaluation/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "surrogate": BASELINE, "case_id": manifest["case_id"],
        "dataset_id": manifest["dataset_id"],
        "dataset_manifest_sha256": sha256(canonical(manifest)).hexdigest(),
        "split": split, "feeders": len(per_feeder),
        "overall": score_voltages(np.concatenate(trues), np.concatenate(preds),
                                  v_min_pu=v_min_pu),
        "per_feeder": per_feeder,
        "note": "Physics baseline (AC-006-06). Learned surrogates must beat it on the same "
                "split; any decision is confirmed by the own solver (ADR-0002).",
    }
    return publish_evidence(output, payload)
