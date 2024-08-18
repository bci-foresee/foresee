import numpy as np

'''
##################################

This module performs the SVM operation on the input features and weights.

output = weights * features + bias

# Inputs
- features [np.array::float]            list of features (output from fft, bbf, xcorr)
- weights [np.array::float]             list of weights
- bias [float]                          bias value

# Outputs
- wxb [float]                          output of the SVM operation

##################################
'''

def svm_py(features, weights, bias):
    # dot product of features and weights
    wx = np.dot(features, weights)
    # add bias
    wxb = wx + bias
    return wxb