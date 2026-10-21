"""Use case: VNR-GIS restored database -> feeder snapshots, geometry and report (spec 001).

R/X come from the case's real equipment catalogue (CYME ``BD_Equipo``), keyed as the REA
recovered (``CodNorma`` + voltage letter); the catalogue is checked for plausibility and
its findings travel with the report. Nothing missing is filled in.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from unitesis_adapters.cyme_ascii import _float, parse_sections
from unitesis_adapters.neutral_json import snapshot_to_payload
from unitesis_adapters.vnrgis_reader import (
    VnrRules,
    build_feeders,
    catalogue_plausibility,
    fetch_tables,
)
from unitesis_config import ApplicationCase, CaseError

CATALOGUE_SECTIONS = ("LINE", "CABLE", "CONCENTRIC NEUTRAL CABLE", "TAPE SHIELDED CABLE")


def catalogue_from_cyme(equipment: Path) -> dict[str, tuple[float, float, float | None]]:
    eq = parse_sections(equipment)
    out: dict[str, tuple[float, float, float | None]] = {}
    for sec in CATALOGUE_SECTIONS:
        for row in eq.get(sec, []):
            r1, x1, amps = _float(row.get("R1")), _float(row.get("X1")), _float(row.get("Amps"))
            if row.get("ID") and row["ID"] != "DEFAULT" and r1 is not None and x1 is not None:
                out[row["ID"]] = (r1, x1, amps if amps and amps > 0 else None)
    return out


def vnr_rules_for(case: ApplicationCase, catalogue: dict, source: str) -> VnrRules:
    rules = case.import_rules.get("vnrgis")
    if not rules:
        raise CaseError(f"case {case.case_id} declares no import_rules.vnrgis")
    return VnrRules(case.frequency_hz, tuple(sorted(rules["voltage_codes"].items())), catalogue,
                    float(rules["sed_power_factor"]),
                    tuple(rules.get("included_states", ("E", "M", "N"))), source)


def import_vnrgis(case: ApplicationCase, client, database: str, equipment: str | Path,
                  out_dir: str | Path) -> dict[str, Any]:
    equipment = Path(equipment)
    catalogue = catalogue_from_cyme(equipment)
    rules = vnr_rules_for(case, catalogue, equipment.name)
    tables = fetch_tables(client, database)
    source = {"database": database, "catalogue_file": equipment.name,
              "catalogue_sha256": hashlib.sha256(equipment.read_bytes()).hexdigest()}
    imports = build_feeders(tables, rules, source)
    out = Path(out_dir)
    feeders_dir = out / "feeders"
    feeders_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for imp in imports:
        row: dict[str, Any] = {
            "network_id": imp.network_id, "state": imp.state,
            "nominal_kv": imp.manifest.get("nominal_kv"),
            "counts": imp.manifest.get("record_counts"),
            "total_length_km": imp.manifest.get("total_length_km"),
            "total_demand_mw": imp.manifest.get("total_demand_mw"),
            "quarantine_reasons": dict(Counter(f"{q.field}: {q.reason[:60]}"
                                               for q in imp.quarantine).most_common(10))}
        if imp.snapshot is not None:
            path = feeders_dir / f"{imp.network_id}.json"
            payload = snapshot_to_payload(imp.snapshot, imp.network_id,
                                          provenance=f"unitesis.vnrgis-reader/1 from {database}; "
                                                     f"R/X {equipment.name}; case {case.case_id}")
            path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
            geo_path = feeders_dir / f"{imp.network_id}.geo.json"
            geo_path.write_text(json.dumps({"crs": case.crs, **imp.geometry},
                                           separators=(",", ":")), encoding="utf-8")
            row.update(snapshot_sha256=imp.snapshot.content_sha256,
                       snapshot_file=str(path.relative_to(out)).replace("\\", "/"),
                       geometry_file=str(geo_path.relative_to(out)).replace("\\", "/"))
        rows.append(row)
    states = Counter(r["state"] for r in rows)
    report = {"schema": "unitesis.network-import/1", "format": "vnrgis",
              "generated_at_utc": datetime.now(UTC).isoformat(), "case_id": case.case_id,
              "source": source, "rules": imports[0].manifest["rules"] if imports else {},
              "interpretations": imports[0].manifest["interpretations"] if imports else [],
              "summary": {"feeders": len(rows), **states},
              "catalogue_findings": catalogue_plausibility(catalogue),
              "feeders": rows, "technical_acceptance": False}
    (out / "import_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    return report
