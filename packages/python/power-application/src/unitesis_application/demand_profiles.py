"""Use case: measured line demand -> silver -> gold forecast datasets -> profiles -> baselines.

Spec 016 on the pilot case; the medallion tiers follow spec 035. Silver rules come from the
case (``import_rules.line_demand_xlsx``); nothing is inferred silently. Profiles are built
on the training period only and the baselines are scored on the gold test split, so the
numbers are the yardstick for any learned forecaster. Values stay in ``local-data``; the
evidence carries counts, hashes and metrics only.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from unitesis_config import ApplicationCase, CaseError
from unitesis_evidence.store import publish_evidence
from unitesis_sciml.datasets import DatasetSpec, build_dataset, write_dataset
from unitesis_sciml.load_profiles import (
    SilverRules,
    apparent_power_consistency,
    baseline_forecasts,
    silver_from_rows,
    typical_profiles,
)

RULES_KEY = "line_demand_xlsx"


def silver_rules_for(case: ApplicationCase) -> SilverRules:
    rules = case.import_rules.get(RULES_KEY)
    if not rules:
        raise CaseError(f"case {case.case_id} declares no import_rules.{RULES_KEY}")
    return SilverRules(rules["timestamp_header"],
                       tuple(tuple(c) for c in rules["columns"]),
                       rules["frequency"], case.timezone, bool(rules["interval_ending"]))


def _sheet_with_header(bronze_dir: Path, header: str) -> tuple[Path, Path]:
    """The bronze sheet whose first row contains the declared timestamp header."""
    for manifest in sorted(bronze_dir.glob("*/manifest.json")):
        info = json.loads(manifest.read_text(encoding="utf-8"))
        for sheet in info.get("sheets", []):
            path = manifest.parent / sheet["file"]
            with path.open(encoding="utf-8") as fh:
                first = json.loads(fh.readline())
            names = [str(c.get("value", "")).replace("\n", " ").strip() for c in first["cells"]]
            if header in names:
                return manifest, path
    raise FileNotFoundError(f"no bronze sheet with header {header!r} in {bronze_dir}")


def run_line_demand_pipeline(case: ApplicationCase, bronze_dir: str | Path,
                             out_dir: str | Path, evidence: str | Path) -> dict[str, Any]:
    rules = silver_rules_for(case)
    manifest_path, sheet = _sheet_with_header(Path(bronze_dir), rules.timestamp_header)
    with sheet.open(encoding="utf-8") as fh:
        rows = [json.loads(line)["cells"] for line in fh]
    silver, quality = silver_from_rows(rows, rules)
    out = Path(out_dir)
    silver_dir = out / "silver"
    silver_dir.mkdir(parents=True, exist_ok=True)
    silver_csv = silver_dir / "line-demand.csv"
    silver.to_csv(silver_csv, float_format="%.6f")
    series_ids = sorted({s for _, s, _ in rules.columns})
    consistency = {s: apparent_power_consistency(silver.get(f"{s}_kw"), silver.get(f"{s}_kvar"),
                                                 silver.get(f"{s}_kva"))
                   for s in series_ids if {f"{s}_kw", f"{s}_kvar", f"{s}_kva"} <= set(silver)}
    results: dict[str, Any] = {}
    profiles_all: dict[str, Any] = {}
    for s in series_ids:
        col = f"{s}_kw"
        if col not in silver:
            continue
        naive = silver[[col]].copy()
        naive.index = naive.index.tz_localize(None)          # wall clock of the case timezone
        csv = silver_dir / f"{s}_kw.csv"
        naive.rename_axis("timestamp").to_csv(csv, float_format="%.6f")
        spec = DatasetSpec(timestamp_column="timestamp", target_column=col,
                           frequency=rules.frequency, horizon_steps=96)
        splits, gold_manifest = build_dataset(csv, spec)
        gold_dir = write_dataset(splits, gold_manifest, out / "gold" / f"forecast-{s}-kw")
        (gold_dir / "manifest.json").write_text(json.dumps(gold_manifest, indent=1, default=str),
                                                 encoding="utf-8")
        train_end = pd.Timestamp(gold_manifest["splits"]["train"]["end"])
        test_start = pd.Timestamp(gold_manifest["splits"]["test"]["start"])
        series = naive[col]
        profiles = typical_profiles(series[series.index <= train_end])
        profiles_all[s] = profiles
        results[s] = {
            "gold_dataset_sha256": gold_manifest["dataset_sha256"],
            "gold_quality": gold_manifest["quality"],
            "splits": {k: {kk: v[kk] for kk in ("rows", "start", "end")}
                       for k, v in gold_manifest["splits"].items()},
            "profiles_built_until": str(train_end),
            "profile_cells": len(profiles["profiles"]),
            "profile_missing_cells": profiles["missing_cells"],
            "baselines_day_ahead": baseline_forecasts(series, train_end, test_start, profiles),
        }
    profiles_path = out / "gold" / "load-profiles.json"
    profiles_payload = {"schema": "unitesis.load-profiles/1", "case_id": case.case_id,
                        "source_id": "eldu-line-demand-l6605-l6606",
                        "built_on": "training period only", "series": profiles_all}
    profiles_path.write_text(json.dumps(profiles_payload, indent=1), encoding="utf-8")
    payload = {
        "schema": "unitesis.demand-pipeline-evidence/1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "case_id": case.case_id,
        "bronze_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "bronze_sheet_sha256": hashlib.sha256(sheet.read_bytes()).hexdigest(),
        "silver_rules": {"timestamp_header": rules.timestamp_header,
                         "columns": [list(c) for c in rules.columns],
                         "frequency": rules.frequency, "timezone": rules.timezone,
                         "interval_ending": rules.interval_ending},
        "silver_quality": quality,
        "silver_sha256": hashlib.sha256(silver_csv.read_bytes()).hexdigest(),
        "apparent_power_consistency": consistency,
        "series": results,
        "load_profiles_sha256": hashlib.sha256(profiles_path.read_bytes()).hexdigest(),
        "limitations": [
            "holidays are not separated (calendar exogenous source not yet read)",
            "profiles are shapes in p.u. of each day's peak; energy scale comes from the study",
            "line measurements, not per-customer: allocation to loads is a declared rule",
        ],
        "technical_acceptance": False,
    }
    return publish_evidence(evidence, payload)
