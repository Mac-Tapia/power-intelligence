"""Knowledge distillation for power-flow surrogates (spec 029; ADR-0011).

Methodology (Hinton, Vinyals & Dean 2015; staged physics-informed distillation, Liu et al.
2025), adapted to a regression surrogate whose ground truth is the own solver:

* stage 0, physics teacher: the own AC solver labels every training scenario
  (``pf-scenarios-<case_id>``; each label carries its residual and engine version);
* stage 1, model teacher: a large GraphSAGE fitted to the solver labels plus the AC
  balance residual on the same Y-bus as the solver (AC-008-A02);
* stage 2, student: a small GraphSAGE fitted to
  ``alpha * |student - teacher|^2 + beta * |student - label|^2 + gamma * AC residual``,
  where the teacher term also covers *unlabelled* load scenarios (perturbations of the
  training loads) that cost no solver call. The physics term keeps the student honest
  where the teacher extrapolates.

Numerics: outputs correct a first-order physics prior on the same Y-bus (``linear_prior``),
so line impedances enter every prediction; the AC residual is
divided by (mean |Y_ii|)^2 of each feeder, so short real lines (|Y| up to 1e6 p.u. on 1 MVA)
do not swamp the gradient; the physics term starts after a warm-up (staged, as in Liu et
al.) and gradients are clipped.

Every model is scored with ``score_voltages`` on feeders it never saw (split by feeder,
AC-029-S01) next to a student of the same size trained without the teacher, so the
benefit of distillation is measured, not assumed. Teachers are restricted to the own
solver and own models (``ALLOWED_TEACHERS``): outputs of third-party proprietary tools
are not distillation targets. A surrogate prioritises; the solver confirms (ADR-0002).
"""

from __future__ import annotations

import hashlib
import io
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch

from .edge_gnn import ImpedanceGNN, edge_features
from .gnn import PowerGraphSAGE, ac_balance_loss
from .surrogate_metrics import score_voltages

ALLOWED_TEACHERS = ("own_physics_solver", "own_model")
ARCHITECTURES = ("graphsage", "impedance")
BASE_MVA = 1.0


@dataclass(frozen=True, slots=True)
class TeacherProvenance:
    teacher_id: str
    kind: str
    version: str
    artefact_sha256: str

    def __post_init__(self) -> None:
        if self.kind not in ALLOWED_TEACHERS:
            raise ValueError(f"teacher kind {self.kind!r} not allowed; "
                             f"allowed: {', '.join(ALLOWED_TEACHERS)}")
        if len(self.artefact_sha256) != 64:
            raise ValueError("teacher artefact must be identified by a SHA-256 digest")


@dataclass(frozen=True, slots=True)
class DistillationSpec:
    alpha_teacher: float = 1.0
    beta_label: float = 1.0
    gamma_physics: float = 0.1
    teacher_hidden: int = 64
    teacher_layers: int = 4
    student_hidden: int = 16
    student_layers: int = 2
    epochs: int = 60
    learning_rate: float = 3e-3
    unlabelled_per_scenario: int = 1      # perturbed load scenarios labelled by the teacher
    physics_warmup_fraction: float = 0.3  # staged: physics term off for the first epochs
    grad_clip: float = 1.0
    perturbation: float = 0.2             # relative load perturbation for those scenarios
    seed: int = 7
    architecture: str = "impedance"      # impedance-aware messages (T029-K06) or graphsage

    def __post_init__(self) -> None:
        weights = (self.alpha_teacher, self.beta_label, self.gamma_physics)
        if min(weights) < 0 or sum(weights) == 0:
            raise ValueError("distillation weights must be >= 0 and not all zero")
        if min(self.teacher_hidden, self.teacher_layers, self.student_hidden,
               self.student_layers, self.epochs) < 1:
            raise ValueError("sizes and epochs must be positive")
        if not 0 <= self.physics_warmup_fraction < 1 or self.grad_clip <= 0:
            raise ValueError("warm-up fraction in [0, 1) and positive gradient clip")
        if self.architecture not in ARCHITECTURES:
            raise ValueError(f"architecture must be one of {', '.join(ARCHITECTURES)}")
        if not 0 <= self.perturbation < 1 or self.unlabelled_per_scenario < 0:
            raise ValueError("perturbation in [0, 1) and non-negative unlabelled count")


