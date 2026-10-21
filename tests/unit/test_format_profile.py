"""Reverse engineering of export formats (REA, ADR-0012): structure, coverage, code recovery."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.format_profile import (  # noqa: E402
    infer_code_mapping,
    profile_export,
    structure_only,
)

CYME = ROOT / "fixtures/networks/cyme-ascii"
FILES = {"network": CYME / "RED_synthetic.txt", "loads": CYME / "CARGA_synthetic.txt",
         "equipment": CYME / "BD_Equipo_synthetic.txt"}


class FormatProfileTest(unittest.TestCase):
    def setUp(self):
        self.profile = profile_export(FILES)

    def test_structure_and_reader_coverage(self):
        roles = {f["role"]: f for f in self.profile["files"]}
        line = roles["equipment"]["sections"]["LINE"]
        self.assertTrue(line["columns"]["R1"]["consumed_by_reader"])
        self.assertTrue(line["columns"]["R0"]["consumed_by_reader"])      # 008-C3
        self.assertFalse(line["columns"]["LockImpedance"]["consumed_by_reader"])
        self.assertIn("LockImpedance", line["unused_filled_columns"])
        self.assertEqual(roles["network"]["sections"]["SECTION"]["columns"]["Phase"]["type"],
                         "text")

    def test_no_record_values_leave_the_profile(self):
        text = str(self.profile)
        loads = (CYME / "CARGA_synthetic.txt").read_text(encoding="latin-1").splitlines()
        device = next(line.split(",")[1] for line in loads
                      if line and not line.startswith(("[", "FORMAT")) and "," in line)
        self.assertNotIn(device, text)
        redacted = str(structure_only(self.profile))
        self.assertNotIn("range", redacted)
        self.assertNotIn("sha256", redacted)

    def test_code_mapping_recovered_only_when_deterministic(self):
        pairs = [("A", "1")] * 5 + [("AB", "3")] * 4 + [("ABC", "7")] * 9
        out = infer_code_mapping(pairs)
        self.assertEqual(out["status"], "deterministic")
        self.assertEqual(out["mapping"]["3"], {"means": "AB", "support": 4})
        conflicting = infer_code_mapping(pairs + [("BC", "7")])
        self.assertEqual(conflicting["status"], "conflicting")
        self.assertNotIn("7", conflicting["mapping"])
        thin = infer_code_mapping([("A", "1")], min_support=3)
        self.assertEqual(thin["status"], "insufficient")


if __name__ == "__main__":
    unittest.main()
