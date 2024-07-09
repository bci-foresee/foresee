from scipy.io import loadmat

# Load the .mat info file

info_file = '../data/ID01_info.mat'
patient_file = '../data/ID01_1h.mat'

data = loadmat(patient_file)

# Print the keys in the dictionary
print(data.keys())

# Inspect the variables
for key in data:
    if not key.startswith('__'):  # Skip internal metadata keys
        print("\n---------------------------------")
        print(f"Key: {key}")
        print(f"Type: {type(data[key])}")
        if hasattr(data[key], 'shape'):
            print(f"Shape: {data[key].shape}")
        else:
            print("Shape: N/A")
        print(f"Contents: {data[key]}")
        print("---------------------------------")
