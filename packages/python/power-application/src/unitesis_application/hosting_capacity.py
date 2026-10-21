"""Use case: remaining capacity per bus (spec 002 T002-03) screened by a surrogate and
certified by the own solver (spec 029 T029-S06, ADR-0002).

For each candidate bus the surrogate sweeps all load levels at once; the solver then checks
the boundary (accepted level passes, next level fails). If the surrogate is wrong, the limit
is searched with the solver itself (bisection over the declared grid) and the disagreement
is recorded. Only solver-confirmed limits are reported as limits.
"""

from __future__ import annotations

import math
from dataclasses import replace
from datetime import UTC, datetime
from typing import Any

import numpy as np
from unitesis_domain import ElectricalSnapshot, Load, StudyRequest
from unitesis_evidence.store import publish_evidence
from unitesis_ports import PowerFlowEngine, SurrogateEngine
from unitesis_simulation import NewtonRaphsonEngine, build_ybus
from unitesis_topology import build_energized_network

from .pf_baselines import BASELINE, linear_voltages

NEW_LOAD_ID = "HOSTING_CAPACITY_PROBE"


class LinearYBusSurrogate:
    """Physics baseline exposed through the SurrogateEngine port."""

    name = BASELINE

    def version(self) -> str:
        return "1.0.0"

    def predict_vm(self, snapshot: ElectricalSnapshot, p_node: np.ndarray,
                   q_node: np.ndarray) -> np.ndarray:
        return linear_voltages(snapshot, p_node, q_node)


def _with_probe(snapshot: ElectricalSnapshot, bus: str, p: float, q: float) -> ElectricalSnapshot:
    return replace(snapshot, loads=(*snapshot.loads, Load(NEW_LOAD_ID, bus, p, q, True)))


