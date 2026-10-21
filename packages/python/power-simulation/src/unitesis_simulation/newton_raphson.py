"""Own Newton-Raphson AC power flow (spec 004-B1): radial or meshed, balanced, one slack.

Polar formulation on the shared Y-bus (``ybus.py``), sparse Jacobian, flat start.
Convergence is declared only when the AC power-balance residual of every non-slack node
is below the effective tolerance (per unit on ``BASE_MVA``); a small step is not enough.
The effective tolerance is ``max(requested, rounding floor)``: with very short real sections
the admittances are large and ``V * conj(Y V)`` cannot be evaluated more precisely than
``ROUNDING_FACTOR * eps * max_row_sum(|Y|)``. Both values are reported in the result.
Scope is declared and enforced by ``build_energized_network``: out-of-scope elements fail
the study with the reason, they are never simplified away.
"""

from __future__ import annotations

import math
import warnings
from dataclasses import replace

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import MatrixRankWarning, spsolve
from unitesis_domain import BranchResult, BusResult, ElectricalSnapshot, StudyRequest, StudyResult
from unitesis_domain.units import SQRT3
from unitesis_topology import TopologyError, build_energized_network

from .ybus import build_ybus, power_mismatch, specified_injections

ENGINE_NAME = "unitesis-newton-raphson"
ENGINE_VERSION = "0.2.0"
ROUNDING_FACTOR = 64.0


def _initial_angles(model, slack_angle_rad: float) -> np.ndarray:
    """Flat start that propagates transformer phase shifts from the slack (BFS).

    A plain flat start places LV buses at the HV angle; with vector-group shifts (e.g. 150 deg)
    Newton then starts far from the solution. Magnitudes stay flat.
    """
    n = len(model.index)
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for _, i, j, _ in model.line_terms:
        adj[i].append((j, 0.0))
        adj[j].append((i, 0.0))
    for _, h, lo, _, t in model.trafo_terms:
        shift = float(np.angle(t))
        adj[h].append((lo, -shift))
        adj[lo].append((h, shift))
    va = np.full(n, np.nan)
    va[0] = slack_angle_rad
    queue = [0]
    while queue:
        k = queue.pop()
        for m, delta in adj[k]:
            if np.isnan(va[m]):
                va[m] = va[k] + delta
                queue.append(m)
    return np.where(np.isnan(va), slack_angle_rad, va)


def _jacobian(ybus: sparse.csr_matrix, v: np.ndarray, pq: np.ndarray) -> sparse.csr_matrix:
    ibus = ybus @ v
    diag_v = sparse.diags(v)
    diag_vnorm = sparse.diags(v / np.abs(v))
    ds_dvm = diag_v @ np.conj(ybus @ diag_vnorm) + np.conj(sparse.diags(ibus)) @ diag_vnorm
    ds_dva = 1j * diag_v @ np.conj(sparse.diags(ibus) - ybus @ diag_v)
    ds_dva = sparse.csr_matrix(ds_dva)[pq][:, pq]
    ds_dvm = sparse.csr_matrix(ds_dvm)[pq][:, pq]
    return sparse.vstack([sparse.hstack([ds_dva.real, ds_dvm.real]),
                          sparse.hstack([ds_dva.imag, ds_dvm.imag])], format="csr")


