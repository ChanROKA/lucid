"""
lucid
=====
Lumeruco's Comprehensive Interface for Deep Learning
"""

from typing import Any
import numpy as np

from lucid._tensor import Tensor
from lucid._func import *

from lucid.types import _ArrayOrScalar


def tensor(
    data: _ArrayOrScalar, requires_grad: bool = False, dtype: Any = np.float32
) -> Tensor:
    return Tensor(data, requires_grad, dtype)
