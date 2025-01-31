import random
from indicies_gen import create_seizure_indices
from splice_data import splice_seizure_data, splice_nonseizure_data
import numpy as np
from multiprocessing import Process, Queue


def process_data(patient_dict, key_subset, shared_queue):
    """
    Process data for a subset of patient keys for seizure data and the full dictionary for non-seizure data.
    """
    # Create a subdictionary for the specific process to handle seizure data
    patient_subdict = {key: patient_dict[key] for key in key_subset}
    nonseizure_splices_remaining = splice_seizure_data(patient_subdict)
    # Use the full patient_dict for non-seizure data processing
    splice_nonseizure_data(patient_dict, nonseizure_splices_remaining,
                           shared_queue)


def create_shared_queue(patient_dict):
    shared_queue = Queue()

    # determine which files not to pool from
    omit_urls = set()
    for patient_id, patient_data in patient_dict.items():
        for i in range(len(patient_data.seizure_start_files)):
            start_file = int(patient_data.seizure_start_files[i])
            end_file = int(patient_data.seizure_end_files[i])
            for f in range(start_file, end_file + 1):
                # print(patient_id, f)
                url = f'http://ieeg-swez.ethz.ch/long-term_dataset/ID{patient_id}/ID{patient_id}_{f}h.mat'
                omit_urls.add(url)

    # get poolable files
    all_data_urls = '../data_urls/all_data.txt'
    with open(all_data_urls, 'r') as f:
        urls = [line.strip() for line in f.readlines()]
        random.shuffle(urls)

    for url in urls:
        parts = url.split('/')
        patient_id = parts[-2][2:]
        if url not in omit_urls and patient_id in patient_dict.keys():
            shared_queue.put(url)

    return shared_queue


def main():
    """
    Main function to create patient indices, split keys among processes,
    and manage the multiprocessing setup.
    """
    patient_dict = create_seizure_indices(offset_beg=-180, offset_end=180)

    # Split patient keys into four groups
    patient_keys = list(patient_dict.keys())
    n = len(patient_keys) // 4
    key_subsets = [
        patient_keys[i:i + n] for i in range(0, len(patient_keys), n)
    ]

    # create shared queue of poolable files for nonseizure splices
    shared_queue = create_shared_queue(patient_dict)

    # Create a process for each group of keys
    processes = []
    for key_subset in key_subsets:
        p = Process(target=process_data,
                    args=(patient_dict, key_subset, shared_queue))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # empty queue
    while not shared_queue.empty():
        shared_queue.get()

    print("Training data ready-----")


if __name__ == "__main__":
    main()
