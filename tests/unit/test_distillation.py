"""Knowledge distillation of power-flow surrogates (spec 029, ADR-0011).

Labels come from the own Newton-Raphson on the synthetic 6-bus feeder (physics teacher);
the checks cover provenance rules, the loss terms, the Y-bus used by the physics term and
the full teacher -> student pipeline with a feeder-disjoint evaluation.
"""

import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

try:
    import torch
    HAS_TORCH = True
except Exception:  # pragma: no cover - torch is an authorised optional dependency
    HAS_TORCH = False

import numpy as np  # noqa: E402
from unitesis_adapters.neutral_json import ingest_file  # noqa: E402
from unitesis_domain import StudyRequest  # noqa: E402
from unitesis_simulation import NewtonRaphsonEngine, build_ybus  # noqa: E402
from unitesis_topology import build_energized_network  # noqa: E402

FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"


def solved_feeder(split, scenarios, seed):
    """Graph of the 6-bus feeder with NR-labelled random load scenarios."""
    from unitesis_sciml.distillation import FeederGraph, _features, ybus_from_edges

    snap = ingest_file(FEEDER).require_snapshot()
    net = build_energized_network(snap)
    model = build_ybus(snap, net)
    nodes = list(net.nodes)
    rng = np.random.default_rng(seed)
    p, q, vm, va = [], [], [], []
    engine = NewtonRaphsonEngine()
    for _ in range(scenarios):
        factor = rng.uniform(0.6, 1.4, len(snap.loads))
        loads = tuple(replace(ld, p_mw=ld.p_mw * f, q_mvar=ld.q_mvar * f)
                      for ld, f in zip(snap.loads, factor, strict=True))
        scen = replace(snap, loads=loads)
        res = engine.solve(scen, StudyRequest(scen.content_sha256, "s", engine.name))
        by = {b.bus_id: b for b in res.buses}
        pn, qn = np.zeros(len(nodes)), np.zeros(len(nodes))
        for ld in (ld for ld in loads if ld.bus in net.node_of):
            pn[model.node_index(ld.bus)] += ld.p_mw
            qn[model.node_index(ld.bus)] += ld.q_mvar
        p.append(pn)
        q.append(qn)
        vm.append([by[n].vm_pu for n in nodes])
        va.append([np.radians(by[n].va_deg) for n in nodes])
    edge_index = np.array([[i for _, i, _, _ in model.line_terms],
                           [j for _, _, j, _ in model.line_terms]], dtype=np.int64)
    z = np.array([1 / y for *_, y in model.line_terms])
    ybus = ybus_from_edges(len(nodes), edge_index, z)
    return FeederGraph(f"six-bus-{split}", split, torch.as_tensor(edge_index),
                       torch.as_tensor(ybus),
                       torch.as_tensor(_features(np.array(p), np.array(q), ybus),
                                       dtype=torch.float32),
                       torch.as_tensor(np.array(vm), dtype=torch.float32),
                       torch.as_tensor(np.array(va), dtype=torch.float32)), model


