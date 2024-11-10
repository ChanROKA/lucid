import numpy as np

from lucid._tensor import Tensor
from lucid.types import _ShapeLike


def seed(seed: int) -> None:
    np.random.seed(seed)


def rand(shape: _ShapeLike, requires_grad: bool = False) -> Tensor:
    return Tensor(np.random.rand(*shape), requires_grad=requires_grad)


def randint(
    low: int, high: int | None, size: int | _ShapeLike, requires_grad: bool = False
) -> Tensor:
    return Tensor(np.random.randint(low, high, size), requires_grad=requires_grad)


def randn(shape: _ShapeLike, requires_grad: bool = False) -> Tensor:
    return Tensor(np.random.randn(*shape), requires_grad=requires_grad)
