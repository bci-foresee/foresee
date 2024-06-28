import ctypes
import numpy as np

# Load the shared library
libsvm = ctypes.CDLL('./libsvm.so')  # Change extension to .dll or .dylib as appropriate

# Define the argument and return types
libsvm.svm_predict.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_uint16), ctypes.c_uint16]
libsvm.svm_predict.restype = ctypes.c_double

# Create sample data
model = np.array([0.1, 0.2, 0.3, 0.4, 0.5], dtype=np.float64)
values = np.array([1, 2, 3, 4, 5], dtype=np.uint16)
size = len(model)

# Convert numpy arrays to ctypes pointers
model_ctypes = model.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
values_ctypes = values.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

# Call the function
result = libsvm.svm_predict(model_ctypes, values_ctypes, size)

print(f"Result: {result}")


#this works

