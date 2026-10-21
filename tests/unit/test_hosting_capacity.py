"""Remaining capacity per bus: surrogate screening certified by the own solver (002/006)."""

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.neutral_json import ingest_file  # noqa: E402
from unitesis_application.hosting_capacity import (  # noqa: E402
    LinearYBusSurrogate,
    _with_probe,
    hosting_capacity,
)
from unitesis_domain import StudyRequest  # noqa: E402
from unitesis_ports import SurrogateEngine  # noqa: E402
from unitesis_simulation import NewtonRaphsonEngine  # noqa: E402

IEEE33 = ingest_file(ROOT / "fixtures/networks/ieee33_baran_wu.json").require_snapshot()
LEVELS = [round(0.25 * k, 2) for k in range(1, 13)]
KW = {"power_factor": 0.95, "v_min_pu": 0.90, "max_loading_percent": 100.0, "margin_pu": 0.0}


class _AlwaysFineSurrogate(LinearYBusSurrogate):
    """Wrong on purpose: predicts flat voltages, so every limit must come from the solver."""

    name = "always-fine"

    def predict_vm(self, snapshot, p_node, q_node):
        return np.ones_like(np.asarray(p_node, dtype=float))


def brute_force_limit(bus: str) -> float:
    eng, last = NewtonRaphsonEngine(), 0.0
    for p in LEVELS:
        scen = _with_probe(IEEE33, bus, p, p * math.tan(math.acos(0.95)))
        res = eng.solve(scen, StudyRequest(scen.content_sha256, "bf", eng.name))
        if res.status != "computed" or min(b.vm_pu for b in res.buses) < 0.90:
            return last
        last = p
    return last


class HostingCapacityTests(unittest.TestCase):
    def test_port_is_implemented(self):
        self.assertIsInstance(LinearYBusSurrogate(), SurrogateEngine)

    def test_confirmed_limits_equal_exhaustive_solver_sweep(self):
        buses = ["B6", "B18", "B25", "B33"]
        for surrogate in (LinearYBusSurrogate(), _AlwaysFineSurrogate()):
            with self.subTest(surrogate=surrogate.name):
                r = hosting_capacity(IEEE33, buses, LEVELS, surrogate=surrogate, **KW)
                got = {b["bus"]: b["confirmed_limit_mw"] for b in r["buses"]}
                self.assertEqual(got, {b: brute_force_limit(b) for b in buses})
                self.assertTrue(all(b["status"] == "confirmed_by_solver" for b in r["buses"]))

    def test_wrong_surrogate_is_detected_not_trusted(self):
        r = hosting_capacity(IEEE33, ["B18"], LEVELS, surrogate=_AlwaysFineSurrogate(), **KW)
        self.assertFalse(r["buses"][0]["surrogate_agreed_with_solver"])

    def test_base_case_violation_is_reported(self):
        r = hosting_capacity(IEEE33, ["B6"], LEVELS, power_factor=0.95, v_min_pu=0.95,
                             max_loading_percent=100.0, margin_pu=0.0)
        self.assertEqual(r["base_case"], {"passes_criteria": False, "criterion": "voltage"})
        self.assertEqual(r["solver_calls"], 1)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            hosting_capacity(IEEE33, ["B6"], [1.0, 0.5], **KW)
        with self.assertRaises(ValueError):
            hosting_capacity(IEEE33, ["B6"], LEVELS, power_factor=1.5, v_min_pu=0.9,
                             max_loading_percent=100.0, margin_pu=0.0)


if __name__ == "__main__":
    unittest.main()
