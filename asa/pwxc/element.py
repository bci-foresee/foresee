import numpy as np
from numpy.typing import NDArray

from asa.parent import ProcessingElement
import matplotlib.pyplot as plt
import seaborn as sns

import os


class PWXC(ProcessingElement):
    """
    Performs a pairwise cross correlation across a set > 2 signals
    """
    name = "PWXC"

    def __init__(self,
                 n_channels: int,
                 clk: int = 0,
                 save_visualization: bool = False,
                 rtl_sim: bool = False,
                 rtl_power_estimation: bool = False) -> None:
        super().__init__(name=self.name,
                         clk=clk,
                         save_visualization=save_visualization,
                         rtl_sim=rtl_sim,
                         rtl_power_estimation=rtl_power_estimation)

        self.num_channels = n_channels

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

        correlations = []

        # pairwise cross correlation, no sliding window, no repeated pairs
        for i in range(self.num_channels):
            for j in range(i + 1, self.num_channels):
                correlation = np.correlate(input[i], input[j], mode='valid')
                correlations.append(correlation)

        correlations = np.array(correlations)
        self.correlations = correlations
        return correlations
    
    def compute_verilog(self, input: NDArray[np.float32]
                        ) -> np.int64:

        input1 = input[0]
        input2 = input[1]

        # Specify the Verilog file for the cross-correlation module
        verilog_file = "pwxc"

        # Convert inputs to appropriate integer type (e.g., int16)
        input1_int = input1.astype(np.int16)
        input2_int = input2.astype(np.int16)

        # Ensure the input arrays have the correct length
        if input1_int.size != 8192 or input2_int.size != 8192:
            raise ValueError("Input signals must be of length 8192.")

        # Define file names for the input and output buffers
        self.input_x_buffer = 'input_x_buffer.txt'
        self.input_y_buffer = 'input_y_buffer.txt'
        self.output_result = 'output_result.txt'

        # Write input1 to "input_x_buffer.txt"
        with open(self.input_x_buffer, 'w') as file_x:
            for sample in input1_int:
                # Writing each sample as a signed hex string
                file_x.write(f"{self.int_to_signedHex(sample)}\n")

        # Write input2 to "input_y_buffer.txt"
        with open(self.input_y_buffer, 'w') as file_y:
            for sample in input2_int:
                # Writing each sample as a signed hex string
                file_y.write(f"{self.int_to_signedHex(sample)}\n")

        # Run the Verilog simulation
        verilog_result = self.run_verilog_simulation(
            PE_name=self.name,
            verilog_file=verilog_file,
            output_file=self.output_result)

        # The result is expected to be in hexadecimal format, read and convert it
        # The 'verilog_result' is a NumPy array containing integers
        # Since the cross-correlation result is a single value, extract the first element
        result_int = verilog_result[0]

        correlations = []

        for i in range(self.num_channels):
            for j in range(i + 1, self.num_channels):
                correlations.append(result_int)

        self.correlations = correlations

        return correlations



    def visualize(self) -> None:
        # Ensure the directory exists
        output_dir = 'plots'
        os.makedirs(output_dir, exist_ok=True)

        # Convert the correlations list into a correlation matrix
        def create_correlation_matrix(correlations, num_channels):
            corr_matrix = np.zeros((num_channels, num_channels))
            idx = 0
            for i in range(num_channels):
                for j in range(i + 1, num_channels):
                    # print(f"correlations[{idx}].shape = {correlations[idx].shape}")
                    corr_matrix[i, j] = correlations[idx].item()
                    idx += 1
            corr_matrix += corr_matrix.T  # Make it symmetric
            np.fill_diagonal(
                corr_matrix, np.nan
            )  # fill diagonal with NaN to prevent it showing up on correlation matrix
            return corr_matrix

        # Create the correlation matrix
        corr_matrix = create_correlation_matrix(self.correlations,
                                                self.num_channels)

        # Plot the correlation matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix,
                    annot=False,
                    fmt=".2f",
                    cmap="coolwarm",
                    square=True,
                    cbar_kws={"shrink": .8})
        plt.title('Correlation Matrix with Black Diagonal')
        plt.xlabel('Channel')
        plt.ylabel('Channel')
        plt.savefig(os.path.join(output_dir, 'pwxc_matrix.png'))

    def __repr__(self) -> str:
        return f"{self.name}"
