"""Transparent financial comparison; no regulatory certification."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class CostYear:
    year: int  # 0 is base date
    investment: float
    operations: float
    maintenance: float
    losses_monetized: float


def present_value_cost(rows: list[CostYear], discount_rate: float) -> float:
    if not isfinite(discount_rate) or discount_rate <= -1:
        raise ValueError("Discount rate invalid")
    if not rows:
        raise ValueError("At least one cashflow required")
    seen = set()
    cost = 0.0
    for row in rows:
        if not isinstance(row.year, int) or row.year < 0 or row.year in seen:
            raise ValueError("Invalid or repeated year")
        seen.add(row.year)
        components = (row.investment, row.operations, row.maintenance, row.losses_monetized)
        if any(not isfinite(v) or v < 0 for v in components):
            raise ValueError(
                "Negative or nonfinite costs must be handled explicitly in a separate adjustment"
            )
        cost += sum(components) / (1.0 + discount_rate) ** row.year
    return cost


def rank_feasible_alternatives(alternatives: list[dict], discount_rate: float) -> list[dict]:
    result = []
    for a in alternatives:
        feasible = a.get("technical_feasible", False)
        if type(feasible) is not bool:
            raise ValueError("technical_feasible must be a boolean")
        if not feasible:
            continue
        total = present_value_cost([CostYear(**r) for r in a["annual_costs"]], discount_rate)
        result.append(
            {
                "alternative_id": a["id"],
                "npv_total_cost": total,
                "status": "engineering_screening_only",
            }
        )
    return sorted(result, key=lambda x: (x["npv_total_cost"], x["alternative_id"]))
