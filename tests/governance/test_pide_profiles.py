import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestPideMethodology(unittest.TestCase):
    def setUp(self):
        self.reference = json.loads(
            (
                ROOT / "config/regulations/profiles/PIDE_2017_METHODOLOGICAL_REFERENCE.json"
            ).read_text(encoding="utf-8")
        )
        self.regulatory = json.loads(
            (ROOT / "config/regulations/profiles/PIDE_2017_DRAFT.json").read_text(encoding="utf-8")
        )
        self.sources = {
            x["id"]: x
            for x in json.loads((ROOT / "docs/regulatory/SOURCES.json").read_text(encoding="utf-8"))
        }

    def test_approved_is_false(self):
        self.assertFalse(self.reference["approved_for_automatic_certification"])
        self.assertFalse(self.regulatory["approved_for_automatic_certification"])

    def test_source_is_official_el_peruano(self):
        self.assertIn("busquedas.elperuano.pe", self.sources["PIDE_EL_PERUANO_2017"]["url"])
        self.assertEqual(self.sources["RM428"]["url"], self.sources["PIDE_EL_PERUANO_2017"]["url"])

    def test_horizons_are_historical_not_default(self):
        self.assertEqual(self.reference["historic_case_horizon_years"]["long_term"], 20)
        self.assertEqual(self.reference["historic_case_horizon_years"]["portfolio"], 4)
        self.assertIsNone(self.reference["planning_horizon_years"])
        self.assertIsNone(self.reference["portfolio_horizon_years"])

    def test_fonafe_restriction(self):
        self.assertEqual(self.regulatory["applicability"], "distribution_FONAFE_only")
        self.assertNotEqual(self.reference["applicability"], self.regulatory["applicability"])

    def test_agent_and_spec(self):
        self.assertTrue((ROOT / "docs/agents/PIDE-DISTRIBUTION-AGENT-QUERY.md").exists())
        self.assertTrue((ROOT / "specs/026-pide-methodological-reference/spec.md").exists())


if __name__ == "__main__":
    unittest.main()
