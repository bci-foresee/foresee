"""
This module takes in a sampled signal and performs the DFT using the FFT 
algorithm to provide a frequency domain representation of the signal.
"""

import numpy as np
import matplotlib.pyplot as plt

from component import ProcessingElement


class FFT(ProcessingElement):
    def __init__(self, name: str, points: list[float]):
        super().__init__(name)
        self.points = points

