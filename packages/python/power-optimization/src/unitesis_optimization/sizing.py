"""Per-line conductor screening on cloned scenarios (idea from SelecCablesAAAC segment_sizing).

Each candidate conductor is evaluated by re-solving the *whole* network with an injected
``PowerFlowEngine``; the source snapshot is never modified. Economics are added only when
the caller supplies explicit costs with their source (no synthetic defaults, unlike the
donor's ``EconomicParameters.synthetic_default``). Output is an engineering proposal:
acceptance still requires independent validation and human review.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from unitesis_domain import ElectricalSnapshot, Line, SolverSettings, StudyRequest
from unitesis_domain.units import require_finite, require_positive
from unitesis_ports import PowerFlowEngine

from .conductors import ConductorCatalog


@dataclass(frozen=True, slots=True)
class SizingCriteria:
    operating_temperature_c: float
    phase_gmd_m: float
    v_min_pu: float = 0.95
    max_loading_percent: float = 100.0

    def __post_init__(self) -> None:
        require_finite(self.operating_temperature_c, "operating_temperature_c")
        require_positive(self.phase_gmd_m, "phase_gmd_m")
        require_positive(self.v_min_pu, "v_min_pu")
        require_positive(self.max_loading_percent, "max_loading_percent")


@dataclass(frozen=True, slots=True)
class ConductorCost:
    """Explicit installed cost per km for one conductor, with documentary source."""

    conductor_id: str
    cost_per_km: float
    currency: str
    base_year: int
    source: str

    def __post_init__(self) -> None:
        require_positive(self.cost_per_km, f"{self.conductor_id}.cost_per_km")
        if not self.currency or not self.source:
            raise ValueError("currency and source are mandatory for any cost")


def swap_conductor(snapshot: ElectricalSnapshot, line_id: str, r: float, x: float,
                    ampacity_ka: float) -> ElectricalSnapshot:
    lines: list[Line] = []
    found = False
    for ln in snapshot.lines:
        if ln.line_id == line_id:
            found = True
            ln = replace(ln, r_ohm_per_km=r, x_ohm_per_km=x, max_current_ka=ampacity_ka)
        lines.append(ln)
    if not found:
        raise KeyError(line_id)
    return replace(snapshot, lines=tuple(lines))


def screen_line_conductors(snapshot: ElectricalSnapshot, line_id: str,
                           catalog: ConductorCatalog, criteria: SizingCriteria,
                           engine: PowerFlowEngine,
                           costs: dict[str, ConductorCost] | None = None) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for cond in catalog.ordered_by_section():
        r = cond.resistance_ohm_km(criteria.operating_temperature_c)
        x, basis = cond.reactance_ohm_km(criteria.phase_gmd_m, snapshot.frequency_hz)
        scenario = swap_conductor(snapshot, line_id, r, x, cond.ampacity_a / 1000.0)
        req = StudyRequest(scenario.content_sha256, f"sizing:{line_id}:{cond.conductor_id}",
                           engine.name, SolverSettings())
        res = engine.solve(scenario, req)
        row: dict[str, Any] = {"conductor_id": cond.conductor_id,
                               "section_mm2": cond.section_mm2, "r_ohm_km": r, "x_ohm_km": x,
                               "reactance_basis": basis, "status": res.status,
                               "scenario_sha256": scenario.content_sha256}
        if res.status == "computed":
            line_res = next(b for b in res.branches if b.branch_id == line_id)
            row.update(min_vm_pu=min(b.vm_pu for b in res.buses),
                       line_loading_percent=line_res.loading_percent,
                       loss_p_mw=res.total_loss_p_mw)
            row["feasible"] = (row["min_vm_pu"] >= criteria.v_min_pu
                               and line_res.loading_percent is not None
                               and line_res.loading_percent <= criteria.max_loading_percent)
        else:
            row["feasible"] = False
        if costs and cond.conductor_id in costs:
            c = costs[cond.conductor_id]
            length = snapshot.lines[[ln.line_id for ln in snapshot.lines].index(line_id)].length_km
            row["capex"] = {"value": c.cost_per_km * length, "currency": c.currency,
                            "base_year": c.base_year, "source": c.source}
        rows.append(row)
    feasible = [r for r in rows if r["feasible"]]
    proposal = feasible[0]["conductor_id"] if feasible else None
    return {"line_id": line_id, "catalog": catalog.name, "catalog_sha256": catalog.sha256,
            "criteria": {k: getattr(criteria, k) for k in criteria.__slots__},
            "engine": engine.name, "candidates": rows,
            "proposal_smallest_feasible_section": proposal,
            "status": "proposal_requires_independent_validation"}
