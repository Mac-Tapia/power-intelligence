"""Data quality gates reproduce the defects found in the 2026-10-20 source review."""

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_sciml.quality import (  # noqa: E402
    forecast_leakage,
    monthly_split_consistency,
    positional_time_index,
    real_coverage,
)

RNG = np.random.default_rng(7)


class ForecastLeakageTests(unittest.TestCase):
    def setUp(self):
        self.actual = 25 + RNG.normal(0, 2, 500)

    def test_future_copy_is_oracle(self):
        for h in (1, 2, 3):
            predicted = np.r_[self.actual[h:], self.actual[-h:]]
            self.assertEqual(forecast_leakage(self.actual, predicted, h)["status"], "oracle")

    def test_persistence_and_honest_forecast(self):
        self.assertEqual(forecast_leakage(self.actual, self.actual, 1)["status"], "persistence")
        noisy = np.r_[self.actual[1:], self.actual[-1:]] + RNG.normal(0, 0.5, 500)
        self.assertEqual(forecast_leakage(self.actual, noisy, 1)["status"], "forecast")

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            forecast_leakage([1, 2], [1, 2], 0)
        with self.assertRaises(ValueError):
            forecast_leakage([1, 2, 3], [1, 2], 1)


class MonthlySplitTests(unittest.TestCase):
    def setUp(self):
        self.peak = RNG.uniform(500, 900, 37)
        self.off = RNG.uniform(1500, 2500, 37)

    def test_consistent(self):
        rep = monthly_split_consistency(self.peak, self.off, self.peak + self.off)
        self.assertEqual((rep["status"], rep["best_lag"]), ("consistent", 0))

    def test_five_month_shift_detected(self):
        total = np.r_[RNG.uniform(100, 300, 5), (self.peak + self.off)[:-5]]
        rep = monthly_split_consistency(self.peak, self.off, total)
        self.assertEqual((rep["status"], rep["best_lag"]), ("shifted", 5))
        self.assertLess(rep["match_lag0"], 0.2)

    def test_unrelated_total_is_inconsistent(self):
        rep = monthly_split_consistency(self.peak, self.off, RNG.uniform(10, 20, 37))
        self.assertEqual(rep["status"], "inconsistent")


class PositionalIndexTests(unittest.TestCase):
    def test_excel_corrupted_hours_but_valid_days(self):
        dates = [f"{d:02d}/01/2024" if i % 7 else "1900-01-01 00:00:00"
                 for d in range(1, 3) for i in range(96)]
        rep = positional_time_index(dates, start="2024-01-01", freq="15min", dayfirst=True)
        self.assertEqual(rep["status"], "rejected")  # 1900 dates disagree with position
        clean = [f"{d:02d}/01/2024" if i % 7 else "garbage" for d in range(1, 3) for i in range(96)]
        rep = positional_time_index(clean, start="2024-01-01", freq="15min", dayfirst=True)
        self.assertEqual(rep["status"], "reconstructable")
        self.assertEqual(rep["end"], "2024-01-02 23:45:00")

    def test_partial_day_rejected(self):
        rep = positional_time_index(["2024-01-01"] * 95, start="2024-01-01", freq="15min")
        self.assertFalse(rep["whole_days"])
        self.assertEqual(rep["status"], "rejected")

    def test_full_timestamps_period_ending_partial_last_day_is_regular(self):
        stamps = [str(t) for t in np.arange(np.datetime64("2023-01-01T00:15"),
                                            np.datetime64("2023-01-03T00:00"),
                                            np.timedelta64(15, "m"))]
        rep = positional_time_index(stamps, start="2023-01-01 00:15", freq="15min")
        self.assertEqual((rep["status"], rep["full_timestamps"]), ("regular", True))

    def test_full_timestamps_with_missing_row_rejected(self):
        stamps = [str(t) for t in np.arange(np.datetime64("2023-01-01T00:00"),
                                            np.datetime64("2023-01-02T00:00"),
                                            np.timedelta64(15, "m"))]
        del stamps[40]
        rep = positional_time_index(stamps, start="2023-01-01", freq="15min")
        self.assertEqual(rep["status"], "rejected")

    def test_shifted_rows_rejected(self):
        dates = ["02/01/2024"] * 96 + ["03/01/2024"] * 96
        rep = positional_time_index(dates, start="2024-01-01", freq="15min", dayfirst=True)
        self.assertEqual(rep["status"], "rejected")


class CoverageTests(unittest.TestCase):
    def test_mostly_empty_file_claiming_thirteen_years(self):
        values = np.r_[RNG.uniform(1, 2, 5472), np.zeros(155_337)]
        rep = real_coverage(values)
        self.assertEqual(rep["status"], "mostly_empty")
        self.assertAlmostEqual(rep["fraction"], 5472 / 160_809)

    def test_claimed_rows_denominator_and_nan(self):
        self.assertEqual(real_coverage([1.0, float("nan"), 2.0, "x"], claimed_rows=2)["status"],
                         "adequate")
        self.assertEqual(real_coverage([1, 1, 0, 1])["status"], "sparse")


if __name__ == "__main__":
    unittest.main()
