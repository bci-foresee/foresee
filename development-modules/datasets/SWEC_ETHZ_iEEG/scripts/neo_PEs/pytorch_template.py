from neo_helper import tkeo_py, avg_py

import numpy as np
import torch

n_features = 16 # 16 input "channels", each has one TKEO operation and so one feature
n_classes = 1


ieeg_signals = np.load("ieeg_signals.npy") # idk how to load in inputs but that is done here
ieeg_signals_labels = np.load("ieeg_signals_labels.npy") # idk how to load in labels but that is done here

x_tensor_list = []

for i in range(len(ieeg_signals)):

    print(f"feature gen iteration {i}")

    # pre computing features for faster training
    tkeo_power_features = tkeo_py(input=ieeg_signals[i])
    tkeo_power_features = np.array(tkeo_power_features).flatten()

    avg_power_features = avg_py(input=ieeg_signals[i])
    avg_power_features = np.array(avg_power_features).flatten()

    concatenated_features = np.concatenate((tkeo_power_features, avg_power_features))

    x_tensor_list.append(torch.tensor(concatenated_features))



X = torch.stack(x_tensor_list)
y = torch.tensor(ieeg_signals_labels)

torch.save(X, "in_feature_gen_tensor.pt")
torch.save(y, "in_label_tensor.pt")