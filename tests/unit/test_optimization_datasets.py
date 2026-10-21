"""Conductor screening on cloned scenarios and leakage-safe datasets (specs 002/018/035)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

import pandas as pd  # noqa: E402
from unitesis_adapters.neutral_json import ingest_file  # noqa: E402
from unitesis_optimization import (  # noqa: E402
    ConductorCost,
    SizingCriteria,
    load_catalog,
    screen_line_conductors,
)
from unitesis_sciml.datasets import DatasetError, DatasetSpec, build_dataset  # noqa: E402
from unitesis_simulation import RadialBFSEngine  # noqa: E402

CATALOG = ROOT / "config/catalogs/conductors/aaac6201_nexans_reference.json"
FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"
SERIES = ROOT / "fixtures/timeseries/synthetic_feeder_load.csv"


class ConductorTests(unittest.TestCase):
    def test_catalog_traceable_and_physics(self):
        cat = load_catalog(CATALOG)
        c = cat.ordered_by_section()[0]
        self.assertAlmostEqual(c.resistance_ohm_km(20.0), c.r20_ohm_km)
        self.assertGreater(c.resistance_ohm_km(75.0), c.r20_ohm_km)
        x, basis = c.reactance_ohm_km(1.0, 60.0)
        self.assertGreater(x, 0.3)
        self.assertEqual(basis, "assumed_gmr_0.7788r")

    def test_missing_catalog_field_never_defaulted(self):
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
        del data["conductors"][0]["alpha20_per_c"]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "c.json"
            p.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_catalog(p)

    def test_screening_uses_clones_and_proposes_smallest_feasible(self):
        snap = ingest_file(FEEDER).require_snapshot()
        before = snap.content_sha256
        cat = load_catalog(CATALOG)
        costs = {c.conductor_id: ConductorCost(c.conductor_id, 10_000 + c.section_mm2 * 100,
                                               "PEN", 2026, "test fixture, not a market price")
                 for c in cat.conductors}
        report = screen_line_conductors(snap, "L01", cat, SizingCriteria(75.0, 1.0),
                                        RadialBFSEngine(), costs)
        self.assertEqual(snap.content_sha256, before)
        feasible = [r for r in report["candidates"] if r["feasible"]]
        self.assertTrue(feasible)
        self.assertEqual(report["proposal_smallest_feasible_section"],
                         feasible[0]["conductor_id"])
        self.assertEqual(report["status"], "proposal_requires_independent_validation")
        self.assertTrue(all("capex" in r for r in report["candidates"]))


class DatasetTests(unittest.TestCase):
    spec = DatasetSpec("timestamp", "p_mw", "15min")

    def test_dataset_is_chronological_and_leakage_safe(self):
        splits, manifest = build_dataset(SERIES, self.spec)
        tr, va, te = splits["train"], splits["validation"], splits["test"]
        step = pd.Timedelta("15min")
        self.assertGreater(va.index[0] - tr.index[-1], step * self.spec.gap_steps)
        self.assertGreater(te.index[0] - va.index[-1], step * self.spec.gap_steps)
        self.assertTrue(all(s["y_is_observed"].all() for s in splits.values()))
        self.assertEqual(manifest["quality"]["outliers_masked"], 1)
        self.assertEqual(manifest["quality"]["frozen_masked"], 30)

    def test_build_is_reproducible(self):
        self.assertEqual(build_dataset(SERIES, self.spec)[1]["dataset_sha256"],
                         build_dataset(SERIES, self.spec)[1]["dataset_sha256"])

    def test_lags_never_use_future(self):
        splits, _ = build_dataset(SERIES, self.spec)
        tr = splits["train"]
        raw = pd.read_csv(SERIES, parse_dates=["timestamp"]).set_index("timestamp")["p_mw"]
        t = tr.index[500]
        # y is the value at t+1 step; lag_1 is the (context) value at t
        self.assertAlmostEqual(tr.loc[t, "y"], raw.loc[t + pd.Timedelta("15min")])
        self.assertAlmostEqual(tr.loc[t, "lag_1"], raw.loc[t])

    def test_conflicting_duplicates_and_off_grid_rejected(self):
        raw = pd.read_csv(SERIES)
        with tempfile.TemporaryDirectory() as tmp:
            dup = raw.copy()
            dup.loc[len(dup)] = [dup.loc[5, "timestamp"], 99.0]
            (Path(tmp) / "d.csv").write_text(dup.to_csv(index=False), encoding="utf-8")
            with self.assertRaises(DatasetError):
                build_dataset(Path(tmp) / "d.csv", self.spec)
            off = raw.copy()
            off.loc[3, "timestamp"] = "2025-01-06 00:07:00"
            (Path(tmp) / "o.csv").write_text(off.to_csv(index=False), encoding="utf-8")
            with self.assertRaises(DatasetError):
                build_dataset(Path(tmp) / "o.csv", self.spec)


if __name__ == "__main__":
    unittest.main()
