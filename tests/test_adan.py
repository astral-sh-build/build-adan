import importlib
from importlib.metadata import version

import pytest
import torch


@pytest.fixture(scope="module")
def device() -> torch.device:
    assert torch.cuda.is_available(), "The tests must run on a CUDA GPU"
    device = torch.device("cuda")
    return device


def test_published_cuda_wheel(device: torch.device) -> None:
    assert version("adan") == "0.0.2+cu.12.8.torch.2.10"
    assert torch.__version__ == "2.10.0+cu128"
    assert torch.version.cuda == "12.8"
    assert torch.cuda.get_device_name(device)


@pytest.mark.parametrize("module_name", ["adan"])
def test_native_module(device: torch.device, module_name: str) -> None:
    assert importlib.import_module(module_name) is not None


@pytest.mark.parametrize("fused", [False, True])
def test_cuda_optimizer_step(device: torch.device, fused: bool) -> None:
    from adan import Adan

    parameter = torch.nn.Parameter(torch.tensor([1.0, -2.0, 3.0], device=device))
    optimizer = Adan([parameter], lr=0.01, fused=fused)
    before = parameter.detach().clone()
    parameter.square().sum().backward()
    optimizer.step()
    assert torch.isfinite(parameter).all()
    assert not torch.equal(parameter, before)
