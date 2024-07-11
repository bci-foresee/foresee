from scipy.io import loadmat

# Load the .mat info file

info_file = '../data_info/ID01_info.mat'
patient_file = '../data/ID01_2h.mat'

data = loadmat(info_file)

# Print the keys in the dictionary
print(data.keys())

# Inspect the variables
for key in data:
    # if not key.startswith('__'):  # Skip internal metadata keys
    print("\n---------------------------------")
    print(f"Key: {key}")
    print(f"Type: {type(data[key])}")
    if hasattr(data[key], 'shape'):
        print(f"Shape: {data[key].shape}")
    else:
        print("Shape: N/A")
    print(f"Contents: {data[key]}")
    print("---------------------------------")


'''
---------------------------------
Key: seizure_end
Type: <class 'numpy.ndarray'>
Shape: (2, 1)
Contents: [[ 432976.20269531]
 [1030274.18042969]]
---------------------------------

---------------------------------
Key: fs
Type: <class 'numpy.ndarray'>
Shape: (1, 1)
Contents: [[512]]
---------------------------------

---------------------------------
Key: seizure_begin
Type: <class 'numpy.ndarray'>
Shape: (2, 1)
Contents: [[ 432362.43824219]
 [1029684.37003906]]
---------------------------------
'''