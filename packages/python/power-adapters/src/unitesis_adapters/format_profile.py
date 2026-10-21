"""Reverse engineering of data formats for interoperability (REA; ADR-0012, specs 001/037).

Design recovery and redocumentation in the sense of Chikofsky & Cross (1990): from export
files the data owner provided, recover the structure of the format (sections, declared
columns, types, fill ratios) and compare it with what the reader consumes, so that unused
information becomes visible and every reader rule rests on observed structure.

Scope limits (ADR-0012): only files supplied by the data owner; no decompilation,
disassembly or interception of proprietary programs; no bypass of licences or protection.
The profile never copies record values: it reports types and counts. Numeric ranges are
reported only for catalogue sections listed in ``RANGE_SECTIONS`` (equipment parameters,
not customers or coordinates).
"""

from __future__ import annotations

import math
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any

from .cyme_ascii import parse_sections

PROFILE_SCHEMA = "unitesis.format-profile/1"
RANGE_SECTIONS = frozenset({"LINE", "LINE UNBALANCED", "CONDUCTOR", "SPACING TABLE FOR LINE",
                            "CONCENTRIC NEUTRAL CABLE", "CABLE", "TRANSFORMER", "REGULATOR",
                            "SHUNT CAPACITOR", "SWITCH", "FUSE", "BREAKER", "RECLOSER"})

# (file role, section) -> columns the CYME reader consumes today (unitesis.cyme-ascii/1)
CYME_READER_COVERAGE: dict[tuple[str, str], frozenset[str]] = {
    ("network", "SECTION"): frozenset({"SectionID", "FromNodeID", "ToNodeID", "Phase"}),
    ("network", "LINE CONFIGURATION"): frozenset({"SectionID", "LineCableID", "Length"}),
    ("network", "SOURCE"): frozenset({"NodeID", "NetworkID", "DesiredVoltage"}),
    ("network", "NODE"): frozenset({"NodeID", "CoordX", "CoordY"}),
    ("network", "INTERMEDIATE NODES"): frozenset({"SectionID", "SeqNumber", "CoordX", "CoordY"}),
    ("network", "SWITCH SETTING"): frozenset({"SectionID", "Status"}),
    ("network", "SECTIONALIZER SETTING"): frozenset({"SectionID", "Status"}),
    ("network", "FUSE SETTING"): frozenset({"SectionID", "Status"}),
    ("network", "BREAKER SETTING"): frozenset({"SectionID", "Status"}),
    ("network", "RECLOSER SETTING"): frozenset({"SectionID", "Status"}),
    ("loads", "CUSTOMER LOADS"): frozenset({"SectionID", "DeviceNumber", "ValueType", "Value1",
                                            "Value2", "ConnectedKVA", "KWH",
                                            "NumberOfCustomer", "Phase"}),
    ("loads", "LOADS"): frozenset({"DeviceNumber", "Connection"}),
    ("equipment", "LINE"): frozenset({"ID", "R1", "X1", "R0", "X0", "B1", "B0", "Amps"}),
    ("equipment", "CABLE"): frozenset({"ID", "R1", "X1", "R0", "X0", "B1", "B0", "Amps"}),
    ("equipment", "CONCENTRIC NEUTRAL CABLE"): frozenset({"ID", "R1", "X1", "R0", "X0", "B1",
                                                          "B0", "Amps"}),
    ("equipment", "TAPE SHIELDED CABLE"): frozenset({"ID", "R1", "X1", "R0", "X0", "B1",
                                                     "B0", "Amps"}),
}


def _kind(value: str) -> str:
    if value == "":
        return "empty"
    try:
        number = float(value)
    except ValueError:
        return "text"
    return "number" if math.isfinite(number) else "text"


