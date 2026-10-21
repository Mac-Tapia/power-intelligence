"""Economic basis: explicit parameters, no defaults, deterministic loss monetization."""

import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_economics import EconomicBasis, load_basis, parse_basis, present_value_cost  # noqa: E402

FIXTURE = ROOT / "fixtures/economics/conductor_alternatives_synthetic.json"


def basis(**overrides):
    data = {"currency": "USD", "base_year": 2026, "discount_rate": 0.1, "horizon_years": 10,
            "energy_price_per_mwh": 50.0, "loss_load_factor": 0.4,
            "annual_om_fraction": 0.02, "source": "test"}
    data.update(overrides)
    return EconomicBasis(**data)


class EconomicBasisTests(unittest.TestCase):
    def test_fixture_loads_with_digest(self):
        b = load_basis(FIXTURE)
        self.assertEqual(b.currency, "USD")
        self.assertEqual(len(b.sha256), 64)
        self.assertEqual(b.cost_per_km("nexans-aaac6201-50-7"), 9000.0)
        self.assertIsNone(b.cost_per_km("unknown"))

    def test_missing_field_is_never_defaulted(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        del data["energy_price_per_mwh"]
        with self.assertRaisesRegex(ValueError, "energy_price_per_mwh"):
            parse_basis(data)

    def test_wrong_schema_rejected(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8")) | {"schema": "other/1"}
        with self.assertRaisesRegex(ValueError, "schema"):
            parse_basis(data)

    def test_invalid_values_rejected(self):
        bad = [{"discount_rate": float("nan")}, {"discount_rate": -0.1},
               {"loss_load_factor": 0.0}, {"loss_load_factor": 1.5},
               {"energy_price_per_mwh": 0.0}, {"horizon_years": 0},
               {"horizon_years": True}, {"annual_om_fraction": -1.0}, {"currency": " "},
               {"source": ""}, {"discount_rate": "0.1"},
               {"conductor_cost_per_km": (("a", 1.0), ("a", 2.0))},
               {"conductor_cost_per_km": (("a", -1.0),)}]
        for override in bad:
            with self.subTest(override=override), self.assertRaises(ValueError):
                basis(**override)

    def test_loss_monetization_and_cash_flows(self):
        b = basis()
        self.assertAlmostEqual(b.loss_cost_per_year(0.01), 0.01 * 8760 * 0.4 * 50.0)
        flows = b.cash_flows(1000.0, 0.01)
        self.assertEqual([r.year for r in flows], list(range(11)))
        self.assertEqual(flows[0].investment, 1000.0)
        self.assertAlmostEqual(flows[5].maintenance, 20.0)
        expected = 1000.0 + sum((20.0 + 1752.0) / 1.1 ** y for y in range(1, 11))
        self.assertTrue(math.isclose(present_value_cost(flows, 0.1), expected, rel_tol=1e-12))
        with self.assertRaises(ValueError):
            b.cash_flows(-1.0, 0.01)
        with self.assertRaises(ValueError):
            b.loss_cost_per_year(float("inf"))

    def test_load_basis_digest_tracks_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "b.json"
            data = json.loads(FIXTURE.read_text(encoding="utf-8"))
            path.write_text(json.dumps(data), encoding="utf-8")
            first = load_basis(path).sha256
            data["energy_price_per_mwh"] = 61.0
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertNotEqual(first, load_basis(path).sha256)


if __name__ == "__main__":
    unittest.main()
