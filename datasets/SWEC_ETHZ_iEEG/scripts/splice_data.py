import numpy as np
from scipy.io import loadmat

# Load the .mat info file

def splice_data(start_file, end_file, start_idx, end_idx):
    if start_file != end_file:
        print("---------start/end file mismatch. Look at splice_data.py---------")
    else:
        patient_file = '../data/ID01_'+str(int(start_file[0]))+'h.mat'
        data = loadmat(patient_file)
        
        # splice of data with a seizure present
        spliced_data = data['EEG'][:, int(start_idx):int(end_idx)]
        print(spliced_data.shape)

        # check dur
        print((end_idx-start_idx)/512)

        # save the array
        np.save('./test_save_data/test_save.npy',spliced_data)
        
        
# # Print the keys in the dictionary
# print(data.keys())

# # Inspect the variables
# for key in data:
#     if not key.startswith('__'):  # Skip internal metadata keys
#         print("\n---------------------------------")
#         print(f"Key: {key}")
#         print(f"Type: {type(data[key])}")
#         if hasattr(data[key], 'shape'):
#             print(f"Shape: {data[key].shape}")
#         else:
#             print("Shape: N/A")
#         print(f"Contents: {data[key]}")
#         print("---------------------------------")


