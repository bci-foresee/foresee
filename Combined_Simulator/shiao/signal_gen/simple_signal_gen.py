import numpy as np
import matplotlib.pyplot as plt

'''
##################################

This module generates a simple superposition of sine waves in channel 0 for testing purposes.

All other channels are filled with with a constant signal of 1.

# Inputs
- num_channels [int]                    number of channels to generate
- sample_window [float]                 how long the window is in seconds
- num_samples [int]                     how many samples in the given window
- frequencies [List::float]             list of frequencies of sine waves 
- amplitudes [List::float]              list of amplitudes of sine waves, corresponding to frequencies
- saveGraphs [Bool]                     boolean 

# Outputs
- sampled_signals [np.array::float]     list of sampled signals
- sampled_signal_plot [png]             plot of the sampled signal
- sampled_signal_int_plot [png]         plot of the sampled signal converted to integers
##################################
'''

def sample_signals(num_channels, 
                   sample_window, 
                   num_samples,
                   frequencies,
                   amplitudes,
                   saveGraphs=False):

    # define a sampled function, and the sample
    def signal1(t):
        # frequencies = [10, 50, 80, 125]
        # amplitudes =  [20,  15,  15,  5]
        # frequencies = [5]
        # amplitudes =  [20]
        returnSignal = 0
        for i in range(len(frequencies)):
            returnSignal += amplitudes[i] * np.sin(2*np.pi*frequencies[i]*t)  
        return (returnSignal)
    
    def randomvals(t):
        return np.ones_like(t)
    
    sampled_signals = []
    for i in range(num_channels):
        x = np.linspace(start=0, stop=sample_window, num=num_samples, endpoint=False)
        if i == 0:
            sampled_signals.append(signal1(x))
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
        else:
            sampled_signals.append(randomvals(x))

    return sampled_signals