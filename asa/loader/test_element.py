
import numpy as np
from asa import LOADER


def test_loader_basic() -> None:

    loader = LOADER()

    signal_in = np.array([
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 6],
    ], dtype=np.int16)


    expected_result = np.array([
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 6],
    ], dtype=np.int16)

    result = loader.run(input=signal_in)

    print(result)

    assert np.allclose(result, expected_result), f"Expected {expected_result}, but got {result}"