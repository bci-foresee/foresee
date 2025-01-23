from io import BytesIO
import os
import re
import numpy as np
import requests
from scipy.io import loadmat
from tqdm import tqdm


def splice_seizure_data(patient_dict):
    '''
    Iterates through each seizure and saves EEG data splices and labels
    '''
    nonseizure_splices_remaining = 0

    for patient_id, patient_data in patient_dict.items():
        print(f"Splicing seizure data from patient {patient_id}")
        num_seizures = len(patient_data.seizure_begin)

        for seizure_index in range(num_seizures):
            start_file = int(patient_data.seizure_start_files[seizure_index])
            end_file = int(patient_data.seizure_end_files[seizure_index])
            start_idx = int(patient_data.seizure_start_indicies[seizure_index])
            end_idx = int(patient_data.seizure_end_indicies[seizure_index])

            nonseizure_splices_remaining += save_seizure_splices(
                start_file, end_file, start_idx, end_idx, patient_id,
                seizure_index, patient_data.offset_beg,
                patient_data.offset_end, patient_data.sample_rate)

        print(f"Done splicing seizure data from patient {patient_id}")

    return nonseizure_splices_remaining


def download_and_load_mat(url, patient_id):
    """
    Downloads file from dataset.
    """
    print(f'Patient {patient_id}: Starting download {url}')
    with requests.get(url, stream=True) as response:
        response.raise_for_status()

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        data_to_load = BytesIO()
        downloaded = 0

        for data in response.iter_content(chunk_size=1024):
            downloaded += len(data)
            data_to_load.write(data)

        print(
            f'Patient {patient_id}: Completed download {url} [{downloaded} bytes]'
        )

        data_to_load.seek(0)
        return loadmat(data_to_load)


def save_seizure_splices(start_file, end_file, start_idx, end_idx, patient_id,
                         seizure_id, offset_beg, offset_end, sample_rate):
    '''
    Splice seizure into 20s windows and save corresponding EEG data and labels
    '''
    base_url = 'http://ieeg-swez.ethz.ch/long-term_dataset/ID{}/ID{}_{}h.mat'
    spliced_data = []

    # get EEG data from seizure bounds
    for file_number in range(start_file, end_file + 1):
        file_url = base_url.format(patient_id, patient_id, file_number)
        mat_data = download_and_load_mat(
            file_url, patient_id)  # Using the new download function
        data = mat_data[
            'EEG'][:
                   16]  # Assuming EEG data is under key 'EEG' and taking first 16 channels

        if file_number == start_file:
            data = data[:, start_idx:]
        if file_number == end_file:
            data = data[:, :end_idx + 1]

        spliced_data.append(data)

    # concatenate data if multi files spanned
    spliced_data = np.concatenate(
        spliced_data, axis=1) if len(spliced_data) > 1 else spliced_data[0]

    # create labels at sample level indicating seizure
    pre_seizure_samples = int(-offset_beg * sample_rate)
    post_seizure_samples = int(offset_end * sample_rate)
    seizure_samples = spliced_data.shape[
        1] - pre_seizure_samples - post_seizure_samples
    labels = np.concatenate([
        np.zeros(pre_seizure_samples),
        np.ones(seizure_samples),
        np.zeros(post_seizure_samples)
    ]).astype(int)

    # generate overlapping slices and label them
    window_size = 20 * sample_rate  # 20 second splice window
    step_size = 10 * sample_rate  # 10 seconds overlap
    slices, slice_labels = [], []
    nonseizure_splices_remaining = 0  # used in save_nonseizure_splices() to balance dataset

    for start in range(0, spliced_data.shape[1] - window_size + 1, step_size):
        end = start + window_size
        slice = spliced_data[:, start:end]
        label = np.argmax(
            np.bincount(labels[start:end])
        )  # Label for the slice is the most common label in this window

        slices.append(slice)
        slice_labels.append(label)
        nonseizure_splices_remaining += 1 if label == 1 else -1

    # save slices and labels
    save_path = './seizure_data/ID{}_{}'.format(patient_id, seizure_id)
    slices_path = save_path + '_positive_signals.npy'
    labels_path = save_path + '_positive_labels.npy'

    np.save(slices_path, np.array(slices))
    print(f'Patient {patient_id}: saved {slices_path}')
    np.save(labels_path, np.array(slice_labels))
    print(f'Patient {patient_id}: saved {labels_path}')

    return nonseizure_splices_remaining


def splice_nonseizure_data(patient_dict, target_slices_count, shared_queue):
    """
    Generate non-seizure EEG data slices
    """
    print('Splicing nonseizure data')

    # slice random nonseizure files until we reach target
    sample_length = 600  # 600 s samples
    offset = 30  # 30 s sample offset
    slice_count = 0

    while slice_count < target_slices_count:
        random_url = shared_queue.pop()
        print("sampled file: " + str(random_url))

        parts = random_url.split('/')  # Split the URL into parts
        id_part = parts[
            -2]  # Get the second last part which includes the patient ID
        patient_id = id_part[
            2:]  # Extract the numeric part of the ID (skip the 'ID')
        hour_part = parts[
            -1]  # Get the last part which includes the hour information
        hour = hour_part.split('_')[1].replace(
            '.mat', '')  # Extract the hour and remove file extension
        sample_rate = patient_dict[patient_id].sample_rate

        mat_data = download_and_load_mat(
            random_url, patient_id)  # Using the new download function
        spliced_data = mat_data['EEG'][:16,
                                       int(offset *
                                           sample_rate):int(sample_length *
                                                            sample_rate)]

        # labels of all 0s
        label_size = len(spliced_data[0])
        label_arr = np.zeros(label_size).astype(np.int64)

        # parameters for slicing
        slice_size = 20 * sample_rate  # 20s windows
        step_size = 10 * sample_rate  # 10s overalaps

        # lists to store slices and labels
        slices = []
        slices_labels = []

        # slice the sample
        for start_index in range(0,
                                 len(spliced_data[0]) - slice_size + 1,
                                 step_size):
            end_index = start_index + slice_size

            # one 20s slice of data
            slice = spliced_data[:, start_index:end_index]

            # is it a seizure or not
            counts = np.bincount(
                label_arr[start_index:end_index])  # how many ones or zeros
            most_common_value = np.argmax(
                counts
            )  # take most common occurence as an indicator of seizure or not

            slices.append(slice)
            slices_labels.append(most_common_value)

        # save slices and labels
        save_path = './seizure_data/ID{}_{}'.format(patient_id, hour)
        slices_path = save_path + '_negative_signals.npy'
        labels_path = save_path + '_negative_labels.npy'

        np.save(slices_path, np.array(slices))
        print(f'Patient {patient_id}: saved {slices_path}')
        np.save(labels_path, np.array(slices_labels))
        print(f'Patient {patient_id}: saved {labels_path}')

        slice_count += len(slices)
