"""Use case: real feeder snapshots -> labelled power-flow scenarios (spec 029 T029-S01..03).

Input: the output folder of ``import_cyme_export`` (or any importer with the same report).
For each validated feeder and scenario the own Newton-Raphson engine produces the labels;
non-converged scenarios are discarded and counted; every label is re-checked with the shared
AC residual (``power_mismatch``); a declared fraction is contrasted with the independent
reference. Output: one ``.npz`` graph dataset per feeder plus a verified manifest.
Arrays are per electrical node (closed switches fused), slack node first.
"""

from __future__ import annotations

import math
from dataclasses import replace
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

import numpy as np
from unitesis_adapters.neutral_json import ingest_file
from unitesis_config import ApplicationCase
from unitesis_domain import ElectricalSnapshot, StudyRequest
from unitesis_evidence.store import canonical, publish_evidence, read_evidence
from unitesis_ports import EngineUnavailable, PowerFlowEngine
from unitesis_sciml.pf_scenarios import ScenarioSpec, feeder_split, sample_loads
from unitesis_simulation import (
    NewtonRaphsonEngine,
    PandapowerEngine,
    build_ybus,
    compare_results,
    power_mismatch,
    specified_injections,
)
from unitesis_topology import build_energized_network

from .study import code_manifest

DATASET_SCHEMA = "unitesis.pf-scenarios/1"


def _feeder_arrays(snapshot: ElectricalSnapshot, attributes: dict[str, dict[str, float]],
                   spec: ScenarioSpec, rng: np.random.Generator, engine: PowerFlowEngine,
                   reference: PowerFlowEngine | None, feeder_id: str) -> dict[str, Any]:
    network = build_energized_network(snapshot)
    model = build_ybus(snapshot, network)
    nodes = list(network.nodes)
    loads = [ld for ld in snapshot.loads if ld.bus in model.network.node_of]
    kva = np.array([attributes.get(ld.load_id, {}).get("connected_kva", 0.0) for ld in loads])
    pf = np.array([attributes.get(ld.load_id, {}).get("power_factor", 1.0) for ld in loads])
    p, q = sample_loads(kva, pf, spec, rng)
    node_of_load = np.array([model.node_index(ld.bus) for ld in loads], dtype=int)
    n_nodes = len(nodes)
    edge_index = np.array([[i for _, i, _, _ in model.line_terms],
                           [j for _, _, j, _ in model.line_terms]], dtype=np.int64)
    z = np.array([1.0 / y for _, _, _, y in model.line_terms], dtype=complex)
    edge_attr = np.column_stack([z.real, z.imag,
                                 [ln.length_km for ln, *_ in model.line_terms]]) \
        if len(z) else np.zeros((0, 3))
    keep_p, keep_q, vm, va, loss, resid, ids = [], [], [], [], [], [], []
    stats = {"scenarios": spec.scenarios_per_feeder, "failed": 0, "contrast_passed": 0,
             "contrast_failed": 0, "contrast_unavailable": 0, "residual_rejected": 0}
    others = [ld for ld in snapshot.loads if ld not in loads]
    for k in range(spec.scenarios_per_feeder):
        new_loads = tuple(replace(ld, p_mw=float(p[k, n]), q_mvar=float(q[k, n]))
                          for n, ld in enumerate(loads)) + tuple(others)
        scen = replace(snapshot, loads=new_loads)
        sid = f"{feeder_id}:{k}"
        res = engine.solve(scen, StudyRequest(scen.content_sha256, sid, engine.name))
        if res.status != "computed":
            stats["failed"] += 1
            continue
        by_bus = {b.bus_id: b for b in res.buses}
        vmk = np.array([by_bus[nd].vm_pu for nd in nodes])
        vak = np.array([by_bus[nd].va_deg for nd in nodes])
        v = vmk * np.exp(1j * np.radians(vak))
        s_spec = specified_injections(scen, model)
        r = float(np.max(np.abs(power_mismatch(model.ybus, v, s_spec)[1:]))) if n_nodes > 1 \
            else 0.0
        if not r <= spec.max_label_residual_pu:
            stats["residual_rejected"] += 1
            continue
        resid.append(r)
        p_node = np.zeros(n_nodes)
        q_node = np.zeros(n_nodes)
        np.add.at(p_node, node_of_load, p[k])
        np.add.at(q_node, node_of_load, q[k])
        keep_p.append(p_node)
        keep_q.append(q_node)
        vm.append(vmk)
        va.append(vak)
        loss.append(res.total_loss_p_mw)
        ids.append(sid)
        if reference is not None and rng.random() < spec.contrast_fraction:
            try:
                ref = reference.solve(scen, StudyRequest(scen.content_sha256, sid, reference.name))
                status = compare_results(ref, res, scen)["status"] if ref.status == "computed" \
                    else "failed"
            except EngineUnavailable:
                status = "unavailable"
            stats[f"contrast_{status}"] += 1
    stats["kept"] = len(ids)
    stats["max_label_residual_pu"] = max(resid, default=None)
    stats["loads_without_connected_kva"] = int(np.sum(kva == 0))
    return {"arrays": {"edge_index": edge_index, "edge_attr_pu_r_x_len_km": edge_attr,
                       "node_kv": model.base_kv, "p_mw": np.array(keep_p),
                       "q_mvar": np.array(keep_q), "vm_pu": np.array(vm),
                       "va_deg": np.array(va), "loss_mw": np.array(loss),
                       "label_residual_pu": np.array(resid), "scenario_id": np.array(ids)},
            "stats": stats, "nodes": n_nodes, "edges": int(edge_index.shape[1]),
            "meshed": network.meshed, "snapshot_sha256": snapshot.content_sha256}


