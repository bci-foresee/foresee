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
prev_file_sign = ""
prev_label_data = None

for file in files:
    print()
    file_path = os.path.join(directory, file)

    
    file_parts = file.split('_')
    current_file_sign = file_parts[2] # whether it is negative or positive labelled
    current_file_type = file_parts[3] # whether it is a signal or label
    # print(file, current_file_type)

    data = np.load(file_path)

    # print(current_file_sign, prev_file_sign)
    
    
    if current_file_type == "signals.npy":
        # print("hmmsmdsmda")
        if current_file_sign == prev_file_sign:
            print("\nadding data: ")
            print(file)

            # add every array item individually
            for i in range(len(data)):
                ieeg_signals.append(data[i])
                ieeg_signals_labels.append(prev_label_data[i])


    elif current_file_type == "labels.npy":
        prev_label_data = data

    prev_file_sign = current_file_sign
    
    
    # data_list.append(data)
    # print(f"Loaded {file}")
    # print(f"shape {data.shape}")

# print(ieeg_signals.shape)
print(ieeg_signals)
print(len(ieeg_signals), len(ieeg_signals_labels))

# ieeg_signals_arr = np.array(ieeg_signals)
# ieeg_signals_labels_arr = np.array(ieeg_signals_labels)

# print(ieeg_signals.shape)
# print(ieeg_signals_labels.shape)

#- - - - - - - - - - - - - - - - - - - - - - - - - - 