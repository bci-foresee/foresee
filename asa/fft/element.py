
import numpy as np
import matplotlib.pyplot as plt

from numpy.typing import NDArray
from typing import List, Tuple

import os
from asa.parent import ProcessingElement


class FFT(ProcessingElement):
    """
    Performs the Discrete Fourier Transform (DFT) using the Fast Fourier 
    Transform (FFT) algorithm.
    """
    name = "FFT"

    def __init__(self, berger_bands: List[Tuple[int, int]],
                 n_samples: int, 
                 fs: int,
                 clk: int = 0, 
                 rtl_sim: bool = False,
                 save_visualization: bool = False,
                 ) -> None:

        super().__init__(name = self.name,
                         clk = clk,
                         rtl_sim = rtl_sim,
                         save_visualization = save_visualization)
        
        self.points = n_samples
        self.sample_freq = fs
        self.berger_bands = berger_bands
    
    def run(self) -> NDArray[np.float32]:
        # load input data
        input_data = self.load_inputs()
        # validate dimensions
        self.dimension_validate(input=input_data)
        # compute
        if self.rtl_sim:
            output = self.compute_verilog(input=input_data) # replace with verilog compute
        else:
            output = self.compute(input=input_data)
        
        # vizualise
        if self.save_visualization:
            self.visualize()
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
        
        assert self.num_samples == self.points, "Number of samples must match"

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

        # also save for visualisation
        fft_power_features = np.array(fft_power_features)
        self.fft_power_features = fft_power_features
        self.fft_outputs = np.array(fft_outputs)

        return fft_power_features
    
    def compute_verilog(self, input: NDArray[np.float32]) -> NDArray[np.float32]:
        
        # do if statements to choose between verilog implementations (ie how many points) here

        PE_name = "spiral_fft_8192"
        verilog_file = "./rtl/" + PE_name + ".v"

        fft_power_features = []
        fft_outputs = []
        num_samples = self.points

        for signal in input:
            
            signal_int = signal.astype(np.int32)

            # 2048 cycles for 8192 points
            with open(self.input_buffer, 'w') as file:
                # writing input buffer
                for i in range(2048):
                    file.write(f"{signal_int[4*i]:08x} {0:08x} {signal_int[4*i+1]:08x} {0:08x} {signal_int[4*i+2]:08x} {0:08x} {signal_int[4*i+3]:08x} {0:08x}\n")

            verilog_result = self.run_verilog_simulation(verilog_file, self.output_buffer)

            fft_output = np.zeros(num_samples, dtype=np.complex64)

            # coalesce the real and imaginary parts
            for i in range(len(verilog_result)//2):
                fft_output[i] = verilog_result[2*i] + 1j*verilog_result[2*i+1]

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

        # also save for visualisation
        fft_power_features = np.array(fft_power_features)
        self.fft_power_features = fft_power_features
        self.fft_outputs = np.array(fft_outputs)

        return fft_power_features


    def visualize(self) -> None:
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