def hosting_capacity(snapshot: ElectricalSnapshot, buses: list[str], p_levels_mw: list[float],
                     *, power_factor: float, v_min_pu: float, max_loading_percent: float,
                     margin_pu: float, surrogate: SurrogateEngine | None = None,
                     engine: PowerFlowEngine | None = None) -> dict[str, Any]:
    levels = np.asarray(p_levels_mw, dtype=float)
    if levels.size == 0 or np.any(levels <= 0) or np.any(np.diff(levels) <= 0):
        raise ValueError("p_levels_mw must be positive and strictly increasing")
    if not 0 < power_factor <= 1 or not 0 < v_min_pu < 1.2 or margin_pu < 0:
        raise ValueError("invalid power factor, v_min or margin")
    surrogate = surrogate or LinearYBusSurrogate()
    engine = engine or NewtonRaphsonEngine()
    network = build_energized_network(snapshot)
    model = build_ybus(snapshot, network)
    n = len(model.index)
    base_p, base_q = np.zeros(n), np.zeros(n)
    for ld in snapshot.loads:
        if ld.in_service and ld.bus in network.node_of:
            base_p[model.node_index(ld.bus)] += ld.p_mw
            base_q[model.node_index(ld.bus)] += ld.q_mvar
    tan_phi = math.tan(math.acos(power_factor))
    solver_calls = 0

    def evaluate(scen: ElectricalSnapshot, scenario_id: str) -> tuple[bool, str]:
        nonlocal solver_calls
        solver_calls += 1
        res = engine.solve(scen, StudyRequest(scen.content_sha256, scenario_id, engine.name))
        if res.status != "computed":
            return False, "no_convergence"
        if min(b.vm_pu for b in res.buses) < v_min_pu:
            return False, "voltage"
        loadings = [b.loading_percent for b in res.branches if b.loading_percent is not None]
        if loadings and max(loadings) > max_loading_percent:
            return False, "loading"
        return True, "ok"

    def check(bus: str, idx: int) -> tuple[bool, str]:
        p = float(levels[idx])
        return evaluate(_with_probe(snapshot, bus, p, p * tan_phi), f"hc:{bus}:{p}")

    base_ok, base_reason = evaluate(snapshot, "hc:base")
    if not base_ok:
        return {"base_case": {"passes_criteria": False, "criterion": base_reason},
                "buses": [{"bus": b, "status": "base_case_violation",
                           "confirmed_limit_mw": 0.0, "limiting_criterion": base_reason}
                          for b in buses],
                "solver_calls": solver_calls,
                "surrogate": {"name": surrogate.name, "version": surrogate.version()},
                "engine": {"name": engine.name, "version": engine.version()}}

    results = []
    for bus in buses:
        if bus not in network.node_of:
            results.append({"bus": bus, "status": "not_energized"})
            continue
        k = model.node_index(bus)
        p_mat = np.tile(base_p, (levels.size, 1))
        q_mat = np.tile(base_q, (levels.size, 1))
        p_mat[:, k] += levels
        q_mat[:, k] += levels * tan_phi
        pred_min = np.asarray(surrogate.predict_vm(snapshot, p_mat, q_mat)).min(axis=1)
        ok_pred = pred_min >= v_min_pu + margin_pu
        est = int(np.argmin(ok_pred)) - 1 if not ok_pred.all() else levels.size - 1
        calls_before = solver_calls
        ok_est, _ = check(bus, est) if est >= 0 else (False, "voltage")
        nxt = (check(bus, est + 1) if est + 1 < levels.size else (False, "grid_end"))
        if ok_est and not nxt[0]:
            confirmed, reason, agreed = est, nxt[1], True
        else:                                     # surrogate wrong: solver bisection
            lo, hi, reason = -1, levels.size, "voltage"
            while hi - lo > 1:
                mid = (lo + hi) // 2
                good, why = check(bus, mid)
                lo, hi = (mid, hi) if good else (lo, mid)
                if not good:
                    reason = why
            confirmed, agreed = lo, False
            if confirmed == levels.size - 1:
                reason = "grid_end"
        results.append({
            "bus": bus,
            "surrogate_limit_mw": float(levels[est]) if est >= 0 else 0.0,
            "confirmed_limit_mw": float(levels[confirmed]) if confirmed >= 0 else 0.0,
            "limiting_criterion": reason,
            "surrogate_agreed_with_solver": agreed,
            "solver_calls": solver_calls - calls_before,
            "status": "confirmed_by_solver"})
    return {"base_case": {"passes_criteria": True}, "buses": results,
            "solver_calls": solver_calls,
            "surrogate": {"name": surrogate.name, "version": surrogate.version()},
            "engine": {"name": engine.name, "version": engine.version()}}


def run_hosting_capacity(snapshot: ElectricalSnapshot, output, *, buses: list[str],
                         p_levels_mw: list[float], power_factor: float, v_min_pu: float,
                         max_loading_percent: float, margin_pu: float,
                         source_manifest: dict[str, Any] | None = None,
                         criteria_source: str = "explicit_request") -> dict[str, Any]:
    run = hosting_capacity(snapshot, buses, p_levels_mw, power_factor=power_factor,
                           v_min_pu=v_min_pu, max_loading_percent=max_loading_percent,
                           margin_pu=margin_pu)
    payload = {
        "schema": "unitesis.hosting-capacity-evidence/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "snapshot_sha256": snapshot.content_sha256, "source_manifest": source_manifest,
        "criteria": {"v_min_pu": v_min_pu, "max_loading_percent": max_loading_percent,
                     "power_factor": power_factor, "surrogate_margin_pu": margin_pu,
                     "p_levels_mw": list(map(float, p_levels_mw)),
                     "source": criteria_source},
        **run,
        "agreement_rate": (sum(r.get("surrogate_agreed_with_solver", False)
                               for r in run["buses"]) / max(1, len(run["buses"]))),
        "technical_acceptance": False,
        "limitations": ["single new balanced load per bus, others at source values",
                        "limits resolved to the declared grid step",
                        "surrogate only screens; every reported limit is solver-confirmed"],
    }
    return publish_evidence(output, payload)
