import sys

sys.path.append("./")

import numpy as np
from numpy.typing import NDArray

# from app.static.processing_elements.processing_element import ProcessingElement
from asa.processing_element import ProcessingElement

class SVM(ProcessingElement):
    """
    Support Vector Machine (SVM)
    """
    name = "SVM"

    def __init__(self,
                 weights: NDArray[np.float32],
                 clk: int = 0,
                 rtl_sim: bool = False,
                 rtl_power_estimation: bool = False,
                 save_visualization: bool = False) -> None:
        super().__init__(name=self.name,
                         clk=clk,
                         rtl_sim=rtl_sim,
                         rtl_power_estimation=rtl_power_estimation,
                         save_visualization=save_visualization)

        self.weights: NDArray[np.int32] = weights

    def load_inputs(self) -> NDArray[np.float32]:
        input_PEs = self.inputs
        # concatenate input data from input PEs
        input_data = []
        for PE in input_PEs:
            input_data.append(
                PE.run().flatten()
            )  # flatten because output of each PE is going to have multiple channels

        # concatenate input data
        input_data = np.concatenate(input_data, axis=0)
        return input_data

    def dimension_validate(self, input: NDArray[np.float32]) -> None:
        self.input_dimension = input.shape

        self.input_val_size = len(input)

        assert len(
            self.weights
        ) == self.input_val_size, f"Input size {self.input_val_size} does not match weights size {len(self.weights)}"

    def compute(self, input: NDArray[np.int32]) -> float:
        assert len(input) == len(self.weights)

        acc: float = 0
        for i in range(len(input)):
            acc += self.weights[i] * input[i]
        return acc
    
    def compute_verilog(self, input: NDArray[np.float32]) -> np.int64:
        """
        Computes the dot product using the Verilog 'svm' module with external weights.

        Args:
            input (NDArray[np.float32]): The input vector for the SVM computation.
            self.weights (NDArray[np.float32]): The weight vector for the SVM computation.

        Returns:
            np.int64: The result of the dot product computation.
        """

        # Convert input and weights to appropriate integer types (e.g., int32)
        input_int = input.astype(np.int32)
        weights_int = self.weights.astype(np.int32)

        # Ensure the input arrays have the correct length
        if input_int.size != 10:
            raise ValueError(f"Input signal must be of length {10}.")
        if weights_int.size != 10:
            raise ValueError(f"Weight vector must be of length {10}.")

        # Define file names for the input and output buffers
        self.input_buffer = 'input_data.txt'
        self.weights_buffer = 'weights_data.txt'
        self.output_result = 'output_result.txt'

        # Write input to "input_data.txt"
        with open(self.input_buffer, 'w') as file_in:
            for sample in input_int:
                # Writing each sample as a signed hex string
                file_in.write(f"{self.int_to_signedHex(sample)}\n")

        # Write weights to "weights_data.txt"
        with open(self.weights_buffer, 'w') as file_weights:
            for weight in weights_int:
                # Writing each weight as a signed hex string
                file_weights.write(f"{self.int_to_signedHex(weight)}\n")

        # Run the Verilog simulation
        verilog_result = self.run_verilog_simulation(
            PE_name=self.name,
            verilog_file='svm',
            output_file=self.output_result)

        # The result is expected to be in decimal format, read and convert it
        with open(self.output_result, 'r') as f:
            result_str = f.readline().strip()
            result_int = int(result_str, 10)  # Assuming decimal format

        return np.array([result_int])

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
