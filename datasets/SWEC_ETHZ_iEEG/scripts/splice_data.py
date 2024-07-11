import numpy as np
from scipy.io import loadmat

# Load the .mat info file

def splice_data(patient_id, patient_dict):

    for i in range(len(patient_dict[patient_id].seizure_start_files)):

        start_file=patient_dict[patient_id].seizure_start_files[i]
        end_file=patient_dict[patient_id].seizure_end_files[i]
        start_idx=patient_dict[patient_id].seizure_start_indicies[i]
        end_idx=patient_dict[patient_id].seizure_end_indicies[i]

        save_seizure_splice(start_file=start_file, 
                            end_file=end_file, 
                            start_idx=start_idx, 
                            end_idx=end_idx, 
                            i=i, 
                            patient_id=patient_id)

        
def save_seizure_splice(start_file, end_file, start_idx, end_idx, i, patient_id):
    if start_file != end_file:
        #start data
        patient_file = '../data/ID01_'+str(int(start_file[0]))+'h.mat'
        
        spliced_data_start = ldata1(patient_file, start_idx)
        
        #end data 
        patient_file = '../data/ID01_'+str(int(end_file[0]))+'h.mat'
        
        # splice of data with a seizure present
        spliced_data_end = ldata2(patient_file, end_idx)

        # print(spliced_data_start.shape)
        # print(spliced_data_end.shape)

        spliced_data_concat = np.concatenate((spliced_data_start, spliced_data_end), axis=1)

        # print(spliced_data_concat.shape)

        np.save('./test_save_data/ID'+patient_id+'_'+str(i)+'_seizure.npy',spliced_data_concat)
        
    else:
        patient_file = '../data/ID01_'+str(int(start_file[0]))+'h.mat'
        data = loadmat(patient_file)
        
        # splice of data with a seizure present
        spliced_data = data['EEG'][:, int(start_idx):int(end_idx)]
        print(spliced_data.shape)

        # check dur
        print((end_idx-start_idx)/512)

        # save the array   
        np.save('./test_save_data/ID'+patient_id+'_'+str(i)+'_seizure.npy',spliced_data)

def ldata1(patient_file, start_idx):
    data = loadmat(patient_file)
    a = data['EEG'][:, int(start_idx):]
    return a

def ldata2(patient_file, end_idx):
    data = loadmat(patient_file)
    b = data['EEG'][:, :int(end_idx)]
    return b