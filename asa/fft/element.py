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

    def __init__(
        self,
        berger_bands: List[Tuple[int, int]],
        n_samples: int,
        fs: int,
        clk: int = 0,
        rtl_sim: bool = False,
        rtl_power_estimation: bool = False,
        save_visualization: bool = False,
    ) -> None:

        super().__init__(name=self.name,
                         clk=clk,
                         rtl_sim=rtl_sim,
                         rtl_power_estimation=rtl_power_estimation,
                         save_visualization=save_visualization)

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
            output = self.compute_verilog(
                input=input_data)  # replace with verilog compute
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
                band_magnitudes = np.abs(
                    positive_freqs[(positive_freq_bins >= band[0])
                                   & (positive_freq_bins < band[1])])
                band_power = np.sum(band_magnitudes)
                fft_power[self.berger_bands.index(band)] = band_power

            fft_power_features.append(fft_power)

        # also save for visualisation
        fft_power_features = np.array(fft_power_features)
        self.fft_power_features = fft_power_features
        self.fft_outputs = np.array(fft_outputs)

        return fft_power_features

    def compute_verilog(self,
                        input: NDArray[np.float32]) -> NDArray[np.float32]:

        # do if statements to choose between verilog implementations (ie how many points) here
        verilog_file = "spiral_fft_8192"

        fft_power_features = []
        fft_outputs = []
        num_samples = self.points

        for signal in input:

            signal_int = signal.astype(np.int32)

            # 2048 cycles for 8192 points < -----  MAKE THIS A HELPER FUNCTION
            with open(self.input_buffer, 'w') as file:
                # writing input buffer
                for i in range(2048):
                    # writing into the buffer in signed hex format
                    file.write(f"{self.int_to_signedHex(signal_int[4*i])} "
                               f"{self.int_to_signedHex(0)} "
                               f"{self.int_to_signedHex(signal_int[4*i+1])} "
                               f"{self.int_to_signedHex(0)} "
                               f"{self.int_to_signedHex(signal_int[4*i+2])} "
                               f"{self.int_to_signedHex(0)} "
                               f"{self.int_to_signedHex(signal_int[4*i+3])} "
                               f"{self.int_to_signedHex(0)}\n")

            verilog_result = self.run_verilog_simulation(
                PE_name=self.name,
                verilog_file=verilog_file,
                output_file=self.output_buffer)

            fft_real_output = np.zeros(len(verilog_result) // 2)
            fft_imag_output = np.zeros(len(verilog_result) // 2)
            fft_output = np.zeros(len(verilog_result) // 2)

            # coalesce the real and imaginary parts
            for i in range(len(verilog_result) // 2):
                fft_real_output[i] = verilog_result[2 * i]
                fft_imag_output[i] = verilog_result[2 * i + 1]

            # replac vals in np_real and np_imag that are above a certain threshold with 0
            # this is likely due to overflow in the fft module
            threshold = (2**31) - 1000
            fft_real_output = np.where(fft_real_output > threshold, 0,
                                       fft_real_output)
            fft_imag_output = np.where(fft_imag_output > threshold, 0,
                                       fft_imag_output)

            # convert to magnitude spectrum from real and imaginary numbers
            for i in range(len(fft_output)):
                fft_output[i] = np.sqrt(fft_real_output[i]**2 +
                                        fft_imag_output[i]**2)

            neg_freqs = fft_output[len(fft_output) // 2:][::-1]
            pos_freqs = fft_output[:len(fft_output) // 2]

            positive_freqs = (neg_freqs + pos_freqs) / 2

            fft_outputs.append(fft_output)
            # positive_freqs = fft_output[:num_samples // 2]

            sample_spacing = 1 / self.sample_freq
            freq_bins = np.fft.fftfreq(num_samples, sample_spacing)
            positive_freq_bins = freq_bins[:num_samples // 2]

            fft_power = np.zeros(len(self.berger_bands))
            for band in self.berger_bands:
                band_magnitudes = np.abs(
                    positive_freqs[(positive_freq_bins >= band[0])
                                   & (positive_freq_bins < band[1])])
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

        neg_freqs = self.fft_outputs[0][len(self.fft_outputs[0]) // 2:][::-1]
        pos_freqs = self.fft_outputs[0][:len(self.fft_outputs[0]) // 2]

        positive_freqs = (neg_freqs + pos_freqs) / 2

        # Plotting the magnitude spectrum
        plt.figure(figsize=(12, 6))
        plt.plot(positive_freq_bins,
                 np.abs(positive_freqs))  # Plot only positive frequencies
        plt.axvline(x=nyquist_freq,
                    color='r',
                    linestyle='--',
                    label='Nyquist Frequency')
        plt.title('Real Magnitude Spectrum of 1st input channel')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(output_dir, 'output_real_spectrum.png'))

        # display power in berger bands
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(self.berger_bands)), self.fft_power_features[0])
        plt.xticks(ticks=range(len(self.berger_bands)),
                   labels=[str(band) for band in self.berger_bands])
        plt.title('Power in Berger Bands for 1st input channel')
        plt.xlabel('Band')
        plt.ylabel('Power')
        plt.grid()
        plt.savefig(os.path.join(output_dir, 'fft_power_in_berger_bands.png'))
