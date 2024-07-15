import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

'''
##################################

This module calculates the power in the Berger bands for each channel of the input signals.

This provides time-domain dependent features for the SVM model.

# Inputs
- sampled_signals [np.array::float]     list of sampled signals
- sample_freq [float]                   frequency of the samples taken (Hz)
- berger_bands [List::Tuple]            list of tuples of the berger bands (Hz)
- saveGraphs [Bool]                     boolean determining if graphs are generated

# Outputs
- bbf_power_features [np.array::float]  list of power estimates in the berger bands for each signal
- power_in_berger_bands [png]           plot of the power in the berger bands

##################################
'''

def bbf_py(sampled_signals, sample_freq, berger_bands, saveGraphs=False):

    def butter_bandpass(lowcut, highcut, fs, order=5):
        # this function returns the coefficients of the bandpass filter
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        # this function applies the bandpass filter to the input data
        # a, b are the coefficients of the bandpass filter
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        y = filtfilt(b, a, data)
        return y
    
    bbf_power_features = []
    
    for i, samples in enumerate(sampled_signals):
        # Apply the bandpass filters and calculate power
        power_bands = []
    
        for lowcut, highcut in berger_bands:
            filtered_signal = butter_bandpass_filter(samples, lowcut, highcut, sample_freq, order=5)

            # normalize the filtered signal
            # filtered_signal = filtered_signal * 0.25

            power = np.sum( np.square(filtered_signal) )

            if np.isinf(power) or np.isnan(power): # idk why this happens yet
                num_inf_nan = np.count_nonzero(np.isnan(power) | np.isinf(power))
                # print(f"filter band: {lowcut}-{highcut} Hz")
                # print(f"Number of values in power that are inf or nan: {num_inf_nan}, power: {power}")
                # print(f"filtered_signal: {filtered_signal}")

            if np.isinf(power) or np.isnan(power): # this is a fix idk why this happens
                power = 0
            power_bands.append(power)

            #print(f"Power in band {lowcut}-{highcut} Hz: {np.mean(power)}")

        bbf_power_features.append(power_bands)
    
        if (i == 0) and saveGraphs:
            # display power in berger bands
            
            plt.figure(figsize=(12, 6))
            plt.bar(range(len(berger_bands)), power_bands)
            plt.xticks(ticks=range(len(berger_bands)), labels=[str(band) for band in berger_bands])
            plt.title('Power in Berger Bands')
            plt.xlabel('Band')
            plt.ylabel('Power')
            plt.grid()
            plt.savefig('plots/python_PEs/bbf_power_in_berger_bands.png')
    
    return bbf_power_features