"""Power-flow scenario dataset, surrogate metrics and physics baseline (spec 006 T006-01..03)."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_application.network_import import import_cyme_export  # noqa: E402
from unitesis_application.pf_baselines import evaluate_baseline, linear_voltages  # noqa: E402
from unitesis_application.pf_dataset import build_pf_dataset  # noqa: E402
from unitesis_config import load_case  # noqa: E402
from unitesis_evidence import read_evidence  # noqa: E402
from unitesis_sciml.pf_scenarios import ScenarioSpec, feeder_split, sample_loads  # noqa: E402
from unitesis_sciml.surrogate_metrics import score_voltages  # noqa: E402
from unitesis_simulation import RadialBFSEngine  # noqa: E402

FIX = ROOT / "fixtures/networks/cyme-ascii"
FILES = (FIX / "RED_synthetic.txt", FIX / "CARGA_synthetic.txt", FIX / "BD_Equipo_synthetic.txt")
CASE = load_case(ROOT / "config/cases/pe-ica-electrodunas.json")


class _SecondBFS(RadialBFSEngine):
    name = "second-bfs-reference"


class ScenarioTests(unittest.TestCase):
    def test_demand_model_is_declared_and_bounded(self):
        spec = ScenarioSpec(200, 0.3, 0.6, 0.0, 1)
        p, q = sample_loads(np.array([1000.0, 0.0]), np.array([0.9, 0.9]), spec,
                            np.random.default_rng(1))
        self.assertEqual(p.shape, (200, 2))
        self.assertTrue(np.all((p[:, 0] >= 0.3 * 0.9) & (p[:, 0] <= 0.6 * 0.9)))
        self.assertTrue(np.all(p[:, 1] == 0))
        self.assertTrue(np.allclose(q, p * np.tan(np.arccos(0.9))))
        self.assertIn("demand_model", spec.as_dict())

    def test_invalid_specs_rejected(self):
        for kwargs in ({"utilisation_min": 0.0}, {"utilisation_max": 5.0},
                       {"load_sigma": 2.0}, {"split_fractions": (0.5, 0.5, 0.5)},
                       {"max_label_residual_pu": 0.1}):
            base = {"scenarios_per_feeder": 5, "utilisation_min": 0.2, "utilisation_max": 0.8,
                    "load_sigma": 0.3, "seed": 1} | kwargs
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                ScenarioSpec(**base)
        with self.assertRaises(ValueError):
            sample_loads(np.array([1.0]), np.array([1.5]), ScenarioSpec(1, 0.2, 0.8, 0.1, 1),
                         np.random.default_rng(0))

    def test_split_is_by_feeder_deterministic_and_disjoint(self):
        ids = [f"F{i}" for i in range(20)]
        spec = ScenarioSpec(1, 0.2, 0.8, 0.1, 42)
        a, b = feeder_split(ids, spec), feeder_split(list(reversed(ids)), spec)
        self.assertEqual(a, b)
        self.assertEqual({"train", "valid", "test"}, set(a.values()))
        self.assertNotEqual(a, feeder_split(ids, ScenarioSpec(1, 0.2, 0.8, 0.1, 43)))


class MetricsTests(unittest.TestCase):
    def test_gate_requires_accuracy_recall_and_enough_violations(self):
        true = np.r_[np.full(100, 0.94), np.full(900, 0.99)]
        self.assertEqual(score_voltages(true, true)["gate_ac_006_02"], "passed")
        missed = true.copy()
        missed[:50] = 0.951
        self.assertEqual(score_voltages(true, missed)["gate_ac_006_02"], "failed")
        few = np.full(100, 0.99)
        self.assertEqual(score_voltages(few, few)["gate_ac_006_02"], "insufficient_violations")
        with self.assertRaises(ValueError):
            score_voltages([1.0], [float("nan")])


class DatasetPipelineTests(unittest.TestCase):
    def test_import_build_and_baseline_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            nets, data = Path(tmp) / "nets", Path(tmp) / "data"
            import_cyme_export(CASE, *FILES, nets)
            spec = ScenarioSpec(6, 0.2, 0.9, 0.2, 3, split_fractions=(0.98, 0.01, 0.01),
                                contrast_fraction=1.0)
            m = build_pf_dataset(CASE, nets, data, spec, reference=_SecondBFS())
            self.assertEqual(m["totals"]["kept"], 6)
            self.assertEqual(m["totals"]["contrast_passed"], 6)
            self.assertLessEqual(m["max_label_residual_pu"], spec.max_label_residual_pu)
            self.assertEqual(read_evidence(data / "manifest.json")["dataset_id"],
                             "pf-scenarios-pe-ica-electrodunas")
            with np.load(data / m["feeders"][0]["file"]) as arrays:
                self.assertEqual(arrays["vm_pu"].shape, arrays["p_mw"].shape)
                self.assertEqual(arrays["edge_index"].shape[0], 2)
            ev = evaluate_baseline(nets, data, Path(tmp) / "base.json", split="train")
            self.assertLess(ev["overall"]["p95_abs_error_pu"], 0.05)

    def test_linear_baseline_is_exact_at_no_load(self):
        from unitesis_adapters.neutral_json import ingest_file
        snap = ingest_file(ROOT / "fixtures/networks/ieee33_baran_wu.json").require_snapshot()
        n = 33
        vm = linear_voltages(snap, np.zeros((1, n)), np.zeros((1, n)))
        self.assertTrue(np.allclose(vm, 1.0))


if __name__ == "__main__":
    unittest.main()
