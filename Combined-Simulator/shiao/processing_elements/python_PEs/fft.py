import numpy as np
import matplotlib.pyplot as plt

def fft_py(sampled_signals, num_samples, sample_freq, nyquist_freq, berger_bands, saveGraphs=False):

    fft_power_features = []
    i = 0

    for samples in sampled_signals:
        fft_output = np.fft.fft(samples)
        positive_freqs = fft_output[:num_samples // 2] # from 0 - Nyquist frequency are the "positive" frequency outputs
        
        # frequency bins
        sample_spacing = 1/sample_freq # how much time between samples
        freq_bins = np.fft.fftfreq(num_samples, sample_spacing) # provide a frequency for each index of the fft output
        positive_freq_bins = freq_bins[:num_samples // 2] # only positive frequencies bins

        # power estimate in berger bands from fft
        # shiao - sum of the magnitudes of the fft output in the berger bands
        fft_power = np.zeros(len(berger_bands))
        for band in berger_bands:
            band_magnitudes = np.abs(positive_freqs[(positive_freq_bins >= band[0]) & (positive_freq_bins < band[1])])
            band_power = np.sum(band_magnitudes)
            fft_power[berger_bands.index(band)] = band_power
        
        fft_power_features.append(fft_power)

        # if the first signal then plot stuff
        if (i == 0) and saveGraphs:
            #Plotting the output spectrum
            plt.figure(figsize=(12, 6))
            plt.plot(freq_bins, np.abs(fft_output))
            plt.title('Output Spectrum')
            plt.xlabel('Frequency')
            plt.ylabel('Magnitude')
            plt.grid()
            plt.savefig('plots/seizure_pipe/output_spectrum.png')

            # Plotting the magnitude spectrum
            plt.figure(figsize=(12, 6))
            # x-axis is the frequency bins,
            plt.plot(positive_freq_bins, np.abs(positive_freqs))  # Plot only positive frequencies
            plt.axvline(x=nyquist_freq, color='r', linestyle='--', label='Nyquist Frequency')
            plt.title('Magnitude Spectrum')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude')
            plt.legend()
            plt.grid()
            plt.savefig('plots/seizure_pipe/fft_magnitude_spectrum.png')

            # display power in berger bands
            plt.figure(figsize=(12, 6))
            plt.bar(range(len(berger_bands)), fft_power)
            plt.xticks(ticks=range(len(berger_bands)), labels=[str(band) for band in berger_bands])
            plt.title('Power in Berger Bands')
            plt.xlabel('Band')
            plt.ylabel('Power')
            plt.grid()
            plt.savefig('plots/seizure_pipe/fft_power_in_berger_bands.png')
        i = i + 1
    
    return fft_power_features
