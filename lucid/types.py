import numpy as np


_Scalar = int | float
_NumPyArray = np.ndarray
_ArrayOrScalar = _Scalar | list | _NumPyArray

_ShapeLike = list[int] | tuple[int]
_ArrayLike = list | _NumPyArray
