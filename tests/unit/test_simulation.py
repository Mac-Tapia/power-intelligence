"""Radial BFS physics, pandapower agreement and comparison gates (spec 008, F04, A07)."""

import cmath
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.neutral_json import ingest_file  # noqa: E402
from unitesis_domain import ComparisonTolerances, StudyRequest, StudyResult  # noqa: E402
from unitesis_ports import EngineUnavailable  # noqa: E402
from unitesis_simulation import PandapowerEngine, RadialBFSEngine, compare_results  # noqa: E402

try:
    import pandapower  # noqa: F401
    HAS_PP = True
except Exception:
    HAS_PP = False

TWO_BUS = ROOT / "fixtures/networks/radial_two_bus.json"
FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"


def solve(engine, snap, scenario="base"):
    return engine.solve(snap, StudyRequest(snap.content_sha256, scenario, engine.name))


class RadialBFSPhysicsTests(unittest.TestCase):
    def test_two_bus_kvl_and_power_balance(self):
        snap = ingest_file(TWO_BUS).require_snapshot()
        res = solve(RadialBFSEngine(), snap)
        self.assertEqual(res.status, "computed")
        v_base = 12.66e3 / 3 ** 0.5
        buses = {b.bus_id: b for b in res.buses}
        v1 = cmath.rect(buses["source"].vm_pu * v_base, 0)
        v2 = cmath.rect(buses["load"].vm_pu * v_base, buses["load"].va_deg * cmath.pi / 180)
        # Load end: S = 3 V2 conj(I)  =>  I = conj(S / 3V2); KVL: V1 - V2 = Z I
        current = (complex(0.5e6, 0.2e6) / (3 * v2)).conjugate()
        self.assertLess(abs(v1 - v2 - complex(0.4, 0.3) * current) / v_base, 1e-9)
        self.assertLess(res.balance_mismatch_mva, 1e-9)
        self.assertAlmostEqual(res.branches[0].i_ka * 1e3, abs(current), places=6)

    def test_hash_mismatch_fails_not_computes(self):
        snap = ingest_file(TWO_BUS).require_snapshot()
        res = RadialBFSEngine().solve(snap, StudyRequest("0" * 64, "base", "x"))
        self.assertEqual(res.status, "failed")

    def test_unsupported_topology_reports_failed(self):
        snap = ingest_file(FEEDER).require_snapshot()
        meshed = replace(snap, switches=tuple(replace(s, closed=True) for s in snap.switches),
                         lines=tuple(replace(ln, in_service=True) for ln in snap.lines))
        res = solve(RadialBFSEngine(), meshed)
        self.assertEqual(res.status, "failed")
        self.assertIn("mesh", res.messages[0])

    def test_open_elements_reported_as_excluded(self):
        snap = ingest_file(FEEDER).require_snapshot()
        res = solve(RadialBFSEngine(), snap)
        self.assertEqual(set(res.excluded_elements), {"L34", "TIE", "bus:B4"})


@unittest.skipUnless(HAS_PP, "pandapower not installed in this interpreter")
class IndependentComparisonTests(unittest.TestCase):
    def setUp(self):
        self.snap = ingest_file(FEEDER).require_snapshot()
        self.bfs = solve(RadialBFSEngine(), self.snap)
        self.pp = solve(PandapowerEngine(), self.snap)

    def test_bfs_matches_pandapower_within_spec_tolerances(self):
        report = compare_results(self.pp, self.bfs, self.snap)
        self.assertEqual(report["status"], "passed", report["issues"])
        self.assertLess(report["max_differences"]["voltage_pu"], 1e-6)

    def test_empty_results_fail_F04(self):
        empty = lambda r: replace(r, buses=(), branches=(), status="failed",  # noqa: E731
                                  converged=False)
        report = compare_results(empty(self.pp), empty(self.bfs), self.snap)
        self.assertEqual(report["status"], "failed")

    def test_same_engine_is_not_independent(self):
        report = compare_results(self.bfs, self.bfs, self.snap)
        self.assertIn("independence", [i["metric"] for i in report["issues"]])

    def test_other_scenario_or_snapshot_fails(self):
        other = replace(self.bfs, scenario_id="other")
        self.assertEqual(compare_results(self.pp, other, self.snap)["status"], "failed")
        moved = replace(self.bfs, snapshot_sha256="f" * 64)
        self.assertEqual(compare_results(self.pp, moved, self.snap)["status"], "failed")

    def test_matching_but_incomplete_coverage_fails_AC09(self):
        partial_a = replace(self.pp, buses=self.pp.buses[:2], branches=self.pp.branches[:1])
        partial_b = replace(self.bfs, buses=self.bfs.buses[:2], branches=self.bfs.branches[:1])
        report = compare_results(partial_a, partial_b, self.snap)
        self.assertIn("bus_coverage", [i["metric"] for i in report["issues"]])

    def test_duplicated_ids_fail(self):
        dup = replace(self.bfs, buses=(*self.bfs.buses, self.bfs.buses[0]))
        self.assertIn("duplicates",
                      [i["metric"] for i in compare_results(self.pp, dup, self.snap)["issues"]])

    def test_proxy_engine_rejected(self):
        proxy = replace(self.bfs, engine="surrogate_proxy")
        self.assertIn("engine",
                      [i["metric"] for i in compare_results(self.pp, proxy, self.snap)["issues"]])

    def test_deviation_beyond_tolerance_fails(self):
        shifted = replace(self.bfs, buses=tuple(replace(b, vm_pu=b.vm_pu + 1e-3)
                                                for b in self.bfs.buses))
        self.assertEqual(compare_results(self.pp, shifted, self.snap)["status"], "failed")

    def test_nonfinite_or_negative_tolerance_rejected_A07(self):
        for bad in (float("inf"), float("nan"), -1.0, 0.0):
            with self.subTest(bad), self.assertRaises(ValueError):
                ComparisonTolerances(voltage_pu=bad)


class EngineUnavailableTests(unittest.TestCase):
    def test_missing_engine_never_reports_success(self):
        from unitesis_application.study import solve_and_compare

        class Missing:
            name = "missing-engine"

            def version(self):
                raise EngineUnavailable("not installed")

            def solve(self, snapshot, request):
                raise EngineUnavailable("not installed")

        snap = ingest_file(TWO_BUS).require_snapshot()
        run = solve_and_compare(snap, "base", reference=Missing())
        self.assertEqual(run["comparison"]["status"], "unavailable")
        self.assertIsNone(run["reference"])

    def test_computed_result_requires_buses(self):
        with self.assertRaises(ValueError):
            StudyResult("a" * 64, "b" * 64, "s", "e", "1", "computed", converged=True)


if __name__ == "__main__":
    unittest.main()