@unittest.skipUnless(HAS_TORCH, "torch not installed")
class DistillationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train_g, cls.model = solved_feeder("train", 24, 1)
        cls.valid_g, _ = solved_feeder("valid", 8, 2)
        cls.test_g, _ = solved_feeder("test", 8, 3)

    def test_teacher_provenance_rules(self):
        from unitesis_sciml.distillation import TeacherProvenance
        TeacherProvenance("nr", "own_physics_solver", "0.2.0", "a" * 64)
        with self.assertRaises(ValueError):
            TeacherProvenance("x", "third_party_proprietary", "1", "a" * 64)
        with self.assertRaises(ValueError):
            TeacherProvenance("nr", "own_physics_solver", "0.2.0", "short")

    def test_edge_ybus_equals_solver_ybus(self):
        np.testing.assert_allclose(self.train_g.ybus.numpy(), self.model.ybus.toarray()
                                   if hasattr(self.model.ybus, "toarray") else self.model.ybus,
                                   atol=1e-12)

    def test_physics_term_vanishes_on_solver_labels(self):
        from unitesis_sciml.distillation import physics_residual
        labels = torch.stack([self.train_g.vm, self.train_g.va_rad], dim=-1)
        # labels are stored in float32: mean squared residual ~ (1e-5 p.u.)^2
        self.assertLess(float(physics_residual(labels, self.train_g, self.train_g.features)),
                        1e-8)

    def test_physics_term_is_normalised_by_feeder_admittance(self):
        # real feeders reach mean |Y_ii| ~ 1e6 p.u.: the residual must be scale free
        from dataclasses import replace as dc_replace

        from unitesis_sciml.distillation import physics_residual
        flat = torch.stack([torch.ones_like(self.train_g.vm),
                            torch.zeros_like(self.train_g.va_rad)], dim=-1)
        g1 = dc_replace(self.train_g, y_scale=1.0)
        g2 = dc_replace(self.train_g, ybus=self.train_g.ybus * 1e3, y_scale=1e3)
        r1 = float(physics_residual(flat, g1, g1.features))
        r2 = float(physics_residual(flat, g2, g2.features * 1e3))
        self.assertAlmostEqual(r1, r2, delta=1e-6 * r1)

    def test_predictions_start_at_the_linear_physics_prior(self):
        from unitesis_sciml.distillation import predict
        from unitesis_sciml.gnn import PowerGraphSAGE
        model = PowerGraphSAGE(5, 8, 2)
        torch.nn.init.zeros_(model.output.weight)
        torch.nn.init.zeros_(model.output.bias)
        out = predict(model, self.train_g.features, self.train_g.edge_index)
        feats = self.train_g.features
        self.assertTrue(torch.allclose(out[..., 0], 1 + feats[..., 3]))
        self.assertTrue(torch.allclose(out[..., 1], feats[..., 4]))
        # the prior alone is already close to the solver on this lightly loaded feeder
        self.assertLess(float((out[..., 0] - self.train_g.vm).abs().max()), 0.01)

    def test_loss_terms(self):
        from unitesis_sciml.distillation import DistillationSpec, distillation_loss
        s = torch.ones(2, 3, 2)
        spec = DistillationSpec(alpha_teacher=2.0, beta_label=3.0, gamma_physics=0.5)
        total = distillation_loss(s, torch.zeros_like(s), torch.full_like(s, 2.0),
                                  torch.tensor(4.0), spec)
        self.assertAlmostEqual(float(total), 2.0 * 1 + 3.0 * 1 + 0.5 * 4)
        unlabelled = distillation_loss(s, torch.zeros_like(s), None, torch.tensor(0.0), spec)
        self.assertAlmostEqual(float(unlabelled), 2.0)
        with self.assertRaises(ValueError):
            DistillationSpec(alpha_teacher=0, beta_label=0, gamma_physics=0)

    def test_pipeline_reports_teacher_student_and_baseline(self):
        from unitesis_sciml.distillation import (
            DistillationSpec,
            TeacherProvenance,
            run_distillation,
        )
        spec = DistillationSpec(epochs=15, teacher_hidden=24, teacher_layers=3,
                                student_hidden=8, student_layers=2)
        physics = TeacherProvenance("unitesis-newton-raphson", "own_physics_solver", "0.2.0",
                                    "b" * 64)
        report, models = run_distillation([self.train_g, self.valid_g, self.test_g], spec,
                                          physics)
        self.assertEqual(set(models), {"teacher", "student", "baseline_student"})
        self.assertLess(report["models"]["student"]["parameters"],
                        report["models"]["teacher"]["parameters"])
        self.assertEqual(report["feeders"]["test"], ["six-bus-test"])
        for name in models:
            test = report["models"][name]["test"]
            self.assertIn("gate_ac_006_02", test)
            self.assertTrue(np.isfinite(test["p95_abs_error_pu"]))
        self.assertIn("mean_abs_gap_to_teacher_pu", report["models"]["student"]["test"])
        self.assertEqual([t["kind"] for t in report["teachers"]],
                         ["own_physics_solver", "own_model"])


if __name__ == "__main__":
    unittest.main()
