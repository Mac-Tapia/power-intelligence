"""Use case: real network export -> per-feeder snapshots + verified import report (spec 001).

Rules come from the application case (``import_rules.cyme_ascii`` and its frequency), never
from code defaults. Validated feeders are written as neutral JSON (re-ingestable by
``scripts/unitesis.py study``); quarantined feeders keep every rejection with its reason.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from unitesis_adapters.cyme_ascii import ReaderRules, read_export
from unitesis_adapters.neutral_json import snapshot_to_payload
from unitesis_config import ApplicationCase, CaseError
from unitesis_evidence.store import publish_evidence


def cyme_rules_for(case: ApplicationCase, *, allow_positive_sequence: bool | None = None
                   ) -> ReaderRules:
    rules = case.import_rules.get("cyme_ascii")
    if rules is None or "default_connector_max_m" not in rules:
        raise CaseError(f"case {case.case_id} declares no import_rules.cyme_ascii")
    allow = rules.get("allow_positive_sequence_approximation", False)
    if allow_positive_sequence is not None:
        allow = allow_positive_sequence
    if not isinstance(allow, bool):
        raise CaseError("allow_positive_sequence_approximation must be a boolean")
    return ReaderRules(case.frequency_hz, float(rules["default_connector_max_m"]), allow)


def import_cyme_export(case: ApplicationCase, network: str | Path, loads: str | Path,
                       equipment: str | Path, out_dir: str | Path, *,
                       allow_positive_sequence: bool | None = None) -> dict[str, Any]:
    rules = cyme_rules_for(case, allow_positive_sequence=allow_positive_sequence)
    out = Path(out_dir)
    feeders_dir = out / "feeders"
    feeders_dir.mkdir(parents=True, exist_ok=True)
    imports = read_export(Path(network), Path(loads), Path(equipment), rules)
    rows: list[dict[str, Any]] = []
    for imp in imports:
        row: dict[str, Any] = {"network_id": imp.network_id, "state": imp.state,
                               "nominal_kv": imp.manifest.get("nominal_kv"),
                               "counts": imp.manifest.get("record_counts"),
                               "non_three_phase_sections":
                                   imp.manifest.get("non_three_phase_sections"),
                               "parameter_quality": imp.manifest.get("parameter_quality"),
                               "quarantine_reasons": dict(Counter(
                                   f"{q.field}: {q.reason.split(';')[0][:60]}"
                                   for q in imp.quarantine).most_common(10))}
        if imp.snapshot is not None:
            path = feeders_dir / f"{imp.network_id}.json"
            payload = snapshot_to_payload(
                imp.snapshot, imp.network_id, authorization=case.import_rules.get(
                    "authorization", "pending_owner_confirmation"),
                provenance=f"{imp.manifest['parser']} from "
                           f"{imp.manifest['files']['network']['file']} "
                           f"(sha256 {imp.manifest['files']['network']['sha256'][:16]}); "
                           f"case {case.case_id}")
            path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
            row.update(snapshot_sha256=imp.snapshot.content_sha256,
                       snapshot_file=str(path.relative_to(out)).replace("\\", "/"),
                       load_attributes=imp.load_attributes)
        rows.append(row)
    report = {
        "schema": "unitesis.network-import/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "case_id": case.case_id,
        "parser": imports[0].manifest["parser"] if imports else None,
        "files": imports[0].manifest["files"] if imports else None,
        "interpretations": imports[0].manifest["interpretations"] if imports else [],
        "rules": imports[0].manifest["rules"] if imports else None,
        "summary": dict(Counter(r["state"] for r in rows)),
        "feeders": rows,
        "technical_acceptance": False,
    }
    return publish_evidence(out / "import_report.json", report)