@dataclass
class FeederGraph:
    network_id: str
    split: str
    edge_index: torch.Tensor          # 2 x E, long
    ybus: torch.Tensor                # N x N complex p.u. (series lines; node 0 = slack)
    features: torch.Tensor            # S x N x 3: p_pu, q_pu, is_slack
    vm: torch.Tensor                  # S x N
    va_rad: torch.Tensor              # S x N
    y_scale: float = 1.0              # mean |Y_ii|: normalises the AC residual per feeder
    edge_attr: torch.Tensor | None = None   # E x 3 scale-free impedance descriptors

    def __post_init__(self) -> None:
        if self.edge_attr is None:
            src, dst = self.edge_index
            y_series = -self.ybus[src, dst]
            self.edge_attr = edge_features(1 / y_series)


def ybus_from_edges(n: int, edge_index: np.ndarray, z_pu: np.ndarray) -> np.ndarray:
    y = np.zeros((n, n), dtype=complex)
    for (i, j), z in zip(edge_index.T, z_pu, strict=True):
        ys = 1 / z
        y[i, i] += ys
        y[j, j] += ys
        y[i, j] -= ys
        y[j, i] -= ys
    return y


def linear_prior(ybus: np.ndarray, p_mw: np.ndarray, q_mvar: np.ndarray
                 ) -> tuple[np.ndarray, np.ndarray]:
    """First-order AC solution on the same Y-bus: V_L = Y_LL^-1 (conj(S_L) - Y_L0), V_0 = 1.

    The physics prior carries the line impedances into every prediction; the network
    only learns the non-linear correction (residual learning on a physics model).
    """
    s = -(p_mw + 1j * q_mvar) / BASE_MVA                     # injections, S x N
    v = np.ones(s.shape, dtype=complex)
    if ybus.shape[0] > 1:
        z_ll = np.linalg.inv(ybus[1:, 1:])
        v[:, 1:] = (np.conj(s[:, 1:]) - ybus[1:, 0][None, :]) @ z_ll.T
    return np.abs(v), np.angle(v)


def _features(p_mw: np.ndarray, q_mvar: np.ndarray, ybus: np.ndarray) -> np.ndarray:
    """Per node: p, q (p.u.), slack flag, linear-prior |V| - 1 and angle (rad)."""
    slack = np.zeros_like(p_mw)
    slack[:, 0] = 1.0
    vm_lin, va_lin = linear_prior(ybus, p_mw, q_mvar)
    return np.stack([p_mw / BASE_MVA, q_mvar / BASE_MVA, slack, vm_lin - 1, va_lin], axis=-1)


def load_feeder_graphs(dataset_dir: str | Path) -> tuple[list[FeederGraph], dict[str, Any]]:
    """Read a ``pf-scenarios`` dataset (verified evidence manifest + per-feeder arrays)."""
    root = Path(dataset_dir)
    raw = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    manifest = raw.get("payload", raw)
    graphs = []
    for f in manifest["feeders"]:
        with np.load(root / f["file"]) as a:
            if len(a["vm_pu"]) == 0:
                continue
            n = a["vm_pu"].shape[1]
            z = a["edge_attr_pu_r_x_len_km"][:, 0] + 1j * a["edge_attr_pu_r_x_len_km"][:, 1]
            ybus = ybus_from_edges(n, a["edge_index"], z)
            graphs.append(FeederGraph(
                f["network_id"], f["split"],
                torch.as_tensor(a["edge_index"], dtype=torch.long),
                torch.as_tensor(ybus),
                torch.as_tensor(_features(a["p_mw"], a["q_mvar"], ybus), dtype=torch.float32),
                torch.as_tensor(a["vm_pu"], dtype=torch.float32),
                torch.as_tensor(np.radians(a["va_deg"]), dtype=torch.float32),
                float(np.abs(np.diag(ybus)).mean())))
    return graphs, manifest


def _injections(features: torch.Tensor) -> torch.Tensor:
    """Specified complex injections (p.u.); loads draw, so injection = -(p + jq)."""
    return torch.complex(-features[..., 0], -features[..., 1]).to(torch.complex128)


def make_model(architecture: str, features: int, hidden: int, layers: int) -> torch.nn.Module:
    if architecture == "impedance":
        return ImpedanceGNN(features, hidden, layers)
    return PowerGraphSAGE(features, hidden, layers)


