import ctypes
import numpy as np
import os

class PE_algorithms:
    def __init__(self, PE_library):
        # setting up the shared object library
        # this allows for the use of functions written in c/c++
        self.PE_library = ctypes.CDLL(os.path.abspath(PE_library))
        

    def svm_predict(self, weights, inputs, size):
        # defining the argument types that the function takes
        self.PE_library.svm_predict.argtypes = [ctypes.POINTER(ctypes.c_double), 
                                                ctypes.POINTER(ctypes.c_uint16), 
                                                ctypes.c_uint16]
        # defining the return type of the function
        self.PE_library.svm_predict.restype = ctypes.c_double

        # converting the numpy arrays to ctypes pointers
        weights_ctypes = weights.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        inputs_ctypes = inputs.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

        # calling the function
        result = self.PE_library.svm_predict(weights_ctypes, inputs_ctypes, size)

        # returning result
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

