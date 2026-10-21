"""Export the IEEE 33-bus test feeder (Baran & Wu, 1989) to the neutral JSON input format.

Source of the numbers: ``pandapower.networks.case33bw`` (MATPOWER case33bw), used only as
a data source for this benchmark fixture. Ampacity is absent in the source (pandapower
uses a 99999 kA placeholder), so ``max_current_ka`` stays null: nothing is invented.
The 5 tie lines are kept as out-of-service lines, as in the original case.

  python scripts/fixtures/build_ieee33.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "fixtures/networks/ieee33_baran_wu.json"


def main() -> int:
    try:
        import pandapower.networks as pn
    except ImportError as exc:
        print(f"pandapower required to export the fixture: {exc}", file=sys.stderr)
        return 3
    net = pn.case33bw()
    name = {i: f"B{i + 1}" for i in net.bus.index}           # Baran-Wu numbering 1..33
    lines = []
    for _, ln in net.line.sort_index().iterrows():
        a, b = name[int(ln.from_bus)], name[int(ln.to_bus)]
        lines.append({"line_id": (f"L{a[1:]}-{b[1:]}" if ln.in_service else f"TIE{a[1:]}-{b[1:]}"),
                      "from_bus": a, "to_bus": b, "length_km": float(ln.length_km),
                      "r_ohm_per_km": float(ln.r_ohm_per_km),
                      "x_ohm_per_km": float(ln.x_ohm_per_km),
                      "max_current_ka": None, "in_service": bool(ln.in_service)})
    payload = {
        "schema": "unitesis.network-input/1",
        "source_id": "ieee33-baran-wu-1989-benchmark",
        "authorization": "public_benchmark",
        "provenance": "Baran & Wu (1989), IEEE Trans. Power Delivery 4(2):1401-1407; numbers "
                      "exported from pandapower.networks.case33bw (MATPOWER case33bw)",
        "units": {"voltage": "kV", "length": "km", "impedance": "ohm/km",
                  "power": "MW/MVAr", "current": "kA", "frequency": "Hz"},
        "network": {
            "frequency_hz": float(net.f_hz),
            "buses": [{"bus_id": name[i], "nominal_kv": float(net.bus.vn_kv.at[i])}
                      for i in net.bus.index],
            "lines": lines,
            "switches": [],
            "loads": [{"load_id": f"D{name[int(ld.bus)][1:]}", "bus": name[int(ld.bus)],
                       "p_mw": float(ld.p_mw), "q_mvar": float(ld.q_mvar), "in_service": True}
                      for _, ld in net.load.iterrows()],
            "slacks": [{"bus": name[int(g.bus)], "vm_pu": float(g.vm_pu),
                        "angle_deg": float(g.va_degree)} for _, g in net.ext_grid.iterrows()],
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(payload['network']['buses'])} buses, "
          f"{len(lines)} lines ({sum(not x['in_service'] for x in lines)} ties open)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
