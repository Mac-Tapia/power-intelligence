"""Pareto front of feasible alternatives and declared emission factor (spec 005 T005-04)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_application.alternatives import run_conductor_alternatives  # noqa: E402
from unitesis_economics import parse_basis  # noqa: E402
from unitesis_optimization.pareto import pareto_front  # noqa: E402

BASIS = ROOT / "fixtures/economics/conductor_alternatives_synthetic.json"
OBJ = {"cost": "min", "losses": "min", "vmin": "max"}


class ParetoTests(unittest.TestCase):
    def test_dominated_alternative_is_removed_and_traced(self):
        items = [{"id": "A", "cost": 10, "losses": 5, "vmin": 0.97},
                 {"id": "B", "cost": 12, "losses": 4, "vmin": 0.97},
                 {"id": "C", "cost": 13, "losses": 6, "vmin": 0.96}]   # worse than A everywhere
        r = pareto_front(items, OBJ)
        self.assertEqual(r["front"], ["A", "B"])
        self.assertEqual(r["dominated_by"], {"C": "A"})

    def test_ties_and_maximisation_direction(self):
        items = [{"id": "A", "cost": 10, "losses": 5, "vmin": 0.97},
                 {"id": "B", "cost": 10, "losses": 5, "vmin": 0.97},
                 {"id": "C", "cost": 10, "losses": 5, "vmin": 0.99}]
        self.assertEqual(pareto_front(items, OBJ)["front"], ["C"])
        self.assertEqual(pareto_front(items[:2], OBJ)["front"], ["A", "B"])

    def test_non_finite_or_missing_objectives_excluded_with_reason(self):
        items = [{"id": "A", "cost": 10, "losses": 5, "vmin": 0.97},
                 {"id": "N", "cost": float("nan"), "losses": 1, "vmin": 0.99},
                 {"id": "M", "losses": 1, "vmin": 0.99},
                 {"id": "T", "cost": True, "losses": 1, "vmin": 0.99}]
        r = pareto_front(items, OBJ)
        self.assertEqual(r["front"], ["A"])
        self.assertEqual(set(r["excluded"]), {"N", "M", "T"})
        with self.assertRaises(ValueError):
            pareto_front(items, {"cost": "lowest"})


class EmissionFactorTests(unittest.TestCase):
    def basis(self, **extra):
        return json.loads(BASIS.read_text(encoding="utf-8")) | extra

    def test_factor_requires_source_and_range(self):
        with self.assertRaises(ValueError):
            parse_basis(self.basis(emission_factor_tco2_per_mwh=0.5))
        with self.assertRaises(ValueError):
            parse_basis(self.basis(emission_factor_tco2_per_mwh=5.0,
                                   emission_factor_source="x"))
        b = parse_basis(self.basis(emission_factor_tco2_per_mwh=0.5,
                                   emission_factor_source="synthetic test value"))
        self.assertAlmostEqual(b.loss_co2_t_per_year(0.01), 0.01 * 8760 * 0.35 * 0.5)
        self.assertIsNone(parse_basis(self.basis()).loss_co2_t_per_year(0.01))

    def test_alternatives_publish_front_with_co2_only_when_declared(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "basis.json"
            path.write_text(json.dumps(self.basis(emission_factor_tco2_per_mwh=0.6,
                                                  emission_factor_source="synthetic")),
                            encoding="utf-8")
            ev = run_conductor_alternatives(
                ROOT / "fixtures/networks/radial_feeder_6bus.json", Path(tmp) / "a.json",
                line_id="L13",
                catalog_path=ROOT / "config/catalogs/conductors/aaac6201_nexans_reference.json",
                basis_path=path, operating_temperature_c=75.0, phase_gmd_m=1.2,
                reference=None)
        self.assertIn("loss_co2_t_per_year", ev["pareto"]["objectives"])
        self.assertTrue(set(ev["pareto"]["front"]) <= {a["id"] for a in ev["alternatives"]
                                                       if a["technical_feasible"]})
        self.assertIn(ev["recommended"], ev["pareto"]["front"])


if __name__ == "__main__":
    unittest.main()
