# from indicies_gen import create_seizure_indices
# from splice_data import splice_seizure_data, splice_nonseizure_data

# import numpy as np

# patient_dict = create_seizure_indices(offset_beg=-180, offset_end=180)

# nonseizure_splices_remaining = splice_seizure_data(patient_dict)

# splice_nonseizure_data(patient_dict, nonseizure_splices_remaining)

# print("training data ready-----")



from indicies_gen import create_seizure_indices
from splice_data import splice_seizure_data, splice_nonseizure_data
import numpy as np
from multiprocessing import Process

def process_data(patient_subdict):
    nonseizure_splices_remaining = splice_seizure_data(patient_subdict)
    splice_nonseizure_data(patient_subdict, nonseizure_splices_remaining)

def main():
    patient_dict = create_seizure_indices(offset_beg=-180, offset_end=180)

    # split patient data into four groups
    patient_keys = list(patient_dict.keys())
    n = len(patient_keys) // 4
    subdicts = [dict(list(patient_dict.items())[i:i + n]) for i in range(0, len(patient_keys), n)]

    # create a process for each group
    processes = []
    for subdict in subdicts:
        p = Process(target=process_data, args=(subdict,))
        processes.append(p)
        p.start()

    # wait for all processes to complete
    for p in processes:
        p.join()

    print("Training data ready-----")

if __name__ == "__main__":
    main()

