
import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple
import os

import matplotlib.pyplot as plt

from asa.components import ProcessingElement


class FFT(ProcessingElement):
    """
    Performs the Discrete Fourier Transform (DFT) using the Fast Fourier 
    Transform (FFT) algorithm.
    """
    name = "FFT"

    def __init__(self, points: int, sample_freq: float, berger_bands: List[Tuple[float, float]],
                 clk: int = 0, save_vizualisation: bool = False) -> None:

        super().__init__(name = self.name,
                         clk = clk,
                         save_vizualisation = save_vizualisation)
        
        self.points = points
        self.sample_freq = sample_freq
        self.berger_bands = berger_bands
    
    def run(self):
        # load input data
        input_data = self.load_inputs()
        # validate dimensions
        self.dimension_validate(input=input_data)
        # compute
        output = self.compute(input=input_data)
        # vizualise
        if self.save_vizualisation:
            self.vizualise()
        # return data
        return output

    def load_inputs(self) -> NDArray[np.float32]:
        input_PEs = self.inputs
        # concatenate input data from input PEs
        input_data = []
        for PE in input_PEs:
            input_data.append(PE.run())

        # concatenate input data
        input_data = np.concatenate(input_data, axis=0)
        return input_data

    def dimension_validate(self, input: NDArray[np.float32]) -> None:
        self.input_dimension = input.shape
        self.channels = self.input_dimension[0]
        self.num_samples = self.input_dimension[1]

    def compute(self, input: NDArray[np.float32]) -> NDArray[np.float32]:
        fft_power_features = []
        fft_outputs = []
        num_samples = self.points

        for signal in input:
            fft_output = np.fft.fft(signal)
            fft_outputs.append(fft_output)
            positive_freqs = fft_output[:num_samples // 2]

            sample_spacing = 1 / self.sample_freq
            freq_bins = np.fft.fftfreq(num_samples, sample_spacing)
            positive_freq_bins = freq_bins[:num_samples // 2]

            fft_power = np.zeros(len(self.berger_bands))
            for band in self.berger_bands:
                band_magnitudes = np.abs(positive_freqs[(positive_freq_bins >= band[0]) & (positive_freq_bins < band[1])])
                band_power = np.sum(band_magnitudes)
                fft_power[self.berger_bands.index(band)] = band_power

            fft_power_features.append(fft_power)

        # also save for vizualisation
        self.fft_power_features = fft_power_features
        self.fft_outputs = fft_outputs

        return fft_power_features
    
    def vizualise(self) -> None:
        # Ensure the directory exists
        output_dir = 'plots'
        os.makedirs(output_dir, exist_ok=True)

        freq_bins = np.fft.fftfreq(self.points, 1 / self.sample_freq)
        positive_freq_bins = freq_bins[:self.points // 2]
        nyquist_freq = self.sample_freq / 2

        #Plotting the output spectrum
        plt.figure(figsize=(12, 6))
        plt.plot(freq_bins, np.abs(self.fft_outputs[0]))
        plt.title('Output Spectrum of 1st input channel')
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')
        plt.grid()
        plt.savefig(os.path.join(output_dir, 'output_spectrum.png'))

        # Plotting the magnitude spectrum
        plt.figure(figsize=(12, 6))
        plt.plot(positive_freq_bins, np.abs(self.fft_outputs[0][:self.points // 2]))  # Plot only positive frequencies
        plt.axvline(x=nyquist_freq, color='r', linestyle='--', label='Nyquist Frequency')
        plt.title('Real Magnitude Spectrum of 1st input channel')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(output_dir, 'output_real_spectrum.png'))

        # display power in berger bands
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(self.berger_bands)), self.fft_power_features[0])
        plt.xticks(ticks=range(len(self.berger_bands)), labels=[str(band) for band in self.berger_bands])
        plt.title('Power in Berger Bands for 1st input channel')
        plt.xlabel('Band')
        plt.ylabel('Power')
        plt.grid()
        plt.savefig(os.path.join(output_dir, 'fft_power_in_berger_bands.png'))
        

    def __repr__(self) -> str:
        return f"{self.name}_{self.points}"
