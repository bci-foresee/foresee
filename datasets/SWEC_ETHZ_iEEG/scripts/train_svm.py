import os
import numpy as np

# Directory containing the .npy files
directory = './test_save_data'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.npy'):
        file_path = os.path.join(directory, filename)
        # Load the array from the .npy file
        loaded_array = np.load(file_path)
        # Append the loaded array to the list
        # arrays.append(loaded_array)
        # Print the array and its shape
        print(f"\n\nLoaded array from {filename}:")
        # print(loaded_array)
        print("Shape of the loaded array:", loaded_array.shape)

# Optionally convert the list of arrays to a NumPy array (if they have the same shape)
# combined_array = np.array(arrays)
