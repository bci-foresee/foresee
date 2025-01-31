Dataset: http://ieeg-swez.ethz.ch/

Example scripts for getting dataset data:
`wget -i ../data_urls/patient1partial_data.txt`
`wget -i ../data_urls/patient1full_data.txt`

generate_training_data.py: obtains training data (uses indicies_gen.py and splice_data.py)
train_neo_svm.py and train_shiao_svm.py: train SVMs

An HPC is required to run the code efficiently. Even so, only patient 1 data was light enough to process. generate_training_data.py needs to be adjusted to generate data for just 1 patient.

model_data contains the already compiled Shiao and NEO models for patient 1.


