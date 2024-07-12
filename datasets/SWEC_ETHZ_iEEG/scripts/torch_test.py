import torch
import torch.nn as nn
import torch.optim as optim

import os
import numpy as np

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
prev_file_type = ""
for file in files:
    file_path = os.path.join(directory, file)

    
    file_parts = file.split('_')
    current_file_type = file_parts[2]
    print(file, current_file_type)
    
    data = np.load(file_path)

    
    # data_list.append(data)
    print(f"Loaded {file}")
    print(f"shape {data.shape}")

#- - - - - - - - - - - - - - - - - - - - - - - - - - 


# Generate synthetic data
# Assuming each feature array has 96+96+120 = 312 features
n_samples = 1000
n_features = 312
n_classes = 2

# Create random data and labels
X = torch.randn(n_samples, n_features)
y = torch.randint(0, n_classes, (n_samples,))

print(X.shape)
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
