"""Independent cross-validation of two study results (replaces flujos ``validation.py``).

Fixes reproduced findings: F04 (empty results passed), A07 (infinite tolerance accepted).
Coverage is checked against the *expected* snapshot elements, not merely between the two
results; duplicates, other scenarios/snapshots, proxy engines and non-finite values fail.
"""

from __future__ import annotations

import math
from typing import Any, Literal

from unitesis_domain import ComparisonTolerances, ElectricalSnapshot, StudyResult
from unitesis_topology import build_radial_tree

ComparisonStatus = Literal["passed", "failed"]
_PROXY_MARKERS = ("proxy", "surrogate", "mock", "fake", "stub")


def expected_coverage(snapshot: ElectricalSnapshot) -> tuple[set[str], set[str]]:
    tree = build_radial_tree(snapshot)
    energized = set(tree.order)
    lines = {ln.line_id for ln in snapshot.lines if ln.in_service and ln.from_bus in energized}
    return energized, lines


def _angle_diff(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def compare_results(reference: StudyResult, candidate: StudyResult,
                    snapshot: ElectricalSnapshot,
                    tolerances: ComparisonTolerances | None = None) -> dict[str, Any]:
    tol = tolerances or ComparisonTolerances()  # validated finite & positive in the domain
    issues: list[dict[str, Any]] = []

    def fail(metric: str, detail: Any, element: str = "*") -> None:
        issues.append({"element": element, "metric": metric, "detail": detail})

    for label, res in (("reference", reference), ("candidate", candidate)):
        if res.status != "computed" or not res.converged:
            fail("status", f"{label} status={res.status}")
        if res.snapshot_sha256 != snapshot.content_sha256:
            fail("snapshot", f"{label} computed on another snapshot")
        if any(m in res.engine.lower() for m in _PROXY_MARKERS):
            fail("engine", f"{label} engine {res.engine!r} is a proxy, not a solver")
    if reference.scenario_id != candidate.scenario_id:
        fail("scenario", "results belong to different scenarios")
    if reference.engine == candidate.engine:
        fail("independence", "both results come from the same engine")

    exp_buses, exp_lines = expected_coverage(snapshot)
    maps: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for label, res in (("reference", reference), ("candidate", candidate)):
        bus_ids = [b.bus_id for b in res.buses]
        br_ids = [b.branch_id for b in res.branches]
        if len(bus_ids) != len(set(bus_ids)) or len(br_ids) != len(set(br_ids)):
            fail("duplicates", f"{label} has duplicated element ids")
        if set(bus_ids) != exp_buses:
            fail("bus_coverage", {"label": label,
                                  "missing": sorted(exp_buses - set(bus_ids)),
                                  "unexpected": sorted(set(bus_ids) - exp_buses)})
        if set(br_ids) != exp_lines:
            fail("branch_coverage", {"label": label,
                                     "missing": sorted(exp_lines - set(br_ids)),
                                     "unexpected": sorted(set(br_ids) - exp_lines)})
        bal = res.balance_mismatch_mva
        load_s = abs(complex(res.total_load_p_mw or 0.0, res.total_load_q_mvar or 0.0))
        if bal is None or not math.isfinite(bal) or bal > max(tol.balance_mva,
                                                              tol.balance_mva * load_s):
            fail("power_balance", {"label": label, "mismatch_mva": bal})
        maps[label] = ({b.bus_id: b for b in res.buses}, {b.branch_id: b for b in res.branches})

    if not exp_buses:
        fail("bus_coverage", "expected snapshot has no energized buses")
    ref_b, ref_l = maps["reference"]
    cand_b, cand_l = maps["candidate"]
    max_dv = max_da = max_di = 0.0
    for bus_id in sorted(exp_buses & ref_b.keys() & cand_b.keys()):
        dv = abs(ref_b[bus_id].vm_pu - cand_b[bus_id].vm_pu)
        da = _angle_diff(ref_b[bus_id].va_deg, cand_b[bus_id].va_deg)
        max_dv, max_da = max(max_dv, dv), max(max_da, da)
        if dv > tol.voltage_pu:
            fail("voltage_pu", dv, bus_id)
        if da > tol.angle_deg:
            fail("angle_deg", da, bus_id)
    for line_id in sorted(exp_lines & ref_l.keys() & cand_l.keys()):
        ia, ib = ref_l[line_id].i_ka * 1e3, cand_l[line_id].i_ka * 1e3
        di = abs(ia - ib)
        max_di = max(max_di, di)
        if di > max(tol.current_a_abs, tol.current_rel * abs(ia)):
            fail("current_a", di, line_id)
    d_loss: float | None
    if reference.total_loss_p_mw is None or candidate.total_loss_p_mw is None:
        fail("losses_mw", "missing total losses")
        d_loss = None
    else:
        d_loss = abs(reference.total_loss_p_mw - candidate.total_loss_p_mw)
        if d_loss > tol.losses_mw:
            fail("losses_mw", d_loss)

    status: ComparisonStatus = "failed" if issues else "passed"
    return {
        "status": status,
        "reference": {"engine": reference.engine, "version": reference.engine_version,
                      "result_sha256": reference.result_sha256},
        "candidate": {"engine": candidate.engine, "version": candidate.engine_version,
                      "result_sha256": candidate.result_sha256},
        "coverage": {"expected_buses": len(exp_buses), "expected_lines": len(exp_lines)},
        "max_differences": {"voltage_pu": max_dv, "angle_deg": max_da, "current_a": max_di,
                            "losses_mw": d_loss},
        "tolerances": {k: getattr(tol, k) for k in tol.__slots__},
        "issues": issues,
        "engineering_acceptance": "pending_human_review",
    }
