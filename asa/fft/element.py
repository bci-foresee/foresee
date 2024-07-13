
import numpy as np
import matplotlib.pyplot as plt

from asa.components import ProcessingElement


class FFT(ProcessingElement):
    """
    Performs the Discrete Fourier Transform (DFT) using the Fast Fourier 
    Transform (FFT) algorithm.
    """
    name = "FFT"

    def __init__(self, points: list[float]):
        super().__init__(self.name)

        self.points = points

