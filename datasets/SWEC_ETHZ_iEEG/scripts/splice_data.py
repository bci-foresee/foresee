import numpy as np
from scipy.io import loadmat
import os
import re

# this function and the following helper functions go into the massive dataset downloaded
# and (with some padding) return the areas of the recording with seizures.
def splice_seizure_data(patient_id, patient_dict, offset_beg, offset_end):

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
                            patient_id=patient_id,
                            offset_beg=offset_beg, 
                            offset_end=offset_end)

        
def save_seizure_splice(start_file, end_file, start_idx, end_idx, i, patient_id, offset_beg, offset_end):
    if start_file != end_file:
        #start data
        patient_file = '../data/ID01_'+str(int(start_file[0]))+'h.mat'
        data = loadmat(patient_file)
        spliced_data_start = data['EEG'][:16, int(start_idx):]
        
        #end data 
        patient_file = '../data/ID01_'+str(int(end_file[0]))+'h.mat'
        data = loadmat(patient_file)
        spliced_data_end = data['EEG'][:16, :int(end_idx)]

        spliced_data_concat = np.concatenate((spliced_data_start, spliced_data_end), axis=1)

        #labels
        splice_size = len(spliced_data_concat[0])
        
        label_arr_1 = np.zeros(-offset_beg)
        label_arr_2 = np.ones(splice_size - (offset_end + (-offset_beg) ))
        label_arr_3 = np.zeros(offset_end)

        label_arr = np.concatenate((label_arr_1, label_arr_2, label_arr_3))

        print(label_arr.shape)
        print(spliced_data_concat.shape)

        #save it
        np.save('./test_save_data/ID'+patient_id+'_'+str(i)+'_seizure_label.npy',label_arr)

        #save
        np.save('./test_save_data/ID'+patient_id+'_'+str(i)+'_seizure.npy',spliced_data_concat)
        
    else:
        patient_file = '../data/ID01_'+str(int(start_file[0]))+'h.mat'
        data = loadmat(patient_file)
        
        # splice of data with a seizure present
        spliced_data = data['EEG'][:16, int(start_idx):int(end_idx)] #take first 16 channels

        splice_size = int(end_idx) - int(start_idx)
        # print(splice_size)
        # print(len(spliced_data[0]))
        
        #labels
        label_arr_1 = np.zeros(-offset_beg)
        label_arr_2 = np.ones(splice_size - (offset_end + (-offset_beg) ))
        label_arr_3 = np.zeros(offset_end)

        label_arr = np.concatenate((label_arr_1, label_arr_2, label_arr_3))

        # print(label_arr.shape)
        # print(spliced_data.shape)

        

        #save it
        np.save('./test_save_data/ID'+patient_id+'_'+str(i)+'_seizure_label.npy',label_arr)
        

        # save the array   
        np.save('./test_save_data/ID'+patient_id+'_'+str(i)+'_seizure.npy',spliced_data)




# this function and the following helper functions generate non-seizure slices of ieeg data
def splice_nonseizure_data(patient_id, patient_dict, samples_to_generate=5):
    # find out which files not to take data from:

    omit_files = set() # set of files to not take nonseizure data from
    
    for i in range(len(patient_dict[patient_id].seizure_start_files)):

        start_file=int(patient_dict[patient_id].seizure_start_files[i][0])
        end_file=int(patient_dict[patient_id].seizure_end_files[i][0])

        correlated_zone_size = 3 # how many files to leave to have no correlation
        
        for j in range(start_file-correlated_zone_size,end_file+correlated_zone_size):
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
    print(sampleable_files)


    sample_length = 600 #seconds
    sample_rate = 512 #Hz
    sample_idx_len = sample_length * sample_rate

    offset = 30 #seconds
    offset_idx = offset * sample_rate
    sample_idx_len = sample_idx_len + offset_idx
    
    for i in range(samples_to_generate):

        # choose random file to sample from
        random_file = np.random.choice(sampleable_files)
        print(random_file)

        # open the chosen random
        patient_file = '../data/ID01_'+str(i+1)+'h.mat'
        data = loadmat(patient_file)
        
        # splice of data with no seizure present
        spliced_data = data['EEG'][:16, int(offset_idx):int(sample_idx_len)]

        print(spliced_data.shape)

        # save the array   
        np.save('./test_save_data/ID'+patient_id+'_'+str(i)+'_nonseizure.npy',spliced_data)
        
    
















    
    
