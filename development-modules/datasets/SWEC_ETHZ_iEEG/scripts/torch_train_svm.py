import torch
import torch.nn as nn
import torch.optim as optim

import plotly.graph_objects as go

import matplotlib.pyplot as plt

import os
import numpy as np

from python_PEs.fft import fft_py
from python_PEs.xcorr import xcorr_py
from python_PEs.bbf import bbf_py
from python_PEs.svm import svm_py
from python_PEs.thr import thr_py

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score

berger_bands = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]

# # ------------- loading in data -----------------

# # Directory containing the .npy files
# directory = './test_save_data'

# # List all files in the directory
# files = [f for f in os.listdir(directory) if f.endswith('.npy')]

# # Sort files alphabetically
# files.sort()

# ieeg_signals = []
# ieeg_signals_labels = []

# # Load each file
# prev_file_sign = ""
# prev_label_data = None

# for file in files:
#     file_path = os.path.join(directory, file)

#     file_parts = file.split('_')
#     current_file_sign = file_parts[
#         2]  # whether it is negative or positive labelled
#     current_file_type = file_parts[3]  # whether it is a signal or label

#     data = np.load(file_path)

#     if current_file_type == "signals.npy":
#         # print("hmmsmdsmda")
#         if current_file_sign == prev_file_sign:
#             print("\nadding data: ")
#             print(file)

#             # add every array item individually
#             for i in range(len(data)):
#                 ieeg_signals.append(data[i].tolist())
#                 ieeg_signals_labels.append(prev_label_data[i].tolist())

#     elif current_file_type == "labels.npy":
#         prev_label_data = data

#     prev_file_sign = current_file_sign

# # ieeg_signals = np.array(ieeg_signals).astype(np.float32)
# # ieeg_signals_labels = np.array(ieeg_signals_labels).astype(np.int64)
# print()
# print(
#     "shape of (ieeg_signals: items, channels, signals), (ieeg_signals_labels):"
# )
# print(len(ieeg_signals), len(ieeg_signals[0]), len(ieeg_signals[0][0]),
#       len(ieeg_signals_labels), "\n")

#- - - - - - - - - - - - - - - - - - - - - - - - - -

#--------------------- training --------------------

# Generate synthetic data
# Assuming each feature array has 96+96+120 = 312 features
# n_samples = len(ieeg_signals)
# n_channels = len(ieeg_signals[0])
n_features = 96 + 96 + 120
n_classes = 1

# x_tensor_list = []

# for i in range(len(ieeg_signals)):

#     print(f"feature gen iteration {i}")

#     # pre computing features for faster training
#     fft_power_features = fft_py(sampled_signals=ieeg_signals[i],
#                                   sample_freq=512,
#                                   berger_bands=berger_bands,
#                                   saveGraphs=False)

#     fft_power_features = np.array(fft_power_features).flatten()

#     bbf_power_features = bbf_py(sampled_signals=ieeg_signals[i],
#                              sample_freq=512,
#                              berger_bands=berger_bands,
#                              saveGraphs=False)

#     bbf_power_features = np.array(bbf_power_features).flatten()

#     xcorr_features = xcorr_py(sampled_signals=ieeg_signals[i],
#                               num_channels=n_channels,
#                               saveGraphs=False)

#     xcorr_features = np.array(xcorr_features).flatten()

#     concatenated_features = np.concatenate((fft_power_features, bbf_power_features, xcorr_features))

#     x_tensor_list.append(torch.tensor(concatenated_features))

# X = torch.stack(x_tensor_list)
# y = torch.tensor(ieeg_signals_labels)

# torch.save(X, "in_feature_gen_tensor.pt")
# torch.save(y, "in_label_tensor.pt")
# Load the tensors from disk

# Load tensors directly
X = torch.load('./model_data/in_feature_gen_tensor.pt')
y = torch.load('./model_data/in_label_tensor.pt')

# Convert labels to {-1, 1}
y = y * 2 - 1

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# # Define the SVM model
# class SVM(nn.Module):
#     def __init__(self, n_features):
#         super(SVM, self).__init__()
#         self.linear = nn.Linear(n_features, 1)

#     def forward(self, x):
#         return self.linear(x)

# def hinge_loss(output, target):
#     return torch.mean(torch.clamp(1 - output * target, min=0))

model = SVC(kernel='linear')
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix: \n", cm)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: ", accuracy)

# # Extract weights
# weights = model.coef_
# intercept = model.intercept_

# # Print the weights and intercept
# print("Weights:", weights)
# print("Intercept:", intercept)

# with torch.no_grad():
#     outputs = model(X_train).squeeze()
#     predictions = outputs > 0
#     accuracy = (predictions == y_train).float().mean()
#     print(f'Test Accuracy: {accuracy.item():.4f}')
