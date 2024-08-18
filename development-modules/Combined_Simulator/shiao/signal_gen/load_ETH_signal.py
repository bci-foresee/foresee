import numpy as np
import matplotlib.pyplot as plt
import os

'''
##################################

This module loads in 20s snippets of signals

# Inputs
- filename [.npy]                       signal to load file name, from SWEC dataset
- saveGraphs [Bool]                     boolean 

# Outputs
- sampled_signals [np.array::float]     list of sampled signals
- sampled_signal_plot [png]             plot of the sampled signal
- sampled_signal_int_plot [png]         plot of the sampled signal converted to integers
##################################
'''

def load_ETH_signal(directory="./test_data",
                    saveGraphs=False):

    # ------------- loading in data -----------------

    # Directory containing the .npy files
    
    # List all files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.npy')]
    
    # Sort files alphabetically
    files.sort()
    
    ieeg_signals = []
    ieeg_signals_labels = []
    
    # Load each file
    data = None
    data_labels = None
    
    for file in files:
        file_path = os.path.join(directory, file)
    
        if file == 'ID01_0_positive_signals.npy':    
            data = np.load(file_path)

        if file == 'ID01_0_positive_labels.npy':
            data_labels = np.load(file_path)

    ieeg_signals.append(data)
    ieeg_signals_labels.append(data_labels)

    print()
    print("shape of (data: items, channels, signals), (ieeg_signals_labels):")
    print(len(data), len(data[0]), len(data[0][0]), len(data_labels), "\n")

    # choose a random positive example
    pos_example = None
    flag = False

    while flag == False:
        random_index = np.random.randint(0, len(data)) # random index within ieeg signal

        # if positive label then assign pos_example
        if data_labels[random_index] == 0:
            pos_example = data[random_index]
            flag = True
        

    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    sampled_signals = pos_example

    num_channels = len(data[0])
    sample_rate = 512
    num_samples = len(data[0][0])
    sample_window = num_samples / sample_rate
    
    for i in range(num_channels):
        x = np.linspace(start=0, stop=sample_window, num=num_samples, endpoint=False)
        if i == 0:

            # display 1st sampled signal
            if saveGraphs:
                plt.figure(figsize=(12, 6))
                plt.plot(x, sampled_signals[0])
                plt.title('Sampled Signal')
                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')
                plt.grid()
                plt.savefig('plots/signal_gen/sampled_signal.png')

                # also printing int converted graph
                int_sampled_signal = [int(sampled_signals[0][i]) for i in range(len(sampled_signals[0]))]
                plt.figure(figsize=(12, 6))
                plt.plot(x, int_sampled_signal)
                plt.title('Sampled Signal int conversion')
                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')
                plt.grid()
                plt.savefig('plots/signal_gen/sampled_signal_int.png')


    return sampled_signals