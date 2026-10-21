"""Application cases keep the core universal: locality lives in validated case files."""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_config import CaseError, check_consistency, list_cases, load_case, parse_case  # noqa: E402

CASES = ROOT / "config/cases"
PROFILES = ROOT / "config/regulations/profiles"
REGISTRY = json.loads((ROOT / "config/datasets/sources.v2.json").read_text(encoding="utf-8"))
PILOT = json.loads((CASES / "pe-ica-electrodunas.json").read_text(encoding="utf-8"))


class PilotCaseTests(unittest.TestCase):
    def test_pilot_case_is_valid_and_synchronized(self):
        case = load_case(CASES / "pe-ica-electrodunas.json")
        self.assertEqual((case.country, case.frequency_hz, case.currency), ("PE", 60.0, "PEN"))
        self.assertFalse(case.crs_verified)
        self.assertFalse(case.authorized)
        self.assertEqual(check_consistency(case, PROFILES, REGISTRY), [])

    def test_templates_are_not_cases(self):
        self.assertNotIn("_template", list_cases(CASES))
        self.assertIn("pe-ica-electrodunas", list_cases(CASES))

    def test_method_references_belong_to_no_case(self):
        refs = [s for s in REGISTRY["sources"] if s["role"] == "method_reference"]
        self.assertTrue(refs)
        self.assertTrue(all(s["case_id"] is None for s in refs))
        self.assertTrue(all(s["role"] in ("application_case", "method_reference")
                            for s in REGISTRY["sources"]))


class UniversalityTests(unittest.TestCase):
    def other_case(self, **changes):
        data = copy.deepcopy(PILOT)
        data.update(case_id="co-antioquia-utility", country="CO", region="Antioquia",
                    utility="Synthetic utility", regulatory_profiles=[], source_ids=[])
        data["economics"]["currency"] = "COP"
        data["time"]["timezone"] = "America/Bogota"
        data["spatial"]["crs"] = "EPSG:9377"
        for key, value in changes.items():
            data[key] = value
        return data

    def test_another_country_and_50hz_parse_without_code_changes(self):
        data = self.other_case()
        data["electrical"]["frequency_hz"] = 50.0
        case = parse_case(data)
        self.assertEqual((case.country, case.frequency_hz), ("CO", 50.0))
        self.assertEqual(check_consistency(case, PROFILES, REGISTRY), [])

    def test_foreign_jurisdiction_profile_is_flagged(self):
        case = parse_case(self.other_case(regulatory_profiles=["PIT_2025_2029"]))
        issues = check_consistency(case, PROFILES, REGISTRY)
        self.assertTrue(any("jurisdiction" in i for i in issues))

    def test_source_of_another_case_is_flagged(self):
        case = parse_case(self.other_case(source_ids=["eldu-vnrgis-2024-04"]))
        self.assertTrue(any("belongs to case" in i
                            for i in check_consistency(case, PROFILES, REGISTRY)))

    def test_invalid_fields_rejected_never_defaulted(self):
        bad = []
        for path, value in (("country", "Peru"), ("case_id", "Ica"), ("role", "x")):
            bad.append({**copy.deepcopy(PILOT), path: value})
        for section, key, value in (("electrical", "frequency_hz", 55),
                                    ("time", "timezone", "Mars/Base"),
                                    ("economics", "currency", "soles"),
                                    ("spatial", "crs", "UTM18S")):
            data = copy.deepcopy(PILOT)
            data[section][key] = value
            bad.append(data)
        missing = copy.deepcopy(PILOT)
        del missing["time"]["timezone"]
        bad.append(missing)
        for data in bad:
            with self.subTest(data=str(data)[:60]), self.assertRaises(CaseError):
                parse_case(data)


if __name__ == "__main__":
    unittest.main()
