import numpy as np
from numpy.typing import NDArray

from asa.parent import ProcessingElement


class SVM(ProcessingElement):
    """
    Support Vector Machine (SVM)
    """
    name = "SVM"

    def __init__(self,
                 weights: NDArray[np.float32],
                 clk: int = 0,
                 save_visualization: bool = False) -> None:
        super().__init__(name=self.name,
                         clk=clk,
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

    def compute(self, features: NDArray[np.int32]) -> float:
        assert len(features) == len(self.weights)

        acc: float = 0
        for i in range(len(features)):
            acc += self.weights[i] * features[i]
        return acc

    def visualize(self) -> None:
        # nothing to visualise for SVM
        pass

    def __repr__(self) -> str:
        return f"{self.name}"
