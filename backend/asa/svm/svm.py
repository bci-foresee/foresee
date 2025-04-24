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
                # PE.run().flatten()
                PE.simulation_data['output_data'].flatten()
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
        return np.array([acc])

    def compute_verilog(self, input: NDArray[np.float32]) -> np.int64:
        """
        Computes the dot product using the Verilog 'svm' module with external weights.

        Args:
            input (NDArray[np.float32]): The input vector for the SVM computation.
            self.weights (NDArray[np.float32]): The weight vector for the SVM computation.

        Returns:
            np.int64: The result of the dot product computation.
        """

        self.rtl_single_module_runs = 1  # verilog is run 1 time to emulate hardware

        # Convert input and weights to appropriate integer types (e.g., int32)
        input_int = input.astype(np.int32)
        weights_int = self.weights.astype(np.int32)

        # Ensure the input arrays have the correct length
        if input_int.size >= 32 * 32:
            raise ValueError(
                f"Input signal must be less than length {32 * 32}.")
        if weights_int.size != input_int.size:
            raise ValueError(
                f"Weight vector must be of length {input_int.size}, same as input weights vector."
            )

        # Pad input_int and weights_int with zeros if their length is not 16*16
        # "Two deep SVM", do SVM once (size 16), then do SVM on result with weights[i] == 1
        if input_int.size <= 32 * 32:
            input_int = np.pad(input_int, (0, 32 * 32 - input_int.size),
                               'constant')
            weights_int = np.pad(weights_int, (0, 32 * 32 - weights_int.size),
                                 'constant')

        # SVM one
        layer_one_result = np.zeros(32)

        # Define file names for the input and output buffers
        self.input_buffer = 'input_buffer.txt'
        self.weights_buffer = 'weights_buffer.txt'
        self.output_result = 'output_buffer.txt'

        for i in range(32):

            curr_input = input_int[i * 32:(i + 1) * 32]
            curr_weights = weights_int[i * 32:(i + 1) * 32]

            # Write input to "input_data.txt"
            with open(self.input_buffer, 'w') as file_in:
                for sample in curr_input:
                    # Writing each sample as a signed hex string
                    file_in.write(f"{self.int_to_signedHex(sample)}\n")

            # Write weights to "weights_data.txt"
            with open(self.weights_buffer, 'w') as file_weights:
                for weight in curr_weights:
                    # Writing each weight as a signed hex string
                    file_weights.write(f"{self.int_to_signedHex(weight)}\n")

            # Run the Verilog simulation
            verilog_result = self.run_verilog_simulation(
                PE_name=self.name,
                verilog_file='svm',
                output_file=self.output_result)

            layer_one_result[i] = verilog_result

            # print(f"Layer_one [{i}]: {layer_one_result[i]}")

        # SVM two
        result_int = 0

        curr_input = layer_one_result.astype(np.int32)
        curr_weights = np.ones(32).astype(np.int32)

        # Write input to "input_data.txt"
        with open(self.input_buffer, 'w') as file_in:
            for sample in curr_input:
                # Writing each sample as a signed hex string
                file_in.write(f"{self.int_to_signedHex(sample)}\n")

        # Write weights to "weights_data.txt"
        with open(self.weights_buffer, 'w') as file_weights:
            for weight in curr_weights:
                # Writing each weight as a signed hex string
                file_weights.write(f"{self.int_to_signedHex(weight)}\n")

        # Run the Verilog simulation
        verilog_result = self.run_verilog_simulation(
            PE_name=self.name,
            verilog_file='svm',
            output_file=self.output_result)

        # print(f"Layer_two: {verilog_result}")

        return np.array([verilog_result])

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
