
import numpy as np
from numpy.typing import NDArray
from asa.parent import ProcessingElement
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
                 clk: int = 0, save_visualization: bool = False) -> None:
        super().__init__(name = self.name,
                         clk = clk,
                         save_visualization = save_visualization)
        
        self.sample_freq = fs
        self.berger_bands = berger_bands

    # necessary method to load input data from input processing elements
    def load_inputs(self) -> NDArray[np.float32]:
        input_PEs = self.inputs
        # concatenate input data from input PEs
        input_data = []
        for PE in input_PEs:
            input_data.append(PE.run())
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
                filtered_signal = butter_bandpass_filter(signal, lowcut, highcut, self.sample_freq, order=5)

                # normalize the filtered signal
                # filtered_signal = filtered_signal * 0.25

                power = np.sum( np.square(filtered_signal) )

                if np.isinf(power) or np.isnan(power): # idk why this happens yet
                    num_inf_nan = np.count_nonzero(np.isnan(power) | np.isinf(power))

                if np.isinf(power) or np.isnan(power): # this is a fix idk why this happens
                    power = 0
                power_bands.append(power)

                #print(f"Power in band {lowcut}-{highcut} Hz: {np.mean(power)}")
            bbf_power_features.append(power_bands)

        bbf_power_features = np.array(bbf_power_features)
        self.bbf_power_features = bbf_power_features
        return bbf_power_features
        
    # necessary method to validate the dimensions of the input data
    def visualize(self) -> None:
        # Ensure the directory exists
        output_dir = 'plots'
        os.makedirs(output_dir, exist_ok=True)
            
        # displaying power bands of first signal
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(self.berger_bands)), self.bbf_power_features[0])
        plt.xticks(ticks=range(len(self.berger_bands)), labels=[str(band) for band in self.berger_bands])
        plt.title('Power in Berger Bands for 1st input channel')
        plt.xlabel('Band')
        plt.ylabel('Power')
        plt.grid()
        plt.savefig(os.path.join(output_dir, 'bbf_power_in_berger_bands.png'))

