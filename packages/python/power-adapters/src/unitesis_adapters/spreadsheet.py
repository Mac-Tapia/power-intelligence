"""Spec 035: typed bronze from offline Excel bytes; no inferred electrical meaning."""

from __future__ import annotations

import json
import math
import shutil
from datetime import date, datetime, time
from hashlib import file_digest
from pathlib import Path
from typing import Any


def digest(path: Path) -> str:
    with path.open("rb") as handle:
        return file_digest(handle, "sha256").hexdigest()


def _value(value: Any, kind: str | None = None) -> dict[str, Any]:
    if kind == "formula":
        return {"kind": kind, "value": value}
    if isinstance(value, (datetime, date, time)):
        return {"kind": type(value).__name__, "value": value.isoformat()}
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite spreadsheet cell")
    if value is not None and not isinstance(value, (str, int, float, bool)):
        raise ValueError("unsupported cell type")
    return {"kind": kind or type(value).__name__, "value": value}


def _sheets(path: Path):
    if path.suffix.lower() in {".xlsx", ".xlsm"}:
        import openpyxl

        book = openpyxl.load_workbook(path, read_only=True, data_only=False, keep_links=False)
        try:
            for sheet in book:
                def rows(sheet=sheet):
                    for row in sheet.iter_rows():
                        yield [_value(c.value, "formula" if c.data_type == "f" else None)
                               for c in row]
                yield sheet.title, rows(), {"formula_representation": "formula_text"}
        finally:
            book.close()
    elif path.suffix.lower() == ".xls":
        import xlrd

        book = xlrd.open_workbook(path, on_demand=True)
        try:
            for sheet in book.sheets():
                def rows(sheet=sheet):
                    for i in range(sheet.nrows):
                        yield [_value(c.value, "excel_date_serial" if c.ctype == 3 else None)
                               for c in sheet.row(i)]
                yield sheet.name, rows(), {"formula_representation": "cached_values_only",
                                           "excel_datemode": book.datemode}
        finally:
            book.release_resources()
    elif path.suffix.lower() == ".xlsb":
        from pyxlsb import open_workbook

        with open_workbook(str(path)) as book:
            for name in book.sheets:
                with book.get_sheet(name) as sheet:
                    yield name, ([_value(c.v) for c in row] for row in sheet.rows()), {
                        "formula_representation": "cached_values_only",
                        "date_system": "not_interpreted"}
    else:
        raise ValueError("unsupported Excel format")


def ingest_workbook(source: Path, output: Path, *, case_id: str, source_id: str) -> dict[str, Any]:
    source, output = Path(source).absolute(), Path(output).absolute()
    if any(p.is_symlink() or p.is_junction() for p in [source, *source.parents,
                                                    output, *output.parents]):
        raise ValueError("linked workbook paths are forbidden")
    if output.exists():
        raise ValueError("bronze destination must be new")
    checksum = digest(source)
    output.mkdir(parents=True)
    raw = output / ("raw" + source.suffix.lower())
    shutil.copyfile(source, raw)
    if digest(raw) != checksum or digest(source) != checksum:
        raise ValueError("raw changed during ingestion")
    sheets = []
    for i, (name, rows, metadata) in enumerate(_sheets(raw)):
        target = output / f"sheet-{i:03d}.jsonl"
        count = 0
        with target.open("x", encoding="utf-8") as handle:
            for count, cells in enumerate(rows, 1):
                handle.write(json.dumps({"row": count, "cells": cells},
                                        ensure_ascii=False, allow_nan=False) + "\n")
        sheets.append({"name": name, "file": target.name, "rows": count,
                       "sha256": digest(target), **metadata})
    report = {"schema": "unitesis.spreadsheet-bronze/1", "case_id": case_id,
              "source_id": source_id, "tier": "bronze", "raw_sha256": checksum,
              "raw_file": raw.name, "sheets": sheets, "rows": sum(s["rows"] for s in sheets),
              "column_origin": "source_values_without_inference", "gold_eligible": False,
              "limitations": ["units, meaning, timezone and mapping require explicit silver rules",
                              "XLSX/XLSM formula text preserved, never evaluated",
                              "XLS/XLSB expose cached values, not formula expressions",
                              "XLS date serials retain the workbook datemode",
                              "XLSB numeric date serials are not inferred as timestamps"]}
    (output / "manifest.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                          encoding="utf-8")
    return report
