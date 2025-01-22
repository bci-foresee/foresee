import os
import requests
from scipy.io import loadmat
import numpy as np
from tqdm import tqdm  # This imports the tqdm function directly


class patient_data_info:

    def __init__(self,
                 patient_id,
                 sample_rate, # sample rate (Hz)
                 seizure_begin, # arr of seizure start times
                 seizure_end, # arr of seizure end times
                 offset_beg, # pre-seizure offset (s)
                 offset_end): # post-seizure offset (s)
        self.id = patient_id
        self.sample_rate = sample_rate
        self.seizure_begin = seizure_begin
        self.seizure_end = seizure_end
        self.offset_beg = offset_beg * self.sample_rate
        self.offset_end = offset_end * self.sample_rate

        # dataset files and indices containing seizures
        self.seizure_start_files = np.zeros_like(self.seizure_begin) 
        self.seizure_end_files = np.zeros_like(self.seizure_begin) 
        self.seizure_start_indicies = np.zeros_like(self.seizure_begin) 
        self.seizure_end_indicies = np.zeros_like(self.seizure_begin) 

        self.extract_seizure_data(offset_beg=offset_beg, offset_end=offset_end)

    def extract_seizure_data(self, file_idx_len=1843200, offset_beg=0, offset_end=0):
        '''
        Extracts dataset files and indices corresponding to seizures
        '''

        # getting seizure start file info
        for i in range(len(self.seizure_begin)):
            # getting index of data where the seizure starts (- an offset)
            overall_start_idx = np.floor(
                self.seizure_begin[i] * self.sample_rate) + offset_beg

            # getting which matlab file the start of the seizure will be found in
            start_file_num = overall_start_idx // file_idx_len

            # within the start file, where does the start idx start
            file_start_idx = overall_start_idx - start_file_num * file_idx_len

            # storing the start file nums and indicies
            self.seizure_start_files[i] = start_file_num  # 1 indexed
            self.seizure_start_indicies[i] = file_start_idx

        # same thing but for seizure end
        # so getting seizure end file and the index within that file that the seizure resides in

        for i in range(len(self.seizure_begin)):
            overall_end_idx = np.ceil(
                self.seizure_end[i] * self.sample_rate) + offset_end

            end_file_num = overall_end_idx // file_idx_len

            file_end_idx = overall_end_idx - end_file_num * file_idx_len

            self.seizure_end_files[i] = end_file_num
            self.seizure_end_indicies[i] = file_end_idx
    
    def save_seizure_data_urls(self):
        num_seizures = len(self.seizure_begin)
        urls_directory = '../data_urls/'
        os.makedirs(urls_directory, exist_ok=True)  # Ensure the directory exists
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
    patient_dict = create_seizure_indices(offset_beg=-180,
                                      offset_end=180)
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
