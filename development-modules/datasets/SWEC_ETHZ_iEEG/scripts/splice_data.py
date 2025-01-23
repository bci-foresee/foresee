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
    for patient_id, patient_data in patient_dict.items():
        print(f"Splicing seizure data from patient {patient_id}")
        num_seizures = len(patient_data.seizure_begin)

        for seizure_index in range(num_seizures):
            start_file = int(patient_data.seizure_start_files[seizure_index])
            end_file = int(patient_data.seizure_end_files[seizure_index])
            start_idx = int(patient_data.seizure_start_indicies[seizure_index])
            end_idx = int(patient_data.seizure_end_indicies[seizure_index])

            save_seizure_splices(start_file, end_file, start_idx, end_idx,
                                 patient_id, seizure_index,
                                 patient_data.offset_beg,
                                 patient_data.offset_end,
                                 patient_data.sample_rate)


def download_and_load_mat(url):
    """
    Download a .mat file from the given URL with a progress bar and load it into memory.
    """
    with requests.get(url, stream=True) as response:
        print(f'Downloading {url}')
        response.raise_for_status()

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB',
                            unit_scale=True)

        data_to_load = BytesIO()
        for data in response.iter_content(chunk_size=1024):
            progress_bar.update(len(data))
            data_to_load.write(data)

        progress_bar.close()
        data_to_load.seek(0)

        return loadmat(data_to_load)

def save_seizure_splices(start_file, end_file, start_idx, end_idx,
                        patient_id, seizure_id, offset_beg, offset_end, sample_rate):
    '''
    Splice seizure into 20s windows and save corresponding EEG data and labels
    '''
    base_url = 'http://ieeg-swez.ethz.ch/long-term_dataset/ID{}/ID{}_{}h.mat'
    spliced_data = []

    # get EEG data from seizure bounds
    for file_number in range(start_file, end_file + 1):
        file_url = base_url.format(patient_id, patient_id, file_number)
        mat_data = download_and_load_mat(
            file_url)  # Using the new download function
        data = mat_data[
            'EEG'][:
                   16]  # Assuming EEG data is under key 'EEG' and taking first 16 channels

        if file_number == start_file:
            data = data[:, start_idx:]
        if file_number == end_file:
            data = data[:, :end_idx + 1]

        spliced_data.append(data)

    # concatenate data if multi files spanned
    spliced_data = np.concatenate(spliced_data, axis=1) if len(spliced_data) > 1 else spliced_data[0]

    # create labels at sample level indicating seizure
    pre_seizure_samples = int(-offset_beg * sample_rate)
    post_seizure_samples = int(offset_end * sample_rate)
    seizure_samples = spliced_data.shape[1] - pre_seizure_samples - post_seizure_samples
    labels = np.concatenate([np.zeros(pre_seizure_samples),
                             np.ones(seizure_samples),
                             np.zeros(post_seizure_samples)]).astype(int)

    # generate overlapping slices and label them
    window_size = 20 * sample_rate  # 20 second splice window
    step_size = 10 * sample_rate  # 10 seconds overlap
    slices, slice_labels = [], []
    nonseizure_splices_remaining = 0 # used in save_nonseizure_splices() to balance dataset

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
    np.save(save_path + '_positive_signals.npy', np.array(slices))
    np.save(save_path + '_positive_labels.npy', np.array(slice_labels))

    return 


def splice_nonseizure_data(patient_dict, target_slices_count):
    """
    Generate non-seizure EEG data slices
    """
    print('Splicing nonseizure data')
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
    usable_urls = [url for url in urls if url not in omit_urls]
    

    # slice random nonseizure files until we reach target
    sample_length = 600 # 600 s samples
    offset = 30 # 30 s sample offset
    slice_count = 0

    while slice_count < target_slices_count:
        random_url = np.random.choice(usable_urls)
        print("sampled file: " + str(random_url))

        parts = random_url.split('/')  # Split the URL into parts
        id_part = parts[-2]     # Get the second last part which includes the patient ID
        patient_id = id_part[2:]  # Extract the numeric part of the ID (skip the 'ID')
        hour_part = parts[-1]  # Get the last part which includes the hour information
        hour = hour_part.split('_')[1].replace('.mat', '')  # Extract the hour and remove file extension
        sample_rate = patient_dict[patient_id].sample_rate

        mat_data = download_and_load_mat(random_url)  # Using the new download function
        spliced_data = mat_data['EEG'][:16, int(offset * sample_rate):int(sample_length * sample_rate)]

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
            

            #print(slice.shape)
            slices.append(slice)
            slices_labels.append(most_common_value)
        
        # Convert the list of slices to a numpy array
        slices_array = np.array(slices)
        slices_labels_array = np.array(slices_labels)

        # save slices and labels
        save_path = './seizure_data/ID{}_{}'.format(patient_id, hour)
        np.save(save_path + '_negative_signals.npy', np.array(slices))
        np.save(save_path + '_negative_labels.npy', np.array(slices_labels))

        slice_count += len(slices)



