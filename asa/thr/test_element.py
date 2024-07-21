
from asa import THR


def test_thr_basic() -> None:
    lower_bound = 2
    upper_bound = 6

    thr = THR(lower_bound, upper_bound)

    value = 5
    result = thr.run(value)

    expected_result = 1
    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    lower_bound = 3
    upper_bound = 4

    thr = THR(lower_bound, upper_bound)

    value = 2
    result = thr.run(value)

    expected_result = 0
    assert result == expected_result, f"Expected {expected_result}, but got {result}"