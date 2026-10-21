"""Own three-phase unbalanced power flow in the phase frame (spec 008-C).

Formulation (Kersting, ch. 10; implicit Z-bus / fixed-point current injection):

* one node per (bus, phase) present; closed switches fuse buses (ideal, all phases);
* nodal admittance in siemens on actual volts, so transformers need no per-unit base:
  lines as pi sections from ``z_phase_ohm_per_km`` / ``b_phase_us_per_km``; YNyn0
  transformers as one two-winding unit per phase (impedance referred to LV, real ratio
  with the HV tap); constant-impedance loads stamped into Y;
* step-voltage regulators are ideal ratios ``V_to = a V_from`` eliminated exactly by the
  node transformation ``Y_r = T^H Y T`` (no fictitious impedance);
* constant-power and constant-current loads (wye or delta) are current injections
  updated each iteration: ``V_L = Y_LL^-1 (I_L(V) - Y_LS V_S)``, one sparse LU.

Convergence is declared on the nodal power mismatch at the solution (MVA), the same
criterion as the balanced Newton-Raphson. Out-of-scope elements fail closed with their
ids (AC-008-A01): lines without a phase matrix (unless the positive-sequence decoupled
approximation is requested explicitly), transformers without an implemented vector group,
and loads on phases the bus does not have.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass

import numpy as np
from scipy.sparse import csc_matrix, lil_matrix
from scipy.sparse.linalg import splu
from unitesis_domain import (
    BranchLoss,
    ElectricalSnapshot,
    Line,
    PhaseBranchFlow,
    PhaseVoltage,
    StudyRequest,
    UnbalancedStudyResult,
    VoltageUnbalance,
)
from unitesis_topology import TopologyError, build_energized_network

ENGINE_NAME = "unitesis-three-phase"
ENGINE_VERSION = "0.1.0"
_PH = "ABC"
_SHIFT = {"A": 0.0, "B": -120.0, "C": 120.0}
_A = cmath.rect(1.0, math.radians(120))


class ScopeError(ValueError):
    """The snapshot holds elements this engine cannot represent."""


@dataclass
class _Model:
    nodes: list[tuple[str, str]]            # (representative bus, phase)
    index: dict[tuple[str, str], int]
    y: lil_matrix                            # full nodal admittance (S)
    v_base: np.ndarray                       # line-to-neutral nominal (V) per node
    slack: list[int]
    t: csc_matrix                            # full -> reduced node transformation
    reduced_of: np.ndarray                   # full index -> reduced column (independent)
    injections: list                         # (kind, element, s_va, nodes, v_nom) PQ/I loads
    z_loads: list                            # (load_id, element, y_s, nodes) for reporting
    lines: list                              # (line, ys, ysh, nodes_f, nodes_t)
    trafos: list                             # (trafo, y, n, nodes_h, nodes_l)
    regulators: list                         # (reg, [(phase, a, i_from, i_to)])


class ThreePhaseEngine:
    """Phase-frame engine. ``positive_sequence_lines`` allows lines without a phase matrix
    as uncoupled ``diag(z1)`` (a declared approximation, reported in the messages)."""

    name = ENGINE_NAME

    def __init__(self, positive_sequence_lines: bool = False) -> None:
        self.positive_sequence_lines = positive_sequence_lines

    def version(self) -> str:
        return ENGINE_VERSION

    def solve(self, snapshot: ElectricalSnapshot,
              request: StudyRequest) -> UnbalancedStudyResult:
        base = dict(request_sha256=request.request_sha256,
                    snapshot_sha256=snapshot.content_sha256, scenario_id=request.scenario_id,
                    engine=ENGINE_NAME, engine_version=ENGINE_VERSION)
        if request.snapshot_sha256 != snapshot.content_sha256:
            return UnbalancedStudyResult(**base, status="failed",
                                         messages=("request snapshot hash does not match model",))
        try:
            network = build_energized_network(snapshot, phase_frame=True)
            model = self._build(snapshot, network)
        except (TopologyError, ScopeError) as exc:
            return UnbalancedStudyResult(**base, status="failed",
                                         messages=(f"unsupported scope: {exc}",))
        return self._iterate(snapshot, network, model, request, base)

    # ------------------------------------------------------------------ model building
    def _build(self, snapshot: ElectricalSnapshot, net) -> _Model:
        rep = net.node_of
        phases: dict[str, set[str]] = {n: set() for n in net.nodes}
        phases[net.slack_bus] |= set(_PH)
        lines = [ln for ln in net.lines]
        for ln in lines:
            for b in (ln.from_bus, ln.to_bus):
                phases[rep[b]] |= set(ln.phases)
        for tr in net.transformers:
            if tr.vector_group != "YNyn0":
                raise ScopeError(f"{tr.transformer_id}: vector_group {tr.vector_group!r} is not "
                                 "implemented in the phase frame (YNyn0 only)")
            phases[rep[tr.hv_bus]] |= set(_PH)
            phases[rep[tr.lv_bus]] |= set(_PH)
        for reg in net.regulators:
            phases[rep[reg.from_bus]] |= set(reg.phases)
            phases[rep[reg.to_bus]] |= set(reg.phases)
        missing = sorted(ln.line_id for ln in lines
                         if ln.z_phase_ohm_per_km is None and not self.positive_sequence_lines)
        if missing:
            raise ScopeError("lines without z_phase_ohm_per_km (phase matrix required): "
                             + ", ".join(missing[:10]))

        nodes = [(b, ph) for b in net.nodes for ph in _PH if ph in phases[b]]
        index = {nd: i for i, nd in enumerate(nodes)}
        n = len(nodes)
        y = lil_matrix((n, n), dtype=complex)
        v_base = np.array([snapshot.bus(b).nominal_kv * 1e3 / math.sqrt(3) for b, _ in nodes])

        def idx(bus: str, phs: str) -> list[int]:
            return [index[(rep[bus], ph)] for ph in phs]

        def stamp(rows: list[int], cols: list[int], block: np.ndarray) -> None:
            for i, r in enumerate(rows):
                for j, c in enumerate(cols):
                    y[r, c] += block[i, j]

        line_data = []
        for ln in lines:
            ys, ysh = _line_admittances(ln)
            nf, nt = idx(ln.from_bus, ln.phases), idx(ln.to_bus, ln.phases)
            stamp(nf, nf, ys + ysh / 2)
            stamp(nt, nt, ys + ysh / 2)
            stamp(nf, nt, -ys)
            stamp(nt, nf, -ys)
            line_data.append((ln, ys, ysh, nf, nt))

        trafo_data = []
        for tr in net.transformers:
            z_pu = complex(tr.vkr_percent, math.sqrt(tr.vk_percent ** 2 - tr.vkr_percent ** 2))
            z_lv = z_pu / 100 * tr.vn_lv_kv ** 2 / tr.sn_mva          # ohm, LV side
            ratio = tr.vn_hv_kv / tr.vn_lv_kv * (1 + tr.tap_pos * tr.tap_step_percent / 100)
            yt = 1 / z_lv
            nh, nl = idx(tr.hv_bus, _PH), idx(tr.lv_bus, _PH)
            for h, lo in zip(nh, nl, strict=True):
                y[h, h] += yt / ratio ** 2
                y[h, lo] -= yt / ratio
                y[lo, h] -= yt / ratio
                y[lo, lo] += yt
            trafo_data.append((tr, yt, ratio, nh, nl))

        injections, z_loads = [], []
        for ld in snapshot.loads:
            if not ld.in_service or ld.bus not in rep:
                continue
            have = phases[rep[ld.bus]]
            if not set(ld.phases) <= have:
                raise ScopeError(f"load {ld.load_id}: phases {ld.phases} not present at bus "
                                 f"{ld.bus} ({''.join(sorted(have))})")
            for element, s_mva in ld.element_powers():
                if s_mva == 0:
                    continue
                s_va = s_mva * 1e6
                nds = idx(ld.bus, element)
                v_nom = cmath.rect(v_base[nds[0]] * (math.sqrt(3) if len(element) == 2 else 1),
                                   math.radians(_SHIFT[element[0]] + (30 if len(element) == 2
                                                                      else 0)))
                if ld.model == "constant_impedance":
                    ye = s_va.conjugate() / abs(v_nom) ** 2
                    if len(nds) == 1:
                        y[nds[0], nds[0]] += ye
                    else:
                        p, q = nds
                        y[p, p] += ye
                        y[q, q] += ye
                        y[p, q] -= ye
                        y[q, p] -= ye
                    z_loads.append((ld.load_id, element, ye, nds))
                else:
                    injections.append((ld.model, ld.load_id, s_va, nds, v_nom))

        slack = idx(net.slack_bus, _PH)
        t, reduced_of, reg_data = _regulator_transform(net.regulators, idx, n)
        return _Model(nodes, index, y, v_base, slack, t, reduced_of, injections, z_loads,
                      line_data, trafo_data, reg_data)

    # ------------------------------------------------------------------ iteration
    def _iterate(self, snapshot, net, m: _Model, request, base) -> UnbalancedStudyResult:
        settings = request.settings
        yf = csc_matrix(m.y)
        yr = (m.t.conj().T @ yf @ m.t).tocsc()
        nr = yr.shape[0]
        slack_r = sorted({int(m.reduced_of[i]) for i in m.slack})
        free_r = [i for i in range(nr) if i not in set(slack_r)]
        slack_v = snapshot.slacks[0]
        vs = np.array([cmath.rect(slack_v.vm_pu * m.v_base[i],
                                  math.radians(slack_v.angle_deg + _SHIFT[m.nodes[i][1]]))
                       for i in m.slack])
        # initial guess: nominal magnitudes with the phase angle, propagated through T
        v0_full = np.array([cmath.rect(slack_v.vm_pu * m.v_base[i],
                                       math.radians(slack_v.angle_deg + _SHIFT[ph]))
                            for i, (_, ph) in enumerate(m.nodes)])
        v_r = np.zeros(nr, dtype=complex)
        for i in range(len(m.nodes)):
            if m.reduced_of[i] >= 0:
                v_r[m.reduced_of[i]] = v0_full[i]
        v_r[slack_r] = vs
        y_ll = yr[free_r][:, free_r].tocsc()
        y_ls = yr[free_r][:, slack_r]
        try:
            lu = splu(y_ll)
        except RuntimeError as exc:
            return UnbalancedStudyResult(**base, status="failed",
                                         messages=(f"singular admittance matrix: {exc}",))
        tol = settings.tolerance_pu * 1e6                # VA (BASE_MVA = 1)
        mismatch = math.inf
        it = 0
        while it < settings.max_iterations:
            it += 1
            v_full = m.t @ v_r
            i_full = _injection_currents(m, v_full)
            i_r = m.t.conj().T @ i_full
            v_r[free_r] = lu.solve(i_r[free_r] - y_ls @ v_r[slack_r])
            v_full = m.t @ v_r
            i_r = m.t.conj().T @ _injection_currents(m, v_full)
            s_mis = v_r[free_r] * np.conj(yr[free_r] @ v_r - i_r[free_r])
            mismatch = float(np.max(np.abs(s_mis))) if len(free_r) else 0.0
            if mismatch <= tol:
                break
        if mismatch > tol:
            return UnbalancedStudyResult(
                **base, status="failed", iterations=it, residual_mva=mismatch / 1e6,
                messages=(f"no convergence in {it} iterations; mismatch "
                          f"{mismatch / 1e6:.3e} MVA",))
        return self._results(snapshot, net, m, m.t @ v_r, it, mismatch / 1e6, base)

    # ------------------------------------------------------------------ results
    def _results(self, snapshot, net, m: _Model, v, it, mismatch, base) -> UnbalancedStudyResult:
        voltages = []
        for bus in net.energized_buses:
            node_bus = net.node_of[bus]
            for ph in _PH:
                i = m.index.get((node_bus, ph))
                if i is not None:
                    voltages.append(PhaseVoltage(bus, ph, abs(v[i]) / m.v_base[i],
                                                 math.degrees(cmath.phase(v[i]))))
        flows, losses = [], []
        for ln, ys, ysh, nf, nt in m.lines:
            vf, vt = v[nf], v[nt]
            i_f = ys @ (vf - vt) + ysh / 2 @ vf
            i_t = ys @ (vt - vf) + ysh / 2 @ vt
            loss = np.sum(vf * np.conj(i_f) + vt * np.conj(i_t))
            for k, ph in enumerate(ln.phases):
                s_f = vf[k] * np.conj(i_f[k])
                loading = (abs(i_f[k]) / (ln.max_current_ka * 1e3) * 100
                           if ln.max_current_ka else None)
                flows.append(PhaseBranchFlow(ln.line_id, ln.from_bus, ln.to_bus, ph,
                                             abs(i_f[k]), abs(i_t[k]), s_f.real / 1e6,
                                             s_f.imag / 1e6, loading))
            losses.append(BranchLoss(ln.line_id, loss.real / 1e6, loss.imag / 1e6))
        for tr, yt, ratio, nh, nl in m.trafos:
            loss = 0j
            for k, ph in enumerate(_PH):
                vh, vl = v[nh[k]], v[nl[k]]
                i_h = yt / ratio ** 2 * vh - yt / ratio * vl
                i_l = -yt / ratio * vh + yt * vl
                s_h = vh * np.conj(i_h)
                loss += s_h + vl * np.conj(i_l)
                i_rated = tr.sn_mva * 1e6 / (3 * tr.vn_hv_kv * 1e3 / math.sqrt(3))
                flows.append(PhaseBranchFlow(tr.transformer_id, tr.hv_bus, tr.lv_bus, ph,
                                             abs(i_h), abs(i_l), s_h.real / 1e6, s_h.imag / 1e6,
                                             abs(i_h) / i_rated * 100))
            losses.append(BranchLoss(tr.transformer_id, loss.real / 1e6, loss.imag / 1e6))

        load_s = 0j
        for _ld, _el, ye, nds in m.z_loads:
            vd = v[nds[0]] - (v[nds[1]] if len(nds) == 2 else 0)
            load_s += vd * np.conj(ye * vd)
        for model, _ld, s_va, nds, v_nom in m.injections:
            vd = v[nds[0]] - (v[nds[1]] if len(nds) == 2 else 0)
            load_s += vd * np.conj(_element_current(model, s_va, vd, v_nom))
        slack_s = complex(np.sum(v[m.slack] * np.conj(_slack_currents(m, v))))
        loss_total = sum(complex(b.p_loss_mw, b.q_loss_mvar) for b in losses)
        unbalance = []
        for bus in net.energized_buses:
            nb = net.node_of[bus]
            if all((nb, ph) in m.index for ph in _PH):
                va, vb, vc = (v[m.index[(nb, ph)]] for ph in _PH)
                v1 = (va + _A * vb + _A ** 2 * vc) / 3
                v2 = (va + _A ** 2 * vb + _A * vc) / 3
                unbalance.append(VoltageUnbalance(bus, abs(v2) / abs(v1) * 100))
        messages = [f"phase frame, implicit Z-bus fixed point; {len(m.nodes)} phase nodes"]
        if self.positive_sequence_lines:
            messages.append("approximation: lines without a phase matrix modelled as diag(z1)")
        return UnbalancedStudyResult(
            **base, status="computed", converged=True, iterations=it, residual_mva=mismatch,
            voltages=tuple(voltages), flows=tuple(flows), losses=tuple(losses),
            unbalance=tuple(unbalance), slack_p_mw=slack_s.real / 1e6,
            slack_q_mvar=slack_s.imag / 1e6, total_load_p_mw=load_s.real / 1e6,
            total_load_q_mvar=load_s.imag / 1e6, total_loss_p_mw=loss_total.real,
            total_loss_q_mvar=loss_total.imag, excluded_elements=net.excluded,
            messages=tuple(messages))


# ---------------------------------------------------------------------- helpers
def _line_admittances(ln: Line) -> tuple[np.ndarray, np.ndarray]:
    n = len(ln.phases)
    if ln.z_phase_ohm_per_km is not None:
        z = np.array([[complex(*c) for c in row] for row in ln.z_phase_ohm_per_km])
    else:
        z = np.eye(n) * complex(ln.r_ohm_per_km, ln.x_ohm_per_km)
    z = z * ln.length_km
    ysh = (np.zeros((n, n), dtype=complex) if ln.b_phase_us_per_km is None else
           1j * np.array(ln.b_phase_us_per_km) * 1e-6 * ln.length_km)
    return np.linalg.inv(z), ysh


def _element_current(model: str, s_va: complex, vd: complex, v_nom: complex) -> complex:
    """Current drawn by a load element at voltage ``vd`` (constant power or current)."""
    if model == "constant_power":
        return np.conj(s_va / vd)
    # constant current: |I| fixed at nominal, power-factor angle kept relative to V
    return abs(s_va) / abs(v_nom) * cmath.exp(1j * (cmath.phase(vd) - cmath.phase(s_va)))


def _injection_currents(m: _Model, v: np.ndarray) -> np.ndarray:
    """Nodal current injections (A) of PQ and I loads; negative where loads draw."""
    inj = np.zeros(len(m.nodes), dtype=complex)
    for model, _ld, s_va, nds, v_nom in m.injections:
        vd = v[nds[0]] - (v[nds[1]] if len(nds) == 2 else 0)
        i = _element_current(model, s_va, vd, v_nom)
        inj[nds[0]] -= i
        if len(nds) == 2:
            inj[nds[1]] += i
    return inj


def _slack_currents(m: _Model, v: np.ndarray) -> np.ndarray:
    """Current delivered by the source into each slack phase node."""
    y = csc_matrix(m.y)
    i_full = y @ v - _injection_currents(m, v)
    # regulators: the current that leaves a regulator's to-node into the network is drawn
    # through the regulator from its from-node (conjugate ratio)
    for _reg, units in m.regulators:
        for _ph, a, i_from, i_to in units:
            i_full[i_from] += np.conj(a) * i_full[i_to]
    return i_full[m.slack]


def _regulator_transform(regulators, idx, n: int):
    """Node transformation for ideal regulators: V_full = T V_reduced."""
    parent: dict[int, tuple[int, float]] = {}
    reg_data = []
    for reg in regulators:
        units = []
        for (ph, a), i_from, i_to in zip(reg.ratios(), idx(reg.from_bus, reg.phases),
                                         idx(reg.to_bus, reg.phases), strict=True):
            if i_to in parent:
                raise ScopeError(f"{reg.regulator_id}: node fed by two regulators")
            parent[i_to] = (i_from, a)
            units.append((ph, a, i_from, i_to))
        reg_data.append((reg, units))

    def root(i: int) -> tuple[int, float]:
        gain = 1.0
        seen = set()
        while i in parent:
            if i in seen:
                raise ScopeError("regulator loop")
            seen.add(i)
            i, a = parent[i]
            gain *= a
        return i, gain

    independent = [i for i in range(n) if i not in parent]
    reduced_of = np.full(n, -1)
    for k, i in enumerate(independent):
        reduced_of[i] = k
    t = lil_matrix((n, len(independent)), dtype=complex)
    for i in range(n):
        r, gain = root(i)
        t[i, reduced_of[r]] = gain
    return csc_matrix(t), reduced_of, reg_data
