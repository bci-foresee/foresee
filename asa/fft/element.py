
import numpy as np

from asa.components import ProcessingElement


class FFT(ProcessingElement):
    """
    Performs the Discrete Fourier Transform (DFT) using the Fast Fourier 
    Transform (FFT) algorithm.
    """
    name = "FFT"

    def __init__(self, points: int, clk: int = 0) -> None:
        super().__init__(self.name, clk)

        self.points = points
    

def run(self,
        sampled_signals: np.ndarray[np.int16], 
        sample_freq, 
        berger_bands, 
        saveGraphs=False):
    
    fft_power_features = []
    i = 0

    nyquist_freq = sample_freq / 2 # Nyquist frequency, max frequency that can be represented in the signal
    num_samples = sampled_signals[0].shape[0]

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

    def __repr__(self) -> str:
        return f"{self.name}_{self.points}"
