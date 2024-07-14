
import numpy as np
from asa import SVM


def test_svm_basic() -> None:
    # dummy weights and input data
    model = np.array([0.1, 0.2, 0.3, 0.4, 0.5], dtype=np.float32)
    values = np.array([1, 2, 3, 4, 5], dtype=np.int32)
    expected_result = 5.5

    svm = SVM(model)
    result = svm.run(values)
    
    # Allow for floating-point precision errors
    assert np.isclose(result, expected_result), f"Expected {expected_result}, but got {result}"