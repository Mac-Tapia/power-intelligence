"""Measured demand silver rules, physical checks, profiles and baselines (spec 016)."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from unitesis_sciml.load_profiles import (  # noqa: E402
    SilverRules,
    apparent_power_consistency,
    baseline_forecasts,
    silver_from_rows,
    typical_profiles,
)

RULES = SilverRules("FECHA", (("L1 KW", "L1", "kw"), ("L1 KVAR", "L1", "kvar"),
                              ("L1 KVA", "L1", "kva")), "15min", "America/Lima", True)


def cells(values):
    kinds = ["datetime"] + ["float"] * (len(values) - 1)
    return [{"kind": k, "value": v} for k, v in zip(kinds, values, strict=True)]


def synthetic_rows(days=70):
    idx = pd.date_range("2025-01-01 00:15", periods=96 * days, freq="15min")
    shape = 0.6 + 0.4 * np.sin(np.linspace(0, 2 * np.pi, 96, endpoint=False)) ** 2
    rows = [cells(["FECHA", "L1\nKW", "L1\nKVAR", "L1\nKVA"])]
    for i, t in enumerate(idx):
        p = 1000 * shape[i % 96] * (1.1 if t.dayofweek < 5 else 0.8)
        q = 0.3 * p
        rows.append(cells([t.isoformat(), p, q, float(np.hypot(p, q))]))
    return rows


class LoadProfilesTest(unittest.TestCase):
    def setUp(self):
        self.rows = synthetic_rows()
        self.frame, self.report = silver_from_rows(self.rows, RULES)

    def test_interval_ending_stamps_become_interval_start(self):
        self.assertEqual(str(self.frame.index[0]), "2025-01-01 00:00:00-05:00")
        self.assertEqual(self.report["off_grid_stamps"], 0)
        self.assertEqual(self.report["unparsable_rows"], 0)

    def test_duplicates_and_gaps_are_reported_not_repaired(self):
        rows = self.rows[:50] + [self.rows[10]] + self.rows[60:]
        frame, report = silver_from_rows(rows, RULES)
        self.assertEqual(report["duplicate_stamps"], 2)
        self.assertEqual(report["missing_per_column"]["L1_kw"], 10)
        self.assertTrue(frame["L1_kw"].isna().sum() == 10)

    def test_declared_columns_must_exist(self):
        bad = SilverRules("FECHA", (("L9 KW", "L9", "kw"),), "15min", "America/Lima", True)
        with self.assertRaises(ValueError):
            silver_from_rows(self.rows, bad)

    def test_apparent_power_consistency(self):
        f = self.frame
        ok = apparent_power_consistency(f["L1_kw"], f["L1_kvar"], f["L1_kva"])
        self.assertGreater(ok["share_consistent"], 0.999)
        broken = apparent_power_consistency(f["L1_kw"], f["L1_kvar"], f["L1_kva"] * 1.5)
        self.assertLess(broken["share_consistent"], 0.01)

    def test_profiles_and_baselines(self):
        s = self.frame["L1_kw"]
        s.index = s.index.tz_localize(None)
        train_end = s.index[96 * 49 - 1]
        prof = typical_profiles(s[s.index <= train_end], min_days=2)
        self.assertIn("01-weekday", prof["profiles"])
        shape = prof["profiles"]["01-weekday"]["shape_pu"]
        self.assertEqual(len(shape), 96)
        self.assertAlmostEqual(max(shape), 1.0, places=6)
        base = baseline_forecasts(s, train_end, s.index[96 * 56], prof)
        self.assertLess(base["profile_x_recent_peak"]["nmae_percent"], 15)
        self.assertGreater(base["seasonal_naive_week"]["points"], 0)


if __name__ == "__main__":
    unittest.main()
