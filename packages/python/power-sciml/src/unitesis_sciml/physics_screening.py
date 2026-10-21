"""Physics screening baselines and learned warm starts (spec 029, AC-029-S06).

A learned surrogate is only worth deploying if it beats the physics baseline on the same
split. The relevant baseline is not only the linear prior (one iteration) but a truncated
fixed-point solve: ``V_L <- Y_LL^-1 (conj(S_L / V_L) - Y_L0 V_0)`` for ``k`` iterations on the
same Y-bus as the solver, with the slack held at its known voltage. ``refine`` applies the
same iterations from any start (e.g. a GNN prediction), which is how a learned model can
earn its place: fewer physics iterations for the same accuracy.

Every result carries the remaining nodal power mismatch, so a screening answer whose
mismatch exceeds the threshold is routed to the full solver instead of being trusted.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

BASE_MVA = 1.0


@dataclass(frozen=True, slots=True)
class ScreeningResult:
    v: np.ndarray                 # S x N complex p.u.
    mismatch_pu: np.ndarray       # S, max nodal |S_calc - S_spec| on non-slack nodes
    iterations: int


class FixedPointScreener:
    """Truncated Z-bus fixed point on one feeder; the factorisation is reused across calls."""

    def __init__(self, ybus: np.ndarray, slack_v: complex = 1.0 + 0j) -> None:
        if ybus.ndim != 2 or ybus.shape[0] != ybus.shape[1] or ybus.shape[0] < 1:
            raise ValueError("square Y-bus required")
        self.ybus = ybus
        self.slack_v = slack_v
        self.z_ll = np.linalg.inv(ybus[1:, 1:]) if ybus.shape[0] > 1 else np.zeros((0, 0))
        self.y_l0 = ybus[1:, 0]

    def specified(self, p_mw: np.ndarray, q_mvar: np.ndarray) -> np.ndarray:
        return -(np.asarray(p_mw) + 1j * np.asarray(q_mvar)) / BASE_MVA

    def mismatch(self, v: np.ndarray, s_spec: np.ndarray) -> np.ndarray:
        s_calc = v * np.conj(v @ self.ybus.T)
        if v.shape[1] < 2:
            return np.zeros(v.shape[0])
        return np.abs(s_calc[:, 1:] - s_spec[:, 1:]).max(axis=1)

    def refine(self, p_mw: np.ndarray, q_mvar: np.ndarray, iterations: int,
               v0: np.ndarray | None = None) -> ScreeningResult:
        if iterations < 0:
            raise ValueError("iterations must be >= 0")
        s = self.specified(p_mw, q_mvar)
        v = np.ones(s.shape, dtype=complex) if v0 is None else np.array(v0, dtype=complex)
        v[:, 0] = self.slack_v
        for _ in range(iterations):
            if v.shape[1] > 1:
                v[:, 1:] = (np.conj(s[:, 1:] / v[:, 1:]) - self.y_l0[None, :] * self.slack_v) \
                    @ self.z_ll.T
        return ScreeningResult(v, self.mismatch(v, s), iterations)
