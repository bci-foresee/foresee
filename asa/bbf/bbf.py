import sys

sys.path.append("./")

import numpy as np
from numpy.typing import NDArray
# from app.static.processing_elements.processing_element import ProcessingElement
from asa.processing_element import ProcessingElement
from typing import List, Tuple
from scipy.signal import butter, filtfilt
import os
import matplotlib.pyplot as plt


class BBF(ProcessingElement):
    """
    Butterworth Bandpass Filter (BBF)
    """
    name = "BBF"

    def __init__(self,
                 fs: int,
                 berger_bands: List[Tuple[int, int]],
                 clk: int = 0,
                 rtl_sim: bool = False,
                 rtl_power_estimation: bool = False,
                 save_visualization: bool = False) -> None:
        super().__init__(name=self.name,
                         clk=clk,
                         rtl_sim=rtl_sim,
                         rtl_power_estimation=rtl_power_estimation,
                         save_visualization=save_visualization)

        self.sample_freq = fs
        self.berger_bands = berger_bands

    # necessary method to load input data from input processing elements
    def load_inputs(self) -> NDArray[np.float32]:
        input_PEs = self.inputs
        # concatenate input data from input PEs
        input_data = []
        for PE in input_PEs:
            input_data.append(
                # PE.run()
                PE.simulation_data['output_data'])
        # concatenate input data
        input_data = np.concatenate(input_data, axis=0)
        return input_data

    # necessary method to validate the dimensions of the input data
    def dimension_validate(self, input: NDArray[np.float32]) -> None:
        self.input_dimension = input.shape
        self.channels = input.shape[1]
        self.num_samples = input.shape[0]

    # necessary method to calculate processing element's computation
    def compute(self, input: NDArray[np.float32]) -> NDArray[np.float32]:

        # helper functions
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

        for signal in input:
            # Apply the bandpass filters and calculate power
            power_bands = []

            for lowcut, highcut in self.berger_bands:
                filtered_signal = butter_bandpass_filter(signal,
                                                         lowcut,
                                                         highcut,
                                                         self.sample_freq,
                                                         order=5)

                # normalize the filtered signal
                # filtered_signal = filtered_signal * 0.25

                power = np.sum(np.square(filtered_signal))

                if np.isinf(power) or np.isnan(
                        power):  # idk why this happens yet
                    num_inf_nan = np.count_nonzero(
                        np.isnan(power) | np.isinf(power))

                if np.isinf(power) or np.isnan(
                        power):  # this is a fix idk why this happens
                    power = 0

                # print(f"Power shape: {power.shape}")

                power_bands.append(power)

                # print(f"Power bands shape: {np.array(power_bands).shape}")

                #print(f"Power in band {lowcut}-{highcut} Hz: {np.mean(power)}")
            bbf_power_features.append(power_bands)

        bbf_power_features = np.array(bbf_power_features)
        self.bbf_power_features = bbf_power_features

        # self.simulation_data

        return bbf_power_features

    def compute_verilog(self,
                        input: NDArray[np.float32]) -> NDArray[np.float32]:
        

        self.rtl_single_module_runs = 8192 # verilog is run 8192 times to emulate hardware

        if input.ndim == 1:
            input = input.reshape(1, -1)

        n_channels, n_samples = input.shape

        assert n_samples == 8192, "Input must have 8192 samples per channel"

        verilog_file = "bbf"

        # helper functions
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

        for signal in input:

            signal_int = signal.astype(np.int32)

            # Apply the bandpass filters and calculate power
            power_bands = []

            for lowcut, highcut in self.berger_bands:
                filtered_signal = butter_bandpass_filter(signal_int,
                                                         lowcut,
                                                         highcut,
                                                         self.sample_freq,
                                                         order=5)

                # normalize the filtered signal
                # filtered_signal = filtered_signal * 0.25

                # Convert to integer representation

                # Write input buffer - 8192 cycles for 8192 points
                with open(self.input_buffer, 'w') as file:
                    for i in range(8192):
                        # Write 1 sample per line (similar to FFT implementation)
                        values = [signal_int[i]]
                        # Convert to hex and write to file
                        hex_values = [self.int_to_signedHex(v) for v in values]
                        file.write(" ".join(hex_values) + "\n")

                # Run Verilog simulation
                bbf_result = self.run_verilog_simulation(
                    PE_name=self.name,
                    verilog_file=verilog_file,
                    output_file=self.output_buffer)

                power = bbf_result[-1]

                # print(f"Power shape: {power.shape}")

                power_bands.append(power)

                # print(f"Power bands shape: {np.array(power_bands).shape}")

                #print(f"Power in band {lowcut}-{highcut} Hz: {np.mean(power)}")
            bbf_power_features.append(power_bands)

        bbf_power_features = np.array(bbf_power_features)
        self.bbf_power_features = bbf_power_features

        # self.simulation_data

        return bbf_power_features

    def get_tooltip(self):
        tooltip_text = f"{self.name}\n"
        tooltip_text += f"Clock Frequency: {self.clk}\n"
        tooltip_text += f"Run Power Estimation: {self.rtl_power_estimation}\n"
        tooltip_text += f"RTL Simulation: {self.rtl_sim}\n"
        tooltip_text += f"Sample Frequency: {self.sample_freq}\n"
        tooltip_text += f"Berger Bands: {self.berger_bands}"
        return tooltip_text

    # necessary method to validate the dimensions of the input data
    def visualize(self) -> None:
        # # Ensure the directory exists
        # output_dir = 'plots'
        # os.makedirs(output_dir, exist_ok=True)

        # # displaying power bands of first signal
        # plt.figure(figsize=(12, 6))
        # plt.bar(range(len(self.berger_bands)), self.bbf_power_features[0])
        # plt.xticks(ticks=range(len(self.berger_bands)),
        #            labels=[str(band) for band in self.berger_bands])
        # plt.title('Power in Berger Bands for 1st input channel')
        # plt.xlabel('Band')
        # plt.ylabel('Power')
        # plt.grid()
        # plt.savefig(os.path.join(output_dir, 'bbf_power_in_berger_bands.png'))
        pass
