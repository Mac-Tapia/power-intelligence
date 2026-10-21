"""Bootstrap tests prove only structuring and provenance invariants."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages/python/power-domain/src"))
from unitesis_domain.models import Equipment, NetworkSnapshot  # noqa: E402


class DomainTests(unittest.TestCase):
    def test_duplicate_equipment_rejected(self):
        item = Equipment("ED-001", "ACLineSegment", 22.9)
        with self.assertRaises(ValueError):
            NetworkSnapshot("authorized-gis-file", (item, item))

    def test_snapshot_hash_stable_for_equipment_order(self):
        a = Equipment("A", "line", 22.9)
        b = Equipment("B", "switch", 22.9)
        self.assertEqual(
            NetworkSnapshot("source", (a, b)).content_sha256,
            NetworkSnapshot("source", (b, a)).content_sha256,
        )

    def test_voltage_validation(self):
        with self.assertRaises(ValueError):
            Equipment("C", "line", 0)


if __name__ == "__main__":
    unittest.main()
