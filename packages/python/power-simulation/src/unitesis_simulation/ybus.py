"""Shared per-unit admittance model and AC power-balance residual (spec 004, AC-004-02).

The single Y-bus formulation used by the Newton-Raphson engine, the comparator and the
physics-informed surrogate of spec 006: no second implementation may exist. Lines are
series R + jX (shunt susceptance not modelled yet, same scope as the BFS engine).
Per-unit bases: ``base_mva`` and each node's nominal line-to-line kV.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse
from unitesis_domain import ElectricalSnapshot, Line, Transformer
from unitesis_topology import EnergizedNetwork

BASE_MVA = 1.0


@dataclass(frozen=True)
class YBusModel:
    network: EnergizedNetwork
    base_mva: float
    index: dict[str, int]                    # node bus id -> matrix index (slack = 0)
    base_kv: np.ndarray                      # per node
    ybus: sparse.csr_matrix                  # per unit
    line_terms: tuple[tuple[Line, int, int, complex], ...]   # line, i, j, series y (pu)
    trafo_terms: tuple[tuple[Transformer, int, int, complex, complex], ...] = ()
    # transformer, hv index, lv index, series y (pu, LV side), complex ratio t (HV side)

    def node_index(self, bus_id: str) -> int:
        return self.index[self.network.node_of[bus_id]]


def build_ybus(snapshot: ElectricalSnapshot, network: EnergizedNetwork,
               base_mva: float = BASE_MVA) -> YBusModel:
    index = {node: k for k, node in enumerate(network.nodes)}
    n = len(index)
    base_kv = np.array([snapshot.bus(node).nominal_kv for node in network.nodes], dtype=float)
    rows: list[int] = []
    cols: list[int] = []
    vals: list[complex] = []
    terms: list[tuple[Line, int, int, complex]] = []
    for ln in network.lines:
        i = index[network.node_of[ln.from_bus]]
        j = index[network.node_of[ln.to_bus]]
        z_base = base_kv[i] ** 2 / base_mva
        y = z_base / ln.z_ohm                 # series admittance in per unit
        terms.append((ln, i, j, y))
        rows += [i, j, i, j]
        cols += [i, j, j, i]
        vals += [y, y, -y, -y]
    tterms: list[tuple[Transformer, int, int, complex, complex]] = []
    for tr in network.transformers:
        h = index[network.node_of[tr.hv_bus]]
        lo = index[network.node_of[tr.lv_bus]]
        kv_h, kv_l = base_kv[h], base_kv[lo]
        scale = (tr.vn_lv_kv / kv_l) ** 2 * base_mva / tr.sn_mva     # to system pu, LV side
        r = tr.vkr_percent / 100.0
        x = (tr.vk_percent ** 2 - tr.vkr_percent ** 2) ** 0.5 / 100.0
        y = 1.0 / (complex(r, x) * scale)
        mag = (tr.vn_hv_kv / kv_h) / (tr.vn_lv_kv / kv_l) * (1 + tr.tap_pos
                                                              * tr.tap_step_percent / 100)
        t = mag * np.exp(1j * np.radians(tr.shift_degree))
        tterms.append((tr, h, lo, y, t))
        rows += [h, h, lo, lo]
        cols += [h, lo, h, lo]
        vals += [y / abs(t) ** 2, -y / np.conj(t), -y / t, y]
    ybus = sparse.csr_matrix((np.array(vals, dtype=complex), (rows, cols)), shape=(n, n))
    return YBusModel(network, base_mva, index, base_kv, ybus, tuple(terms), tuple(tterms))


def specified_injections(snapshot: ElectricalSnapshot, model: YBusModel) -> np.ndarray:
    """Net specified complex injection per node in per unit (loads are negative)."""
    s = np.zeros(len(model.index), dtype=complex)
    energized = set(model.network.energized_buses)
    for ld in snapshot.loads:
        if ld.in_service and ld.bus in energized:
            s[model.node_index(ld.bus)] -= complex(ld.p_mw, ld.q_mvar) / model.base_mva
    return s


def power_mismatch(ybus: sparse.csr_matrix, v: np.ndarray, s_spec: np.ndarray) -> np.ndarray:
    """AC balance residual per node, S_calc - S_spec = V * conj(Y V) - S_spec (per unit).

    Zero at an exact solution for every non-slack node; this is the physics term reused
    by the spec 006 surrogate and the residual reported by the Newton-Raphson engine.
    """
    return v * np.conj(ybus @ v) - s_spec
