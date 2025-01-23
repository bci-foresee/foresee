from indicies_gen import create_seizure_indices
from splice_data import splice_seizure_data, splice_nonseizure_data

import numpy as np

patient_dict = create_seizure_indices(offset_beg=-180, offset_end=180)

nonseizure_splices_remaining = splice_seizure_data(patient_dict)

splice_nonseizure_data(patient_dict, nonseizure_splices_remaining)

print("training data ready-----")
