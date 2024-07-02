import os
import ctypes
import pytest
import numpy as np
from pipeline import Pipeline
from scipy.signal import butter, filtfilt

'''
To run the tests:

cd High_level_simulations/shiao
pytest -v test_shiao.py

-v stands for verbose
'''

# loading in all the c functions for the pipeline
pipeline = Pipeline(kernel_lib='libkernels.so')

# XCORR ------------------------------------------------------------------------------------------
def test_xcorr_basic():
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

def test_xcorr_8000():
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
        # return np.ones_like(x)
        return 10*np.sin(x) + 5*np.sin(2*x) + 2*np.sin(3*x) + 1*np.sin(4*x)
    
    #dummy data
    sample_rate = 400 #Hz, how many samples per second
    num_samples = 8000 # how many samples fed into bbf <- may need to change

    sample_window = (1/sample_rate) * num_samples # seconds, how much time the samples are taken over around 2.56 seconds

    # taking samples
    sample_space = np.linspace(0, sample_window * 2 * np.pi, num_samples) # assuming 2 pi radians per second
    signal_samples = signal(sample_space)
    signal_samples = np.array(signal_samples, dtype=np.uint16)

    # print("...signal_samples...")
    # print(len(signal_samples))
    # print(signal_samples[:10])

    # choose gain, filter vals
    chosen_bandpass = "30-80"
    gain, filter_vals = give_me_bbf_values(chosen_bandpass)

    #printing all the inputs that go in
    print("...inputs...")
    print("chosen band: ", chosen_bandpass)
    print("signal_in: ", signal_samples[:10], "...")
    print("filter_vals[0,1]: ", filter_vals[0:2])
    print("filter_vals[2,3]: ", filter_vals[2:4])
    print("filter_vals[4,5]: ", filter_vals[4:6])
    print("filter_vals[6,7]: ", filter_vals[6:8])
    print("filter_vals[8,9]: ", filter_vals[8:10])
    print("gain: ", gain)
    print("num_points: ", num_samples)
    print()

    # calling the c function, result is power in a certain band (need to implement band part)
    result = pipeline.bbf(signal_in=signal_samples, 
                          filter_vals=filter_vals, 
                          gain=gain,
                          num_points=num_samples)

    #printing the output:
    print("...output...")
    print("result: ", result)
    print()

    print("...test 2 bbf...")
    out = expected_bbf(signal_samples)
    print(out)
    print("30-80: ", out[4])

    assert result == result - 1 + 1 , "Test not implemented"

def give_me_bbf_values(filter_range):
    if filter_range == "30-80":
        filter_vals = np.array([
             -0.0723156691,  0.6368872577,
             -2.8198218361,  8.0640603736,
            -16.3818055300, 24.6025699180,
            -27.6694600560, 23.0616757780,
            -13.6958889160,  5.2541969233
            ], dtype=np.double)
        gain =  3.049509079e+02
        return (gain, filter_vals)
    
def expected_bbf(signal):
    SAMPLING_FREQ = 400
    BANDS = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]

    result = []
    for band in BANDS:
        order = 5
        low_freq = band[0] / (SAMPLING_FREQ / 2.0) # why is it div by 2?
        high_freq = band[1] / (SAMPLING_FREQ / 2.0)
        # low_freq = band[0] / (SAMPLING_FREQ)
        # high_freq = band[1] / (SAMPLING_FREQ)
        # print("low_freq: ", low_freq)
        # print("high_freq: ", high_freq)
        b, a = butter(order, [low_freq, high_freq], btype="bandpass")
        # print(b[10])
        filtered_signal = filtfilt(b, a, signal)
        # print(len(filtered_signal))
        power_est = np.dot(filtered_signal, filtered_signal)
        result.append(power_est)
    return result

# FFT --------------------------------------------------------------------------------------------

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


def test_fft_8000():
    # dummy data
    # 8000 points, so 16000 values (pair of real and complex for each "point")
    num_points = 8000
    signal_in = np.zeros(num_points*2, dtype=np.double)

    for i in range(num_points):
        signal_in[2 * i] = 100 # real part of the signal
        signal_in[2*i + 1] = 0 # imaginary part of the signal
    
    # calling the c function
    result = pipeline.fft(signal_in, num_points=num_points)

    # further testing code
    real_out = [result[2*i] for i in range(num_points)]
    imag_out = [result[2*i + 1] for i in range(num_points)]

    # get magnitude of output
    magnitude = np.zeros(num_points, dtype=np.double)
    for i in range(num_points):
        magnitude[i] = np.sqrt(real_out[i]**2 + imag_out[i]**2)

    # "ideal" using np.fft.fft
    real_signal_in = [signal_in[2*i] for i in range(num_points)]
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