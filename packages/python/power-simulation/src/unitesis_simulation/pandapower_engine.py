"""Independent pandapower Newton-Raphson adapter (inspired by flujos/SelecCablesAAAC backends).

Optional dependency: if pandapower is not importable the engine raises
``EngineUnavailable``; it never falls back to another algorithm or reports success.
Unlike the donors, there is no silent NR->BFSW fallback and no default ampacity.
"""

from __future__ import annotations

import math
from typing import Any

from unitesis_domain import BranchResult, BusResult, ElectricalSnapshot, StudyRequest, StudyResult
from unitesis_ports import EngineUnavailable
from unitesis_topology import TopologyError, require_balanced

ENGINE_NAME = "pandapower-nr"
_UNBOUNDED_KA = 1e6  # pandapower requires max_i_ka; loading is then reported as None


def _import_pp() -> Any:
    try:
        import pandapower as pp
    except Exception as exc:  # pragma: no cover - depends on environment
        raise EngineUnavailable(f"pandapower not available: {exc}") from exc
    return pp


class PandapowerEngine:
    name = ENGINE_NAME

    def version(self) -> str:
        return str(_import_pp().__version__)

    def solve(self, snapshot: ElectricalSnapshot, request: StudyRequest) -> StudyResult:
        pp = _import_pp()
        version = str(pp.__version__)
        base = dict(request_sha256=request.request_sha256, snapshot_sha256=snapshot.content_sha256,
                    scenario_id=request.scenario_id, engine=self.name, engine_version=version)
        if request.snapshot_sha256 != snapshot.content_sha256:
            return StudyResult(**base, status="failed",
                               messages=("request snapshot hash does not match model",))
        try:
            require_balanced(snapshot)
        except TopologyError as exc:
            return StudyResult(**base, status="failed", messages=(f"unsupported topology: {exc}",))
        net = pp.create_empty_network(f_hz=snapshot.frequency_hz, sn_mva=1.0)
        idx = {b.bus_id: pp.create_bus(net, vn_kv=b.nominal_kv, name=b.bus_id)
               for b in snapshot.buses}
        for s in snapshot.slacks:
            pp.create_ext_grid(net, bus=idx[s.bus], vm_pu=s.vm_pu, va_degree=s.angle_deg)
        line_idx: dict[str, int] = {}
        for ln in snapshot.lines:
            line_idx[ln.line_id] = pp.create_line_from_parameters(
                net, from_bus=idx[ln.from_bus], to_bus=idx[ln.to_bus], length_km=ln.length_km,
                r_ohm_per_km=ln.r_ohm_per_km, x_ohm_per_km=ln.x_ohm_per_km, c_nf_per_km=0.0,
                max_i_ka=ln.max_current_ka or _UNBOUNDED_KA, in_service=ln.in_service,
                name=ln.line_id)
        trafo_idx: dict[str, int] = {}
        for tr in snapshot.transformers:
            trafo_idx[tr.transformer_id] = pp.create_transformer_from_parameters(
                net, hv_bus=idx[tr.hv_bus], lv_bus=idx[tr.lv_bus], sn_mva=tr.sn_mva,
                vn_hv_kv=tr.vn_hv_kv, vn_lv_kv=tr.vn_lv_kv, vk_percent=tr.vk_percent,
                vkr_percent=tr.vkr_percent, pfe_kw=0.0, i0_percent=0.0,
                shift_degree=tr.shift_degree, tap_side="hv", tap_neutral=0,
                tap_changer_type="Ratio",          # pandapower >= 3 ignores taps without it
                tap_pos=tr.tap_pos, tap_step_percent=tr.tap_step_percent,
                tap_min=min(tr.tap_pos, 0), tap_max=max(tr.tap_pos, 0),
                in_service=tr.in_service, name=tr.transformer_id)
        for sw in snapshot.switches:
            pp.create_switch(net, bus=idx[sw.from_bus], element=idx[sw.to_bus], et="b",
                             closed=sw.closed, name=sw.switch_id)
        for ld in snapshot.loads:
            pp.create_load(net, bus=idx[ld.bus], p_mw=ld.p_mw, q_mvar=ld.q_mvar,
                           in_service=ld.in_service, name=ld.load_id)
        try:
            # A flat start can converge to a spurious low-voltage solution with large vector-
            # group shifts; a DC start is used whenever a transformer shifts the phase.
            shifted = any(t.shift_degree and t.in_service for t in snapshot.transformers)
            pp.runpp(net, algorithm="nr", calculate_voltage_angles=True,
                     tolerance_mva=request.settings.tolerance_pu,
                     max_iteration=request.settings.max_iterations,
                     init="dc" if shifted else "flat",
                     numba=False)
        except Exception as exc:
            return StudyResult(**base, status="failed", messages=(f"pandapower: {exc}",))
        if not bool(net.converged):
            return StudyResult(**base, status="failed", messages=("pandapower did not converge",))

        buses = []
        deenergized = []
        for bus_id, i in idx.items():
            vm, va = float(net.res_bus.vm_pu.at[i]), float(net.res_bus.va_degree.at[i])
            if math.isnan(vm):
                deenergized.append(f"bus:{bus_id}")
                continue
            buses.append(BusResult(bus_id, vm, va))
        branches = []
        energized = {b.bus_id for b in buses}
        for ln in snapshot.lines:
            if not ln.in_service or ln.from_bus not in energized:
                continue
            r = net.res_line.loc[line_idx[ln.line_id]]
            loading = float(r.loading_percent) if ln.max_current_ka else None
            branches.append(BranchResult(ln.line_id, ln.from_bus, ln.to_bus, float(r.i_ka),
                                         float(r.p_from_mw), float(r.q_from_mvar),
                                         float(r.pl_mw), float(r.ql_mvar), loading))
        for tr in snapshot.transformers:
            if not tr.in_service or tr.hv_bus not in energized:
                continue
            r = net.res_trafo.loc[trafo_idx[tr.transformer_id]]
            branches.append(BranchResult(tr.transformer_id, tr.hv_bus, tr.lv_bus,
                                         float(r.i_hv_ka), float(r.p_hv_mw), float(r.q_hv_mvar),
                                         float(r.pl_mw), float(r.ql_mvar),
                                         float(r.loading_percent)))
        excluded = sorted([ln.line_id for ln in snapshot.lines if not ln.in_service]
                          + [t.transformer_id for t in snapshot.transformers if not t.in_service]
                          + [s.switch_id for s in snapshot.switches if not s.closed])
        loads = net.res_load
        return StudyResult(
            **base, status="computed", converged=True,
            iterations=int(net._ppc.get("iterations", 0)) if getattr(net, "_ppc", None) else 0,
            buses=tuple(sorted(buses, key=lambda b: b.bus_id)),
            branches=tuple(sorted(branches, key=lambda b: b.branch_id)),
            slack_p_mw=float(net.res_ext_grid.p_mw.sum()),
            slack_q_mvar=float(net.res_ext_grid.q_mvar.sum()),
            total_load_p_mw=float(loads.p_mw.sum()) if len(loads) else 0.0,
            total_load_q_mvar=float(loads.q_mvar.sum()) if len(loads) else 0.0,
            total_loss_p_mw=(float(net.res_line.pl_mw.sum()) if len(net.line) else 0.0)
            + (float(net.res_trafo.pl_mw.sum()) if len(net.trafo) else 0.0),
            total_loss_q_mvar=(float(net.res_line.ql_mvar.sum()) if len(net.line) else 0.0)
            + (float(net.res_trafo.ql_mvar.sum()) if len(net.trafo) else 0.0),
            excluded_elements=tuple(excluded) + tuple(sorted(deenergized)),
            messages=(f"pandapower {version} Newton-Raphson, line shunt capacitance 0",))