def predict(model: torch.nn.Module, features: torch.Tensor, g: FeederGraph) -> torch.Tensor:
    """[vm, angle] as a correction of the linear physics prior carried in the features."""
    out = (model(features, g.edge_index, g.edge_attr) if getattr(model, "uses_edge_attr", False)
           else model(features, g.edge_index))
    return torch.stack([1 + features[..., 3] + out[..., 0], features[..., 4] + out[..., 1]],
                       dim=-1)


def physics_residual(out: torch.Tensor, g: FeederGraph, features: torch.Tensor) -> torch.Tensor:
    """AC balance residual divided by (mean |Y_ii|)^2: comparable across feeders, ~ dV^2."""
    vm = out[..., 0].double()
    va = out[..., 1].double()
    raw = ac_balance_loss(vm, va, g.ybus, _injections(features))
    return (raw / g.y_scale ** 2).float()


def distillation_loss(student: torch.Tensor, teacher: torch.Tensor | None,
                      label: torch.Tensor | None, physics: torch.Tensor,
                      spec: DistillationSpec) -> torch.Tensor:
    """Weighted sum; absent terms (no teacher / unlabelled scenario) contribute zero."""
    total = spec.gamma_physics * physics
    if teacher is not None and spec.alpha_teacher:
        total = total + spec.alpha_teacher * (student - teacher).square().mean()
    if label is not None and spec.beta_label:
        total = total + spec.beta_label * (student - label).square().mean()
    return total


def _perturbed(features: torch.Tensor, spec: DistillationSpec,
               gen: torch.Generator) -> torch.Tensor:
    scale = 1 + spec.perturbation * (2 * torch.rand(features.shape[:-1], generator=gen) - 1)
    out = features.clone()
    out[..., 0] *= scale
    out[..., 1] *= scale
    return out


def _labels(g: FeederGraph) -> torch.Tensor:
    return torch.stack([g.vm, g.va_rad], dim=-1)


def train(model: torch.nn.Module, graphs: list[FeederGraph], spec: DistillationSpec, *,
          teacher: torch.nn.Module | None = None) -> list[float]:
    """Fit on the ``train`` split; with a teacher, add its soft targets and unlabelled scenarios."""
    torch.manual_seed(spec.seed)
    gen = torch.Generator().manual_seed(spec.seed)
    opt = torch.optim.Adam(model.parameters(), lr=spec.learning_rate)
    history = []
    train_set = [g for g in graphs if g.split == "train"]
    warmup = int(spec.epochs * spec.physics_warmup_fraction)
    for epoch_i in range(spec.epochs):
        phase = spec if epoch_i >= warmup else DistillationSpec(
            **{**asdict(spec), "gamma_physics": 0.0,
               "beta_label": spec.beta_label or 1.0})
        epoch = 0.0
        for g in train_set:
            batches = [(g.features, _labels(g))]
            if teacher is not None:
                batches += [(_perturbed(g.features, spec, gen), None)
                            for _ in range(spec.unlabelled_per_scenario)]
            for feats, label in batches:
                t_out = None
                if teacher is not None:
                    with torch.no_grad():
                        t_out = predict(teacher, feats, g)
                if label is None and phase.gamma_physics == 0 and t_out is None:
                    continue
                out = predict(model, feats, g)
                physics = (physics_residual(out, g, feats) if phase.gamma_physics
                           else out.new_zeros(()))
                loss = distillation_loss(out, t_out, label, physics, phase)
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), spec.grad_clip)
                opt.step()
                epoch += float(loss)
        history.append(epoch)
    return history


def evaluate(model: torch.nn.Module, graphs: list[FeederGraph], split: str,
             teacher: torch.nn.Module | None = None) -> dict[str, Any]:
    true, pred, fidelity = [], [], []
    with torch.no_grad():
        for g in (g for g in graphs if g.split == split):
            out = predict(model, g.features, g)
            true.append(g.vm.numpy().ravel())
            pred.append(out[..., 0].numpy().ravel())
            if teacher is not None:
                fidelity.append((out - predict(teacher, g.features, g))[..., 0]
                                .abs().numpy().ravel())
    if not true:
        return {"split": split, "nodes_scored": 0}
    metrics = score_voltages(np.concatenate(true), np.concatenate(pred))
    metrics["split"] = split
    if fidelity:
        metrics["mean_abs_gap_to_teacher_pu"] = float(np.concatenate(fidelity).mean())
    return metrics


