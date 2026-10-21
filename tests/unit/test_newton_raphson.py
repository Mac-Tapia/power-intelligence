"""Own Newton-Raphson engine, shared Y-bus and meshed topology (spec 008, T008-B1)."""

import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.neutral_json import build_snapshot, ingest_file  # noqa: E402
from unitesis_application.study import engine_by_name, solve_and_compare  # noqa: E402
from unitesis_domain import Bus, Line, Load, Slack, StudyRequest  # noqa: E402
from unitesis_simulation import (  # noqa: E402
    NewtonRaphsonEngine,
    RadialBFSEngine,
    build_ybus,
    power_mismatch,
    specified_injections,
)
from unitesis_topology import build_energized_network  # noqa: E402

IEEE33 = ROOT / "fixtures/networks/ieee33_baran_wu.json"
FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"
try:
    import pandapower  # noqa: F401
    HAS_PP = True
except Exception:
    HAS_PP = False


def solve(snapshot, engine=None, scenario="s"):
    engine = engine or NewtonRaphsonEngine()
    return engine.solve(snapshot, StudyRequest(snapshot.content_sha256, scenario, engine.name))


def ieee33(close_ties: bool = False):
    payload = json.loads(IEEE33.read_text(encoding="utf-8"))
    if close_ties:
        for ln in payload["network"]["lines"]:
            ln["in_service"] = True
    return build_snapshot(payload, "test").require_snapshot()


class Ieee33Tests(unittest.TestCase):
    def test_radial_matches_published_baran_wu_values(self):
        res = solve(ieee33())
        self.assertEqual(res.status, "computed")
        vmin = min(res.buses, key=lambda b: b.vm_pu)
        self.assertEqual(vmin.bus_id, "B18")
        self.assertAlmostEqual(vmin.vm_pu, 0.9131, delta=2e-4)       # Baran & Wu (1989)
        self.assertAlmostEqual(res.total_loss_p_mw * 1e3, 202.7, delta=0.5)
        self.assertLessEqual(res.iterations, 6)
        self.assertLess(res.balance_mismatch_mva, 1e-9)
        self.assertEqual(len(res.branches), 32)
        self.assertEqual(sum(e.startswith("TIE") for e in res.excluded_elements), 5)

    def test_nr_and_bfs_agree_on_radial(self):
        snap = ieee33()
        run = solve_and_compare(snap, "s", candidate=NewtonRaphsonEngine(),
                                reference=RadialBFSEngine())
        self.assertEqual(run["comparison"]["status"], "passed", run["comparison"]["issues"])

    def test_meshed_network_solved_by_nr_rejected_by_bfs(self):
        snap = ieee33(close_ties=True)
        self.assertTrue(build_energized_network(snap).meshed)
        self.assertEqual(solve(snap, RadialBFSEngine()).status, "failed")
        meshed = solve(snap)
        self.assertEqual(meshed.status, "computed")
        self.assertLess(meshed.total_loss_p_mw, solve(ieee33()).total_loss_p_mw)
        self.assertLess(meshed.balance_mismatch_mva, 1e-9)

    @unittest.skipUnless(HAS_PP, "pandapower required for the independent reference")
    def test_independent_contrast_radial_and_meshed(self):
        for close in (False, True):
            with self.subTest(meshed=close):
                run = solve_and_compare(ieee33(close), "s", candidate=NewtonRaphsonEngine())
                self.assertEqual(run["comparison"]["status"], "passed",
                                 run["comparison"]["issues"])
                self.assertLess(run["comparison"]["max_differences"]["voltage_pu"], 1e-8)


class YBusTests(unittest.TestCase):
    def test_residual_vanishes_only_at_solution(self):
        snap = ieee33()
        model = build_ybus(snap, build_energized_network(snap))
        s_spec = specified_injections(snap, model)
        res = solve(snap)
        v = np.array([res.buses[[b.bus_id for b in res.buses].index(n)].vm_pu
                      * np.exp(1j * np.radians(res.buses[[b.bus_id for b in res.buses]
                                                         .index(n)].va_deg))
                      for n in model.network.nodes])
        self.assertLess(np.max(np.abs(power_mismatch(model.ybus, v, s_spec)[1:])), 1e-8)
        flat = np.ones(len(v), dtype=complex)
        self.assertGreater(np.max(np.abs(power_mismatch(model.ybus, flat, s_spec)[1:])), 1e-3)

    def test_ybus_is_symmetric_with_zero_row_sums(self):
        snap = ieee33(close_ties=True)
        y = build_ybus(snap, build_energized_network(snap)).ybus.toarray()
        self.assertTrue(np.allclose(y, y.T))
        self.assertTrue(np.allclose(y.sum(axis=1), 0))   # series-only branches


