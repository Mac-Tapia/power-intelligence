"""Unbalanced power-flow benchmark (spec 008-C, AC-008-A03).

* ``ieee13-kersting``: own three-phase engine against the published node voltages
  (GridLAB-D ``complex_assert`` values and tolerances, ``fixtures/networks/ieee13_reference.json``).
* ``*-phase-frame``: balanced cases rewritten with symmetric phase matrices; the
  three-phase engine must reproduce the own balanced Newton-Raphson (itself contrasted
  with pandapower in ``benchmarks/power-flow/results.json``).

Publishes verified evidence. Exit 0 only if every case passes.

  python scripts/benchmarks/unbalanced_power_flow.py
"""

import cmath
import json
import math
import platform
import sys
import time
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.neutral_json import ingest_file  # noqa: E402
from unitesis_domain import StudyRequest  # noqa: E402
from unitesis_evidence.store import publish_evidence  # noqa: E402
from unitesis_simulation import NewtonRaphsonEngine, ThreePhaseEngine  # noqa: E402

OUT = ROOT / "benchmarks/power-flow/unbalanced-results.json"
EQUIVALENCE_TOL_PU = 1e-8


def run(engine, snap):
    t0 = time.perf_counter()
    res = engine.solve(snap, StudyRequest(snap.content_sha256, "benchmark", engine.name))
    return res, round(time.perf_counter() - t0, 4)


def ieee13() -> dict:
    snap = ingest_file(ROOT / "fixtures/networks/ieee13_kersting.json").require_snapshot()
    ref = json.loads((ROOT / "fixtures/networks/ieee13_reference.json").read_text("utf-8"))
    res, wall = run(ThreePhaseEngine(), snap)
    worst_v, worst_ratio = 0.0, 0.0
    if res.status == "computed":
        for node in ref["nodes"]:
            v = res.voltage(node["bus"], node["phase"])
            v_ln = snap.bus(node["bus"]).nominal_kv * 1e3 / math.sqrt(3)
            d = abs(cmath.rect(v.vm_pu * v_ln, math.radians(v.va_deg))
                    - cmath.rect(node["vm_v"], math.radians(node["va_deg"])))
            worst_v = max(worst_v, d)
            worst_ratio = max(worst_ratio, d / node["tolerance_v"])
    passed = res.status == "computed" and worst_ratio <= 1.0
    return {"case": "ieee13-kersting", "reference": ref["reference"],
            "engine": res.engine, "engine_version": res.engine_version, "status": res.status,
            "comparison": "passed" if passed else "failed", "iterations": res.iterations,
            "residual_mva": res.residual_mva, "balance_mismatch_mva": res.balance_mismatch_mva,
            "reference_values": len(ref["nodes"]), "max_abs_dv_v": worst_v,
            "max_dv_over_tolerance": worst_ratio, "slack_p_mw": res.slack_p_mw,
            "slack_q_mvar": res.slack_q_mvar, "loss_p_mw": res.total_loss_p_mw,
            "max_vuf_percent": max((u.vuf_percent for u in res.unbalance), default=None),
            "wall_time_s": wall, "snapshot_sha256": snap.content_sha256}


def phase_frame(snapshot, zm_ratio=0.3):
    lines = []
    for ln in snapshot.lines:
        z1 = complex(ln.r_ohm_per_km, ln.x_ohm_per_km)
        zm, zs = z1 * zm_ratio, z1 * (1 + zm_ratio)
        z = [[[zs.real, zs.imag] if i == j else [zm.real, zm.imag] for j in range(3)]
             for i in range(3)]
        lines.append(replace(ln, z_phase_ohm_per_km=z))
    return replace(snapshot, lines=tuple(lines))


def equivalence(case: str, path: str) -> dict:
    base = ingest_file(ROOT / path).require_snapshot()
    nr, _ = run(NewtonRaphsonEngine(), base)
    snap = phase_frame(base)
    tp, wall = run(ThreePhaseEngine(), snap)
    dv = None
    if tp.status == "computed" and nr.status == "computed":
        dv = max(abs(tp.voltage(b.bus_id, ph).vm_pu - b.vm_pu)
                 for b in nr.buses for ph in "ABC")
    passed = dv is not None and dv <= EQUIVALENCE_TOL_PU
    return {"case": f"{case}-phase-frame", "reference": f"own Newton-Raphson {nr.engine_version}",
            "engine": tp.engine, "engine_version": tp.engine_version, "status": tp.status,
            "comparison": "passed" if passed else "failed", "iterations": tp.iterations,
            "residual_mva": tp.residual_mva, "balance_mismatch_mva": tp.balance_mismatch_mva,
            "max_abs_dv_pu": dv, "tolerance_pu": EQUIVALENCE_TOL_PU,
            "loss_p_mw": tp.total_loss_p_mw, "reference_loss_p_mw": nr.total_loss_p_mw,
            "wall_time_s": wall, "snapshot_sha256": snap.content_sha256}


def main() -> int:
    rows = [ieee13(),
            equivalence("synthetic-6bus", "fixtures/networks/radial_feeder_6bus.json"),
            equivalence("ieee33-radial", "fixtures/networks/ieee33_baran_wu.json")]
    ok = all(r["comparison"] == "passed" for r in rows)
    payload = {"schema": "unitesis.unbalanced-power-flow-benchmark/1",
               "generated_at_utc": datetime.now(UTC).isoformat(),
               "python": platform.python_version(), "platform": platform.platform(),
               "all_passed": ok, "results": rows,
               "note": "Phase frame: Kron-reduced line matrices with shunt admittance, YNyn0 "
                       "transformers, ideal step-voltage regulators with fixed taps, ZIP loads "
                       "(wye/delta). No automatic regulator control, no Dyn transformers yet."}
    publish_evidence(OUT, payload)
    for r in rows:
        diff = (f"dV_V={r['max_abs_dv_v']:.3f}" if "max_abs_dv_v" in r
                else f"dV_pu={r['max_abs_dv_pu'] or 0:.2e}")
        print(f"{r['case']:28s} {r['status']:9s} {r['comparison']:7s} "
              f"it={r['iterations']:<3} {diff}")
    print("all passed:", ok, "->", OUT.relative_to(ROOT))
    return 0 if ok else 5


if __name__ == "__main__":
    raise SystemExit(main())
