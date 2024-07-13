
import numpy as np
from numpy.typing import NDArray

from asa.components import ProcessingElement


class BBF(ProcessingElement):
    """
    Butterworth Bandpass Filter (BBF)
    """
    name = "BBF"

    def __init__(self, clk: int = 0):
        super().__init__(self.name, clk)

    def run(self):
        pass
