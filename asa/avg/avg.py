import sys

sys.path.append("./")

import numpy as np
from numpy.typing import NDArray

# from app.static.processing_elements.processing_element import ProcessingElement
from asa.processing_element import ProcessingElement


class AVG(ProcessingElement):
    """
    Average Unit, computes the average of the input signal
    """
    name = "AVG"

    def __init__(self,
                 n_channels: int,
                 clk: int = 0,
                 rtl_sim: bool = False,
                 rtl_power_estimation: bool = False,
                 save_visualization: bool = False) -> None:
        super().__init__(name=self.name,
                         clk=clk,
                         rtl_sim=rtl_sim,
                         rtl_power_estimation=rtl_power_estimation,
                         save_visualization=save_visualization)

        self.num_channels = n_channels

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

    def dimension_validate(self, input: NDArray[np.float32]) -> None:
        self.input_dimension = input.shape

        # self.input_val_size = len(input)

        assert self.input_dimension == self.input_dimension, f"Input size {self.input_val_size} does not match weights size {len(self.weights)}"

    def compute(self, input: NDArray[np.float64]) -> NDArray[np.float64]:
        """
        Vectorized implementation of AVG computation for multiple channels

        Args:

            input: Input signal array of shape (n_channels, n_samples)
                    where n_channels is the number of channels and
                    n_samples is the number of samples per channel

        Returns:
            NDArray containing AVG values for all channels
        """

        return np.mean(input, axis=1)

    def compute_verilog(self,
                        input: NDArray[np.float32]) -> NDArray[np.float32]:
        """
        Compute average using Verilog implementation
        
        Args:
            input: Input signals of shape (n_channels, 8192)
                  Each channel should have 8192 samples
        
        Returns:
            NDArray containing average values for all channels
        """
        if input.ndim == 1:
            input = input.reshape(1, -1)

        n_channels, n_samples = input.shape
        assert n_samples == 8192, "Input must have 8192 samples per channel"

        verilog_file = "avg"
        averages = []

        for signal in input:
            # Convert to integer representation (16-bit)
            signal_int = signal.astype(np.int16)

            # Write input buffer - one value per line
            with open(self.input_buffer, 'w') as file:
                for sample in signal_int:
                    file.write(f"{self.int_to_signedHex(sample)}\n")

            # Run Verilog simulation
            average_result = self.run_verilog_simulation(
                PE_name=self.name,
                verilog_file=verilog_file,
                output_file=self.output_buffer)

            # Handle potential overflow
            threshold = (2**31) - 1000
            average_result = np.where(average_result > threshold, 0,
                                      average_result)

            averages.append(average_result[0])  # Just need the single value

        return np.array(averages)

    def get_tooltip(self):
        tooltip_text = f"{self.name}\n"
        tooltip_text += f"Clock Frequency: {self.clk}\n"
        tooltip_text += f"Run Power Estimation: {self.rtl_power_estimation}\n"
        tooltip_text += f"RTL Simulation: {self.rtl_sim}\n"
        tooltip_text += f"Weights: {self.weights}"
        return tooltip_text

    def visualize(self) -> None:
        # nothing to visualise for SVM
        pass

    def __repr__(self) -> str:
        return f"{self.name}"
