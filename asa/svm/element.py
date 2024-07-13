
import numpy as np
from numpy.typing import NDArray

from asa.components import ProcessingElement


class SVM(ProcessingElement):
    """
    Support Vector Machine (SVM)
    """
    name = "SVM"

    def __init__(self, weights: NDArray[np.float32], clk: int = 0):
        super().__init__(self.name, clk)

        self.weights: NDArray[np.int32] = weights

    def run(self, features: NDArray[np.int32]) -> float:
        assert len(features) == len(self.weights)

        acc: float = 0
        for i in range(len(features)):
           acc += self.weights[i] * features[i] 
        return acc

    def __repr__(self) -> str:
        return f"{self.name}"
