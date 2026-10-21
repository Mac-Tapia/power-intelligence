"""Offline reader for CYMDIST ASCII exports (spec 001, T010; ADR-0010: no CYME runtime).

Reads the three text files of an export (network, loads, equipment catalogue) and builds
one ``ElectricalSnapshot`` per feeder (``NetworkID``). Every transformation is a declared
rule recorded in the per-feeder manifest; anything that cannot be represented goes to the
quarantine and blocks that feeder, never the silent completion of a value.

Format facts used (CYME ASCII, ``[SI]`` units): section lengths in metres, line/cable
``R1``/``X1`` in ohm/km, ``Amps`` in A, ``DesiredVoltage`` in kV line-to-line, customer
loads with ``ValueType`` 2 = (kW, power factor). Interpretations that the format does not
make explicit are listed in ``INTERPRETATIONS`` and copied into every manifest.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any

from unitesis_domain import (
    Bus,
    ElectricalSnapshot,
    Line,
    Load,
    QuarantineRecord,
    Slack,
    SnapshotError,
    Switch,
)

PARSER = "unitesis.cyme-ascii/1"
INTERPRETATIONS = (
    "section Length is metres ([SI] export)",
    "device setting Status 1 = closed, 0 = open",
    "customer load ValueType 2 = Value1 kW total over its phases, Value2 power factor",
    "a load is connected at the ToNode of its section",
    "feeder nominal voltage = SOURCE DesiredVoltage (kV line-to-line); slack at 1.0 pu",
)
_PHASES_3 = "ABC"


class CymeFormatError(ValueError):
    """The files are not a readable CYME ASCII export."""


@dataclass(frozen=True, slots=True)
class ReaderRules:
    """Explicit import rules; each one is recorded with its counts in the manifest."""

    frequency_hz: float
    default_connector_max_m: float
    allow_positive_sequence_approximation: bool = False

    def __post_init__(self) -> None:
        if self.frequency_hz not in (50.0, 60.0):
            raise ValueError("frequency_hz must come from the application case (50 or 60)")
        if not 0 <= self.default_connector_max_m <= 50:
            raise ValueError("default_connector_max_m must be within [0, 50] m")


@dataclass
class FeederImport:
    network_id: str
    state: str                                   # model_validated | quarantined
    manifest: dict[str, Any]
    quarantine: list[QuarantineRecord] = field(default_factory=list)
    snapshot: ElectricalSnapshot | None = None
    load_attributes: dict[str, dict[str, float]] = field(default_factory=dict)


def parse_sections(path: Path) -> dict[str, list[dict[str, str]]]:
    """``[SECTION]`` -> rows as dicts, honouring repeated ``FORMAT_`` headers.

    ``FEEDER=`` lines inside ``[SECTION]`` are returned as rows with key ``__feeder__``.
    """
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    current: str | None = None
    formats: dict[str, list[str]] = {}
    with path.open(encoding="latin-1") as stream:
        for raw in stream:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                current = line[1:-1]
                out.setdefault(current, [])
                continue
            if current is None:
                continue
            if line.startswith("FORMAT_"):
                key, _, cols = line.partition("=")
                formats[key[7:]] = cols.split(",")
                continue
            if line.startswith("FEEDER="):
                values = line[7:].split(",")
                cols = formats.get("FEEDER", ["NetworkID", "HeadNodeID"])
                out[current].append({"__feeder__": "1", **dict(zip(cols, values, strict=False))})
                continue
            if "=" in line.split(",")[0]:
                continue                          # GENERAL key=value lines
            fmt_key = current.replace(" ", "").upper()
            cols = next((v for k, v in formats.items() if k.upper() == fmt_key), None)
            if cols is None:
                cols = formats.get(fmt_key.rstrip("S")) or formats.get(fmt_key + "S")
            if cols is None:
                raise CymeFormatError(f"{path.name}: no FORMAT_ header for [{current}]")
            out[current].append(dict(zip(cols, line.split(","), strict=False)))
    return dict(out)


def _file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _float(value: str | None) -> float | None:
    try:
        number = float(value) if value not in (None, "") else None
    except ValueError:
        return None
    return number if number is not None and math.isfinite(number) else None


def read_export(network: Path, loads: Path, equipment: Path,
                rules: ReaderRules) -> list[FeederImport]:
    net = parse_sections(network)
    lds = parse_sections(loads)
    eqp = parse_sections(equipment)
    for name, needed in ((network, ("SECTION", "LINE CONFIGURATION", "SOURCE")),
                         (loads, ("CUSTOMER LOADS",)), (equipment, ("LINE",))):
        src = net if name == network else lds if name == loads else eqp
        missing = [s for s in needed if s not in src]
        if missing:
            raise CymeFormatError(f"{name.name}: missing sections {missing}")
    files = {"network": {"file": network.name, "sha256": _file_sha(network)},
             "loads": {"file": loads.name, "sha256": _file_sha(loads)},
             "equipment": {"file": equipment.name, "sha256": _file_sha(equipment)}}

    catalog: dict[str, tuple[float, float, float | None]] = {}
    for sec in ("LINE", "CABLE", "CONCENTRIC NEUTRAL CABLE", "TAPE SHIELDED CABLE"):
        for row in eqp.get(sec, []):
            r1, x1, amps = _float(row.get("R1")), _float(row.get("X1")), _float(row.get("Amps"))
            if row.get("ID") and r1 is not None and x1 is not None:
                catalog[row["ID"]] = (r1, x1, amps if amps and amps > 0 else None)
    config = {r["SectionID"]: r for r in net["LINE CONFIGURATION"]}
    status: dict[str, str] = {}
    for sec in ("SWITCH SETTING", "SECTIONALIZER SETTING", "FUSE SETTING", "BREAKER SETTING",
                "RECLOSER SETTING"):
        for row in net.get(sec, []):
            status[row["SectionID"]] = row.get("Status", "")
    sources = {r["NetworkID"]: r for r in net["SOURCE"]}
    loads_by_section: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in lds["CUSTOMER LOADS"]:
        loads_by_section[row["SectionID"]].append(row)

    feeders: dict[str, list[dict[str, str]]] = defaultdict(list)
    current = None
    for row in net["SECTION"]:
        if row.get("__feeder__"):
            current = row["NetworkID"]
            continue
        if current is None:
            raise CymeFormatError("SECTION rows found before any FEEDER= line")
        feeders[current].append(row)

    results = []
    for network_id in sorted(feeders):
        results.append(_build_feeder(network_id, feeders[network_id], sources.get(network_id),
                                     config, catalog, status, loads_by_section, rules, files))
    return results


def _build_feeder(network_id, sections, source, config, catalog, status, loads_by_section,
                  rules: ReaderRules, files) -> FeederImport:
    ref = f"{files['network']['file']}#{network_id}"
    quarantine: list[QuarantineRecord] = []
    counts: dict[str, int] = defaultdict(int)
    if source is None or _float(source.get("DesiredVoltage")) is None:
        quarantine.append(QuarantineRecord(network_id, "SOURCE", "no source or voltage", ref))
        kv = None
    else:
        kv = _float(source["DesiredVoltage"])
    lines: list[Line] = []
    switches: list[Switch] = []
    nodes: set[str] = set()
    non_abc = 0
    for sec in sections:
        sid, a, b = sec["SectionID"], sec["FromNodeID"], sec["ToNodeID"]
        nodes |= {a, b}
        counts["sections"] += 1
        if a == b:
            quarantine.append(QuarantineRecord(sid, "ToNodeID", "self-loop section", ref))
            continue
        phase = sec.get("Phase", "")
        if phase != _PHASES_3:
            non_abc += 1
        cfg = config.get(sid)
        closed = status.get(sid, "1") != "0"
        if not closed:
            counts["open_devices"] += 1
        if cfg is None:
            quarantine.append(QuarantineRecord(sid, "LineCableID", "no line configuration", ref))
            continue
        code, length_m = cfg.get("LineCableID", ""), _float(cfg.get("Length"))
        if length_m is None or length_m < 0:
            quarantine.append(QuarantineRecord(sid, "Length", "missing or negative", ref))
            continue
        if code == "DEFAULT" or length_m == 0:
            if length_m <= rules.default_connector_max_m:
                switches.append(Switch(sid, a, b, closed))
                counts["ideal_connectors"] += 1
            else:
                quarantine.append(QuarantineRecord(
                    sid, "LineCableID", f"DEFAULT conductor over {length_m:.1f} m has no real "
                    "impedance", ref))
            continue
        if code not in catalog:
            quarantine.append(QuarantineRecord(sid, "LineCableID",
                                               f"code {code} not in equipment catalogue", ref))
            continue
        r1, x1, amps = catalog[code]
        if r1 + x1 <= 0:
            quarantine.append(QuarantineRecord(sid, "LineCableID", f"code {code} has zero "
                                               "impedance", ref))
            continue
        lines.append(Line(sid, a, b, length_m / 1000.0, r1, x1,
                          amps / 1000.0 if amps else None, closed))
        counts["lines"] += 1
    if non_abc and not rules.allow_positive_sequence_approximation:
        quarantine.append(QuarantineRecord(
            network_id, "Phase", f"{non_abc} non three-phase sections need the unbalanced "
            "model (004-C) or an explicit positive-sequence approximation", ref))

    loads: list[Load] = []
    attributes: dict[str, dict[str, float]] = {}
    to_node = {s["SectionID"]: s["ToNodeID"] for s in sections}
    for sid in sorted(to_node):
        for row in loads_by_section.get(sid, []):
            dev = row.get("DeviceNumber") or f"{sid}:load"
            counts["loads"] += 1
            if row.get("ValueType") != "2":
                quarantine.append(QuarantineRecord(dev, "ValueType", f"unsupported value type "
                                                   f"{row.get('ValueType')}", ref))
                continue
            kw, pf = _float(row.get("Value1")), _float(row.get("Value2"))
            if kw is None or pf is None or not 0 < pf <= 1 or kw < 0:
                quarantine.append(QuarantineRecord(dev, "Value1/Value2", "invalid kW or pf", ref))
                continue
            q_mvar = kw / 1000.0 * math.tan(math.acos(pf))
            loads.append(Load(dev, to_node[sid], kw / 1000.0, q_mvar, True))
            counts["loads_with_kw"] += kw > 0
            attributes[dev] = {"connected_kva": _float(row.get("ConnectedKVA")) or 0.0,
                               "kwh": _float(row.get("KWH")) or 0.0,
                               "customers": _float(row.get("NumberOfCustomer")) or 0.0,
                               "power_factor": pf}
    pfs = {round(a["power_factor"], 4) for a in attributes.values()}
    manifest: dict[str, Any] = {
        "schema": "unitesis.source-manifest/1", "source_id": network_id, "parser": PARSER,
        "files": files, "interpretations": list(INTERPRETATIONS),
        "rules": {"frequency_hz": rules.frequency_hz,
                  "default_connector_max_m": rules.default_connector_max_m,
                  "allow_positive_sequence_approximation":
                      rules.allow_positive_sequence_approximation},
        "nominal_kv": kv, "record_counts": dict(counts), "non_three_phase_sections": non_abc,
        "quarantined_fields": len(quarantine),
        "parameter_quality": {
            "uniform_power_factor": len(pfs) == 1 and bool(pfs),
            "loads_without_kw": counts["loads"] - counts["loads_with_kw"],
            "positive_sequence_approximation": bool(non_abc)},
        "geometry": "not_ingested (node UTM coordinates available for spec 003)",
    }
    if quarantine or kv is None:
        return FeederImport(network_id, "quarantined", manifest, quarantine)
    try:
        snapshot = ElectricalSnapshot(
            frequency_hz=rules.frequency_hz,
            buses=tuple(Bus(n, kv) for n in sorted(nodes)),
            lines=tuple(lines), switches=tuple(switches), loads=tuple(loads),
            slacks=(Slack(source["NodeID"], 1.0, 0.0),), name=network_id)
    except (SnapshotError, ValueError) as exc:
        quarantine.append(QuarantineRecord(network_id, "*", str(exc), ref))
        return FeederImport(network_id, "quarantined", manifest, quarantine)
    manifest["snapshot_sha256"] = snapshot.content_sha256
    return FeederImport(network_id, "model_validated", manifest, quarantine, snapshot, attributes)
