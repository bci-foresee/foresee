import pickle
import numpy as np
import os
# from joblib import Parallel, delayed
import torch
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

from neo_PEs.neo_helper import tkeo_py, avg_py

# Directory and settings
directory = './seizure_data'
berger_bands = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]
sample_rate = 512
feature_file = "./model_data/neo_feature_tensor.pt"
label_file = "./model_data/neo_label_tensor.pt"


# Function to generate features for each signal
def generate_features(signal):
    # pre computing features for faster training
    tkeo_power_features = tkeo_py(input=signal)
    tkeo_power_features = np.array(tkeo_power_features).flatten()
    print('tkeo', tkeo_power_features.shape)

    avg_power_features = avg_py(input=signal)
    avg_power_features = np.array(avg_power_features).flatten()
    print('avg', tkeo_power_features.shape)

    concatenated_features = np.concatenate((tkeo_power_features, avg_power_features))
    return concatenated_features


# Function to append tensors to a file
def append_tensor_to_file(tensor, file_path):
    try:
        existing_tensor = torch.load(file_path)
        updated_tensor = torch.cat((existing_tensor, tensor))
    except FileNotFoundError:
        updated_tensor = tensor
    torch.save(updated_tensor, file_path)

# Process data and save immediately after each pair
def process_and_save_data(file_map, directory):
    count = 1
    for key, files in file_map.items():
        if "signals" in files and "labels" in files:
            print(f'File {count}: {files['labels']}')
            count += 1
            signals_path = os.path.join(directory, files['signals'])
            labels_path = os.path.join(directory, files['labels'])

            signals_data = np.load(signals_path, mmap_mode='r')
            labels_data = np.load(labels_path, mmap_mode='r')
            print('channels', len(signals_data[0]))

            # Process each signal and corresponding label
            for signal, label in zip(signals_data, labels_data):
                features = generate_features(signal)
                feature_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)  # Ensure it is 2D for concatenation
                print(feature_tensor.size())
                label_tensor = torch.tensor([label], dtype=torch.int64)  # Ensure it is 1D for concatenation

                # Append to files
                append_tensor_to_file(feature_tensor, feature_file)
                append_tensor_to_file(label_tensor, label_file)

# Set up file map
file_map = {}
for f in os.listdir(directory):
    if f.endswith('.npy'):
        parts = f.split('_')
        key = '_'.join(parts[:-1])
        file_type = parts[-1][:-4]
        if key not in file_map:
            file_map[key] = {}
        file_map[key][file_type] = f

# Call the function to process data
process_and_save_data(file_map, directory)

# run prior code first to save feature files; then run the following to train the model

# # Load tensors directly
# X = torch.load('./model_data/neo_feature_tensor.pt')
# y = torch.load('./model_data/neo_label_tensor.pt')

# # if not torch.isfinite(X).all():
# #     print("Data contains NaN, infinity or values too large for dtype('float64').")
# #     # Replace inf values with a large finite number and NaNs with zero or mean/median value
# #     X[torch.isinf(X)] = torch.finfo(X.dtype).max  # Replace inf with the largest finite number possible
# #     X[torch.isnan(X)] = 0  # or you can choose to fill with the mean/median of your dataset depending on your context

# # Convert labels to {-1, 1}
# y = y * 2 - 1

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X.numpy(), y.numpy(), test_size=0.20, random_state=42)

# # Training the model
# model = SVC(kernel='linear')
# model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# cm = confusion_matrix(y_test, y_pred)
# accuracy = accuracy_score(y_test, y_pred)

# print("Confusion matrix: \n", cm)
# print("Accuracy: ", accuracy)

# # Save the model
# filename = './model_data/neo_svm_model.pkl'
# with open(filename, 'wb') as file:
#     pickle.dump(model, file)

# print("Model saved to", filename)
