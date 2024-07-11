from scipy.io import loadmat
import numpy as np

class patient_data_info:
    def __init__(self, sample_rate, seizure_begin, seizure_end):
        self.sample_rate = sample_rate
        self.seizure_begin = seizure_begin
        self.seizure_end = seizure_end
        self.gen_indices()
    
    def gen_indices(self, file_idx_len=1843200, offset_beg = 0, offset_end = 0):
        
        sample_rate = 512
        offset_beg = -180 * 512 #120s * 512Hz
        offset_end =  180 * 512  #120s * 512Hz

        # within which file the seizure starts
        self.seizure_start_files = np.zeros_like(self.seizure_begin)

        # which index the seizure starts at within that file
        self.seizure_start_indicies = np.zeros_like(self.seizure_start_files)

        # getting seizure start file info
        for i in range(len(self.seizure_begin)):
            # getting index of data where the seizure starts (- an offset)
            overall_start_idx = np.floor(self.seizure_begin[i] * self.sample_rate[0][0]) + offset_beg
            #print(self.seizure_begin[i], self.sample_rate[0][0], self.seizure_begin[i] * self.sample_rate[0][0])

            # getting which matlab file the start of the seizure will be found in
            start_file_num = overall_start_idx // file_idx_len

            # within the start file, where does the start idx start 
            file_start_idx = overall_start_idx - start_file_num * file_idx_len

            # storing the start file nums and indicies
            self.seizure_start_files[i] = start_file_num # 1 indexed
            self.seizure_start_indicies[i] = file_start_idx

        # same thing but for seizure end
        # so getting seizure end file and the index within that file that the seizure resides in
        
        self.seizure_end_files = np.zeros_like(self.seizure_begin)
        self.seizure_end_indicies = np.zeros_like(self.seizure_end_files)

        for i in range(len(self.seizure_begin)):
            overall_end_idx = np.ceil(self.seizure_end[i] * self.sample_rate[0][0]) - offset_beg
            #print(self.seizure_begin[i], self.sample_rate[0][0], self.seizure_begin[i] * self.sample_rate[0][0])

            end_file_num = overall_end_idx // file_idx_len

            file_end_idx = overall_end_idx - end_file_num * file_idx_len

            self.seizure_end_files[i] = end_file_num
            self.seizure_end_indicies[i] = file_end_idx

def create_seizure_indices():
    patient_dict = {}

    # Load the .mat info file
    patient_nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18']

    for patient_num in patient_nums:
        info_file = '../data_info/ID' + patient_num + '_info.mat'
        data = loadmat(info_file)
        #print(data['fs'])

        patient_dict[patient_num] = patient_data_info(data['fs'], data['seizure_begin'], data['seizure_end'])

    return patient_dict

# print('\n')
# print(patient_dict['01'].seizure_end)

# print('\n')
# print(patient_dict['01'].seizure_start_files)
# print('\n')
# print(patient_dict['01'].seizure_end_files)

# #print
# print("\nsample_rate: " + str(sample_rate))
# print("\nseizure_begin: " + str(seizure_begin))
# print("\nseizure_end: " + str(seizure_end))

