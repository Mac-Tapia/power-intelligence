"""ElectricalSnapshot v2 identity and radial topology (spec 004, A05)."""

import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_domain import (  # noqa: E402
    Bus,
    ElectricalSnapshot,
    Line,
    Load,
    Slack,
    SnapshotError,
    Switch,
)
from unitesis_topology import TopologyError, build_radial_tree  # noqa: E402


def feeder(**overrides):
    base = dict(
        frequency_hz=60.0,
        buses=(Bus("A", 22.9), Bus("B", 22.9), Bus("C", 22.9), Bus("D", 22.9)),
        lines=(Line("L1", "A", "B", 1.0, 0.3, 0.4, 0.3, True),
               Line("L2", "B", "C", 1.0, 0.3, 0.4, 0.3, True)),
        switches=(Switch("S1", "C", "D", False),),
        loads=(Load("P1", "B", 1.0, 0.3, True), Load("P2", "C", 0.5, 0.2, True)),
        slacks=(Slack("A", 1.0, 0.0),),
    )
    base.update(overrides)
    return ElectricalSnapshot(**base)


class SnapshotIdentityTests(unittest.TestCase):
    def test_hash_invariant_to_record_order(self):
        a = feeder()
        b = feeder(lines=tuple(reversed(a.lines)), loads=tuple(reversed(a.loads)),
                   buses=tuple(reversed(a.buses)))
        self.assertEqual(a.content_sha256, b.content_sha256)

    def test_hash_changes_with_every_electrical_field(self):
        base = feeder()
        mutations = {
            "p": feeder(loads=(Load("P1", "B", 1.1, 0.3, True), base.loads[1])),
            "q": feeder(loads=(Load("P1", "B", 1.0, 0.31, True), base.loads[1])),
            "switch_state": feeder(switches=(Switch("S1", "C", "D", True),)),
            "r": feeder(lines=(replace(base.lines[0], r_ohm_per_km=0.31), base.lines[1])),
            "connection": feeder(lines=(base.lines[0], replace(base.lines[1], from_bus="A"))),
            "in_service": feeder(lines=(base.lines[0], replace(base.lines[1], in_service=False))),
            "kv": feeder(buses=(Bus("A", 23.0), *base.buses[1:])),
            "frequency": feeder(frequency_hz=50.0),
        }
        for name, snap in mutations.items():
            with self.subTest(name):
                self.assertNotEqual(base.content_sha256, snap.content_sha256)

    def test_name_is_provenance_not_identity(self):
        self.assertEqual(feeder(name="x").content_sha256, feeder(name="y").content_sha256)

    def test_canonical_roundtrip(self):
        snap = feeder()
        self.assertEqual(ElectricalSnapshot.from_canonical(snap.canonical()).content_sha256,
                         snap.content_sha256)

    def test_nonfinite_and_bool_rejected_A05(self):
        for bad in (float("nan"), float("inf"), True):
            with self.subTest(bad), self.assertRaises(ValueError):
                Bus("X", bad)
        with self.assertRaises(ValueError):
            feeder(frequency_hz=float("nan"))
        with self.assertRaises(ValueError):
            Slack("A", float("nan"))
        with self.assertRaises(ValueError):
            Line("L", "A", "B", 1.0, 0.3, 0.4, None, "false")

    def test_structural_errors(self):
        with self.assertRaises(SnapshotError):
            feeder(loads=(Load("P1", "ZZ", 1.0, 0.3, True),))
        with self.assertRaises(SnapshotError):
            feeder(switches=(Switch("L1", "C", "D", False),))  # id clash with a line
        with self.assertRaises(SnapshotError):
            feeder(slacks=())
        with self.assertRaises(SnapshotError):
            Line("L", "A", "B", 1.0, 0.0, 0.0)
        for kv in (0, -10.0, 2500.0):
            with self.assertRaises((SnapshotError, ValueError)):
                Bus("V", kv)                       # nominal voltage must be physical


class TopologyTests(unittest.TestCase):
    def test_open_switch_excluded_not_deleted(self):
        snap = feeder()
        tree = build_radial_tree(snap)
        self.assertEqual(tree.excluded, ("S1",))
        self.assertEqual(tree.deenergized_buses, ("D",))
        self.assertIn("S1", [s.switch_id for s in snap.switches])

    def test_mesh_rejected(self):
        snap = feeder(switches=(Switch("S1", "C", "A", True),))
        with self.assertRaises(TopologyError):
            build_radial_tree(snap)

    def test_load_on_deenergized_island_rejected(self):
        snap = feeder(loads=(Load("P9", "D", 0.2, 0.1, True),))
        with self.assertRaises(TopologyError):
            build_radial_tree(snap)

    def test_voltage_mismatch_rejected(self):
        snap = feeder(buses=(Bus("A", 22.9), Bus("B", 10.0), Bus("C", 22.9), Bus("D", 22.9)))
        with self.assertRaises(TopologyError):
            build_radial_tree(snap)

    def test_multiple_slacks_rejected(self):
        with self.assertRaises(TopologyError):
            build_radial_tree(feeder(slacks=(Slack("A"), Slack("C"))))


if __name__ == "__main__":
    unittest.main()
