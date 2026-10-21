"""Three-phase unbalanced power flow (spec 008-C): line constants, engine, scope, identity.

Independent references: GridLAB-D's IEEE 13-node line matrices and its published node
voltages (``fixtures/networks/ieee13_*.json``, built by ``scripts/fixtures/build_ieee13.py``);
and the own balanced Newton-Raphson on a balanced case expressed in the phase frame.
"""

import cmath
import json
import math
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

import numpy as np  # noqa: E402
from unitesis_adapters.neutral_json import build_snapshot, ingest_file, snapshot_to_payload  # noqa: E402
from unitesis_domain import (  # noqa: E402
    SNAPSHOT_SCHEMA_V4,
    Bus,
    ElectricalSnapshot,
    Line,
    Load,
    Slack,
    SnapshotError,
    StudyRequest,
    Transformer,
    VoltageRegulator,
)
from unitesis_simulation import NewtonRaphsonEngine, PandapowerEngine, ThreePhaseEngine  # noqa: E402

NET = ROOT / "fixtures/networks/ieee13_kersting.json"
REF = json.loads((ROOT / "fixtures/networks/ieee13_reference.json").read_text(encoding="utf-8"))
DUMP = json.loads((ROOT / "fixtures/networks/ieee13_line_dump.json").read_text(encoding="utf-8"))
SIX_BUS = ROOT / "fixtures/networks/radial_feeder_6bus.json"


def solve(snapshot, engine=None):
    engine = engine or ThreePhaseEngine()
    return engine.solve(snapshot, StudyRequest(snapshot.content_sha256, "base", engine.name))


def matrix(rows):
    return np.array([[complex(*c) if isinstance(c, list | tuple) else c for c in r]
                     for r in rows])


class LineConstantsTest(unittest.TestCase):
    """Own Carson/Kron and concentric-neutral results against GridLAB-D's computed matrices."""

    def setUp(self):
        self.lines = {ln.line_id: ln for ln in ingest_file(NET).require_snapshot().lines}

    def series_ratio(self, line_id):
        ln = self.lines[line_id]
        ph = ["ABC".index(p) for p in ln.phases]
        ours = matrix(ln.z_phase_ohm_per_km) * ln.length_km
        theirs = matrix(DUMP["lines"][line_id]["b"])[np.ix_(ph, ph)]
        return np.abs(ours - theirs).max() / np.abs(theirs).max()

    def test_overhead_series_impedance_matches_reference(self):
        for line_id in ("632-6321", "6321-671", "671-680", "632-633", "632-645", "645-646",
                        "671-684", "684-611"):
            with self.subTest(line=line_id):
                self.assertLess(self.series_ratio(line_id), 1e-5)

    def test_reference_dump_anomaly_is_isolated(self):
        # 630-632 shares configuration 601 with 632-6321; only the dumped A-A term differs
        # (GridLAB-D dump artefact), so the comparison excludes that single element.
        ln = self.lines["630-632"]
        ours = matrix(ln.z_phase_ohm_per_km) * ln.length_km
        theirs = matrix(DUMP["lines"]["630-632"]["b"])
        mask = np.ones((3, 3), dtype=bool)
        mask[0, 0] = False
        self.assertLess(np.abs((ours - theirs)[mask]).max() / np.abs(theirs).max(), 1e-5)

    def test_concentric_neutral_cables_match_reference(self):
        self.assertLess(self.series_ratio("692-675"), 1e-5)    # config 606, three cables
        self.assertLess(self.series_ratio("684-652"), 1e-5)    # config 607, single cable

    def test_shunt_admittance_close_to_reference(self):
        # a = I + Z Y / 2 (Kersting); compared on the diagonal, where it is well conditioned
        for line_id in ("632-6321", "692-675", "684-652"):
            ln = self.lines[line_id]
            ph = ["ABC".index(p) for p in ln.phases]
            z = matrix(ln.z_phase_ohm_per_km) * ln.length_km
            y = 1j * np.array(ln.b_phase_us_per_km) * 1e-6 * ln.length_km
            ours = np.diag(z @ y / 2)
            theirs = np.diag(matrix(DUMP["lines"][line_id]["a"])[np.ix_(ph, ph)]) - 1
            with self.subTest(line=line_id):
                self.assertLess(np.abs(ours - theirs).max() / np.abs(theirs).max(), 0.05)


