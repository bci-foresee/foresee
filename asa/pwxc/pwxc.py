import sys

sys.path.append("./")

import numpy as np
from numpy.typing import NDArray

# from app.static.processing_elements.processing_element import ProcessingElement
from asa.processing_element import ProcessingElement
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
            input_data.append(
                # PE.run()
                PE.simulation_data['output_data'])

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

    def compute_verilog(self,
                        input: NDArray[np.float32]) -> NDArray[np.float32]:

        # do if statements to choose between verilog implementations (ie how many points) here
        verilog_file = "pwxc"
        correlations = []

        input = input.astype(int)

        print("-------------- input shape --------------")
        print(input.shape)

        # need to do this for every single signal correlation

        for i in range(self.num_channels):
            for j in range(i + 1, self.num_channels):

                with open("input_x_buffer.txt", 'w') as file:
                    for k in range(8192):
                        # writing into the buffer in signed hex format
                        file.write(f"{self.int_to_signedHex(input[i][k])}\n")

                with open("input_y_buffer.txt", 'w') as file:
                    for k in range(8192):
                        # writing into the buffer in signed hex format
                        file.write(f"{self.int_to_signedHex(input[j][k])}\n")

                verilog_result = self.run_verilog_simulation(
                    PE_name=self.name,
                    verilog_file=verilog_file,
                    output_file=self.output_buffer)

                correlations.append(
                    verilog_result[0])  # need as val, conv to arr later

        correlations = np.array(correlations)
        self.correlations = correlations
        return correlations

    def get_tooltip(self):
        tooltip_text = f"{self.name}\n"
        tooltip_text += f"Clock Frequency: {self.clk}\n"
        tooltip_text += f"Run Power Estimation: {self.rtl_power_estimation}\n"
        tooltip_text += f"RTL Simulation: {self.rtl_sim}\n"
        tooltip_text += f"Number of Channels: {self.num_channels}"
        return tooltip_text

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
