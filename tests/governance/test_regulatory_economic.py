import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages/python/power-regulation/src"))
sys.path.insert(0, str(ROOT / "packages/python/power-economics/src"))
from unitesis_economics import CostYear, present_value_cost, rank_feasible_alternatives
from unitesis_regulation import (
    RegulatoryBlock,
    check_profile_for_submission,
    evaluate_completeness,
    load_profile,
)


class RegulatoryTests(unittest.TestCase):
    def test_profiles_exist_distinct(self):
        cfg = ROOT / "config/regulations/profiles"
        pit = load_profile("PIT_SST_SCT_217_2013_BASE", cfg)
        pide = load_profile("PIDE_2017_DRAFT", cfg)
        self.assertEqual(pit["applicability"], "transmission_SST_SCT")
        self.assertEqual(pide["applicability"], "distribution_FONAFE_only")
        self.assertEqual(pit["evaluation_years"], 10)
        self.assertEqual(pit["forecast_years"], 30)
        self.assertEqual(pit["implementation_years"], 4)

    def test_draft_or_unconsolidated_is_blocked(self):
        cfg = ROOT / "config/regulations/profiles"
        for key in ("PIDE_2017_DRAFT", "PIT_2025_2029"):
            with self.assertRaises(RegulatoryBlock):
                check_profile_for_submission(load_profile(key, cfg))

    def test_profile_path_traversal_blocked(self):
        with self.assertRaises(RegulatoryBlock):
            load_profile("../secrets", ROOT / "config/regulations/profiles")

    def test_no_automatic_submission_when_missing_fields(self):
        r = evaluate_completeness({"project_id": "P1"})
        self.assertFalse(r["complete"])
        self.assertIn("reviewer", r["missing"])

    def test_sourced_catalog_study_types(self):
        cat = json.loads((ROOT / "config/studies/catalog.json").read_text())
        self.assertGreaterEqual(sum(map(len, cat["study_families"].values())), 35)

    def test_pmbok_fields(self):
        t = json.loads((ROOT / "templates/projects/PMBOK6/project.json").read_text())
        self.assertEqual(len(t["knowledge_areas"]), 10)
        self.assertEqual(len(t["lifecycle"]), 5)

    def test_alternatives_profile_split(self):
        x = json.loads((ROOT / "config/regulations/alternatives.json").read_text())
        self.assertIn("PIT_SST_SCT", x["families"])
        self.assertIn("PIDE_INTERNAL", x["families"])


class EconomicTests(unittest.TestCase):
    def test_zero_rate(self):
        rows = [CostYear(0, 100, 0, 0, 0), CostYear(1, 0, 10, 5, 5)]
        self.assertAlmostEqual(present_value_cost(rows, 0), 120)

    def test_discounting(self):
        rows = [CostYear(0, 100, 0, 0, 0), CostYear(1, 0, 10, 0, 0)]
        self.assertAlmostEqual(present_value_cost(rows, 0.10), 100 + 10 / 1.1)

    def test_bad_data(self):
        for rows, r in [
            ([], 0.1),
            ([CostYear(0, -1, 0, 0, 0)], 0.1),
            ([CostYear(0, 1, 0, 0, 0)], -1),
        ]:
            with self.assertRaises(ValueError):
                present_value_cost(rows, r)

    def test_feasibility_before_price(self):
        a = [
            {
                "id": "cheap_invalid",
                "technical_feasible": False,
                "annual_costs": [
                    dict(year=0, investment=1, operations=0, maintenance=0, losses_monetized=0)
                ],
            },
            {
                "id": "safe",
                "technical_feasible": True,
                "annual_costs": [
                    dict(year=0, investment=5, operations=0, maintenance=0, losses_monetized=0)
                ],
            },
        ]
        self.assertEqual(
            [r["alternative_id"] for r in rank_feasible_alternatives(a, 0.1)], ["safe"]
        )


if __name__ == "__main__":
    unittest.main()
