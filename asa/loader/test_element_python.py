# idk what this does anymore. I think obsolete.

# import numpy as np
# from asa import LOADER


# def test_loader_basic() -> None:

#     signal_in = np.array([
#         [1, 2, 3, 2, 1],
#         [10, 5, -1, 4, 6],
#     ], dtype=np.int16)

#     loader = LOADER(input=signal_in,
#         save_visualization=True)

#     expected_result = np.array([
#         [1, 2, 3, 2, 1],
#         [10, 5, -1, 4, 6],
#     ], dtype=np.int16)

#     result = loader.run()

#     print(result)

#     assert np.allclose(result, expected_result), f"Expected {expected_result}, but got {result}"