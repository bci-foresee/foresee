import os
import ctypes
import pytest
import numpy as np
from pipeline import Pipeline

'''
To run the tests:

cd High_level_simulations/shiao
pytest -v test_shiao.py

-v stands for verbose
'''

# loading in all the c functions for the pipeline
pipeline = Pipeline(kernel_lib='libkernels.so')

# XCORR ------------------------------------------------------------------------------------------
def test_xcorr():
    # dummy data
    inputs = np.array([
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 6],
        [1, 2, 3, 4, 7],
    ], dtype=np.uint16)
    num_channels, num_samples = inputs.shape

    # calling the c function
    result = pipeline.cross_correlation(inputs, num_channels, num_samples)

    # Use numpy's dot product for expected result
    expected_result = [
        np.dot(inputs[0], inputs[1]), 
        np.dot(inputs[0], inputs[2]), 
        np.dot(inputs[1], inputs[2]), 
    ]

    # Allow for floating-point precision errors
    assert np.allclose(result, expected_result), f"Expected {expected_result}, but got {result}"

# BBF --------------------------------------------------------------------------------------------

# ------ to do ------

# FFT --------------------------------------------------------------------------------------------
# now in c!
def test_fft_1024():
    # dummy data
    # 1024 points, so 2048 values (pair of real and complex for each "point")
    signal_in = np.zeros(2048, dtype=np.double)

    for i in range(1024):
        signal_in[2 * i] = 100 # real part of the signal
        signal_in[2*i + 1] = 0 # imaginary part of the signal
    
    # calling the c function
    result = pipeline.fft(signal_in, num_points=1024)

    # # print for now
    # print(result[0:20])
    # print("\n look here \n")

    # further testing code
    real_out = [result[2*i] for i in range(1024)]
    imag_out = [result[2*i + 1] for i in range(1024)]

    # get magnitude of output
    magnitude = np.zeros(1024, dtype=np.double)
    for i in range(1024):
        magnitude[i] = np.sqrt(real_out[i]**2 + imag_out[i]**2)

    # "ideal" using np.fft.fft
    real_signal_in = [signal_in[2*i] for i in range(1024)]
    ideal_out = np.fft.fft(real_signal_in)

    # test
    assert np.allclose(magnitude, np.abs(ideal_out)), f"Expected {np.abs(ideal_out)}, but got {magnitude}"


# SVM --------------------------------------------------------------------------------------------
def test_svm_predict():
    # dummy weights and input data
    model = np.array([0.1, 0.2, 0.3, 0.4, 0.5], dtype=np.float64)
    values = np.array([1, 2, 3, 4, 5], dtype=np.uint16)
    size = len(values)

    # calling the c function
    result = pipeline.svm_predict(model, values, size)
    
    # Use numpy's dot product for expected result
    expected_result = np.dot(model, values)
    
    # Allow for floating-point precision errors
    assert np.isclose(result, expected_result), f"Expected {expected_result}, but got {result}"

# THR --------------------------------------------------------------------------------------------

def test_threshold():
    # dummy data
    value = 5
    low_bound = 2
    high_bound = 6

    # calling the c function
    result = pipeline.threshold(value, low_bound, high_bound)

    # Use numpy's dot product for expected result
    expected_result = 1

    # Allow for floating-point precision errors
    assert result == 1, f"Expected {expected_result}, but got {result}"


# test_fft_1024()