import h5py

# Open the .mat file
file_path = '../data/ID01_1h.mat'
with h5py.File(file_path, 'r') as f:
    # List all groups
    print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[0]

    # Get the data
    data = f[a_group_key]

    # Inspect the variables
    for key in f.keys():
        print("\n---------------------------------")
        print(f"Key: {key}")
        dataset = f[key]
        print(f"Type: {type(dataset)}")
        print(f"Shape: {dataset.shape}")
        # Load a chunk of data
        chunk = dataset[0:100]  # Load the first 100 entries
        print(f"Contents (first 100 entries): {chunk}")
        print("---------------------------------")
