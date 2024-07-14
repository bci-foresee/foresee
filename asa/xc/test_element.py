
import math
import numpy as np

from asa import XC


def test_xc_basic() -> None:
    xc = XC()

    inputs = np.array([
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 6],
    ], dtype=np.int16)
    expected_result = 60.0

    result = xc.run(inputs[0], inputs[1])

    assert np.isclose(result, expected_result), f"Expected {expected_result}, but got {result}"
