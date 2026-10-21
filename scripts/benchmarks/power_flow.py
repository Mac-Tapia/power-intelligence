"""Power-flow benchmark (spec 004, AC-004-03): own engines vs the independent reference.

Cases: synthetic 6-bus feeder, IEEE 33-bus radial and IEEE 33-bus meshed (ties closed).
Publishes verified evidence with engine versions, comparison status, maximum differences,
iterations and wall time. Exit 0 only if every applicable comparison passes.

  python scripts/benchmarks/power_flow.py
"""

import json
import platform
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.neutral_json import build_snapshot  # noqa: E402
from unitesis_application.study import solve_and_compare  # noqa: E402
from unitesis_evidence.store import publish_evidence  # noqa: E402
from unitesis_simulation import NewtonRaphsonEngine, PandapowerEngine, RadialBFSEngine  # noqa: E402
from unitesis_topology import build_energized_network  # noqa: E402

OUT = ROOT / "benchmarks/power-flow/results.json"


def load(path: str, close_ties: bool = False):
    payload = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if close_ties:
        for ln in payload["network"]["lines"]:
            ln["in_service"] = True
        payload["source_id"] += "-ties-closed"
    return build_snapshot(payload, path).require_snapshot()


CASES = {
    "synthetic-6bus": lambda: load("fixtures/networks/radial_feeder_6bus.json"),
    "ieee33-radial": lambda: load("fixtures/networks/ieee33_baran_wu.json"),
    "ieee33-meshed": lambda: load("fixtures/networks/ieee33_baran_wu.json", close_ties=True),
}


def main() -> int:
    reference = PandapowerEngine()
    rows = []
    ok = True
    for case, factory in CASES.items():
        snap = factory()
        meshed = build_energized_network(snap).meshed
        for engine in (NewtonRaphsonEngine(), RadialBFSEngine()):
            t0 = time.perf_counter()
            run = solve_and_compare(snap, case, candidate=engine, reference=reference)
            elapsed = time.perf_counter() - t0
            cand, comp = run["candidate"], run["comparison"]
            applicable = not (meshed and engine.name == RadialBFSEngine.name)
            row = {"case": case, "meshed": meshed, "engine": engine.name,
                   "engine_version": engine.version(), "status": cand.status,
                   "comparison": comp["status"], "applicable": applicable,
                   "iterations": cand.iterations, "residual_pu": cand.residual_pu,
                   "min_vm_pu": min((b.vm_pu for b in cand.buses), default=None),
                   "loss_p_mw": cand.total_loss_p_mw,
                   "max_differences": comp.get("max_differences"),
                   "wall_time_s_incl_reference": round(elapsed, 4),
                   "snapshot_sha256": snap.content_sha256}
            if applicable:
                ok &= comp["status"] == "passed"
            else:  # out of scope must fail explicitly, never pass silently
                ok &= cand.status == "failed"
            rows.append(row)
    payload = {"schema": "unitesis.power-flow-benchmark/1",
               "generated_at_utc": datetime.now(UTC).isoformat(),
               "reference": {"engine": reference.name, "version": reference.version()},
               "python": platform.python_version(), "platform": platform.platform(),
               "all_applicable_passed": ok, "results": rows,
               "note": "Balanced positive-sequence scope; series lines without shunt "
                       "susceptance. Not an unbalanced three-phase benchmark (004-C)."}
    publish_evidence(OUT, payload)
    for r in rows:
        md = r["max_differences"] or {}
        print(f"{r['case']:15s} {r['engine']:24s} {r['status']:9s} {r['comparison']:9s} "
              f"it={r['iterations']:<3} dV={md.get('voltage_pu')}")
    print("all applicable passed:", ok, "->", OUT.relative_to(ROOT))
    return 0 if ok else 5


if __name__ == "__main__":
    raise SystemExit(main())
