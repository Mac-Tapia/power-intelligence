"""Two-winding transformers (spec 004-B2): domain, identity, topology, solver, contrast."""

import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.neutral_json import build_snapshot, ingest_file, snapshot_to_payload  # noqa: E402
from unitesis_application.study import solve_and_compare  # noqa: E402
from unitesis_domain import (  # noqa: E402
    Bus,
    ElectricalSnapshot,
    Line,
    Load,
    Slack,
    SnapshotError,
    StudyRequest,
    Transformer,
)
from unitesis_simulation import NewtonRaphsonEngine, RadialBFSEngine  # noqa: E402
from unitesis_topology import TopologyError, build_energized_network  # noqa: E402

FIXTURE = ROOT / "fixtures/networks/mv_lv_transformers.json"
try:
    import pandapower  # noqa: F401
    HAS_PP = True
except Exception:
    HAS_PP = False


def network(shift=0.0, tap=0, vn_hv=22.9, trafo=True):
    buses = (Bus("MT0", 22.9), Bus("MT1", 22.9), Bus("BT1", 0.4), Bus("BT2", 0.4))
    tr = (Transformer("T1", "MT1", "BT1", 0.25, vn_hv, 0.4, 4.0, 1.2, tap, 2.5, shift),)
    return ElectricalSnapshot(
        60.0, buses=buses if trafo else buses[:2],
        lines=(Line("L1", "MT0", "MT1", 3.0, 0.3, 0.4, 0.2),)
        + ((Line("LB", "BT1", "BT2", 0.2, 0.5, 0.1, 0.4),) if trafo else ()),
        loads=(Load("C2", "MT1", 0.5, 0.2),) + ((Load("C1", "BT2", 0.12, 0.05),) if trafo else ()),
        slacks=(Slack("MT0"),), transformers=tr if trafo else ())


def solve(snap, engine=None):
    engine = engine or NewtonRaphsonEngine()
    return engine.solve(snap, StudyRequest(snap.content_sha256, "s", engine.name))


class DomainTests(unittest.TestCase):
    def test_invalid_transformers_rejected(self):
        base = dict(transformer_id="T", hv_bus="A", lv_bus="B", sn_mva=0.25, vn_hv_kv=22.9,
                    vn_lv_kv=0.4, vk_percent=4.0, vkr_percent=1.2)
        for bad in ({"vkr_percent": 5.0}, {"vk_percent": 0.0}, {"vn_hv_kv": 0.2},
                    {"lv_bus": "A"}, {"tap_pos": 1.5}, {"tap_pos": 40, "tap_step_percent": 2.5},
                    {"sn_mva": float("nan")}, {"in_service": "yes"}):
            with self.subTest(bad=bad), self.assertRaises((SnapshotError, ValueError)):
                Transformer(**(base | bad))

    def test_identity_v2_unchanged_without_transformers_and_v3_with_them(self):
        plain = network(trafo=False)
        self.assertEqual(plain.canonical()["schema"], "unitesis.electrical-snapshot/v2")
        self.assertNotIn("transformers", plain.canonical())
        with_t = network()
        self.assertEqual(with_t.canonical()["schema"], "unitesis.electrical-snapshot/v3")
        self.assertNotEqual(network(tap=1).content_sha256, with_t.content_sha256)
        self.assertEqual(ElectricalSnapshot.from_canonical(with_t.canonical()).content_sha256,
                         with_t.content_sha256)

    def test_neutral_json_roundtrip_and_quarantine(self):
        snap = ingest_file(FIXTURE).require_snapshot()
        payload = snapshot_to_payload(snap, "rt")
        again = build_snapshot(payload, "rt").require_snapshot()
        self.assertEqual(again.content_sha256, snap.content_sha256)
        bad = json.loads(FIXTURE.read_text(encoding="utf-8"))
        del bad["network"]["transformers"][0]["vk_percent"]
        res = build_snapshot(bad, "bad")
        self.assertEqual(res.state, "quarantined")
        self.assertIn(("SED1", "vk_percent"), {(q.element_id, q.field) for q in res.quarantine})


class TopologyAndScopeTests(unittest.TestCase):
    def test_transformer_joins_voltage_levels_and_bfs_refuses(self):
        net = build_energized_network(network())
        self.assertEqual({b for b in net.energized_buses}, {"MT0", "MT1", "BT1", "BT2"})
        res = solve(network(), RadialBFSEngine())
        self.assertEqual(res.status, "failed")
        self.assertIn("Newton-Raphson", res.messages[0])

    def test_incompatible_rated_voltage_rejected(self):
        snap = network()
        wrong = replace(snap, transformers=(replace(snap.transformers[0], vn_lv_kv=0.23),))
        with self.assertRaises(TopologyError):
            build_energized_network(wrong)

    def test_out_of_service_transformer_deenergizes_lv_side(self):
        snap = network()
        off = replace(snap, transformers=(replace(snap.transformers[0], in_service=False),),
                      loads=snap.loads[:1])
        res = solve(off)
        self.assertEqual(res.status, "computed")
        self.assertIn("T1", res.excluded_elements)
        self.assertIn("bus:BT1", res.excluded_elements)

    def test_tap_raises_hv_ratio_and_lowers_lv_voltage(self):
        lv = {t: next(b.vm_pu for b in solve(network(tap=t)).buses if b.bus_id == "BT1")
              for t in (-2, 0, 2)}
        self.assertGreater(lv[-2], lv[0])
        self.assertGreater(lv[0], lv[2])

    def test_phase_shift_moves_lv_angle(self):
        a0 = next(b.va_deg for b in solve(network()).buses if b.bus_id == "BT1")
        a150 = next(b.va_deg for b in solve(network(shift=150.0)).buses if b.bus_id == "BT1")
        self.assertAlmostEqual((a0 - a150) % 360.0, 150.0, places=6)


@unittest.skipUnless(HAS_PP, "pandapower required for the independent reference")
class IndependentContrastTests(unittest.TestCase):
    def test_tap_shift_and_off_nominal_cases_match_reference(self):
        for shift, tap, vn_hv in ((0.0, 0, 22.9), (150.0, 0, 22.9), (30.0, 2, 22.9),
                                  (0.0, -1, 23.5), (-30.0, 3, 22.0)):
            with self.subTest(shift=shift, tap=tap, vn_hv=vn_hv):
                run = solve_and_compare(network(shift, tap, vn_hv), "s",
                                        candidate=NewtonRaphsonEngine())
                self.assertEqual(run["comparison"]["status"], "passed",
                                 run["comparison"]["issues"])

    def test_mv_lv_fixture_passes(self):
        snap = ingest_file(FIXTURE).require_snapshot()
        run = solve_and_compare(snap, "s", candidate=NewtonRaphsonEngine())
        self.assertEqual(run["comparison"]["status"], "passed", run["comparison"]["issues"])
        trafos = {b.branch_id for b in run["candidate"].branches}
        self.assertTrue({"SED1", "SED2"} <= trafos)


if __name__ == "__main__":
    unittest.main()
