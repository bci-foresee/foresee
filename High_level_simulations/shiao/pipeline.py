import os
import ctypes
import numpy as np

BANDS = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]


class Pipeline:
    def __init__(self, kernel_lib):
        self.kernels = ctypes.CDLL(os.path.abspath(kernel_lib))
        self.libc = ctypes.CDLL('libc.so.6')

    def filter_bank(self):
        pass

    def cross_correlation(self, inputs, num_channels, num_samples):
        flatten_inputs = inputs.flatten()

        self.kernels.xcorr.argtypes = [
            ctypes.POINTER(ctypes.c_uint16),
            ctypes.c_uint16,
            ctypes.c_uint16,
        ]
        self.kernels.xcorr.restype = ctypes.POINTER(ctypes.c_uint32)

        inputs_ctypes = inputs.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

        results_ptr = self.kernels.xcorr(inputs_ctypes, num_channels, num_samples)

        num_correlations = (num_channels * (num_channels - 1)) >> 1
        results = np.ctypeslib.as_array(results_ptr, shape=(num_correlations,))
        
        correlations = [val for val in results]

        self.libc.free(results_ptr)
        return correlations
        
    def svm_predict(self, weights, inputs, size):
        self.kernels.svm_predict.argtypes = [
            ctypes.POINTER(ctypes.c_double), 
            ctypes.POINTER(ctypes.c_uint16), 
            ctypes.c_uint16
        ]
        self.kernels.svm_predict.restype = ctypes.c_double

        # converting the numpy arrays to ctypes pointers
        weights_ctypes = weights.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        inputs_ctypes = inputs.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

        result = self.kernels.svm_predict(weights_ctypes, inputs_ctypes, size)

        return result

    def fft(self, signal_in, num_points):
        # implemented using numpy because not written previously for halo
        spectrum_out = np.fft.fft(signal_in, num_points)
        return spectrum_out

    def threshold(self, value, low_bound, high_bound):
        if (high_bound >= value >= low_bound):
            return 1
        else:
            return 0
