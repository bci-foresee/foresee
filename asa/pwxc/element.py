
import numpy as np
from numpy.typing import NDArray

from asa.components import ProcessingElement


class PWXC(ProcessingElement):
    """
    Performs a pairwise cross correlation across a set > 2 signals
    """
    name = "PWXC"

    def __init__(self, clk: int = 0):
        super().__init__(self.name, clk)

    def run(self):
        pass
