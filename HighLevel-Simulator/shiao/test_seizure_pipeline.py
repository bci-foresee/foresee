# this is for testing the entire seizure pipeline

# import os
# import ctypes
# import pytest
import numpy as np
from pipeline import Pipeline
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import seaborn as sns

# loading in all the c functions for the pipeline
pipeline = Pipeline(kernel_lib='libkernels.so')

def test_seizure_pipeline():

    # pipe setup -------------------------------------------------------------------------------------
    # Sample information
    sample_freq = 400 # Hz
    num_channels = 16 # 1 for now, will be 16 in the future.
    sample_window = 20 # seconds

    num_samples = sample_freq * sample_window # how many samples in 20 s window at 400hz
    nyquist_freq = sample_freq / 2 # Nyquist frequency, max frequency that can be represented in the signal
    
    # berger bands
    berger_bands = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]
    
    # sample ieeg signals ----------------------------------------------------------------------------
    
    sampled_signals = sample_signals(num_signals=num_channels, 
                                     sample_window=sample_window, 
                                     num_samples=num_samples,
                                     saveGraphs=True)

    # fft --------------------------------------------------------------------------------------------
    
    fft_power_features = fft(sampled_signals=sampled_signals, 
                             num_samples=num_samples, 
                             sample_freq=sample_freq,
                             nyquist_freq=nyquist_freq,
                             berger_bands=berger_bands,
                             saveGraphs=True)

    # bbf --------------------------------------------------------------------------------------------

    # note look at fix for setting inf/nan values to 0

    bbf_power_features = bbf(sampled_signals=sampled_signals,
                             sample_freq=sample_freq, 
                             berger_bands=berger_bands, 
                             saveGraphs=True)

    # xcorr --------------------------------------------------------------------------------------------

    xcorr_features = xcorr(sampled_signals=sampled_signals, 
          num_channels=num_channels, 
          num_samples=num_samples,
          saveGraphs=True)
    
    # data manipulation -------------------------------------------------------------------------------

    fft_power_features_arr = np.array(fft_power_features)
    bbf_power_features_arr = np.array(bbf_power_features)
    xcorr_features_arr = np.array(xcorr_features)
    
    fft_features_flat = fft_power_features_arr.flatten()
    bbf_features_flat = bbf_power_features_arr.flatten()
    xcorr_features_flat = xcorr_features_arr.flatten()

    # 312 features in one array
    features_arr = np.concatenate((fft_features_flat, bbf_features_flat, xcorr_features_flat))
    
    # svm ---------------------------------------------------------------------------------------------

    weights = np.random.rand(312)
    bias = np.random.rand(1)
    svm_output = svm(features=features_arr, 
                     weights=weights, 
                     bias=bias)

    # thr ---------------------------------------------------------------------------------------------
    
    upper_bound = 1
    lower_bound = 0
    thr_output = thr(val=svm_output, 
                     upper_bound=upper_bound, 
                     lower_bound=lower_bound)
    
    print(thr_output)
    print(svm_output)

# sampling input ieeg signals --------------------------------------------------------------------------
def sample_signals(num_signals, sample_window, num_samples, saveGraphs=False):

    # define a sampled function, and the sample
    def signal1(t):
        frequencies = [10, 20, 60, 125]
        amplitudes =  [5,  1,  2,  3]
        returnSignal = 0
        for i in range(len(frequencies)):
            returnSignal += amplitudes[i] * np.sin(2*np.pi*frequencies[i]*t) 
        return returnSignal
    
    def randomvals(t):
        return np.ones_like(t)
    
    sampled_signals = []
    for i in range(num_signals):
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
                plt.savefig('plots/seizure_pipe/sampled_signal.png')
        else:
            sampled_signals.append(randomvals(x))

    return sampled_signals

# fft ------------------------------------------------------------------------------------------------
def fft(sampled_signals, num_samples, sample_freq, nyquist_freq, berger_bands, saveGraphs=False):

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

# bbf ------------------------------------------------------------------------------------------------
def bbf(sampled_signals, sample_freq, berger_bands, saveGraphs=False):

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

# xcorr --------------------------------------------------------------------------------------------
def xcorr(sampled_signals, num_channels, num_samples, saveGraphs=False):
    correlations = []

    # Calculate normalized cross-correlations
    for i in range(num_channels):
        for j in range(i + 1, num_channels):
            corr = np.correlate(sampled_signals[i], sampled_signals[j], mode='valid')[0]
            norm_corr = corr #/ (num_samples * np.std(sampled_signals[i]) * np.std(sampled_signals[j]))
            correlations.append(norm_corr)

    # Convert the correlations list into a correlation matrix
    def create_correlation_matrix(correlations, num_channels):
        corr_matrix = np.zeros((num_channels, num_channels))
        idx = 0
        for i in range(num_channels):
            for j in range(i + 1, num_channels):
                corr_matrix[i, j] = correlations[idx]
                idx += 1
        corr_matrix += corr_matrix.T  # Make it symmetric
        return corr_matrix
    
    if saveGraphs:
        # Create the correlation matrix
        corr_matrix = create_correlation_matrix(correlations, num_channels)

        # Plot the correlation matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap="coolwarm", square=True)
        plt.title('Correlation Matrix')
        plt.xlabel('Channel')
        plt.ylabel('Channel')
        plt.savefig('plots/seizure_pipe/xcorr_corr_matrix.png')

    return correlations

def xcorr_c(sampled_signals, num_channels, num_samples, saveGraphs=False):

    # NOTE: normalization would be helpful.
    # seems to do weird things.
    def create_correlation_matrix(feature_vector, num_channels):
        # Initialize an empty correlation matrix
        corr_matrix = np.zeros((num_channels, num_channels))

        # Fill the upper triangle with the feature vector
        idx = 0
        for i in range(num_channels):
            for j in range(i + 1, num_channels):
                corr_matrix[i, j] = feature_vector[idx]
                idx += 1

        # Reflect the upper triangle to the lower triangle to make it symmetric
        corr_matrix = corr_matrix + corr_matrix.T

        return corr_matrix

    # sampled_signals_array = np.array(sampled_signals[1:3]) // I think we are hitting overflows.
    sampled_signals_array = np.array(sampled_signals)
    print(sampled_signals_array.shape)

    # calling the c function
    xcorr_features = pipeline.cross_correlation(sampled_signals_array, num_channels, num_samples)

    # display correlation matrix:
    if saveGraphs:
        corr_matrix = create_correlation_matrix(xcorr_features, num_channels)
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap="coolwarm", square=True)
        plt.title('Correlation Matrix')
        plt.xlabel('Channel')
        plt.ylabel('Channel')
        plt.savefig('plots/seizure_pipe/xcorr_corr_matrix.png')

    # return
    return xcorr_features

# svm ---------------------------------------------------------------------------------------------
def svm(features, weights, bias):
    # dot product of features and weights
    wx = np.dot(features, weights)
    # add bias
    wxb = wx + bias
    return wxb
   
# thr ---------------------------------------------------------------------------------------------
def thr(val, upper_bound, lower_bound):
    if (val >= lower_bound) and (val <= upper_bound):
        return 1
    else:
        return 0
    
test_seizure_pipeline()
# note normalise all of these algorithms
# using np.mean seems more reasonable.