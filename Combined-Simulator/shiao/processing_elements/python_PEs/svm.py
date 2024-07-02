import numpy as np

def svm_py(features, weights, bias):
    # dot product of features and weights
    wx = np.dot(features, weights)
    # add bias
    wxb = wx + bias
    return wxb