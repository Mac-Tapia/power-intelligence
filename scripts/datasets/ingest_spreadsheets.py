"""Ingest all workbooks of a registered, authorized application-case source to bronze."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))

from unitesis_adapters.spreadsheet import digest, ingest_workbook
from unitesis_config import load_case
from unitesis_evidence import publish_evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    case = load_case(ROOT / "config/cases" / f"{args.case}.json")
    if not case.authorized:
        raise ValueError("case authorization required")
    sources = json.loads((ROOT / "config/datasets/sources.v2.json").read_text(encoding="utf-8"))
    source = next(s for s in sources["sources"] if s["source_id"] == args.source_id)
    if (source["case_id"] != case.case_id or source["role"] != "application_case"
            or source["kind"] != "spreadsheet_folder" or source["root"] != "archive"):
        raise ValueError("not an application-case spreadsheet source")
    output = args.output.absolute()
    if any(p.is_symlink() or p.is_junction() for p in [output, *output.parents]):
        raise ValueError("linked output forbidden")
    if not output.resolve().is_relative_to(ROOT / "local-data") or output.exists():
        raise ValueError("new output under local-data required")
    folder = (args.archive_root / source["path"]).resolve(strict=True)
    if not folder.is_relative_to(args.archive_root.resolve(strict=True)):
        raise ValueError("source outside registered archive")
    books = sorted(p for p in folder.rglob("*") if p.is_file()
                   and p.suffix.lower() in {".xls", ".xlsx", ".xlsm", ".xlsb"})
    if not books:
        raise ValueError("no workbooks found")
    reports, seen = [], set()
    for book in books:
        checksum = digest(book)
        if checksum in seen:
            continue
        seen.add(checksum)
        reports.append(ingest_workbook(book, output / checksum, case_id=case.case_id,
                                       source_id=args.source_id))
    report = {"schema": "unitesis.source-bronze/1", "case_id": case.case_id,
              "source_id": args.source_id, "workbooks_found": len(books),
              "unique_workbooks": len(reports), "rows": sum(r["rows"] for r in reports),
              "workbooks": reports, "gold_eligible": False}
    publish_evidence(output / "evidence.json", report)
    print(json.dumps({k: report[k] for k in ("source_id", "unique_workbooks", "rows",
                                            "gold_eligible")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
