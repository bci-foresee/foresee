import sys

sys.path.append("./")

import numpy as np
from numpy.typing import NDArray

# from app.static.processing_elements.processing_element import ProcessingElement
from asa.processing_element import ProcessingElement


class TKEO(ProcessingElement):
    """
    Teager-Kaiser Energy Operator (TKEO)
    """
    name = "TKEO"

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
        Vectorized implementation of TKEO computation for multiple channels
        
        Args:
            input: Input signal array of shape (n_channels, n_samples)
                    where n_channels is the number of channels and
                    n_samples is the number of samples per channel
            
        Returns:
            NDArray containing TKEO values for all channels, shape (n_channels, n_samples)
        """
        # Ensure input is 2D array
        if input.ndim == 1:
            input = input.reshape(1, -1)

        # Convert input to float64 if it isn't already
        input = input.astype(np.float64)

        # Get dimensions
        n_channels, n_samples = input.shape

        # Initialize output array
        output = np.zeros_like(input)

        # Compute main TKEO values using vectorized operations for all channels
        output[:, 1:-1] = input[:, 1:-1]**2 - input[:, :-2] * input[:, 2:]

        # Handle edge cases for all channels
        output[:, 0] = input[:, 0]**2 - input[:, 0] * input[:, 1]
        output[:, -1] = input[:, -1]**2 - input[:, -2] * input[:, -1]

        return output

    def compute_verilog(self,
                        input: NDArray[np.float32]) -> NDArray[np.float32]:
        """
        Compute TKEO using Verilog implementation
        
        Args:
            input: Input signals of shape (n_channels, n_samples)
                  Each channel should have 8192 samples
        
        Returns:
            NDArray containing TKEO values for all channels
        """
        if input.ndim == 1:
            input = input.reshape(1, -1)

        n_channels, n_samples = input.shape

        assert n_samples == 8192, "Input must have 8192 samples per channel"

        self.rtl_single_module_runs = n_samples  # verilog is run 8192 times to emulate hardware

        verilog_file = "tkeo"
        tkeo_outputs = []

        for signal in input:
            # Convert to integer representation
            signal_int = signal.astype(np.int32)

            # Write input buffer - 8192 cycles for 8192 points
            with open(self.input_buffer, 'w') as file:
                for i in range(8192):
                    # Write 1 sample per line (similar to FFT implementation)
                    values = [signal_int[i]]
                    # Convert to hex and write to file
                    hex_values = [self.int_to_signedHex(v) for v in values]
                    file.write(" ".join(hex_values) + "\n")

            # Run Verilog simulation
            tkeo_result = self.run_verilog_simulation(
                PE_name=self.name,
                verilog_file=verilog_file,
                output_file=self.output_buffer)

            # temp
            # tkeo_result = np.zeros(n_samples)

            # zero pad tkeo_result to 8192
            tkeo_result = np.pad(tkeo_result, (0, 8192 - len(tkeo_result)),
                                 'constant')

            # Handle potential overflow
            threshold = (2**31) - 1000
            tkeo_result = np.where(tkeo_result > threshold, 0, tkeo_result)

            tkeo_outputs.append(tkeo_result)

        return np.array(tkeo_outputs)

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
