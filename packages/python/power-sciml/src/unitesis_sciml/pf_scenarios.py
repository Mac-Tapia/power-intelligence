"""Load scenarios and leakage-safe splits for the physics-informed surrogate (spec 029).

Scenario demand is an explicit, recorded assumption, never presented as measurement:
``P_i = connected_kVA_i / 1000 * u * e_i * pf_i`` with a feeder-wide utilisation ``u``
drawn from ``U(u_min, u_max)`` and a per-load lognormal factor ``e_i`` (median 1, ``sigma``),
``Q_i = P_i * tan(acos(pf_i))`` using the source power factor. Splits are by feeder
(AC-029-S01): a feeder's scenarios never appear in two partitions.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from hashlib import sha256

import numpy as np

SCENARIO_SCHEMA = "unitesis.pf-scenario-spec/1"


@dataclass(frozen=True)
class ScenarioSpec:
    scenarios_per_feeder: int
    utilisation_min: float
    utilisation_max: float
    load_sigma: float
    seed: int
    split_fractions: tuple[float, float, float] = (0.7, 0.15, 0.15)
    contrast_fraction: float = 0.1
    max_label_residual_pu: float = 1e-6

    def __post_init__(self) -> None:
        if not 1 <= self.scenarios_per_feeder <= 100_000:
            raise ValueError("scenarios_per_feeder must be within 1..100000")
        if not 0 < self.utilisation_min <= self.utilisation_max <= 2.0:
            raise ValueError("0 < utilisation_min <= utilisation_max <= 2")
        if not 0 <= self.load_sigma <= 1.0:
            raise ValueError("load_sigma must be within [0, 1]")
        if abs(sum(self.split_fractions) - 1.0) > 1e-9 or min(self.split_fractions) <= 0:
            raise ValueError("split fractions must be positive and sum to 1")
        if not 0 <= self.contrast_fraction <= 1:
            raise ValueError("contrast_fraction must be within [0, 1]")
        if not 0 < self.max_label_residual_pu <= 1e-3:
            raise ValueError("max_label_residual_pu must be within (0, 1e-3]")

    def as_dict(self) -> dict:
        return {"schema": SCENARIO_SCHEMA, **asdict(self),
                "demand_model": "P = connected_kVA/1000 * U(u_min,u_max) * LogNormal(0, sigma)"
                                " * pf ; Q = P * tan(acos(pf))"}


def sample_loads(connected_kva: np.ndarray, power_factor: np.ndarray, spec: ScenarioSpec,
                 rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Return (P_mw, Q_mvar) arrays of shape (scenarios, loads)."""
    kva = np.asarray(connected_kva, dtype=float)
    pf = np.asarray(power_factor, dtype=float)
    if kva.shape != pf.shape or np.any(kva < 0) or np.any((pf <= 0) | (pf > 1)):
        raise ValueError("connected kVA must be >= 0 and power factor within (0, 1]")
    n = spec.scenarios_per_feeder
    u = rng.uniform(spec.utilisation_min, spec.utilisation_max, size=(n, 1))
    e = rng.lognormal(mean=0.0, sigma=spec.load_sigma, size=(n, kva.size)) \
        if spec.load_sigma > 0 else np.ones((n, kva.size))
    p = kva / 1000.0 * u * e * pf
    q = p * np.tan(np.arccos(pf))
    return p, q


def feeder_split(feeder_ids: list[str], spec: ScenarioSpec) -> dict[str, str]:
    """Deterministic feeder -> train/valid/test assignment (seeded hash order)."""
    order = sorted(feeder_ids, key=lambda f: sha256(f"{spec.seed}:{f}".encode()).hexdigest())
    n = len(order)
    n_train = max(1, math.floor(n * spec.split_fractions[0])) if n >= 3 else n
    n_valid = max(1, math.floor(n * spec.split_fractions[1])) if n >= 3 else 0
    split = {}
    for i, f in enumerate(order):
        split[f] = "train" if i < n_train else "valid" if i < n_train + n_valid else "test"
    return split