class ScopeTests(unittest.TestCase):
    def base(self):
        return ingest_file(FEEDER).require_snapshot()

    def test_closed_switch_fuses_buses_and_parallel_line_carries_no_current(self):
        snap = self.base()
        par = Line("LPAR", "B2", "B2S", 0.5, 0.3, 0.3, None, True)
        res = solve(replace(snap, lines=(*snap.lines, par)))
        self.assertEqual(res.status, "computed")
        by_id = {b.bus_id: b for b in res.buses}
        self.assertEqual(by_id["B2"].vm_pu, by_id["B2S"].vm_pu)
        self.assertEqual(next(b for b in res.branches if b.branch_id == "LPAR").i_ka, 0.0)

    def test_out_of_scope_fails_with_reason(self):
        snap = self.base()
        two_slacks = replace(snap, slacks=(*snap.slacks, Slack("B1")))
        res = solve(two_slacks)
        self.assertEqual(res.status, "failed")
        self.assertIn("slack", res.messages[0])
        mixed_kv = replace(snap, buses=(*snap.buses, Bus("LV", 0.4)),
                           lines=(*snap.lines, Line("LX", "B1", "LV", 0.1, 0.1, 0.1)))
        self.assertIn("transformers", solve(mixed_kv).messages[0])

    def test_non_convergence_is_failed_not_computed(self):
        snap = self.base()
        heavy = replace(snap, loads=(*snap.loads, Load("HUGE", "B3", 500.0, 300.0)))
        res = solve(heavy)
        self.assertEqual(res.status, "failed")
        self.assertFalse(res.converged)

    def test_switch_island_without_load_is_reported_deenergized(self):
        snap = self.base()
        res = solve(snap)
        self.assertIn("bus:B4", res.excluded_elements)
        self.assertNotIn("B4", {b.bus_id for b in res.buses})

    def test_integer_json_values_keep_identity_and_solve(self):
        payload = json.loads(FEEDER.read_text(encoding="utf-8"))
        as_float = build_snapshot(payload, "f").require_snapshot()
        payload["network"]["slacks"][0]["vm_pu"] = 1          # JSON.stringify(1.0) -> 1
        payload["network"]["buses"][0]["nominal_kv"] = float(payload["network"]["buses"][0]
                                                             ["nominal_kv"])
        payload["network"]["loads"][0]["p_mw"] = 1 if payload["network"]["loads"][0][
            "p_mw"] == 1.0 else payload["network"]["loads"][0]["p_mw"]
        as_int = build_snapshot(payload, "i").require_snapshot()
        self.assertEqual(as_int.content_sha256, as_float.content_sha256)
        self.assertIsInstance(as_int.slacks[0].vm_pu, float)
        self.assertEqual(solve(as_int).status, "computed")

    def test_deterministic_identity(self):
        snap = ieee33()
        self.assertEqual(solve(snap).result_sha256, solve(snap).result_sha256)

    def test_engine_selection_never_falls_back(self):
        self.assertEqual(engine_by_name("nr").name, "unitesis-newton-raphson")
        self.assertEqual(engine_by_name("bfs").name, "unitesis-radial-bfs")
        with self.assertRaises(ValueError):
            engine_by_name("cymdist")

    def test_open_switch_parallel_path_meshes_when_closed(self):
        snap = self.base()
        closed = replace(snap, switches=tuple(replace(s, closed=True) for s in snap.switches),
                         lines=tuple(replace(ln, in_service=True) for ln in snap.lines))
        self.assertTrue(build_energized_network(closed).meshed)
        self.assertEqual(solve(closed).status, "computed")


if __name__ == "__main__":
    unittest.main()
