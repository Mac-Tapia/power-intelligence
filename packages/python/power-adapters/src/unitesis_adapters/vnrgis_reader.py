"""VNR-GIS -> one ``ElectricalSnapshot`` per MT feeder (spec 001, T001-U03/U04).

The adapter targets the VNRGIS schema version (universal across concessions), not a
company. Every interpretation is a declared rule, recovered by REA with evidence:

* topology is explicit: ``mtTramo.CodTramoMTPadre`` links a section to its parent (roots
  start at the feeder head); GIS coordinates never create connections (ADR-0003);
* ``Longitud`` is metres (polyline check); nominal voltage comes from ``CodTenNomi``
  through the case's code map;
* VNR carries no impedances: R/X come from a real catalogue of the same case, keyed by
  ``CodNorma`` + voltage letter (the CYME catalogue uses exactly that key);
* ``CodNorma`` ends with the conductor count; VNR does not say which phases a 1- or
  2-conductor lateral uses, so such feeders are quarantined instead of guessed;
* an ``NA`` (normally open) MT device opens its section; SED demand ``MaxDemTotal`` (kW)
  is a load at its ``mtNodoEnlace`` node with the case-declared power factor.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from unitesis_domain import (
    Bus,
    ElectricalSnapshot,
    Line,
    Load,
    QuarantineRecord,
    Slack,
    SnapshotError,
)

PARSER = "unitesis.vnrgis-reader/1"
TABLES = {
    "mtSalida": ["CodSalidaMT", "CodTenNomi", "UTMEste", "UTMNorte"],
    "mtTramo": ["CodTramoMT", "CodSalidaMT", "CodTenNomi", "CodNorma", "Longitud",
                "CodTramoMTPadre", "EstadoVnr"],
    "mtNodoEnlace": ["CodNodoMT", "CodTramoMT", "CodSed"],
    "Sed": ["CodSed", "CodSalidaMT", "MaxDemTotal", "PotInstalada", "EstadoVnr"],
    "mtEquipo": ["CodEqp", "CodTramoMT", "CodEstadoOperacion", "EstadoVnr"],
    "verTramoMT": ["CodTramoMT", "SecVertice", "UTMEste", "UTMNorte"],
}
INTERPRETATIONS = (
    "mtTramo.Longitud is metres (checked against the UTM polyline)",
    "topology from mtTramo.CodTramoMTPadre only; roots ('0' or empty) start at the feeder head",
    "R/X/amps from the declared catalogue keyed by CodNorma + CodTenNomi letter",
    "CodNorma last two digits = conductor count; non three-conductor feeders quarantined",
    "mtEquipo CodEstadoOperacion NA opens its section; NC keeps it closed",
    "Sed.MaxDemTotal is kW at the SED's mtNodoEnlace node; Q from the declared power factor",
)


@dataclass(frozen=True)
class VnrRules:
    frequency_hz: float
    voltage_codes: tuple[tuple[str, float], ...]          # CodTenNomi -> kV (line-to-line)
    catalogue: dict[str, tuple[float, float, float | None]]   # code -> (r1, x1 ohm/km, amps)
    sed_power_factor: float
    included_states: tuple[str, ...] = ("E", "M", "N")
    catalogue_source: str = ""

    def __post_init__(self) -> None:
        if self.frequency_hz not in (50.0, 60.0):
            raise ValueError("frequency_hz must come from the application case")
        if not 0 < self.sed_power_factor <= 1:
            raise ValueError("sed_power_factor must be in (0, 1]")
        if not self.voltage_codes:
            raise ValueError("voltage code map required")


@dataclass
class VnrFeederImport:
    network_id: str
    state: str
    manifest: dict[str, Any]
    quarantine: list[QuarantineRecord] = field(default_factory=list)
    snapshot: ElectricalSnapshot | None = None
    geometry: dict[str, Any] = field(default_factory=dict)


def _s(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _f(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def build_feeders(tables: dict[str, list[dict[str, Any]]], rules: VnrRules,
                  source: dict[str, Any]) -> list[VnrFeederImport]:
    kv_of = dict(rules.voltage_codes)
    tramos: dict[str, list[dict]] = defaultdict(list)
    feeder_of: dict[str, str] = {}
    for t in tables["mtTramo"]:
        tramos[_s(t["CodSalidaMT"])].append(t)
        feeder_of[_s(t["CodTramoMT"])] = _s(t["CodSalidaMT"])
    node_seds: dict[str, list[str]] = defaultdict(list)
    for n in tables["mtNodoEnlace"]:
        if _s(n.get("CodSed")):
            node_seds[_s(n["CodTramoMT"])].append(_s(n["CodSed"]))
    seds = {_s(s["CodSed"]): s for s in tables["Sed"]}
    open_tramos = {_s(e["CodTramoMT"]) for e in tables["mtEquipo"]
                   if _s(e.get("CodEstadoOperacion")) == "NA" and _s(e.get("CodTramoMT"))}
    vertices: dict[str, list[tuple[int, float, float]]] = defaultdict(list)
    for v in tables.get("verTramoMT", []):
        x, y, k = _f(v["UTMEste"]), _f(v["UTMNorte"]), _f(v["SecVertice"])
        if x is not None and y is not None and k is not None:
            vertices[_s(v["CodTramoMT"])].append((int(k), x, y))
    results = []
    for salida in sorted(tables["mtSalida"], key=lambda r: _s(r["CodSalidaMT"])):
        fid = _s(salida["CodSalidaMT"])
        results.append(_feeder(fid, salida, tramos.get(fid, []), feeder_of, node_seds, seds,
                               open_tramos, vertices, kv_of, rules, source))
    return results


def _feeder(fid, salida, rows, feeder_of, node_seds, seds, open_tramos, vertices, kv_of,
            rules: VnrRules, source) -> VnrFeederImport:
    ref = f"{source.get('database', 'vnrgis')}#mtSalida/{fid}"
    quarantine: list[QuarantineRecord] = []
    counts: dict[str, int] = defaultdict(int)
    kv = kv_of.get(_s(salida.get("CodTenNomi")))
    if kv is None:
        quarantine.append(QuarantineRecord(fid, "CodTenNomi", f"voltage code "
                                           f"{_s(salida.get('CodTenNomi'))!r} not declared", ref))
    head = f"H:{fid}"
    buses = {head}
    lines: list[Line] = []
    included = [t for t in rows if _s(t.get("EstadoVnr")) in rules.included_states]
    counts["sections"] = len(rows)
    counts["excluded_by_state"] = len(rows) - len(included)
    non_three = 0
    letter = _s(salida.get("CodTenNomi"))
    for t in included:
        tid = _s(t["CodTramoMT"])
        norm = _s(t["CodNorma"])
        parent = _s(t.get("CodTramoMTPadre"))
        length_m = _f(t.get("Longitud"))
        if parent and parent != "0" and feeder_of.get(parent) not in (None, fid):
            quarantine.append(QuarantineRecord(tid, "CodTramoMTPadre", f"parent {parent} "
                                               f"belongs to feeder {feeder_of[parent]}", ref))
            continue
        if length_m is None or length_m <= 0:
            quarantine.append(QuarantineRecord(tid, "Longitud", "missing or non-positive", ref))
            continue
        if norm[-2:].isdigit() and int(norm[-2:]) != 3:
            non_three += 1
        cat = rules.catalogue.get(norm + _s(t.get("CodTenNomi") or letter))
        if cat is None:
            quarantine.append(QuarantineRecord(tid, "CodNorma", f"{norm} has no impedance in "
                                               "the declared catalogue", ref))
            continue
        r1, x1, amps = cat
        start = head if not parent or parent == "0" else f"N:{parent}"
        end = f"N:{tid}"
        buses |= {start, end}
        lines.append(Line(tid, start, end, length_m / 1000.0, r1, x1,
                          amps / 1000.0 if amps else None, tid not in open_tramos))
        counts["lines"] += 1
        counts["open_sections"] += tid in open_tramos
    if non_three:
        quarantine.append(QuarantineRecord(fid, "CodNorma", f"{non_three} sections with 1 or 2 "
                                           "conductors: VNR does not state their phases", ref))
    loads: list[Load] = []
    tan = math.tan(math.acos(rules.sed_power_factor))
    for t in included:
        tid = _s(t["CodTramoMT"])
        for sed_id in node_seds.get(tid, []):
            sed = seds.get(sed_id)
            if sed is None:
                quarantine.append(QuarantineRecord(sed_id, "CodSed", "SED not found", ref))
                continue
            kw = _f(sed.get("MaxDemTotal"))
            counts["seds"] += 1
            if kw is None or kw < 0:
                quarantine.append(QuarantineRecord(sed_id, "MaxDemTotal", "missing", ref))
                continue
            if kw == 0:
                counts["seds_without_demand"] += 1
                continue
            loads.append(Load(f"SED:{sed_id}", f"N:{tid}", kw / 1000.0, kw / 1000.0 * tan))
    manifest: dict[str, Any] = {
        "schema": "unitesis.source-manifest/1", "source_id": fid, "parser": PARSER,
        "source": source, "interpretations": list(INTERPRETATIONS),
        "rules": {"frequency_hz": rules.frequency_hz, "voltage_codes": dict(rules.voltage_codes),
                  "sed_power_factor": rules.sed_power_factor,
                  "included_states": list(rules.included_states),
                  "catalogue_source": rules.catalogue_source},
        "nominal_kv": kv, "record_counts": dict(counts),
        "quarantined_fields": len(quarantine),
        "total_length_km": round(sum(ln.length_km for ln in lines), 6),
        "total_demand_mw": round(sum(ld.p_mw for ld in loads), 6),
    }
    geometry = {"nodes": {head: [_f(salida.get("UTMEste")), _f(salida.get("UTMNorte"))]},
                "sections": {ln.line_id: [[x, y] for _, x, y in sorted(vertices[ln.line_id])]
                             for ln in lines if vertices.get(ln.line_id)}}
    if quarantine or kv is None or not lines:
        if not lines and not quarantine:
            quarantine.append(QuarantineRecord(fid, "mtTramo", "feeder without sections", ref))
        return VnrFeederImport(fid, "quarantined", manifest, quarantine, geometry=geometry)
    try:
        snapshot = ElectricalSnapshot(
            frequency_hz=rules.frequency_hz, buses=tuple(Bus(b, kv) for b in sorted(buses)),
            lines=tuple(lines), loads=tuple(loads), slacks=(Slack(head, 1.0, 0.0),), name=fid)
    except (SnapshotError, ValueError) as exc:
        quarantine.append(QuarantineRecord(fid, "*", str(exc), ref))
        return VnrFeederImport(fid, "quarantined", manifest, quarantine, geometry=geometry)
    manifest["snapshot_sha256"] = snapshot.content_sha256
    return VnrFeederImport(fid, "model_validated", manifest, [], snapshot, geometry)


def fetch_tables(client, database: str) -> dict[str, list[dict[str, Any]]]:
    """SELECT-only extraction of the tables the reader uses."""
    from .vnrgis_sql import select_rows
    return {name: select_rows(client, database, f"dbo.{name}", cols)
            for name, cols in TABLES.items()}


def catalogue_plausibility(catalogue: dict[str, tuple[float, float, float | None]]
                           ) -> list[dict[str, Any]]:
    """Codes ``MMsssPP<V>`` (material, section mm2, conductors, voltage letter): within one
    material/conductors/letter family, R1 must strictly decrease as the section grows.

    Violations are data-quality findings for the owner; the values are not altered.
    """
    families: dict[tuple[str, str, str], list[tuple[int, str, float]]] = defaultdict(list)
    for code, (r1, _x1, _a) in catalogue.items():
        if len(code) == 8 and code[2:5].isdigit() and code[5:7].isdigit():
            families[(code[:2], code[5:7], code[7])].append((int(code[2:5]), code, r1))
    findings = []
    for (material, conductors, letter), items in sorted(families.items()):
        items.sort()
        for (s_a, c_a, r_a), (s_b, c_b, r_b) in zip(items, items[1:], strict=False):
            if s_b > s_a and not r_b < r_a:
                findings.append({"family": f"{material}..{conductors}{letter}",
                                 "smaller_section": c_a, "larger_section": c_b,
                                 "r1_smaller": r_a, "r1_larger": r_b,
                                 "issue": "R1 does not decrease with cross-section"})
    return findings
