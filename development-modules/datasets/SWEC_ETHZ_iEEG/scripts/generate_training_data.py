from indicies_gen import create_seizure_indices
from splice_data import splice_seizure_data, splice_nonseizure_data

import numpy as np

sample_rate=512 # Hz
offset_beg = -180 * sample_rate #120s * 512Hz
offset_end =  180 * sample_rate  #120s * 512Hz

patient_dict = create_seizure_indices(offset_beg=offset_beg,
                                      offset_end=offset_end)

# print('\n')
# print(patient_dict['01'].seizure_end)

# print('\nStart file numbers:')
# print(patient_dict['01'].seizure_start_files)
# print('\nEnd file numbers:')
# print(patient_dict['01'].seizure_end_files)

# print('\n')
# print(len(patient_dict))

patient_nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18']



splice_seizure_data(patient_id='01',
                    patient_dict=patient_dict,
                    offset_beg=offset_beg,
                    offset_end=offset_end)


splice_nonseizure_data(patient_id='01', 
                       patient_dict=patient_dict,
                       samples_to_generate=5)

print("training data ready-----")