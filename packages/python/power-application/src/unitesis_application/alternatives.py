"""Use case: conductor alternatives for one line -> technical screen -> independent check
-> present-value ranking -> verified evidence.

Technical feasibility comes from the candidate engine on cloned scenarios; each feasible
alternative is re-solved by the independent reference and compared. An alternative whose
comparison does not pass is *not* ranked as feasible. Alternatives without an explicit cost
are reported but never priced. Ranking is engineering screening, not an approval.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from unitesis_adapters.neutral_json import ingest_file
from unitesis_domain import ElectricalSnapshot
from unitesis_economics import (
    EconomicBasis,
    load_basis,
    present_value_cost,
    rank_feasible_alternatives,
)
from unitesis_evidence.store import publish_evidence
from unitesis_optimization import (
    ConductorCatalog,
    ConductorCost,
    SizingCriteria,
    load_catalog,
    screen_line_conductors,
    swap_conductor,
)
from unitesis_ports import PowerFlowEngine
from unitesis_simulation import RadialBFSEngine

from .study import LIMITATIONS, solve_and_compare


def evaluate_conductor_alternatives(snapshot: ElectricalSnapshot, line_id: str,
                                    catalog: ConductorCatalog, criteria: SizingCriteria,
                                    basis: EconomicBasis, *,
                                    engine: PowerFlowEngine | None = None,
                                    reference: PowerFlowEngine | None = None) -> dict[str, Any]:
    engine = engine or RadialBFSEngine()
    costs = {cid: ConductorCost(cid, cost, basis.currency, basis.base_year, basis.source)
             for cid, cost in basis.conductor_cost_per_km}
    screen = screen_line_conductors(snapshot, line_id, catalog, criteria, engine, costs)
    alternatives: list[dict[str, Any]] = []
    for row in screen["candidates"]:
        alt: dict[str, Any] = {"id": row["conductor_id"], "screen": row}
        feasible = row["feasible"] is True
        if feasible:
            cond = catalog.by_id(row["conductor_id"])
            scenario = swap_conductor(snapshot, line_id, row["r_ohm_km"], row["x_ohm_km"],
                                       cond.ampacity_a / 1000.0)
            check = solve_and_compare(scenario, f"alternative:{line_id}:{cond.conductor_id}",
                                      candidate=engine, reference=reference)
            alt["independent_check"] = check["comparison"]["status"]
            feasible = alt["independent_check"] == "passed"
        else:
            alt["independent_check"] = "not_run"
        alt["technical_feasible"] = feasible
        if "capex" in row and row["status"] == "computed":
            flows = basis.cash_flows(row["capex"]["value"], row["loss_p_mw"])
            alt["annual_costs"] = [asdict(r) for r in flows]
            alt["npv_capex"] = row["capex"]["value"]
            alt["npv_losses_and_om"] = present_value_cost(flows, basis.discount_rate) - \
                row["capex"]["value"]
        else:
            alt["unpriced_reason"] = ("no explicit cost in economic basis" if "capex" not in row
                                      else f"study {row['status']}")
        alternatives.append(alt)
    priced = [a for a in alternatives if "annual_costs" in a]
    ranking = rank_feasible_alternatives(priced, basis.discount_rate)
    return {
        "line_id": line_id,
        "snapshot_sha256": snapshot.content_sha256,
        "catalog": {"name": catalog.name, "sha256": catalog.sha256,
                    "source_url": catalog.source_url},
        "criteria": screen["criteria"],
        "economic_basis": basis.as_dict(),
        "engine": engine.name,
        "alternatives": alternatives,
        "ranking": ranking,
        "recommended": ranking[0]["alternative_id"] if ranking else None,
        "smallest_feasible_section": screen["proposal_smallest_feasible_section"],
        "status": "proposal_requires_human_review",
        "technical_acceptance": False,
    }


def run_conductor_alternatives(source: str | Path, output: str | Path, *, line_id: str,
                               catalog_path: str | Path, basis_path: str | Path,
                               operating_temperature_c: float, phase_gmd_m: float,
                               v_min_pu: float = 0.95, max_loading_percent: float = 100.0,
                               reference: PowerFlowEngine | None = None) -> dict[str, Any]:
    ingestion = ingest_file(source)
    snapshot = ingestion.require_snapshot()
    report = evaluate_conductor_alternatives(
        snapshot, line_id, load_catalog(catalog_path),
        SizingCriteria(operating_temperature_c, phase_gmd_m, v_min_pu, max_loading_percent),
        load_basis(basis_path), reference=reference)
    payload = {"schema": "unitesis.alternatives-evidence/1",
               "generated_at_utc": datetime.now(UTC).isoformat(),
               "source_manifest": ingestion.manifest, **report,
               "limitations": [*LIMITATIONS,
                               "losses monetized from peak losses and a declared loss load "
                               "factor; economic basis must be reviewed before any decision"]}
    return publish_evidence(output, payload)
