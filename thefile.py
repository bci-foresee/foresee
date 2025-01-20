from scipy.signal import butter, filtfilt
import numpy as np


def butter_bandpass(lowcut, highcut, fs, order=5):
    # this function returns the coefficients of the bandpass filter
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    # this function applies the bandpass filter to the input data
    # a, b are the coefficients of the bandpass filter
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


test_data = np.random.rand(1000)

test_out = butter_bandpass_filter(test_data, 4, 12, 1000, order=5)

print(test_out.shape)
