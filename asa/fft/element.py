
import numpy as np

from asa.components import ProcessingElement


class FFT(ProcessingElement):
    """
    Performs the Discrete Fourier Transform (DFT) using the Fast Fourier 
    Transform (FFT) algorithm.
    """
    name = "FFT"

    def __init__(self, points: int, clk: int = 0) -> None:
        super().__init__(self.name, clk)

        self.points = points

    def __repr__(self) -> str:
        return f"{self.name}_{self.points}"
