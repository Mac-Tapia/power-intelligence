"""Unit autograd/physics checks only; these are not dataset training runs."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages/python/power-sciml/src"))


def test_graphsage_dimensions_gradients_and_permutation():
    torch = pytest.importorskip("torch")
    from unitesis_sciml.gnn import PowerGraphSAGE

    torch.manual_seed(4)
    model = PowerGraphSAGE(features=4, hidden=8, layers=2)
    x = torch.randn(3, 3, 4)
    edges = torch.tensor([[0, 1], [1, 2]])
    prediction = model(x, edges)
    assert prediction.shape == (3, 3, 2)
    prediction.square().mean().backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
    order = torch.tensor([2, 0, 1])
    inverse = torch.argsort(order)
    permuted = model(x[:, order], inverse[edges])
    assert torch.allclose(permuted[:, inverse], prediction, atol=1e-6)


def test_ac_residual_zero_at_no_load_and_positive_for_wrong_voltage():
    torch = pytest.importorskip("torch")
    from unitesis_sciml.gnn import ac_balance_loss

    y = torch.tensor([[1-2j, -1+2j], [-1+2j, 1-2j]], dtype=torch.complex64)
    vm = torch.ones((2, 2), requires_grad=True)
    angle = torch.zeros((2, 2))
    injections = torch.zeros((2, 2), dtype=torch.complex64)
    assert ac_balance_loss(vm, angle, y, injections).item() == 0
    wrong = vm * torch.tensor([1.0, 0.9])
    loss = ac_balance_loss(wrong, angle, y, injections)
    assert loss.item() > 0
    loss.backward()
    assert torch.isfinite(vm.grad).all()
