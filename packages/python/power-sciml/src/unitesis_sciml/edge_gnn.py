"""Impedance-aware message passing for power-flow surrogates (spec 029, T029-K06).

The plain GraphSAGE sees only nodal P/Q and treats every neighbour alike, so it cannot
know how much voltage a section drops. Here each message carries the section's series
impedance (scale-free: log10 |z|, r/|z|, x/|z|) and is weighted by the normalised
admittance ``|y_ij| / sum_k |y_ik|``, the same coupling the Y-bus uses. Output is the
2-channel correction added to the linear physics prior (``distillation.predict``).
"""

from __future__ import annotations

import torch
from torch import nn

EDGE_FEATURES = 3


def edge_features(z_pu: torch.Tensor) -> torch.Tensor:
    """Scale-free section descriptors from complex series impedance (p.u.)."""
    mag = z_pu.abs().clamp_min(1e-12)
    return torch.stack([torch.log10(mag), z_pu.real / mag, z_pu.imag / mag], dim=-1).float()


class ImpedanceGNN(nn.Module):
    uses_edge_attr = True

    def __init__(self, features: int, hidden: int = 32, layers: int = 6) -> None:
        super().__init__()
        if min(features, hidden, layers) < 1:
            raise ValueError("positive feature/hidden/layer counts required")
        self.input = nn.Linear(features, hidden)
        self.messages = nn.ModuleList(nn.Linear(hidden + EDGE_FEATURES, hidden)
                                      for _ in range(layers))
        self.updates = nn.ModuleList(nn.Linear(hidden * 2, hidden) for _ in range(layers))
        self.output = nn.Linear(hidden, 2)

    def forward(self, features: torch.Tensor, edge_index: torch.Tensor,
                edge_attr: torch.Tensor) -> torch.Tensor:
        if features.ndim != 3 or edge_index.shape[0] != 2:
            raise ValueError("expected batch x nodes x features and 2 x edges")
        if edge_attr.shape != (edge_index.shape[1], EDGE_FEATURES):
            raise ValueError("edge_attr must be edges x 3")
        src = torch.cat((edge_index[0], edge_index[1]))
        dst = torch.cat((edge_index[1], edge_index[0]))
        attr = torch.cat((edge_attr, edge_attr))
        y = torch.pow(10.0, -attr[:, 0])                      # |y| = 1 / |z|
        norm = torch.zeros(features.shape[1], dtype=y.dtype, device=y.device)
        norm.index_add_(0, dst, y)
        weight = (y / norm[dst].clamp_min(1e-12))[None, :, None]
        hidden = torch.tanh(self.input(features))
        e = attr[None].expand(features.shape[0], -1, -1)
        for message, update in zip(self.messages, self.updates, strict=True):
            m = torch.tanh(message(torch.cat((hidden[:, src], e), dim=-1))) * weight
            agg = torch.zeros_like(hidden).index_add_(1, dst, m)
            hidden = torch.tanh(update(torch.cat((hidden, agg), dim=-1)))
        return self.output(hidden)
