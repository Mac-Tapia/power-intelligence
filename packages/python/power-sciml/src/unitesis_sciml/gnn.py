"""Spec 029 GraphSAGE and AC balance regularizer; inference is not certification.

Tensor output is [voltage magnitude p.u., angle rad] per node. Consumers must
gate deployment using held-out metrics and confirm decisions with the own solver.
"""

from __future__ import annotations

import torch
from torch import nn


class PowerGraphSAGE(nn.Module):
    def __init__(self, features: int, hidden: int = 32, layers: int = 3) -> None:
        super().__init__()
        if min(features, hidden, layers) < 1:
            raise ValueError("positive feature/hidden/layer counts required")
        self.input = nn.Linear(features, hidden)
        self.updates = nn.ModuleList(nn.Linear(hidden * 2, hidden) for _ in range(layers))
        self.output = nn.Linear(hidden, 2)

    def forward(self, features: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        if features.ndim != 3 or edge_index.ndim != 2 or edge_index.shape[0] != 2:
            raise ValueError("expected batch x nodes x features and 2 x edges")
        if edge_index.dtype != torch.long or not torch.isfinite(features).all():
            raise ValueError("finite features and integer edges required")
        if edge_index.numel() and (edge_index.min() < 0 or edge_index.max() >= features.shape[1]):
            raise ValueError("unknown edge endpoint")
        edges = torch.cat((edge_index, edge_index.flip(0)), dim=1)
        source, target = edges
        degree = torch.zeros(features.shape[1], device=features.device, dtype=features.dtype)
        degree.index_add_(0, target, torch.ones_like(target, dtype=features.dtype))
        hidden = torch.tanh(self.input(features))
        for update in self.updates:
            summed = torch.zeros_like(hidden).index_add_(1, target, hidden[:, source])
            mean = summed / degree.clamp_min(1)[None, :, None]
            hidden = torch.tanh(update(torch.cat((hidden, mean), dim=-1)))
        return self.output(hidden)


def ac_balance_loss(vm: torch.Tensor, angle_rad: torch.Tensor, ybus: torch.Tensor,
                    specified_injections_pu: torch.Tensor) -> torch.Tensor:
    """Mean |V conj(YV) - S_spec|² on non-slack nodes; all quantities in p.u."""
    if (vm.ndim != 2 or angle_rad.shape != vm.shape or ybus.shape != (vm.shape[1], vm.shape[1])
            or specified_injections_pu.shape != vm.shape):
        raise ValueError("AC residual dimensions mismatch")
    if not all(torch.isfinite(t).all() for t in (vm, angle_rad, ybus, specified_injections_pu)):
        raise ValueError("non-finite AC residual inputs")
    voltage = torch.polar(vm, angle_rad)
    current = voltage @ ybus.to(voltage.dtype).T
    residual = voltage * current.conj() - specified_injections_pu
    return residual[:, 1:].abs().square().mean() if vm.shape[1] > 1 else residual.abs().sum() * 0
