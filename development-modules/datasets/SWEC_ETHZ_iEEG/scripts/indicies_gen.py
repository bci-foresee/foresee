import os
import requests
from scipy.io import loadmat
import numpy as np


class patient_data_info:

    def __init__(
            self,
            patient_id,
            sample_rate,  # sample rate (Hz)
            seizure_begin,  # arr of seizure start times
            seizure_end,  # arr of seizure end times
            offset_beg,  # pre-seizure offset (s)
            offset_end):  # post-seizure offset (s)
        self.id = patient_id
        self.sample_rate = sample_rate
        self.seizure_begin = seizure_begin
        self.seizure_end = seizure_end
        self.offset_beg = offset_beg
        self.offset_end = offset_end

        # dataset files and indices containing seizures
        self.seizure_start_files = np.zeros_like(self.seizure_begin)
        self.seizure_end_files = np.zeros_like(self.seizure_begin)
        self.seizure_start_indicies = np.zeros_like(self.seizure_begin)
        self.seizure_end_indicies = np.zeros_like(self.seizure_begin)

        self.get_seizure_bounds()

    def get_seizure_bounds(self): #, file_idx_len=1843200):
        '''
        Extracts dataset files and indices corresponding to seizures
        '''

        # get start file and index
        for i in range(len(self.seizure_begin)):
            start_time = self.seizure_begin[i] + self.offset_beg # in s
            start_file_num = (start_time // 3600) + 1 # in hrs
            relative_start_time = start_time % 3600 # in s
            start_index = np.floor(relative_start_time * self.sample_rate)

            self.seizure_start_files[i] = start_file_num
            self.seizure_start_indicies[i] = start_index

        # get end file and index
        for i in range(len(self.seizure_end)):
            end_time = self.seizure_end[i] + self.offset_end # in s
            end_file_num = (end_time // 3600) + 1 # in hrs
            relative_end_time = end_time % 3600 # in s
            end_index = np.floor(relative_end_time * self.sample_rate)

            self.seizure_end_files[i] = end_file_num
            self.seizure_end_indicies[i] = end_index

    def save_seizure_data_urls(self):
        num_seizures = len(self.seizure_begin)
        urls_directory = '../data_urls/'
        os.makedirs(urls_directory,
                    exist_ok=True)  # Ensure the directory exists
        urls_file_path = os.path.join(urls_directory, 'seizure_data.txt')

        # read existing urls
        existing_urls = set()
        if os.path.exists(urls_file_path):
            with open(urls_file_path, 'r') as file:
                existing_urls = set(file.read().splitlines())

        # append new urls
        with open(urls_file_path, 'a') as file:
            for i in range(num_seizures):
                start_file = int(self.seizure_start_files[i])
                end_file = int(self.seizure_end_files[i])

                for f in range(start_file, end_file + 1):
                    url = f'http://ieeg-swez.ethz.ch/long-term_dataset/ID{self.id}/ID{self.id}_{f}h.mat'
                    if url not in existing_urls:
                        file.write(url + '\n')
                        existing_urls.add(url)


def create_seizure_indices(offset_beg=0, offset_end=0):
    patient_dict = {}

    # Load the .mat info file
    patient_nums = [
        '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
        '13', '14', '15', '16', '17', '18'
    ]

    for patient_id in patient_nums:
        info_file = '../data_info/ID' + patient_id + '_info.mat'
        data = loadmat(info_file)

        patient_dict[patient_id] = patient_data_info(patient_id,
                                                     data['fs'][0][0],
                                                     data['seizure_begin'],
                                                     data['seizure_end'],
                                                     offset_beg, offset_end)

        # download seizure files
        patient_dict[patient_id].save_seizure_data_urls()

    return patient_dict


# Tests
if __name__ == "__main__":
    patient_dict = create_seizure_indices(offset_beg=-180, offset_end=180)
    patient_1 = patient_dict['01']
    print("Patient 1 Data:")

    print('\nSeizure start times in s:')
    print(patient_1.seizure_begin)
    print('\nSeizure end times in s:')
    print(patient_1.seizure_end)

    print('\nStart file numbers:')
    print(patient_1.seizure_start_files)
    print('\nEnd file numbers:')
    print(patient_1.seizure_end_files)
    print('\nStart file indices:')
    print(patient_1.seizure_start_indicies)
    print('\nEnd file indices:')
    print(patient_1.seizure_end_indicies)

    print('\nNum of patients with seizure data:')
    print(len(patient_dict))
