"""Auditable planning reference, NOT a PIDE regulatory compliance engine.

Parameters from a 2018 Electro Puno TDR apply only to an explicitly opted-in
historical case. Nothing here declares the unpublished MINEM annex approved.
No external dependencies; no power flow is implemented in this module.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


class ReferenceGateError(ValueError):
    """Documentary or economic prerequisites are absent."""


ALLOWED_CATEGORIES = {
    "expansion_reinforcement",
    "quality_improvement",
    "remodeling",
    "technology_efficiency",
    "supply_safety",
}


@dataclass(frozen=True)
class CostSummary:
    capital: float
    annual_om: float
    annual_loss_cost: float
    discount_rate: float
    life_years: int
    equivalent_annual_cost: float


def annual_equivalent_cost(
    capital: float, annual_om: float, annual_loss_cost: float, rate: float, years: int
) -> CostSummary:
    """Illustrative annualized *cost*, not VAN/TIR or approved VAD computation."""
    if not isinstance(years, int) or isinstance(years, bool) or years <= 0:
        raise ReferenceGateError("Positive integer life_years required")
    vals = (capital, annual_om, annual_loss_cost, rate)
    if any(
        not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) for v in vals
    ):
        raise ReferenceGateError("Costs/rate must be finite numeric values")
    if min(capital, annual_om, annual_loss_cost) < 0 or not (0 <= rate <= 1):
        raise ReferenceGateError("Nonnegative costs and 0<=rate<=1 required")
    crf = 1.0 / years if rate == 0 else rate / -math.expm1(-years * math.log1p(rate))
    return CostSummary(
        float(capital),
        float(annual_om),
        float(annual_loss_cost),
        float(rate),
        years,
        float(capital * crf + annual_om + annual_loss_cost),
    )


def assess_reference_case(payload: dict[str, Any]) -> dict[str, Any]:
    """Evaluate documentary readiness, without certifying technical/legal compliance."""
    issues: list[str] = []
    warnings: list[str] = [
        "PIDE 2017 is a PREPUBLICATION; original Annex unavailable; "
        "evaluation is NOT normative approval"
    ]
    hist = payload.get("profile") == "ELECTRO_PUNO_TDR_2018_HISTORIC"
    if payload.get("request_official_certification"):
        raise ReferenceGateError(
            "Formal PIDE certification is never available from a prepublication TDR profile"
        )
    if payload.get("regulatory_label") in {"approved", "binding", "certified"}:
        raise ReferenceGateError("Forbidden regulatory status")
    if not payload.get("project_id"):
        issues.append("missing project_id")
    if not payload.get("network_snapshot_id"):
        issues.append("missing network_snapshot_id")
    if not payload.get("source_evidence"):
        issues.append("missing source_evidence")
    scenarios = payload.get("alternatives", [])
    if not isinstance(scenarios, list):
        raise ReferenceGateError("alternatives must be a list")
    if not scenarios:
        issues.append("at least one explicitly evaluated alternative is required")
    if hist and len(scenarios) < 3:
        issues.append("historical Electro Puno TDR case requires at least three alternatives")
    if not hist:
        warnings.append(
            "Non-historical case: no 20/4-year horizon or 3-alternative default is imposed"
        )
    r = payload.get("discount_rate")
    src = payload.get("discount_rate_source")
    years = payload.get("economic_life_years")
    if r is None or not src or years is None:
        issues.append(
            "economic rate, source and life must be explicitly declared; no PIT/default rates"
        )
    else:
        try:
            annual_equivalent_cost(0, 0, 0, r, years)
        except ReferenceGateError as error:
            issues.append(f"invalid economics - {error}")
    results = []
    seen = set()
    for a in scenarios:
        if not isinstance(a, dict):
            issues.append("non-object alternative")
            continue
        aid = a.get("id")
        if not aid or aid in seen:
            issues.append("missing or repeated alternative id")
            continue
        seen.add(aid)
        if a.get("category") not in ALLOWED_CATEGORIES:
            issues.append(f"{aid}: invalid project category")
        if not a.get("evidence"):
            issues.append(f"{aid}: no evidence of alternative design")
        status = a.get("technical_feasibility")
        if status not in {"feasible", "infeasible", "not_evaluated"}:
            issues.append(f"{aid}: feasibility state missing")
        if status == "feasible" and not a.get("solver_evidence_id"):
            issues.append(f"{aid}: no independent solver evidence")
        c = a.get("costs", {})
        if not isinstance(c, dict) or any(
            k not in c for k in ("capex", "annual_om", "annual_loss_cost")
        ):
            issues.append(f"{aid}: incomplete cost breakdown")
            continue
        annual = None
        if r is not None and src and years is not None:
            try:
                annual = annual_equivalent_cost(
                    c["capex"], c["annual_om"], c["annual_loss_cost"], r, years
                ).equivalent_annual_cost
            except (TypeError, ReferenceGateError) as e:
                issues.append(f"{aid}: invalid economics - {e}")
        results.append({"id": aid, "feasibility": status, "annualized_cost_illustrative": annual})
    return {
        "status": "reference_only_not_certified",
        "historical_tdr_case": hist,
        "documentary_complete": not issues,
        "issues": issues,
        "warnings": warnings,
        "alternatives": results,
        "official_forms_export_allowed": False,
        "original_minem_annex_verified": False,
    }