class NewtonRaphsonEngine:
    name = ENGINE_NAME

    def version(self) -> str:
        return ENGINE_VERSION

    def solve(self, snapshot: ElectricalSnapshot, request: StudyRequest) -> StudyResult:
        base = dict(request_sha256=request.request_sha256, snapshot_sha256=snapshot.content_sha256,
                    scenario_id=request.scenario_id, engine=self.name,
                    engine_version=ENGINE_VERSION)
        if request.snapshot_sha256 != snapshot.content_sha256:
            return StudyResult(**base, status="failed",
                               messages=("request snapshot hash does not match model",))
        try:
            network = build_energized_network(snapshot)
        except TopologyError as exc:
            return StudyResult(**base, status="failed", messages=(f"unsupported topology: {exc}",))

        model = build_ybus(snapshot, network)
        s_spec = specified_injections(snapshot, model)
        slack = snapshot.slacks[0]
        n = len(model.index)
        pq = np.arange(1, n)
        vm = np.full(n, slack.vm_pu)
        va = _initial_angles(model, math.radians(slack.angle_deg))
        v = vm * np.exp(1j * va)
        settings = request.settings
        row_sum = float(abs(model.ybus).sum(axis=1).max()) if n > 1 else 0.0
        floor = ROUNDING_FACTOR * float(np.finfo(float).eps) * row_sum
        tolerance = max(settings.tolerance_pu, floor)
        residual = 0.0
        iterations = 0
        converged = n == 1
        while not converged and iterations < settings.max_iterations:
            mis = power_mismatch(model.ybus, v, s_spec)[pq]
            f = np.concatenate([mis.real, mis.imag])
            residual = float(np.max(np.abs(f)))
            if not math.isfinite(residual):
                break
            if residual <= tolerance:
                converged = True
                break
            with warnings.catch_warnings():
                warnings.simplefilter("error", MatrixRankWarning)
                try:
                    dx = spsolve(_jacobian(model.ybus, v, pq), -f)
                except MatrixRankWarning:
                    return StudyResult(**base, status="failed", iterations=iterations,
                                       messages=("singular Jacobian",))
            iterations += 1
            va[pq] += dx[: len(pq)]
            vm[pq] += dx[len(pq):]
            v = vm * np.exp(1j * va)
        if converged and n > 1:
            residual = float(np.max(np.abs(power_mismatch(model.ybus, v, s_spec)[pq])))
        if not converged or not np.all(np.isfinite(v)):
            return StudyResult(**base, status="failed", iterations=iterations,
                               residual_pu=residual if math.isfinite(residual) else None,
                               excluded_elements=network.excluded,
                               messages=("Newton-Raphson did not converge "
                                         f"(effective tolerance {tolerance:.2e} pu)",))
        result = self._result(base, snapshot, network, model, s_spec, v, iterations, residual)
        note = (f"effective tolerance {tolerance:.2e} pu (requested "
                f"{settings.tolerance_pu:.0e}, rounding floor {floor:.2e})")
        return replace(result, messages=(*result.messages, note))

    @staticmethod
    def _result(base, snapshot, network, model, s_spec, v, iterations, residual) -> StudyResult:
        buses = []
        for bus_id in network.energized_buses:
            vk = v[model.node_index(bus_id)]
            buses.append(BusResult(bus_id, float(abs(vk)), math.degrees(float(np.angle(vk)))))
        branches = []
        loss = 0j
        for ln, i, j, y in model.line_terms:
            current = (v[i] - v[j]) * y                       # per unit, from -> to
            s_from = v[i] * np.conj(current) * model.base_mva
            s_loss = abs(current) ** 2 / y * model.base_mva if v[i] != v[j] else 0j
            loss += s_loss
            i_ka = abs(current) * model.base_mva / (SQRT3 * model.base_kv[i])
            loading = float(100.0 * i_ka / ln.max_current_ka) if ln.max_current_ka else None
            branches.append(BranchResult(ln.line_id, ln.from_bus, ln.to_bus, float(i_ka),
                                         float(s_from.real), float(s_from.imag),
                                         float(s_loss.real), float(s_loss.imag), loading))
        for tr, h, lo, y, t in model.trafo_terms:
            i_hv = (y / abs(t) ** 2) * v[h] - (y / np.conj(t)) * v[lo]     # per unit, into HV
            i_lv = -(y / t) * v[h] + y * v[lo]                              # per unit, into LV
            s_hv = v[h] * np.conj(i_hv) * model.base_mva
            s_lv = v[lo] * np.conj(i_lv) * model.base_mva
            s_loss = s_hv + s_lv
            loss += s_loss
            i_hv_ka = abs(i_hv) * model.base_mva / (SQRT3 * model.base_kv[h])
            i_lv_ka = abs(i_lv) * model.base_mva / (SQRT3 * model.base_kv[lo])
            loading = 100.0 * max(i_hv_ka * SQRT3 * tr.vn_hv_kv,
                                  i_lv_ka * SQRT3 * tr.vn_lv_kv) / tr.sn_mva
            branches.append(BranchResult(tr.transformer_id, tr.hv_bus, tr.lv_bus, float(i_hv_ka),
                                         float(s_hv.real), float(s_hv.imag),
                                         float(s_loss.real), float(s_loss.imag), float(loading)))
        calc0 = v[0] * np.conj((model.ybus @ v)[0])
        s_slack = (calc0 - s_spec[0]) * model.base_mva
        total_load = -s_spec.sum() * model.base_mva
        scope = "meshed" if network.meshed else "radial"
        return StudyResult(
            **base, status="computed", converged=True, iterations=iterations,
            residual_pu=residual, buses=tuple(buses),
            branches=tuple(sorted(branches, key=lambda r: r.branch_id)),
            slack_p_mw=float(s_slack.real), slack_q_mvar=float(s_slack.imag),
            total_load_p_mw=float(total_load.real), total_load_q_mvar=float(total_load.imag),
            total_loss_p_mw=float(loss.real), total_loss_q_mvar=float(loss.imag),
            excluded_elements=network.excluded
            + tuple(f"bus:{b}" for b in network.deenergized_buses),
            messages=(f"balanced positive-sequence Newton-Raphson ({scope}); series lines "
                      "without shunt susceptance; transformers without magnetising branch; "
                      "not an unbalanced 3-phase study",))
