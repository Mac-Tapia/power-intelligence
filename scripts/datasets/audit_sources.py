"""Audit registered training sources with the power-sciml quality gates.

Reads ``config/datasets/sources.v2.json``. Each source resolves under a root: ``archive``
(--archive-root, external and read-only) or ``local_reference`` (local-data/reference).
Writes a metadata-only report (hashes, counts and check metrics; never data values or
customer names) as verified evidence. Sources that need a reader or a database restore
that is not available are reported as pending, never as passed.

  python scripts/datasets/audit_sources.py --case pe-ica-electrodunas \
      --archive-root D:/Proyectos/PowerIntelligence_archivo_2026-10-20/consolidacion
"""

import argparse
import hashlib
import importlib.util
import io
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_evidence.store import publish_evidence  # noqa: E402
from unitesis_sciml.quality import (  # noqa: E402
    forecast_leakage,
    monthly_split_consistency,
    positional_time_index,
    real_coverage,
)

BLOCKING = {"oracle", "shifted", "inconsistent", "rejected", "mostly_empty"}
SPREADSHEET_SUFFIXES = {".xlsx", ".xls", ".xlsb", ".xlsm"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path, reader: dict, usecols: list[str] | None = None) -> pd.DataFrame:
    if "header_end_marker" in reader:
        text = path.read_text(encoding="utf-8", errors="replace")
        text = text.split(reader["header_end_marker"], 1)[1].lstrip("\r\n")
        frame = pd.read_csv(io.StringIO(text), usecols=usecols)
    else:
        frame = pd.read_csv(path, usecols=usecols, low_memory=False)
    if "missing_sentinel" in reader:
        frame = frame.replace(reader["missing_sentinel"], float("nan"))
    return frame


def audit_citylearn(path: Path, checks: dict) -> list[dict]:
    schema = json.loads((path / "schema.json").read_text(encoding="utf-8"))
    expected = schema["simulation_end_time_step"] - schema["simulation_start_time_step"] + 1
    bad_rows = [f.name for f in sorted(path.glob("*.csv")) if len(pd.read_csv(f)) != expected]
    out = [{"check": "row_count_vs_schema", "expected_rows": expected,
            "status": "consistent" if not bad_rows else "inconsistent", "files": bad_rows}]
    for spec in checks.get("forecast_leakage", []):
        frame = pd.read_csv(path / spec["file"])
        for col in sorted(c for c in frame.columns if c.startswith(spec["prefix"])):
            horizon = int(col.rsplit("_", 1)[-1])
            out.append({"file": spec["file"], "column": col,
                        **forecast_leakage(frame[spec["actual"]], frame[col], horizon)})
    return out


def audit_monthly(path: Path, spec: dict) -> list[dict]:
    out = []
    for f in sorted(path.glob(spec["glob"])):
        frame = pd.read_csv(f, sep=spec["sep"], decimal=spec["decimal"],
                            encoding=spec["encoding"], low_memory=False).dropna(how="all")
        frame = frame.dropna(subset=[spec["peak"], spec["offpeak"], spec["total"]], how="all")
        cols = [pd.to_numeric(frame[spec[k]], errors="coerce")
                for k in ("peak", "offpeak", "total")]
        out.append({"file": f.name, "sha256": sha256_file(f),
                    **monthly_split_consistency(*cols)})
    return out


def audit_timeseries(path: Path, checks: dict, reader: dict) -> list[dict]:
    out = []
    usecols = sorted({c[k] for c in checks.values() for k in ("column", "date_column") if k in c})
    frame = read_csv(path, reader, usecols or None)
    if "positional_time_index" in checks:
        spec = checks["positional_time_index"]
        out.append(positional_time_index(frame[spec["date_column"]], start=spec["start"],
                                         freq=spec["freq"], dayfirst=spec.get("dayfirst", False)))
    if "real_coverage" in checks:
        spec = checks["real_coverage"]
        claimed = None
        if "claimed_start" in spec:
            claimed = len(pd.date_range(spec["claimed_start"], f"{spec['claimed_end']} 23:59",
                                        freq=spec["freq"]))
        out.append(real_coverage(frame[spec["column"]], claimed_rows=claimed))
    return out


def cyme_ascii_sections(path: Path) -> dict[str, int]:
    """Data rows per ``[SECTION]`` of a CYME ASCII export (offline text parsing only)."""
    counts: dict[str, int] = {}
    current = None
    with path.open(encoding="latin-1") as stream:
        for raw in stream:
            line = raw.strip()
            if line.startswith("[") and line.endswith("]"):
                current = line[1:-1]
                counts.setdefault(current, 0)
            elif current and line and not line.startswith("FORMAT_") and "=" not in line[:20]:
                counts[current] += 1
    return counts


