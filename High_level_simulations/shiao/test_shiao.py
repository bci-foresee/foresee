import os
import ctypes
import numpy as np
from pipeline import Pipeline

pipeline = Pipeline(kernel_lib='libkernels.so')

# SVM
model = np.array([0.1, 0.2, 0.3, 0.4, 0.5], dtype=np.float64)
values = np.array([1, 2, 3, 4, 5], dtype=np.uint16)
size = len(values)

result = pipeline.svm_predict(model, values, size)
assert result == np.dot(model, values)

# XCORR
inputs = np.array([
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 6],
    [1, 2, 3, 4, 7],
], dtype=np.uint16)
num_channels, num_samples = inputs.shape

result = pipeline.cross_correlation(inputs, num_channels, num_samples)

assert result == [
    np.dot(inputs[0], inputs[1]), 
    np.dot(inputs[0], inputs[2]), 
    np.dot(inputs[1], inputs[2]), 
]