def state_sha256(model: torch.nn.Module) -> str:
    buf = io.BytesIO()
    torch.save({k: v.cpu() for k, v in model.state_dict().items()}, buf)
    return hashlib.sha256(buf.getvalue()).hexdigest()


def _params(model: torch.nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())


def _latency_ms(model: torch.nn.Module, graphs: list[FeederGraph]) -> float:
    with torch.no_grad():
        t0 = time.perf_counter()
        n = 0
        for g in graphs:
            predict(model, g.features, g)
            n += g.features.shape[0]
    return (time.perf_counter() - t0) * 1e3 / max(n, 1)


def run_distillation(graphs: list[FeederGraph], spec: DistillationSpec,
                     physics_teacher: TeacherProvenance) -> tuple[dict[str, Any], dict]:
    """Teacher, distilled student and same-size baseline student; returns (report, models)."""
    torch.manual_seed(spec.seed)
    features = graphs[0].features.shape[-1]
    teacher = make_model(spec.architecture, features, spec.teacher_hidden, spec.teacher_layers)
    teacher_spec = DistillationSpec(**{**asdict(spec), "alpha_teacher": 0.0})
    train(teacher, graphs, teacher_spec)
    teacher.eval()
    model_teacher = TeacherProvenance(f"{spec.architecture}-teacher", "own_model", "1",
                                      state_sha256(teacher))
    torch.manual_seed(spec.seed)
    student = make_model(spec.architecture, features, spec.student_hidden, spec.student_layers)
    train(student, graphs, spec, teacher=teacher)
    torch.manual_seed(spec.seed)
    baseline = make_model(spec.architecture, features, spec.student_hidden,
                          spec.student_layers)
    train(baseline, graphs, teacher_spec)
    models = {"teacher": teacher, "student": student, "baseline_student": baseline}
    report: dict[str, Any] = {
        "schema": "unitesis.distillation-report/1",
        "spec": asdict(spec),
        "teachers": [asdict(physics_teacher), asdict(model_teacher)],
        "split_policy": "by feeder (AC-029-S01)",
        "feeders": {s: sorted(g.network_id for g in graphs if g.split == s)
                    for s in ("train", "valid", "test")},
        "models": {},
    }
    for name, model in models.items():
        report["models"][name] = {
            "parameters": _params(model), "state_sha256": state_sha256(model),
            "latency_ms_per_scenario": _latency_ms(model, graphs),
            "valid": evaluate(model, graphs, "valid", teacher if name != "teacher" else None),
            "test": evaluate(model, graphs, "test", teacher if name != "teacher" else None),
        }
    s, b = report["models"]["student"]["test"], report["models"]["baseline_student"]["test"]
    report["distillation_effect_test_p95_pu"] = (
        None if "p95_abs_error_pu" not in s else
        b["p95_abs_error_pu"] - s["p95_abs_error_pu"])
    report["decision_rule"] = ("a surrogate is usable for screening only if its test gate "
                               "passes; every decision is confirmed by the own solver")
    return report, models


def select_by_validation(graphs: list[FeederGraph], candidates: list[DistillationSpec]
                         ) -> tuple[DistillationSpec, list[dict[str, Any]]]:
    """Fit a teacher per candidate and keep the lowest *validation* p95.

    The test split is never looked at here; it is evaluated once, on the chosen spec, by
    ``run_distillation``. Ties keep the earlier (simpler) candidate.
    """
    table = []
    features = graphs[0].features.shape[-1]
    for spec in candidates:
        torch.manual_seed(spec.seed)
        model = make_model(spec.architecture, features, spec.teacher_hidden,
                           spec.teacher_layers)
        train(model, graphs, DistillationSpec(**{**asdict(spec), "alpha_teacher": 0.0}))
        valid = evaluate(model, graphs, "valid")
        table.append({"spec": asdict(spec), "parameters": _params(model),
                      "valid_p95_pu": valid.get("p95_abs_error_pu"),
                      "valid_recall": valid.get("violation_recall")})
    best = min(range(len(table)), key=lambda i: (table[i]["valid_p95_pu"] or float("inf"), i))
    return candidates[best], table
