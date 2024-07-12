import torch
import torch.nn as nn
import torch.optim as optim

import os
import numpy as np

from python_PEs.fft import fft_py
from python_PEs.xcorr import xcorr_py
from python_PEs.bbf import bbf_py
from python_PEs.svm import svm_py
from python_PEs.thr import thr_py

berger_bands = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]

# ------------- loading in data -----------------

# Directory containing the .npy files
directory = './test_save_data'

# List all files in the directory
files = [f for f in os.listdir(directory) if f.endswith('.npy')]

# Sort files alphabetically
files.sort()

ieeg_signals = []
ieeg_signals_labels = []

# Load each file
prev_file_sign = ""
prev_label_data = None

for file in files:
    file_path = os.path.join(directory, file)

    
    file_parts = file.split('_')
    current_file_sign = file_parts[2] # whether it is negative or positive labelled
    current_file_type = file_parts[3] # whether it is a signal or label

    data = np.load(file_path)

    
    if current_file_type == "signals.npy":
        # print("hmmsmdsmda")
        if current_file_sign == prev_file_sign:
            print("\nadding data: ")
            print(file)

            # add every array item individually
            for i in range(len(data)):
                ieeg_signals.append(data[i].tolist())
                ieeg_signals_labels.append(prev_label_data[i].tolist())


    elif current_file_type == "labels.npy":
        prev_label_data = data

    prev_file_sign = current_file_sign

# ieeg_signals = np.array(ieeg_signals).astype(np.float32)
# ieeg_signals_labels = np.array(ieeg_signals_labels).astype(np.int64)
print()
print("shape of (ieeg_signals: items, channels, signals), (ieeg_signals_labels):")
print(len(ieeg_signals), len(ieeg_signals[0]), len(ieeg_signals[0][0]), len(ieeg_signals_labels), "\n")

#- - - - - - - - - - - - - - - - - - - - - - - - - - 

#--------------------- training --------------------

# Generate synthetic data
# Assuming each feature array has 96+96+120 = 312 features
n_samples = len(ieeg_signals)
n_features = 96
n_classes = 1

# Create random data and labels

# X = torch.randn(n_samples, n_features)
# y = torch.randint(0, n_classes, (n_samples,))

x_tensor_list = []

for i in range(len(ieeg_signals)):

    # pre computing features for faster training
    fft_power_features = fft_py(sampled_signals=ieeg_signals[i], 
                                  sample_freq=512,
                                  berger_bands=berger_bands,
                                  saveGraphs=False)

    fft_power_features = np.array(fft_power_features).flatten()
    
    x_tensor_list.append(torch.tensor(fft_power_features))

X = torch.stack(x_tensor_list)
y = torch.tensor(ieeg_signals_labels)

print("\nSize of tensors:")
# print(ieeg_signals.shape)
print(X.shape)
# print(ieeg_signals_labels.shape)
print(y.shape)

# Convert labels to {-1, 1}
y = y * 2 - 1

# Define the custom SVM model
class SVM(nn.Module):
    def __init__(self, n_features):
        super(SVM, self).__init__()
        self.linear = nn.Linear(n_features, 1)
    
    def forward(self, x):
        return self.linear(x)

# Define hinge loss function
def hinge_loss(output, target):
    return torch.mean(torch.clamp(1 - output * target, min=0))

# Instantiate the model, define the optimizer
model = SVM(n_features)
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training loop
n_epochs = 100
for epoch in range(n_epochs):
    model.train()
    optimizer.zero_grad()
    
    # Forward pass
    outputs = model(X).squeeze()
    
    # Compute the loss
    loss = hinge_loss(outputs, y.float())
    
    # Backward pass and optimization
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{n_epochs}], Loss: {loss.item():.4f}')

print("Training completed.")
