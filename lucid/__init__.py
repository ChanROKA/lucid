"""
# `Lucid `

**Lucid** is an educational deep learning framework developed to help users understand 
the underlying mechanics of deep learning models and tensor operations. 

It is designed to provide a simple yet powerful environment to experiment with neural networks, 
optimization, and backpropagation using only `NumPy`. 

Lucid is ideal for those who want to learn about the inner workings of deep learning 
algorithms and operations without the complexity of high-level frameworks.

[📑 Lucid Documentation](https://chanlumerico.github.io/lucid/build/html/index.html)
"""

from contextlib import contextmanager
from typing import Any, Generator, SupportsIndex
import numpy as np

from lucid._tensor import Tensor
from lucid._func import *
from lucid._util import *

from lucid.types import _ArrayOrScalar, _NumPyArray, _ArrayLike, _ShapeLike

import lucid.linalg as linalg
import lucid.random as random
import lucid.nn as nn

_grad_enabled: bool = True

newaxis = np.newaxis

pi = np.pi
inf = np.inf


def tensor(
    data: Tensor | _ArrayOrScalar,
    requires_grad: bool = False,
    keep_grad: bool = False,
    dtype: Any = np.float32,
) -> Tensor:
    if isinstance(data, Tensor):
        data = data.data
    return Tensor(data, requires_grad, keep_grad, dtype)


@contextmanager
def no_grad() -> Generator:
    global _grad_enabled
    prev_state = _grad_enabled
    _grad_enabled = False
    try:
        yield
    finally:
        _grad_enabled = prev_state


def grad_enabled() -> bool:
    return _grad_enabled


def to_tensor(
    a: _ArrayLike,
    requires_grad: bool = False,
    keep_grad: bool = False,
    dtype: Any = np.float32,
) -> Tensor:
    return tensor(a, requires_grad, keep_grad, dtype)


def shape(a: Tensor | _NumPyArray) -> _ShapeLike:
    if hasattr(a, "shape"):
        return a.shape

    raise ValueError(f"The argument must be a Tensor or a NumPy array.")


def _set_tensor_grad(
    tensor: Tensor, grad: _NumPyArray, idx: SupportsIndex = ...
) -> None:
    if tensor.requires_grad:
        if tensor.grad is None:
            tensor.grad = grad
        else:
            tensor.grad[idx] = tensor.grad[idx] + grad


def _check_is_tensor(any: Tensor | _ArrayOrScalar) -> Tensor:
    if not isinstance(any, Tensor):
        return Tensor(any)
    return any


def _match_grad_shape_(data: _NumPyArray, grad: _NumPyArray) -> _NumPyArray:
    if data.shape == grad.shape:
        return grad

    if data.size == grad.size:
        matched_grad = grad
    elif data.size < grad.size:
        axis = []
        if data.ndim == 0:
            axis.extend(range(grad.ndim))
        else:
            for ax in range(data.ndim):
                if data.shape[ax] != grad.shape[ax] and data.shape[ax] == 1:
                    axis.append(ax)

        matched_grad = np.sum(grad, axis=tuple(axis)).reshape(data.shape)
    else:
        matched_grad = np.broadcast_to(grad, data.shape)

    return matched_grad


def _match_grad_shape(
    data: _NumPyArray, grad: _NumPyArray, final_broadcast: bool = True
) -> _NumPyArray:
    if data.shape == grad.shape:
        return grad

    matched_grad = None
    if data.ndim > grad.ndim:
        matched_grad = grad.reshape(data.shape)

    elif data.ndim < grad.ndim:
        squeezed = grad.squeeze()
        matched_grad = squeezed.reshape(data.shape)

    else:
        if data.size == grad.size:
            matched_grad = grad
        elif data.size < grad.size:
            axis = []
            if data.ndim == 0:
                axis.extend(range(grad.ndim))
            else:
                for ax in range(data.ndim):
                    if data.shape[ax] != grad.shape[ax] and data.shape[ax] == 1:
                        axis.append(ax)

            matched_grad = np.sum(grad, axis=tuple(axis)).reshape(data.shape)
        else:
            if final_broadcast:
                matched_grad = np.broadcast_to(grad, data.shape)

    # DEBUG:
    if matched_grad is None:
        print(data.shape, grad.shape)

    return matched_grad