def audit_cyme_ascii(path: Path, spec: dict) -> list[dict]:
    out = []
    for name, required in spec.items():
        f = path / name
        if not f.is_file():
            out.append({"check": "cyme_ascii_structure", "file": name, "status": "rejected",
                        "detail": "file missing"})
            continue
        counts = cyme_ascii_sections(f)
        present = {sec for sec, n in counts.items() if n > 0}
        missing = [r for r in required if not any(r in sec for sec in present)]
        out.append({"check": "cyme_ascii_structure", "file": name, "sha256": sha256_file(f),
                    "status": "consistent" if not missing else "rejected",
                    "missing_sections": missing,
                    "rows_per_section": {k: v for k, v in sorted(counts.items()) if v}})
    return out


def inventory_folder(path: Path) -> dict:
    files = [p for p in sorted(path.rglob("*")) if p.is_file() and not p.name.startswith("~$")]
    return {"files": len(files), "bytes": sum(p.stat().st_size for p in files),
            "by_extension": dict(Counter(p.suffix.lower() or "<none>" for p in files)),
            "sha256": {str(p.relative_to(path)).replace("\\", "/"): sha256_file(p)
                       for p in files}}


def audit_source(src: dict, roots: dict[str, Path]) -> dict:
    path = roots[src.get("root", "archive")] / src["path"]
    entry = {k: src.get(k) for k in ("source_id", "case_id", "role", "purpose", "kind",
                                     "origin", "column_origin", "sensitivity",
                                     "authorization", "root", "path")}
    if not path.exists():
        return entry | {"status": "missing", "checks": []}
    kind = src["kind"]
    if kind == "sqlserver_backup":
        return entry | {"status": "pending_restore", "checks": [],
                        "sha256": sha256_file(path), "bytes": path.stat().st_size,
                        "next_step": "restore into a new local database, then run the 001 adapter"}
    if kind == "access_mdb_folder":
        inv = inventory_folder(path)
        reader_ok = importlib.util.find_spec("pyodbc") is not None
        return entry | {"status": "inventoried" if reader_ok else "pending_reader", "checks": [],
                        "inventory": inv,
                        "next_step": "authorize an Access reader (pyodbc + Access ODBC driver, "
                                     "or mdbtools) for offline table export"}
    if kind in ("spreadsheet_folder", "document_folder"):
        inv = inventory_folder(path)
        if kind == "document_folder":
            return entry | {"status": "inventoried", "checks": [], "inventory": inv}
        has_sheets = any(ext in SPREADSHEET_SUFFIXES for ext in inv["by_extension"])
        reader_ok = importlib.util.find_spec("openpyxl") is not None
        status = "pending_reader" if has_sheets and not reader_ok else "inventoried"
        return entry | {"status": status, "checks": [], "inventory": inv,
                        "next_step": "authorize openpyxl/pyxlsb to parse spreadsheets"
                        if status == "pending_reader" else "define bronze parser"}
    if kind == "citylearn_dataset":
        checks = audit_citylearn(path, src["checks"])
    elif kind == "cyme_ascii_export":
        checks = audit_cyme_ascii(path, src["checks"]["cyme_ascii_structure"])
    elif kind == "monthly_meter_bills":
        checks = audit_monthly(path, src["checks"]["monthly_split_consistency"])
    else:
        entry["sha256"] = sha256_file(path)
        checks = audit_timeseries(path, src["checks"], src.get("reader", {}))
    blocking = sorted({c["status"] for c in checks} & BLOCKING)
    return entry | {"checks": checks, "blocking": blocking,
                    "status": "blocked" if blocking else "passed_quality_gates"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--registry", type=Path, default=ROOT / "config/datasets/sources.v2.json")
    parser.add_argument("--case", help="audit only sources of this case_id")
    parser.add_argument("--include-method-references", action="store_true",
                        help="with --case, also audit role=method_reference sources")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    roots = {"archive": args.archive_root, "local_reference": ROOT / "local-data/reference"}
    selected = [s for s in registry["sources"]
                if args.case is None or s.get("case_id") == args.case
                or (args.include_method_references and s.get("role") == "method_reference")]
    results = [audit_source(src, roots) for src in selected]
    output = args.output or ROOT / "datasets/quality" / f"source_audit_{args.case or 'all'}.json"
    payload = {"schema": "unitesis.source-audit/2",
               "generated_at_utc": datetime.now(UTC).isoformat(),
               "registry": str(args.registry.relative_to(ROOT)).replace("\\", "/"),
               "case_id": args.case, "sources": results,
               "summary": dict(Counter(r["status"] for r in results)),
               "note": "Quality gates only. Passing grants neither authorization nor acceptance."}
    publish_evidence(output, payload)
    for r in results:
        print(f"[{r['role']}] {r['source_id']}: {r['status']} {r.get('blocking', '')}")
    print("summary:", payload["summary"], "->", output)
    return 0 if all(r["status"] == "passed_quality_gates" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
