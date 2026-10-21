"""VNR-GIS reader (spec 001, T001-U03/U04): explicit topology, declared rules, quarantine."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.vnrgis_reader import (  # noqa: E402
    VnrRules,
    build_feeders,
    catalogue_plausibility,
)
from unitesis_domain import StudyRequest  # noqa: E402
from unitesis_simulation import NewtonRaphsonEngine  # noqa: E402

CATALOGUE = {"AA05003D": (0.6755, 0.4669, 195.0), "AA03503D": (0.9651, 0.4805, 160.0)}
RULES = VnrRules(60.0, (("D", 10.0),), CATALOGUE, 0.97)


def tables(**over):
    base = {
        "mtSalida": [{"CodSalidaMT": "AL1", "CodTenNomi": "D", "UTMEste": "1", "UTMNorte": "2"}],
        "mtTramo": [
            {"CodTramoMT": "T1", "CodSalidaMT": "AL1", "CodTenNomi": "D", "CodNorma": "AA05003",
             "Longitud": "1200", "CodTramoMTPadre": "0", "EstadoVnr": "E"},
            {"CodTramoMT": "T2", "CodSalidaMT": "AL1", "CodTenNomi": "D", "CodNorma": "AA03503",
             "Longitud": "800", "CodTramoMTPadre": "T1", "EstadoVnr": "E"},
            {"CodTramoMT": "T3", "CodSalidaMT": "AL1", "CodTenNomi": "D", "CodNorma": "AA03503",
             "Longitud": "500", "CodTramoMTPadre": "T1", "EstadoVnr": "P"},
        ],
        "mtNodoEnlace": [{"CodNodoMT": "N1", "CodTramoMT": "T2", "CodSed": "S1"}],
        "Sed": [{"CodSed": "S1", "CodSalidaMT": "AL1", "MaxDemTotal": "250",
                 "PotInstalada": "400", "EstadoVnr": "E"}],
        "mtEquipo": [],
        "verTramoMT": [{"CodTramoMT": "T1", "SecVertice": "1", "UTMEste": "0", "UTMNorte": "0"},
                       {"CodTramoMT": "T1", "SecVertice": "2", "UTMEste": "1200",
                        "UTMNorte": "0"}],
    }
    base.update(over)
    return base


class VnrReaderTest(unittest.TestCase):
    def feeder(self, **over):
        return build_feeders(tables(**over), RULES, {"database": "test"})[0]

    def test_explicit_tree_with_declared_rules_validates_and_solves(self):
        imp = self.feeder()
        self.assertEqual(imp.state, "model_validated", [q.as_dict() for q in imp.quarantine])
        snap = imp.snapshot
        t2 = next(ln for ln in snap.lines if ln.line_id == "T2")
        self.assertEqual((t2.from_bus, t2.to_bus, t2.length_km), ("N:T1", "N:T2", 0.8))
        self.assertEqual(snap.bus("H:AL1").nominal_kv, 10.0)
        self.assertNotIn("T3", {ln.line_id for ln in snap.lines})      # proyectado excluded
        load = snap.loads[0]
        self.assertAlmostEqual(load.p_mw, 0.25)
        self.assertAlmostEqual(load.q_mvar / load.p_mw, 0.2506, places=4)   # pf 0.97
        self.assertIn("T1", imp.geometry["sections"])
        res = NewtonRaphsonEngine().solve(snap, StudyRequest(snap.content_sha256, "s", "nr"))
        self.assertEqual(res.status, "computed")

    def test_normally_open_device_opens_its_section(self):
        imp = self.feeder(mtEquipo=[{"CodEqp": "E1", "CodTramoMT": "T2",
                                     "CodEstadoOperacion": "NA", "EstadoVnr": "E"}])
        t2 = next(ln for ln in imp.snapshot.lines if ln.line_id == "T2")
        self.assertFalse(t2.in_service)

    def test_missing_impedance_and_unknown_phases_are_quarantined(self):
        rows = tables()["mtTramo"]
        rows[1] = dict(rows[1], CodNorma="CU01603")                      # not in catalogue
        imp = self.feeder(mtTramo=rows)
        self.assertEqual(imp.state, "quarantined")
        self.assertTrue(any(q.field == "CodNorma" and "CU01603" in q.reason
                            for q in imp.quarantine))
        rows = tables()["mtTramo"]
        rows[1] = dict(rows[1], CodNorma="AA03502")                      # two conductors
        imp = self.feeder(mtTramo=rows)
        self.assertTrue(any("do" in q.reason and "phases" in q.reason for q in imp.quarantine))

    def test_parent_in_another_feeder_and_unknown_voltage_are_reported(self):
        rows = tables()["mtTramo"] + [{"CodTramoMT": "X1", "CodSalidaMT": "AL2",
                                       "CodTenNomi": "D", "CodNorma": "AA05003",
                                       "Longitud": "10", "CodTramoMTPadre": "0",
                                       "EstadoVnr": "E"}]
        rows[1] = dict(rows[1], CodTramoMTPadre="X1")
        imp = self.feeder(mtTramo=rows)
        self.assertTrue(any(q.field == "CodTramoMTPadre" for q in imp.quarantine))
        imp = self.feeder(mtSalida=[{"CodSalidaMT": "AL1", "CodTenNomi": "Z",
                                     "UTMEste": None, "UTMNorte": None}])
        self.assertTrue(any(q.field == "CodTenNomi" for q in imp.quarantine))

    def test_catalogue_plausibility_flags_non_decreasing_resistance(self):
        findings = catalogue_plausibility({"AA01603D": (1.0891, 0.4, 100.0),
                                           "AA02503D": (1.0891, 0.4, 120.0),
                                           "AA05003D": (0.6755, 0.4, 195.0)})
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["larger_section"], "AA02503D")


if __name__ == "__main__":
    unittest.main()
