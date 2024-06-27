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

    def fft(self, signal_in, num_points=1024):
        # written with spiral software in c
        #  double* fft_1024(double *X){
        # // set up Y, 2048 vals, pair of real and complex for each "point"
        # double* Y = (double*)malloc(2048 * sizeof(double));

        # input type is pointer to double array
        self.kernels.fft_1024.argtypes = [ctypes.POINTER(ctypes.c_double)]
        
        # output type is pointer to double array
        self.kernels.fft_1024.restype = ctypes.POINTER(ctypes.c_double)

        # convert input numpy signal in to ctypes pointer
        signal_in_ctypes = signal_in.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        # call the function, get result pointer
        result_ptr = self.kernels.fft_1024(signal_in_ctypes)

        # convert the result pointer to a numpy array
        result_spectrum = np.ctypeslib.as_array(result_ptr, shape=(2048,))

        # free the memory
        spectrum_out = [val for val in result_spectrum]
        self.libc.free(result_ptr)

        return spectrum_out


    def bbf(self, signal_in, filter_vals, gain, num_points=1024):
        # input types
        self.kernels.butterworth_filter.argtypes = [ctypes.POINTER(ctypes.c_uint16),
                                                    ctypes.c_uint32,
                                                    ctypes.POINTER(ctypes.c_double),
                                                    ctypes.c_double]
        
        # output types - power of band
        self.kernels.butterworth_filter.restype = ctypes.c_float

        # convert input numpy signal in to ctypes pointer
        signal_in_ctypes = signal_in.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

        # convert input numpy filter values to ctypes pointer
        filter_vals_ctypes = filter_vals.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        # call the function, get result power float
        result = self.kernels.butterworth_filter(signal_in_ctypes, 
                                                 num_points,
                                                 filter_vals_ctypes,
                                                 gain)

        #return 
        return result

    
    def svm_predict(self, weights, inputs, size):
        # converting inputs into strongly typed values for the c function
        self.kernels.svm_predict.argtypes = [
            ctypes.POINTER(ctypes.c_double), 
            ctypes.POINTER(ctypes.c_uint16), 
            ctypes.c_uint16
        ]
        self.kernels.svm_predict.restype = ctypes.c_double

        # converting the numpy arrays to ctypes pointers
        weights_ctypes = weights.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        inputs_ctypes = inputs.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

        # calling function
        result = self.kernels.svm_predict(weights_ctypes, inputs_ctypes, size)

        # return
        return result

    def threshold(self, value, low_bound, high_bound):
        
        # converting inputs into strongly typed values for the c function
        self.kernels.threshold.argtypes = [
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double
        ]
        self.kernels.threshold.restype = ctypes.c_bool

        # calling function
        result = self.kernels.threshold(value, low_bound, high_bound)

        return result
