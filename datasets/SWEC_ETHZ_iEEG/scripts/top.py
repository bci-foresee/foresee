from indicies_gen import create_seizure_indices
from splice_data import splice_data

import numpy as np

patient_dict = create_seizure_indices()

print('\n')
print(patient_dict['01'].seizure_end)

print('\n')
print(patient_dict['01'].seizure_start_files)
print('\n')
print(patient_dict['01'].seizure_end_files)

print('\n')
print(len(patient_dict))

patient_nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18']


#important to check below:

# for patient in patient_nums:
#     print('\n--------------------')
#     print(patient)
#     # print(patient_dict[patient].seizure_start_files)
#     # print(patient_dict[patient].seizure_end_files)
#     print("are the arrays equal: " + str(np.array_equal(patient_dict[patient].seizure_start_files, patient_dict[patient].seizure_end_files)) )
#     if not (np.array_equal(patient_dict[patient].seizure_start_files, patient_dict[patient].seizure_end_files)):
#         print(patient_dict[patient].seizure_start_files)
#         print(patient_dict[patient].seizure_end_files)
#     print('--------------------')


splice_data(patient_id='01',
            patient_dict=patient_dict)