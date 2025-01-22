from io import BytesIO
import os
import numpy as np
import requests
from scipy.io import loadmat
from tqdm import tqdm


def splice_seizure_data(patient_dict):
    '''
    Iterates through each patient and each seizure, downloads the corresponding seizure files,
    extracts the seizure splice, and saves it.
    '''
    for patient_id, patient_data in patient_dict.items():
        print(f"Processing patient {patient_id} data")
        num_seizures = len(patient_data.seizure_begin)

        for seizure_index in range(num_seizures):
            start_file = int(patient_data.seizure_start_files[seizure_index])
            end_file = int(patient_data.seizure_end_files[seizure_index])
            start_idx = int(patient_data.seizure_start_indicies[seizure_index])
            end_idx = int(patient_data.seizure_end_indicies[seizure_index])

            save_seizure_splices(start_file, end_file, start_idx, end_idx,
                                patient_id, seizure_index, patient_data.offset_beg,
                                patient_data.offset_end, patient_data.sample_rate)


def download_and_load_mat(url):
    """
    Download a .mat file from the given URL with a progress bar and load it into memory.
    """
    with requests.get(url, stream=True) as response:
        print(f'Downloading {url}')
        response.raise_for_status() 

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        
        data_to_load = BytesIO()
        for data in response.iter_content(chunk_size=1024):
            progress_bar.update(len(data))
            data_to_load.write(data)
        
        progress_bar.close()
        data_to_load.seek(0)
        
        return loadmat(data_to_load)

def save_seizure_splices(start_file, end_file, start_idx, end_idx,
                        patient_id, seizure_id, offset_beg, offset_end, sample_rate):
    base_url = 'http://ieeg-swez.ethz.ch/long-term_dataset/ID{}/ID{}_{}h.mat'
    spliced_data = []

    # Load data across multiple files if needed
    for file_number in range(start_file, end_file + 1):
        file_url = base_url.format(patient_id, patient_id, file_number)
        mat_data = download_and_load_mat(file_url)  # Using the new download function
        data = mat_data['EEG'][:16]  # Assuming EEG data is under key 'EEG' and taking first 16 channels

        if file_number == start_file:
            data = data[:, start_idx:]
        if file_number == end_file:
            data = data[:, :end_idx + 1]

        spliced_data.append(data)

    # Concatenate data from potentially multiple files
    spliced_data = np.concatenate(spliced_data, axis=1) if len(spliced_data) > 1 else spliced_data[0]

    # Create labels indicating seizure presence
    pre_seizure_samples = int(-offset_beg)
    post_seizure_samples = int(offset_end)
    seizure_samples = spliced_data.shape[1] - pre_seizure_samples - post_seizure_samples
    labels = np.concatenate([np.zeros(pre_seizure_samples),
                             np.ones(seizure_samples),
                             np.zeros(post_seizure_samples)]).astype(int)

    # Generate overlapping slices
    window_size = 20 * sample_rate  # 20 second splice window
    step_size = 10 * sample_rate  # 10 seconds overlap
    slices, slice_labels = [], []

    for start in range(0, spliced_data.shape[1] - window_size + 1, step_size):
        end = start + window_size
        slice = spliced_data[:, start:end]
        label = np.argmax(np.bincount(labels[start:end]))  # Label for the slice is the most common label in this window

        slices.append(slice)
        slice_labels.append(label)

    # Save the slices and labels
    save_path = './seizure_data/ID{}_{}'.format(patient_id, seizure_id)
    np.save(save_path + '_signals.npy', np.array(slices))
    np.save(save_path + '_labels.npy', np.array(slice_labels))


# Example usage:
# Assuming patient_dict is defined and contains the necessary patient data
# splice_seizure_data(patient_dict)

# import numpy as np
# from scipy.io import loadmat
# import os
# import re

# def splice_seizure_data(patient_dict):
#     '''
#     Iterates through seizures in dataset and saves spliced EEG data
#     '''
#     patient_nums = [
#         '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
#         '13', '14', '15', '16', '17', '18'
#     ]

#     for patient_num in patient_nums:
#         patient_data = patient_dict[patient_num]
#         num_seizures = len(patient_data.seizure_start_files)

#         for i in range(num_seizures):
#             save_seizure_splice(start_file=patient_data.seizure_start_files[i],
#                             end_file=patient_data.seizure_end_files[i],
#                             start_idx=patient_data.seizure_start_indicies[i],
#                             end_idx=patient_data.seizure_end_indicies[i],
#                             patient_id=patient_num,
#                             seizure_id=i,
#                             offset_beg=patient_data.offset_beg,
#                             offset_end=patient_data.offset_end)

# def save_seizure_splice(start_file, end_file, start_idx, end_idx, seizure_id,
#                         patient_id, offset_beg, offset_end):
#     if start_file != end_file:
#         #start data
#         patient_file = '../data/ID01_' + str(int(start_file[0])) + 'h.mat'
#         data = loadmat(patient_file)
#         spliced_data_start = data['EEG'][:16, int(start_idx):]

#         #end data
#         patient_file = '../data/ID01_' + str(int(end_file[0])) + 'h.mat'
#         data = loadmat(patient_file)
#         spliced_data_end = data['EEG'][:16, :int(end_idx)]

#         spliced_data = np.concatenate((spliced_data_start, spliced_data_end),
#                                       axis=1)

#         #labels
#         splice_size = len(spliced_data[0])

#         label_arr_1 = np.zeros(-offset_beg)
#         label_arr_2 = np.ones(splice_size - (offset_end + (-offset_beg)))
#         label_arr_3 = np.zeros(offset_end)

#         label_arr = np.concatenate(
#             (label_arr_1, label_arr_2, label_arr_3)).astype(np.int64)