class IEEE13Test(unittest.TestCase):
    def setUp(self):
        self.snap = ingest_file(NET).require_snapshot()
        self.res = solve(self.snap)

    def test_published_voltages_within_reference_tolerance(self):
        self.assertEqual(self.res.status, "computed", self.res.messages)
        self.assertEqual(len(REF["nodes"]), 32)
        for ref in REF["nodes"]:
            v = self.res.voltage(ref["bus"], ref["phase"])
            v_ln = self.snap.bus(ref["bus"]).nominal_kv * 1e3 / math.sqrt(3)
            ours = cmath.rect(v.vm_pu * v_ln, math.radians(v.va_deg))
            theirs = cmath.rect(ref["vm_v"], math.radians(ref["va_deg"]))
            with self.subTest(bus=ref["bus"], phase=ref["phase"]):
                self.assertLessEqual(abs(ours - theirs), ref["tolerance_v"])
                self.assertLess(abs(ours - theirs), 0.5)   # well inside: reference rounding

    def test_convergence_and_power_balance(self):
        self.assertTrue(self.res.converged)
        self.assertLessEqual(self.res.residual_mva, 1e-8)
        self.assertLess(self.res.balance_mismatch_mva, 1e-6)
        self.assertGreater(self.res.total_loss_p_mw, 0)

    def test_voltage_unbalance_reported_for_three_phase_buses(self):
        vuf = {u.bus_id: u.vuf_percent for u in self.res.unbalance}
        self.assertIn("671", vuf)
        self.assertNotIn("684", vuf)             # two-phase bus
        self.assertTrue(0 < vuf["671"] < 10)

    def test_balanced_engines_refuse_phase_frame_data(self):
        nr = solve(self.snap, NewtonRaphsonEngine())
        self.assertEqual(nr.status, "failed")
        self.assertIn("three-phase engine", nr.messages[0])
        try:
            pp = solve(self.snap, PandapowerEngine())
        except Exception:  # pandapower absent: the engine reports unavailable by raising
            return
        self.assertEqual(pp.status, "failed")


def phase_frame(snapshot, zm_ratio=0.3):
    """Balanced snapshot rewritten with symmetric phase matrices (z_s - z_m = z1)."""
    lines = []
    for ln in snapshot.lines:
        z1 = complex(ln.r_ohm_per_km, ln.x_ohm_per_km)
        zm = z1 * zm_ratio
        zs = z1 + zm
        z = [[[zs.real, zs.imag] if i == j else [zm.real, zm.imag] for j in range(3)]
             for i in range(3)]
        lines.append(replace(ln, z_phase_ohm_per_km=z))
    return replace(snapshot, lines=tuple(lines))


class BalancedEquivalenceTest(unittest.TestCase):
    def test_phase_frame_reproduces_newton_raphson_on_a_balanced_case(self):
        base = ingest_file(SIX_BUS).require_snapshot()
        nr = solve(base, NewtonRaphsonEngine())
        tp = solve(phase_frame(base))
        self.assertEqual(tp.status, "computed", tp.messages)
        for bus in nr.buses:
            for ph, shift in (("A", 0), ("B", -120), ("C", 120)):
                v = tp.voltage(bus.bus_id, ph)
                self.assertAlmostEqual(v.vm_pu, bus.vm_pu, places=9)
                self.assertAlmostEqual((v.va_deg - shift - bus.va_deg + 180) % 360 - 180, 0,
                                       places=7)
        self.assertAlmostEqual(tp.total_loss_p_mw, nr.total_loss_p_mw, places=9)
        self.assertLess(max(u.vuf_percent for u in tp.unbalance), 1e-9)


def two_bus(**kw):
    z = [[[0.3, 0.6], [0.1, 0.3], [0.1, 0.3]], [[0.1, 0.3], [0.3, 0.6], [0.1, 0.3]],
         [[0.1, 0.3], [0.1, 0.3], [0.3, 0.6]]]
    line = Line("L1", "R", "B", 1.0, 0.2, 0.3, z_phase_ohm_per_km=z)
    defaults = dict(frequency_hz=60.0, buses=(Bus("S", 13.2), Bus("R", 13.2), Bus("B", 13.2)),
                    lines=(line,), slacks=(Slack("S"),),
                    regulators=(VoltageRegulator("RG", "S", "R", "ABC", (8, 0, -8), 0.625),))
    defaults.update(kw)
    return ElectricalSnapshot(**defaults)


