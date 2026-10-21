"""Explicit economic basis and loss monetization for engineering alternatives.

Every monetary parameter (currency, base year, discount rate, horizon, energy price,
loss load factor, O&M fraction, costs) must be declared with its documentary source:
nothing is defaulted. Results are screening values, not tariff or regulatory figures.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from math import isfinite
from pathlib import Path
from typing import Any

from .core import CostYear

HOURS_PER_YEAR = 8760.0
BASIS_SCHEMA = "unitesis.economic-basis/1"


def _finite(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return float(value)


@dataclass(frozen=True, slots=True)
class EconomicBasis:
    currency: str
    base_year: int
    discount_rate: float
    horizon_years: int
    energy_price_per_mwh: float
    loss_load_factor: float
    annual_om_fraction: float
    source: str
    conductor_cost_per_km: tuple[tuple[str, float], ...] = ()
    sha256: str = ""

    def __post_init__(self) -> None:
        if not self.currency.strip() or not self.source.strip():
            raise ValueError("currency and source are mandatory")
        for name in ("base_year", "horizon_years"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
        if not 1 <= self.horizon_years <= 60:
            raise ValueError("horizon_years must be within 1..60")
        rate = _finite(self.discount_rate, "discount_rate")
        if not 0.0 <= rate < 1.0:
            raise ValueError("discount_rate must be within [0, 1)")
        if _finite(self.energy_price_per_mwh, "energy_price_per_mwh") <= 0:
            raise ValueError("energy_price_per_mwh must be positive")
        llf = _finite(self.loss_load_factor, "loss_load_factor")
        if not 0.0 < llf <= 1.0:
            raise ValueError("loss_load_factor must be within (0, 1]")
        if _finite(self.annual_om_fraction, "annual_om_fraction") < 0:
            raise ValueError("annual_om_fraction must be non-negative")
        ids = [cid for cid, _ in self.conductor_cost_per_km]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate conductor cost entries")
        for cid, cost in self.conductor_cost_per_km:
            if _finite(cost, f"{cid}.cost_per_km") <= 0:
                raise ValueError(f"{cid}.cost_per_km must be positive")

    def cost_per_km(self, conductor_id: str) -> float | None:
        return dict(self.conductor_cost_per_km).get(conductor_id)

    def loss_cost_per_year(self, loss_p_mw: float) -> float:
        """Peak network losses (MW) -> annual loss energy cost via the loss load factor."""
        loss = _finite(loss_p_mw, "loss_p_mw")
        if loss < 0:
            raise ValueError("loss_p_mw must be non-negative")
        return loss * HOURS_PER_YEAR * self.loss_load_factor * self.energy_price_per_mwh

    def cash_flows(self, capex: float, loss_p_mw: float) -> list[CostYear]:
        """Year 0 investment; years 1..horizon O&M and monetized losses."""
        investment = _finite(capex, "capex")
        if investment < 0:
            raise ValueError("capex must be non-negative")
        losses = self.loss_cost_per_year(loss_p_mw)
        rows = [CostYear(0, investment, 0.0, 0.0, 0.0)]
        rows += [CostYear(y, 0.0, 0.0, investment * self.annual_om_fraction, losses)
                 for y in range(1, self.horizon_years + 1)]
        return rows

    def as_dict(self) -> dict[str, Any]:
        return {"currency": self.currency, "base_year": self.base_year,
                "discount_rate": self.discount_rate, "horizon_years": self.horizon_years,
                "energy_price_per_mwh": self.energy_price_per_mwh,
                "loss_load_factor": self.loss_load_factor,
                "annual_om_fraction": self.annual_om_fraction, "source": self.source,
                "conductor_cost_per_km": dict(self.conductor_cost_per_km),
                "basis_sha256": self.sha256}


def load_basis(path: str | Path) -> EconomicBasis:
    raw = Path(path).read_bytes()
    return parse_basis(json.loads(raw.decode("utf-8")), sha256(raw).hexdigest())


def parse_basis(data: dict[str, Any], digest: str | None = None) -> EconomicBasis:
    """Build a basis from a decoded document; ``digest`` defaults to its canonical SHA-256."""
    if not isinstance(data, dict):
        raise ValueError("economic basis must be a JSON object")
    if digest is None:
        digest = sha256(json.dumps(data, sort_keys=True, separators=(",", ":"),
                                   allow_nan=False).encode()).hexdigest()
    if data.get("schema") != BASIS_SCHEMA:
        raise ValueError(f"unsupported economic basis schema {data.get('schema')!r}")
    required = ("currency", "base_year", "discount_rate", "horizon_years",
                "energy_price_per_mwh", "loss_load_factor", "annual_om_fraction", "source",
                "conductor_costs")
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"economic basis missing {missing}; values are never defaulted")
    if not isinstance(data["conductor_costs"], list):
        raise ValueError("conductor_costs must be an array")
    costs = []
    for i, row in enumerate(data["conductor_costs"]):
        if "conductor_id" not in row or "cost_per_km" not in row:
            raise ValueError(f"conductor_costs[{i}] requires conductor_id and cost_per_km")
        costs.append((row["conductor_id"], row["cost_per_km"]))
    return EconomicBasis(
        currency=data["currency"], base_year=data["base_year"],
        discount_rate=data["discount_rate"], horizon_years=data["horizon_years"],
        energy_price_per_mwh=data["energy_price_per_mwh"],
        loss_load_factor=data["loss_load_factor"],
        annual_om_fraction=data["annual_om_fraction"], source=data["source"],
        conductor_cost_per_km=tuple(costs), sha256=digest)