#         # print("Spliced data shape:")
#         # print(label_arr.shape)
#         # print(spliced_data.shape)

#     else:
#         patient_file = '../data/ID01_' + str(int(start_file[0])) + 'h.mat'
#         data = loadmat(patient_file)

#         # splice of data with a seizure present
#         spliced_data = data['EEG'][:16, int(start_idx):int(
#             end_idx)]  #take first 16 channels

#         splice_size = int(end_idx) - int(start_idx)
#         # print(splice_size)
#         # print(len(spliced_data[0]))

#         #labels
#         label_arr_1 = np.zeros(-offset_beg)
#         label_arr_2 = np.ones(splice_size - (offset_end + (-offset_beg)))
#         label_arr_3 = np.zeros(offset_end)

#         label_arr = np.concatenate(
#             (label_arr_1, label_arr_2, label_arr_3)).astype(np.int64)

#     # convert it into format for training
#     # 20s windows with a label saying "seizure" or not "seizure"

#     # Parameters for slicing
#     slice_size = 20 * 512  # 20s * 512 Hz (num indexes)
#     step_size = 10 * 512  # 10s * 512 Hz (how much shift between slices)

#     # List to store the slices
#     slices = []
#     slices_labels = []

#     # Loop to create overlapping slices
#     for start_index in range(0,
#                              len(spliced_data[0]) - slice_size + 1, step_size):
#         end_index = start_index + slice_size

#         # one 20s slice of data, all 16 channel
#         slice = spliced_data[:, start_index:end_index]

#         print("shape", start_index)
#         print(slice.shape)

#         # is it a seizure or not
#         counts = np.bincount(
#             label_arr[start_index:end_index])  # how many ones or zeros
#         most_common_value = np.argmax(
#             counts
#         )  # take most common occurence as an indicator of seizure or not

#         # print(type(slice))
#         slices.append(slice)
#         slices_labels.append(most_common_value)

#     # Convert the list of slices to a numpy array
#     slices_array = np.array(slices)
#     slices_labels_array = np.array(slices_labels)

#     print("slices shape seizure (num_items, channels, signals):")
#     print(slices_array.shape)
#     # print(slices_array[0].shape)
#     print(slices_labels_array.shape)

#     #save labels
#     # format:
#     # 93 items each corresponding to a label in ieeg_signals.npy
#     np.save(
#         './test_save_data/ID' + patient_id + '_' + str(seizure_id) +
#         '_positive_labels.npy', slices_labels_array)

#     #save the ieeg data
#     # format:
#     # 93 rows each of a 20s ieeg input with a corresponding label
#     np.save(
#         './test_save_data/ID' + patient_id + '_' + str(seizure_id) +
#         '_positive_signals.npy', slices_array)


# this function and the following helper functions generate non-seizure slices of ieeg data
def splice_nonseizure_data(patient_id, patient_dict, samples_to_generate=5):
    # find out which files not to take data from:

    omit_files = set()  # set of files to not take nonseizure data from

    for i in range(len(patient_dict[patient_id].seizure_start_files)):

        start_file = int(patient_dict[patient_id].seizure_start_files[i][0])
        end_file = int(patient_dict[patient_id].seizure_end_files[i][0])

        correlated_zone_size = 3  # how many files to leave to have no correlation

        for j in range(start_file - correlated_zone_size,
                       end_file + correlated_zone_size):
            omit_files.add(j)

    # sort omit_files
    # omit_files = sorted(omit_files)
    # print(omit_files)

    #finding upper limit of file indexes we can sample from:
    directory = '../data'

    numbers = set()
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.mat'):
            file_path = os.path.join(directory, filename)
            # print(filename)
            pattern = re.compile(r'_(\d+)h')

            numbers.add(int(pattern.search(filename).group(1)))

    #finding intersection of files to sample from non-seizure files

    sampleable_files = np.array([x for x in numbers if x not in omit_files])
    # print(sampleable_files)

    sample_length = 600  #seconds
    sample_rate = 512  #Hz
    sample_idx_len = sample_length * sample_rate

    offset = 30  #seconds
    offset_idx = offset * sample_rate
    sample_idx_len = sample_idx_len + offset_idx

    for i in range(samples_to_generate):

        # choose random file to sample from
        random_file = np.random.choice(sampleable_files)
        print("sampled_file: " + str(random_file))

        # open the chosen random
        patient_file = '../data/ID01_' + str(i + 1) + 'h.mat'
        data = loadmat(patient_file)

        # splice of data with no seizure present
        spliced_data = data['EEG'][:16, int(offset_idx):int(sample_idx_len)]

        # print(spliced_data.shape)

        # labels of all 0s
        label_size = len(spliced_data[0])

        label_arr = np.zeros(label_size).astype(np.int64)
        # print(label_arr.shape)

        # Parameters for slicing
        slice_size = 20 * 512  # 20s * 512 Hz (num indexes)
        step_size = 10 * 512  # 10s * 512 Hz (how much shift between slices)

        # List to store the slices
        slices = []
        slices_labels = []

        # Loop to create overlapping slices
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

        print("slices shape nonseizure:")
        print(slices_array.shape)
        print(slices_array[0].shape)
        print(slices_labels_array.shape)

        #save labels
        # format:
        # 93 items each corresponding to a label in ieeg_signals.npy
        np.save(
            './test_save_data/ID' + patient_id + '_' + str(i) +
            '_negative_labels.npy', slices_labels_array)

        #save the ieeg data
        # format:
        # 93 rows each of a 20s ieeg input with a corresponding label
        np.save(
            './test_save_data/ID' + patient_id + '_' + str(i) +
            '_negative_signals.npy', slices_array)
