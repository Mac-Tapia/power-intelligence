"""Export the IEEE 13-node test feeder to the neutral JSON input format (spec 008-C).

Source: the GridLAB-D ``powerflow/autotest`` models of the IEEE PES 13-node feeder
(Kersting, IEEE PES Distribution System Analysis Subcommittee), read offline from the
donor archive. GridLAB-D is open source (Battelle, BSD-style licence); only the public
benchmark numbers are exported here, never its code.

Three outputs, all versioned with provenance:

* ``fixtures/networks/ieee13_kersting.json``: the network. Line matrices are computed
  by ``unitesis_simulation.line_constants`` from the published conductor data and
  spacings (earth resistivity 100 ohm.m, as in the benchmark definition).
* ``fixtures/networks/ieee13_reference.json``: expected node voltages with the
  tolerances of GridLAB-D's own ``complex_assert`` checks (``test_IEEE_13_NR.glm``).
* ``fixtures/networks/ieee13_line_dump.json``: GridLAB-D's series impedance (``b``) and
  ``a`` matrices per line (``IEEE_13_node_impedance_dump.xml``), used only to verify the
  line-constant implementation, never as solver input.

  python scripts/fixtures/build_ieee13.py --gridlabd-autotest <dir>
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_simulation.line_constants import (  # noqa: E402
    ConcentricNeutralCable,
    OverheadConductor,
    as_snapshot_matrices,
    concentric_neutral_impedance,
    concentric_neutral_susceptance,
    overhead_phase_impedance,
    overhead_shunt_susceptance,
    positive_sequence,
)

OUT = ROOT / "fixtures/networks"
FT, INCH, MILE = 0.3048, 0.0254, 1.609344
FREQ, RHO = 60.0, 100.0
UNITS = {"voltage": "kV", "length": "km", "impedance": "ohm/km", "power": "MW/MVAr",
         "current": "kA", "frequency": "Hz"}
PROVENANCE = ("IEEE PES 13-node radial test feeder (Kersting); data as modelled in "
              "GridLAB-D powerflow/autotest/test_IEEE_13_NR.glm (Battelle, open source). "
              "Line matrices computed by unitesis line_constants (modified Carson, Kron, "
              "images, concentric neutral), earth resistivity 100 ohm.m, 60 Hz.")
BUS = {"n650": "650", "n630": "RG60", "n632": "632", "n633": "633", "l634": "634",
       "l645": "645", "l646": "646", "l6321": "6321", "l671": "671", "n680": "680",
       "n684": "684", "l611": "611", "l652": "652", "l692": "692", "l675": "675"}
DELTA = {"A": "AB", "B": "BC", "C": "CA"}
ANGLE = {"A": 0.0, "B": -120.0, "C": 120.0, "AB": 30.0, "BC": -90.0, "CA": 150.0}


def parse_glm(text: str) -> list[dict]:
    """Flat list of objects ({'_type', props...}); nested asserts attach to their parent."""
    text = re.sub(r"//[^\n]*", "", text)
    objs: list[dict] = []
    stack: list[dict] = []
    for token in re.finditer(r"object\s+(\w+)\s*(?::\s*\S+)?\s*\{|\}|([^;{}]+);", text):
        if token.group(1):
            obj = {"_type": token.group(1), "_children": []}
            (stack[-1]["_children"] if stack else objs).append(obj)
            stack.append(obj)
        elif token.group(0) == "}":
            if stack:
                stack.pop()
        elif stack and token.group(2):
            parts = token.group(2).strip().split(None, 1)
            if len(parts) == 2:
                stack[-1][parts[0]] = parts[1].strip().strip('"')
    return objs


def num(value: str) -> float:
    return float(value.split()[0])


def length_m(value: str) -> float:
    v, *unit = value.split()
    return float(v) * (INCH if unit == ["in"] else FT)


def phasor(value: str) -> complex:
    """GridLAB-D complex: '2445.01-2.56d' (polar, degrees) or '56.6+32.5j' (rectangular)."""
    value = value.replace(" ", "")
    if value.endswith("d"):
        m = re.fullmatch(r"([+-]?[\d.]+)([+-][\d.]+)d", value)
        return cmath.rect(float(m.group(1)), math.radians(float(m.group(2))))
    if value.endswith("j"):
        return complex(value)
    return complex(float(value), 0.0)


def line_matrices(line: dict, by_name: dict) -> tuple[str, list, list]:
    config = by_name[line["configuration"]]
    spacing = by_name[config["spacing"]]
    phases = "".join(p for p in line["phases"] if p in "ABC")
    dist = {}
    for key, value in spacing.items():
        if key.startswith("distance_") and not key.endswith("E"):
            a, b = key[9], key[10]
            dist[frozenset((a, b))] = float(value) * FT
    if line["_type"] == "overhead_line":
        cond = []
        for ph in (*phases, "N"):
            name = config.get(f"conductor_{ph}")
            if name is None:
                continue
            c = by_name[name]
            cond.append(OverheadConductor(
                ph, num(c["resistance"]) / MILE, num(c["geometric_mean_radius"]) * FT,
                length_m(c["diameter"]), num(spacing[f"distance_{ph}E"]) * FT))
        lab, z = overhead_phase_impedance(cond, dist, frequency_hz=FREQ,
                                          earth_resistivity_ohm_m=RHO)
        _, b = overhead_shunt_susceptance(cond, dist, frequency_hz=FREQ)
    else:
        cables = []
        for ph in phases:
            c = by_name[config[f"conductor_{ph}"]]
            cables.append(ConcentricNeutralCable(
                ph, num(c["conductor_resistance"]) / MILE, num(c["conductor_gmr"]) * FT,
                num(c["conductor_diameter"]) * INCH, num(c["outer_diameter"]) * INCH,
                num(c["neutral_resistance"]) / MILE, num(c["neutral_gmr"]) * FT,
                num(c["neutral_diameter"]) * INCH, int(num(c["neutral_strands"])),
                num(c["insulation_relative_permitivitty"])))
        # As in the reference model, a separate conductor_N of a concentric-neutral
        # cable is not added: GridLAB-D uses the cable's own neutral (config 607).
        lab, z = concentric_neutral_impedance(cables, dist, frequency_hz=FREQ,
                                              earth_resistivity_ohm_m=RHO)
        _, b = concentric_neutral_susceptance(cables, frequency_hz=FREQ)
    assert lab == phases, (lab, phases)
    zj, bj = as_snapshot_matrices(z, b)
    return phases, zj, bj


def loads_of(obj: dict, bus: str) -> list[dict]:
    tag = obj["name"].removeprefix("l")
    raw = obj["phases"]
    delta = "D" in raw
    v_ln = num(obj["nominal_voltage"])
    out = []
    groups: dict[str, dict[str, complex]] = {}
    for key, value in obj.items():
        m = re.fullmatch(r"constant_(power|impedance|current)_([ABC])", key)
        if not m or phasor(value) == 0:
            continue
        element = DELTA[m.group(2)] if delta else m.group(2)
        v_nom = cmath.rect(v_ln * (math.sqrt(3) if delta else 1.0), math.radians(ANGLE[element]))
        val = phasor(value)
        if m.group(1) == "power":
            s = val
        elif m.group(1) == "impedance":
            s = abs(v_nom) ** 2 / val.conjugate()
        else:
            s = v_nom * val.conjugate()
        model = {"power": "constant_power", "impedance": "constant_impedance",
                 "current": "constant_current"}[m.group(1)]
        kind = "cap" if model == "constant_impedance" and s.real == 0 and s.imag < 0 else model
        groups.setdefault(kind, {})[element] = s / 1e6
    order = {"A": 0, "B": 1, "C": 2, "AB": 0, "BC": 1, "CA": 2}
    for kind, elems in groups.items():
        keys = sorted(elems, key=order.get)
        phases = "".join(sorted({p for k in keys for p in k}))
        if delta and len(keys) < 3 and keys == ["CA"]:
            phases = "AC"
        p = [round(elems[k].real, 12) for k in keys]
        q = [round(elems[k].imag, 12) for k in keys]
        row = {"load_id": f"{tag}-{kind.replace('constant_', '')}", "bus": bus,
               "p_mw": sum(p), "q_mvar": sum(q), "in_service": True, "phases": phases,
               "connection": "delta" if delta else "wye",
               "model": "constant_impedance" if kind == "cap" else kind,
               "phase_p_mw": p, "phase_q_mvar": q}
        row["p_mw"], row["q_mvar"] = math.fsum(p), math.fsum(q)
        out.append(row)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gridlabd-autotest", type=Path, required=True)
    args = ap.parse_args()
    glm = args.gridlabd_autotest / "test_IEEE_13_NR.glm"
    dump = args.gridlabd_autotest / "IEEE_13_node_impedance_dump.xml"
    if not glm.is_file() or not dump.is_file():
        print(f"missing GridLAB-D sources in {args.gridlabd_autotest}", file=sys.stderr)
        return 2
    objs = parse_glm(glm.read_text(encoding="utf-8"))
    by_name = {o["name"]: o for o in objs if "name" in o}

    buses = [{"bus_id": b, "nominal_kv": 0.48 if b == "634" else 4.16} for b in BUS.values()]
    lines, loads, reference = [], [], []
    for o in objs:
        if o["_type"] in ("overhead_line", "underground_line"):
            phases, z, b = line_matrices(o, by_name)
            z1 = positive_sequence(__import__("numpy").array(
                [[complex(*c) for c in row] for row in z]))
            lines.append({"line_id": o["name"].removeprefix("line_"),
                          "from_bus": BUS[o["from"]], "to_bus": BUS[o["to"]],
                          "length_km": num(o["length"]) * FT / 1000,
                          "r_ohm_per_km": z1.real, "x_ohm_per_km": z1.imag,
                          "in_service": True, "phases": phases,
                          "z_phase_ohm_per_km": z, "b_phase_us_per_km": b})
        if o["_type"] == "load":
            bus = BUS[o.get("parent", o["name"])]
            loads += loads_of(o, bus)
        if o["_type"] in ("node", "load") and "parent" not in o:
            for a in o["_children"]:
                if a["_type"] == "complex_assert":
                    v = phasor(a["value"])
                    reference.append({"bus": BUS[o["name"]], "phase": a["target"][-1],
                                      "vm_v": abs(v), "va_deg": math.degrees(cmath.phase(v)),
                                      "tolerance_v": num(a["within"])})
    reg = by_name["regconfig6506321"]
    tc = by_name["tc400"]
    network = {
        "frequency_hz": FREQ,
        "buses": buses,
        "lines": sorted(lines, key=lambda r: r["line_id"]),
        "switches": [{"switch_id": "671-692", "from_bus": "671", "to_bus": "692",
                      "closed": by_name["switch_671-692"]["status"] == "CLOSED"}],
        "loads": sorted(loads, key=lambda r: r["load_id"]),
        "slacks": [{"bus": "650", "vm_pu": 1.0, "angle_deg": 0.0}],
        "transformers": [{
            "transformer_id": "XFM-1", "hv_bus": "633", "lv_bus": "634",
            "sn_mva": num(tc["power_rating"]) / 1000,
            "vn_hv_kv": num(tc["primary_voltage"]) / 1000,
            "vn_lv_kv": num(tc["secondary_voltage"]) / 1000,
            "vk_percent": 100 * abs(complex(num(tc["resistance"]), num(tc["reactance"]))),
            "vkr_percent": 100 * num(tc["resistance"]), "in_service": True,
            "vector_group": "YNyn0"}],
        "regulators": [{
            "regulator_id": "RG60", "from_bus": "650", "to_bus": "RG60", "phases": "ABC",
            "tap_positions": [int(num(reg[f"tap_pos_{p}"])) for p in "ABC"],
            "step_percent": 100 * num(reg["regulation"]) / num(reg["raise_taps"]),
            "in_service": True}],
    }
    payload = {"schema": "unitesis.network-input/1", "source_id": "ieee13-kersting-benchmark",
               "authorization": "public_benchmark", "provenance": PROVENANCE, "units": UNITS,
               "network": network}
    (OUT / "ieee13_kersting.json").write_text(json.dumps(payload, indent=1) + "\n",
                                              encoding="utf-8")
    ref = {"schema": "unitesis.benchmark-reference/1", "case": "ieee13-kersting",
           "reference": "GridLAB-D test_IEEE_13_NR.glm complex_assert (IEEE PES published "
                        "voltages); tolerance as set by GridLAB-D per node and phase",
           "voltage_unit": "V line-to-neutral (480 V bus: 634)",
           "nodes": sorted(reference, key=lambda r: (r["bus"], r["phase"]))}
    (OUT / "ieee13_reference.json").write_text(json.dumps(ref, indent=1) + "\n",
                                               encoding="utf-8")
    tree = ET.parse(dump)
    lines_dump = {}
    for el in tree.getroot():
        # GridLAB-D writes the underground tag misspelt ("undergound_line")
        if el.tag not in ("overhead_line", "underground_line", "undergound_line"):
            continue
        rec = {"phases": el.findtext("phases"),
               "length_ft": float(el.findtext("length"))}
        for mat in ("a", "b"):
            node = el.find(f"{mat}_matrix")
            rec[mat] = [[[complex(node.findtext(f"{mat}{i}{j}").replace("j", "j")).real,
                          complex(node.findtext(f"{mat}{i}{j}")).imag] for j in (1, 2, 3)]
                        for i in (1, 2, 3)]
        lines_dump[el.findtext("name").removeprefix("line_")] = rec
    dump_out = {"schema": "unitesis.line-constant-reference/1",
                "reference": "GridLAB-D IEEE_13_node_impedance_dump.xml: a and b (ohm) matrices "
                             "per line, 3x3 with zero rows for absent phases",
                "lines": lines_dump}
    (OUT / "ieee13_line_dump.json").write_text(json.dumps(dump_out, indent=1) + "\n",
                                               encoding="utf-8")
    print(f"ieee13: {len(lines)} lines, {len(loads)} loads, {len(reference)} reference values, "
          f"{len(lines_dump)} dumped lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
