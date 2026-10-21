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
from unitesis_domain import ElectricalSnapshot, Line
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
    ybus = sparse.csr_matrix((np.array(vals, dtype=complex), (rows, cols)), shape=(n, n))
    return YBusModel(network, base_mva, index, base_kv, ybus, tuple(terms))


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
