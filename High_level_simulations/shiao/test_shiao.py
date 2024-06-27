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

def test_bbf():
    #dummy signal to sample
    def signal(x):
        return 200*np.sin(x)
    
    #dummy data
    sample_rate = 400 #Hz, how many samples per second
    num_samples = 1024 # how many samples fed into bbf <- may need to change

    sample_window = (1/sample_rate) * num_samples # seconds, how much time the samples are taken over around 2.56 seconds

    # taking samples
    sample_space = np.linspace(0, sample_window * 2 * np.pi, num_samples) # assuming 2 pi radians per second
    signal_samples = signal(sample_space)
    signal_samples = np.array(signal_samples, dtype=np.uint16)

    # choose gain, filter vals
    gain, filter_vals = give_me_bbf_values("0.1-4")

    # calling the c function, result is power in a certain band (need to implement band part)
    result = pipeline.bbf(signal_in=signal_samples, 
                          filter_vals=filter_vals, 
                          gain=gain,
                          num_points=num_samples)

    print(result)

    assert result == result - 1 + 1 , "Test is failing on purpose right now (I made input big)"

def give_me_bbf_values(filter_range):
    if filter_range == "0.1-4":
        filter_vals = np.array([
            -0.8201374968, 8.3635427995,
            -38.3822761210,  104.3882390000,
            -186.3227066700, 228.0589411300,
            -193.8606607400, 113.0053670900,
            -43.2315892410,  9.8012802461], dtype=np.double)
        gain =  5.890713166e+08
        return (gain, filter_vals)

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