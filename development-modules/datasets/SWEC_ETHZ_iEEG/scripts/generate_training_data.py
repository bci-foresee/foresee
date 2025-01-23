from indicies_gen import create_seizure_indices
from splice_data import splice_seizure_data, splice_nonseizure_data
import numpy as np
from multiprocessing import Process

def process_data(patient_dict, key_subset):
    """
    Process data for a subset of patient keys for seizure data and the full dictionary for non-seizure data.
    """
    # Create a subdictionary for the specific process to handle seizure data
    patient_subdict = {key: patient_dict[key] for key in key_subset}
    nonseizure_splices_remaining = splice_seizure_data(patient_subdict)
    # Use the full patient_dict for non-seizure data processing
    splice_nonseizure_data(patient_dict, nonseizure_splices_remaining)

def main():
    """
    Main function to create patient indices, split keys among processes,
    and manage the multiprocessing setup.
    """
    patient_dict = create_seizure_indices(offset_beg=-180, offset_end=180)

    # Split patient keys into four groups
    patient_keys = list(patient_dict.keys())
    n = len(patient_keys) // 4
    key_subsets = [patient_keys[i:i + n] for i in range(0, len(patient_keys), n)]

    # Create a process for each group of keys
    processes = []
    for key_subset in key_subsets:
        p = Process(target=process_data, args=(patient_dict, key_subset))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("Training data ready-----")

if __name__ == "__main__":
    main()
