"""Physics screening baseline and warm-start refinement (spec 029, AC-029-S06)."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

import numpy as np  # noqa: E402
from unitesis_adapters.neutral_json import ingest_file  # noqa: E402
from unitesis_domain import StudyRequest  # noqa: E402
from unitesis_sciml.physics_screening import FixedPointScreener  # noqa: E402
from unitesis_simulation import NewtonRaphsonEngine, build_ybus  # noqa: E402
from unitesis_topology import build_energized_network  # noqa: E402

FEEDER = ROOT / "fixtures/networks/ieee33_baran_wu.json"


class FixedPointScreenerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        snap = ingest_file(FEEDER).require_snapshot()
        net = build_energized_network(snap)
        cls.model = build_ybus(snap, net)
        ybus = cls.model.ybus.toarray() if hasattr(cls.model.ybus, "toarray") else cls.model.ybus
        cls.screener = FixedPointScreener(np.asarray(ybus))
        n = len(net.nodes)
        cls.p, cls.q = np.zeros((1, n)), np.zeros((1, n))
        for ld in snap.loads:
            if ld.bus in net.node_of:
                cls.p[0, cls.model.node_index(ld.bus)] += ld.p_mw
                cls.q[0, cls.model.node_index(ld.bus)] += ld.q_mvar
        res = NewtonRaphsonEngine().solve(snap, StudyRequest(snap.content_sha256, "b", "nr"))
        by = {b.bus_id: b for b in res.buses}
        cls.vm_true = np.array([[by[nd].vm_pu for nd in net.nodes]])

    def test_converges_to_the_solver_solution(self):
        res = self.screener.refine(self.p, self.q, 30)
        np.testing.assert_allclose(np.abs(res.v), self.vm_true, atol=1e-8)
        self.assertLess(res.mismatch_pu.max(), 1e-8)

    def test_error_and_mismatch_shrink_with_iterations(self):
        errs, mis = [], []
        for k in (1, 2, 3, 5):
            res = self.screener.refine(self.p, self.q, k)
            errs.append(np.abs(np.abs(res.v) - self.vm_true).max())
            mis.append(res.mismatch_pu.max())
        self.assertEqual(errs, sorted(errs, reverse=True))
        self.assertEqual(mis, sorted(mis, reverse=True))

    def test_slack_is_held_and_a_good_warm_start_saves_iterations(self):
        noisy = np.abs(self.vm_true) * (1 + 0.002) + 0j
        noisy[:, 0] = 0.9                       # a wrong slack guess must be overwritten
        warm = self.screener.refine(self.p, self.q, 1, v0=noisy)
        self.assertEqual(warm.v[0, 0], 1.0)
        flat = self.screener.refine(self.p, self.q, 1)
        self.assertLess(np.abs(np.abs(warm.v) - self.vm_true).max(),
                        np.abs(np.abs(flat.v) - self.vm_true).max())

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            FixedPointScreener(np.zeros((2, 3)))
        with self.assertRaises(ValueError):
            self.screener.refine(self.p, self.q, -1)


if __name__ == "__main__":
    unittest.main()