# # this function and the following helper functions generate non-seizure slices of ieeg data
# def splice_nonseizure_data(patient_id, patient_dict, samples_to_generate=5):
#     # find out which files not to take data from:

#     omit_files = set()  # set of files to not take nonseizure data from

#     for i in range(len(patient_dict[patient_id].seizure_start_files)):

#         start_file = int(patient_dict[patient_id].seizure_start_files[i][0])
#         end_file = int(patient_dict[patient_id].seizure_end_files[i][0])

#         correlated_zone_size = 3  # how many files to leave to have no correlation

#         for j in range(start_file - correlated_zone_size,
#                        end_file + correlated_zone_size):
#             omit_files.add(j)

#     # sort omit_files
#     # omit_files = sorted(omit_files)
#     # print(omit_files)

#     #finding upper limit of file indexes we can sample from:
#     directory = '../data'

#     numbers = set()
#     # Iterate over all files in the directory
#     for filename in os.listdir(directory):
#         if filename.endswith('.mat'):
#             file_path = os.path.join(directory, filename)
#             # print(filename)
#             pattern = re.compile(r'_(\d+)h')

#             numbers.add(int(pattern.search(filename).group(1)))

#     #finding intersection of files to sample from non-seizure files

#     sampleable_files = np.array([x for x in numbers if x not in omit_files])
#     # print(sampleable_files)

#     sample_length = 600  #seconds
#     sample_rate = 512  #Hz
#     sample_idx_len = sample_length * sample_rate

#     offset = 30  #seconds
#     offset_idx = offset * sample_rate
#     sample_idx_len = sample_idx_len + offset_idx

#     for i in range(samples_to_generate):

#         # choose random file to sample from
#         random_file = np.random.choice(sampleable_files)
#         print("sampled_file: " + str(random_file))

#         # open the chosen random
#         patient_file = '../data/ID01_' + str(i + 1) + 'h.mat'
#         data = loadmat(patient_file)

#         # splice of data with no seizure present
#         spliced_data = data['EEG'][:16, int(offset_idx):int(sample_idx_len)]

#         # print(spliced_data.shape)

#         # labels of all 0s
#         label_size = len(spliced_data[0])

#         label_arr = np.zeros(label_size).astype(np.int64)
#         # print(label_arr.shape)

#         # Parameters for slicing
#         slice_size = 20 * 512  # 20s * 512 Hz (num indexes)
#         step_size = 10 * 512  # 10s * 512 Hz (how much shift between slices)

#         # List to store the slices
#         slices = []
#         slices_labels = []

#         # Loop to create overlapping slices
#         for start_index in range(0,
#                                  len(spliced_data[0]) - slice_size + 1,
#                                  step_size):
#             end_index = start_index + slice_size

#             # one 20s slice of data
#             slice = spliced_data[:, start_index:end_index]

#             # is it a seizure or not
#             counts = np.bincount(
#                 label_arr[start_index:end_index])  # how many ones or zeros
#             most_common_value = np.argmax(
#                 counts
#             )  # take most common occurence as an indicator of seizure or not
            

#             #print(slice.shape)
#             slices.append(slice)
#             slices_labels.append(most_common_value)

#         # Convert the list of slices to a numpy array
#         slices_array = np.array(slices)
#         slices_labels_array = np.array(slices_labels)

#         print("slices shape nonseizure:")
#         print(slices_array.shape)
#         print(slices_array[0].shape)
#         print(slices_labels_array.shape)

#         #save labels
#         # format:
#         # 93 items each corresponding to a label in ieeg_signals.npy
#         np.save(
#             './test_save_data/ID' + patient_id + '_' + str(i) +
#             '_negative_labels.npy', slices_labels_array)

#         #save the ieeg data
#         # format:
#         # 93 rows each of a 20s ieeg input with a corresponding label
#         np.save(
#             './test_save_data/ID' + patient_id + '_' + str(i) +
#             '_negative_signals.npy', slices_array)