def build_pf_dataset(case: ApplicationCase, networks_dir: str | Path, out_dir: str | Path,
                     spec: ScenarioSpec, *, engine: PowerFlowEngine | None = None,
                     reference: PowerFlowEngine | None = None,
                     limit_feeders: int | None = None) -> dict[str, Any]:
    networks = Path(networks_dir)
    report = read_evidence(networks / "import_report.json")
    if report.get("case_id") != case.case_id:
        raise ValueError(f"import report belongs to case {report.get('case_id')!r}")
    engine = engine or NewtonRaphsonEngine()
    reference = reference if reference is not None else PandapowerEngine()
    rows = [r for r in report["feeders"] if r.get("snapshot_file")]
    rows = rows[:limit_feeders] if limit_feeders else rows
    split = feeder_split([r["network_id"] for r in rows], spec)
    out = Path(out_dir)
    (out / "feeders").mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(spec.seed)
    feeders = []
    for row in rows:
        snap = ingest_file(networks / row["snapshot_file"]).require_snapshot()
        if snap.content_sha256 != row["snapshot_sha256"]:
            raise ValueError(f"{row['network_id']}: snapshot differs from import report")
        built = _feeder_arrays(snap, row.get("load_attributes", {}), spec, rng, engine,
                               reference, row["network_id"])
        path = out / "feeders" / f"{row['network_id']}.npz"
        np.savez_compressed(path, **built["arrays"])
        feeders.append({"network_id": row["network_id"], "split": split[row["network_id"]],
                        "file": f"feeders/{path.name}",
                        "sha256": sha256(path.read_bytes()).hexdigest(),
                        "nodes": built["nodes"], "edges": built["edges"],
                        "meshed": built["meshed"], "snapshot_sha256": built["snapshot_sha256"],
                        **built["stats"]})
    worst = max((f["max_label_residual_pu"] or 0.0 for f in feeders), default=0.0)
    totals = {k: sum(f[k] for f in feeders) for k in
              ("scenarios", "kept", "failed", "residual_rejected", "contrast_passed",
               "contrast_failed", "contrast_unavailable")}
    manifest = {
        "schema": DATASET_SCHEMA,
        "dataset_id": f"pf-scenarios-{case.case_id}",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "case_id": case.case_id,
        "source_import_report_sha256": sha256(canonical(report)).hexdigest(),
        "source_parser": report.get("parser"), "source_files": report.get("files"),
        "scenario_spec": spec.as_dict(),
        "engine": {"name": engine.name, "version": engine.version()},
        "reference": {"name": reference.name},
        "code_tree_sha256": sha256(canonical(code_manifest())).hexdigest(),
        "split_policy": "by feeder (AC-029-S01); a feeder never spans two partitions",
        "split_counts": {s: sum(f["split"] == s for f in feeders)
                         for s in ("train", "valid", "test")},
        "totals": totals, "max_label_residual_pu": worst,
        "feeders": feeders,
        "column_origin": {"topology_impedance": "measured_inventory (real export)",
                          "p_q": "scenario (declared demand model)",
                          "labels": "own Newton-Raphson solver"},
        "limitations": ["balanced positive-sequence labels; three-phase feeders only",
                        "demand is a declared scenario model, not measurement",
                        "series lines without shunt susceptance"],
        "authorization": "confirmed" if case.authorized else "pending_owner_confirmation",
        "technical_acceptance": False,
    }
    if math.isnan(worst):
        raise ValueError("non-finite label residual")
    return publish_evidence(out / "manifest.json", manifest)