class ScopeAndModelTest(unittest.TestCase):
    def test_regulator_is_an_exact_ideal_ratio(self):
        res = solve(two_bus())
        self.assertEqual(res.status, "computed", res.messages)
        for ph, tap in (("A", 8), ("B", 0), ("C", -8)):
            self.assertAlmostEqual(res.voltage("R", ph).vm_pu, 1 + tap * 0.00625, places=12)

    def test_unbalanced_single_phase_load_draws_only_its_phase(self):
        snap = two_bus(loads=(Load("LA", "B", 0.3, 0.1, phases="A"),))
        res = solve(snap)
        self.assertEqual(res.status, "computed", res.messages)
        flows = {f.phase: f.i_from_a for f in res.flows if f.branch_id == "L1"}
        self.assertGreater(flows["A"], 1.0)
        self.assertLess(max(flows["B"], flows["C"]), 1e-9)
        self.assertAlmostEqual(res.total_load_p_mw, 0.3, places=9)

    def test_delta_impedance_load_draws_nominal_power_at_nominal_voltage(self):
        snap = ElectricalSnapshot(60.0, buses=(Bus("S", 4.16),), slacks=(Slack("S"),),
                                  loads=(Load("D", "S", 0.2, 0.1, phases="BC",
                                              connection="delta", model="constant_impedance"),))
        res = solve(snap)
        self.assertEqual(res.status, "computed", res.messages)
        self.assertAlmostEqual(res.total_load_p_mw, 0.2, places=9)
        self.assertAlmostEqual(res.total_load_q_mvar, 0.1, places=9)

    def test_line_without_phase_matrix_is_refused_unless_declared(self):
        plain = replace(two_bus(), lines=(Line("L1", "R", "B", 1.0, 0.2, 0.3),))
        res = solve(plain)
        self.assertEqual(res.status, "failed")
        self.assertIn("L1", res.messages[0])
        declared = solve(plain, ThreePhaseEngine(positive_sequence_lines=True))
        self.assertEqual(declared.status, "computed")
        self.assertTrue(any("approximation" in m for m in declared.messages))

    def test_load_on_missing_phase_fails_closed(self):
        z = [[[0.3, 0.6]]]
        snap = two_bus(lines=(Line("L1", "R", "B", 1.0, 0.3, 0.6, phases="A",
                                   z_phase_ohm_per_km=z),),
                       loads=(Load("LC", "B", 0.1, 0.0, phases="C"),))
        res = solve(snap)
        self.assertEqual(res.status, "failed")
        self.assertIn("LC", res.messages[0])

    def test_transformer_without_vector_group_is_refused(self):
        snap = two_bus(buses=(Bus("S", 13.2), Bus("R", 13.2), Bus("B", 13.2), Bus("L", 0.4)),
                       transformers=(Transformer("T1", "B", "L", 0.5, 13.2, 0.4, 4.0, 1.0),))
        res = solve(snap)
        self.assertEqual(res.status, "failed")
        self.assertIn("T1", res.messages[0])


class IdentityTest(unittest.TestCase):
    def test_v4_round_trip_keeps_the_hash(self):
        snap = ingest_file(NET).require_snapshot()
        self.assertEqual(snap.canonical()["schema"], SNAPSHOT_SCHEMA_V4)
        again = build_snapshot(snapshot_to_payload(snap, "rt"), "rt").require_snapshot()
        self.assertEqual(again.content_sha256, snap.content_sha256)

    def test_v4_vocabulary_does_not_change_balanced_hashes(self):
        base = ingest_file(SIX_BUS).require_snapshot()
        self.assertNotIn("phases", base.canonical()["lines"][0])
        self.assertEqual(replace(base).content_sha256, base.content_sha256)

    def test_domain_validation(self):
        with self.assertRaises(SnapshotError):
            Line("L", "a", "b", 1.0, 0.1, 0.1, phases="A")              # matrix required
        with self.assertRaises(SnapshotError):
            Load("x", "b", 0.3, 0.0, phases="A", connection="delta")     # delta needs 2 phases
        with self.assertRaises(SnapshotError):
            Load("x", "b", 0.3, 0.0, phase_p_mw=(0.1, 0.1, 0.0), phase_q_mvar=(0, 0, 0))
        with self.assertRaises(SnapshotError):
            VoltageRegulator("r", "a", "b", "AB", (1,), 0.625)           # one tap per phase


if __name__ == "__main__":
    unittest.main()
