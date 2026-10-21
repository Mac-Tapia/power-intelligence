"""Balanced radial backward/forward sweep (adapted from SelecCablesAAAC ``bfs_solver.py``).

Rewritten on the standard library (complex arithmetic, no numpy/networkx) and bound to
``ElectricalSnapshot``. Scope: one slack, constant-PQ loads, series lines, closed switches
as ideal ties, single voltage level per energized tree. Anything else is rejected by
``unitesis_topology`` before solving. Never fills a missing parameter.
"""

from __future__ import annotations

import cmath
import math

from unitesis_domain import (
    BranchResult,
    BusResult,
    ElectricalSnapshot,
    Line,
    StudyRequest,
    StudyResult,
)
from unitesis_domain.units import SQRT3
from unitesis_topology import TopologyError, build_radial_tree

ENGINE_NAME = "unitesis-radial-bfs"
ENGINE_VERSION = "0.1.0"


class RadialBFSEngine:
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
            tree = build_radial_tree(snapshot)
        except TopologyError as exc:
            return StudyResult(**base, status="failed", messages=(f"unsupported topology: {exc}",))

        slack = snapshot.slacks[0]
        energized = set(tree.order)
        v_base = {b.bus_id: b.nominal_kv * 1e3 / SQRT3 for b in snapshot.buses}  # V phase
        v_slack = cmath.rect(slack.vm_pu * v_base[slack.bus], math.radians(slack.angle_deg))
        s_load: dict[str, complex] = dict.fromkeys(energized, 0j)  # VA per phase
        for ld in snapshot.loads:
            if ld.in_service and ld.bus in energized:
                s_load[ld.bus] += complex(ld.p_mw, ld.q_mvar) * 1e6 / 3.0

        v = {bus: v_slack * (v_base[bus] / v_base[slack.bus]) for bus in tree.order}
        i_branch: dict[str, complex] = {}
        settings = request.settings
        residual = math.inf
        converged = False
        iterations = 0
        for iterations in range(1, settings.max_iterations + 1):  # noqa: B007
            i_branch = self._backward(tree, v, s_load)
            v_new = self._forward(tree, v_slack, i_branch)
            residual = max(abs(v_new[b] - v[b]) / v_base[b] for b in tree.order)
            v = v_new
            if residual <= settings.tolerance_pu:
                converged = True
                break
        if not converged or any(not math.isfinite(abs(x)) for x in v.values()):
            return StudyResult(**base, status="failed", iterations=iterations,
                               residual_pu=residual if math.isfinite(residual) else None,
                               excluded_elements=tree.excluded,
                               messages=("backward/forward sweep did not converge",))

        # Final currents consistent with the converged voltages.
        i_branch = self._backward(tree, v, s_load)
        buses = tuple(
            BusResult(b, abs(v[b]) / v_base[b], math.degrees(cmath.phase(v[b])))
            for b in sorted(tree.order))
        branches: list[BranchResult] = []
        loss = 0j
        for child in tree.order[1:]:
            br = tree.parent_branch[child]
            if not isinstance(br, Line):
                continue
            current = i_branch[child]
            parent = tree.parent_bus[child]
            s_from = 3.0 * v[parent] * current.conjugate() / 1e6
            s_loss = 3.0 * abs(current) ** 2 * br.z_ohm / 1e6
            loss += s_loss
            i_ka = abs(current) / 1e3
            loading = 100.0 * i_ka / br.max_current_ka if br.max_current_ka else None
            sign = 1.0 if br.from_bus == parent else -1.0
            branches.append(BranchResult(br.line_id, br.from_bus, br.to_bus, i_ka,
                                         sign * s_from.real, sign * s_from.imag,
                                         s_loss.real, s_loss.imag, loading))
        s_slack = 3.0 * s_load[slack.bus] / 1e6
        for child in tree.children(slack.bus):
            s_slack += 3.0 * v[slack.bus] * i_branch[child].conjugate() / 1e6
        total_load = sum(s_load.values()) * 3.0 / 1e6
        return StudyResult(
            **base, status="computed", converged=True, iterations=iterations,
            residual_pu=residual, buses=buses, branches=tuple(sorted(branches,
                                                                     key=lambda r: r.branch_id)),
            slack_p_mw=s_slack.real, slack_q_mvar=s_slack.imag,
            total_load_p_mw=total_load.real, total_load_q_mvar=total_load.imag,
            total_loss_p_mw=loss.real, total_loss_q_mvar=loss.imag,
            excluded_elements=tree.excluded + tuple(f"bus:{b}" for b in tree.deenergized_buses),
            messages=("balanced radial positive-sequence scope; not an unbalanced 3-phase study",))

    @staticmethod
    def _backward(tree, v: dict[str, complex], s_load: dict[str, complex]) -> dict[str, complex]:
        downstream = {b: (s_load[b] / v[b]).conjugate() for b in tree.order}
        currents: dict[str, complex] = {}
        for child in reversed(tree.order[1:]):
            currents[child] = downstream[child]
            downstream[tree.parent_bus[child]] += downstream[child]
        return currents

    @staticmethod
    def _forward(tree, v_slack: complex, i_branch: dict[str, complex]) -> dict[str, complex]:
        v = {tree.slack_bus: v_slack}
        for child in tree.order[1:]:
            br = tree.parent_branch[child]
            z = br.z_ohm if isinstance(br, Line) else 0j
            v[child] = v[tree.parent_bus[child]] - z * i_branch[child]
        return v
