"""Regression gates for real integration, economics/regulation regressions F01-F03/A06."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for source in (ROOT / "packages/python").glob("*/src"):
    sys.path.insert(0, str(source))

from unitesis_economics.core import rank_feasible_alternatives
from unitesis_regulation.core import RegulatoryBlock, check_profile_for_submission
from unitesis_regulation.pide_reference import annual_equivalent_cost, assess_reference_case


class ConsolidationEconomicsTests(unittest.TestCase):
    def test_string_false_is_not_feasible(self):
        item = {
            "id": "A",
            "technical_feasible": "false",
            "annual_costs": [
                {
                    "year": 0,
                    "investment": 100,
                    "operations": 0,
                    "maintenance": 0,
                    "losses_monetized": 0,
                }
            ],
        }
        with self.assertRaises(ValueError):
            rank_feasible_alternatives([item], 0.1)

    def test_tiny_rate_is_stable(self):
        self.assertAlmostEqual(
            annual_equivalent_cost(100, 1, 2, 1e-20, 10).equivalent_annual_cost, 13
        )

    def test_empty_nonhistorical_case_is_incomplete(self):
        case = json.loads(
            (ROOT / "fixtures/pide/reference_case_synthetic.json").read_text(encoding="utf-8")
        )
        case.update(
            profile="internal", alternatives=[], discount_rate="invalid", economic_life_years=-1
        )
        self.assertFalse(assess_reference_case(case)["documentary_complete"])

    def test_string_false_cannot_authorize_submission(self):
        with self.assertRaises(RegulatoryBlock):
            check_profile_for_submission({"approved_for_automatic_certification": "false"})
