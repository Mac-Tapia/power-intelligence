"""Bronze preserves cell types/formulas and verifies raw copies; never guesses fields."""

import json
import sys
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))


def test_bronze_keeps_raw_values_formulas_and_lineage(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    from unitesis_adapters.spreadsheet import ingest_workbook

    source = tmp_path / "input.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["timestamp", "p_kw", "formula"])
    sheet.append([datetime(2024, 1, 1), 12.5, "=B2*2"])
    workbook.save(source)
    output = tmp_path / "bronze"
    report = ingest_workbook(source, output, case_id="xy-test-grid", source_id="test-source")
    assert report["rows"] == 2
    assert report["tier"] == "bronze"
    assert report["gold_eligible"] is False
    rows = [json.loads(line) for line in (output / report["sheets"][0]["file"]).read_text(
        encoding="utf-8").splitlines()]
    assert rows[1]["cells"][0]["kind"] == "datetime"
    assert rows[1]["cells"][1]["value"] == 12.5
    assert rows[1]["cells"][2] == {"kind": "formula", "value": "=B2*2"}
    assert (output / report["raw_file"]).read_bytes() == source.read_bytes()
    with pytest.raises(ValueError):
        ingest_workbook(source, output, case_id="xy-test-grid", source_id="test-source")