def profile_file(path: Path, role: str,
                 coverage: dict[tuple[str, str], frozenset[str]] | None = None
                 ) -> dict[str, Any]:
    """Structure of one sectioned ASCII export, with reader coverage per column."""
    coverage = coverage if coverage is not None else CYME_READER_COVERAGE
    sections = parse_sections(path)
    out: dict[str, Any] = {"role": role, "file": path.name,
                           "sha256": sha256(path.read_bytes()).hexdigest(), "sections": {}}
    for name, rows in sorted(sections.items()):
        data = [r for r in rows if not r.get("__feeder__")]
        columns: dict[str, dict[str, Any]] = {}
        kinds: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        ranges: dict[str, list[float]] = {}
        order: list[str] = []
        for row in data:
            for col, value in row.items():
                if col not in kinds:
                    order.append(col)
                k = _kind(value)
                kinds[col][k] += 1
                if k == "number" and name in RANGE_SECTIONS:
                    v = float(value)
                    lo_hi = ranges.setdefault(col, [v, v])
                    lo_hi[0], lo_hi[1] = min(lo_hi[0], v), max(lo_hi[1], v)
        used = coverage.get((role, name), frozenset())
        for col in order:
            counts = dict(kinds[col])
            filled = len(data) - counts.get("empty", 0)
            col_info: dict[str, Any] = {
                "type": max((k for k in counts if k != "empty"), key=counts.get,
                            default="empty"),
                "fill_ratio": round(filled / len(data), 4) if data else 0.0,
                "consumed_by_reader": col in used,
            }
            if col in ranges:
                col_info["range"] = ranges[col]
            columns[col] = col_info
        out["sections"][name] = {
            "rows": len(data), "columns": columns,
            "consumed_by_reader": bool(used),
            "unused_filled_columns": sorted(c for c, i in columns.items()
                                            if not i["consumed_by_reader"]
                                            and i["fill_ratio"] > 0),
        }
    return out


def profile_export(files: dict[str, Path],
                   coverage: dict[tuple[str, str], frozenset[str]] | None = None
                   ) -> dict[str, Any]:
    """Profile a multi-file export (``{"network": ..., "loads": ..., "equipment": ...}``)."""
    profiles = [profile_file(Path(p), role, coverage) for role, p in sorted(files.items())]
    unread = [{"role": p["role"], "section": name, "rows": s["rows"]}
              for p in profiles for name, s in p["sections"].items()
              if s["rows"] and not s["consumed_by_reader"]]
    return {"schema": PROFILE_SCHEMA, "method": "design recovery from owner-supplied files "
            "(ADR-0012); no record values copied", "files": profiles,
            "unread_sections_with_rows": unread}


def structure_only(profile: dict[str, Any]) -> dict[str, Any]:
    """Redacted copy safe to version: structure, types and coverage; no ranges, no hashes."""
    files = []
    for p in profile["files"]:
        sections = {name: {"columns": {c: {k: v for k, v in i.items() if k != "range"}
                                       for c, i in s["columns"].items()},
                           "consumed_by_reader": s["consumed_by_reader"],
                           "populated": s["rows"] > 0}
                    for name, s in p["sections"].items()}
        files.append({"role": p["role"], "sections": sections})
    return {"schema": PROFILE_SCHEMA, "method": profile["method"], "files": files,
            "unread_sections": sorted({f"{u['role']}:{u['section']}"
                                       for u in profile["unread_sections_with_rows"]})}


def infer_code_mapping(pairs: list[tuple[str | None, str | None]], *,
                       min_support: int = 1) -> dict[str, Any]:
    """Recover the meaning of an undocumented code from a documented field of the same record.

    ``pairs`` are (reference value, code) observed on joined records (e.g. section phase
    text vs a load's numeric phase code). The mapping is ``deterministic`` only when every
    code co-occurs with a single reference value; otherwise the conflicts are reported and
    nothing is assumed. Codes seen fewer than ``min_support`` times stay ``unconfirmed``.
    """
    seen: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for ref, code in pairs:
        if ref is None or code is None:
            continue
        seen[code][ref] += 1
    mapping, conflicts, unconfirmed = {}, {}, {}
    for code, refs in sorted(seen.items()):
        if len(refs) > 1:
            conflicts[code] = dict(refs)
        elif sum(refs.values()) < min_support:
            unconfirmed[code] = dict(refs)
        else:
            (ref, n), = refs.items()
            mapping[code] = {"means": ref, "support": n}
    status = "deterministic" if mapping and not conflicts else (
        "conflicting" if conflicts else "insufficient")
    return {"status": status, "mapping": mapping, "conflicts": conflicts,
            "unconfirmed": unconfirmed,
            "observations": sum(sum(r.values()) for r in seen.values())}
