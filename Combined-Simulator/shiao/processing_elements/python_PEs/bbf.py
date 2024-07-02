import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

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
            power = np.sum( np.square(filtered_signal) )

            if np.isinf(power) or np.isnan(power): # this is a fix
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
            plt.savefig('plots/seizure_pipe/bbf_power_in_berger_bands.png')
    
    return bbf_power_features