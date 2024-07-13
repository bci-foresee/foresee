
import math
import pytest
import numpy as np

from asa import XC


def test_xc_basic():
    xc = XC()

    inputs = np.array([
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 6],
    ], dtype=np.int16)

    result = xc.run(inputs[0], inputs[1])

    assert math.isclose(result, 60.0)

