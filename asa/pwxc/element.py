
import numpy as np
from numpy.typing import NDArray

from asa.parent import ProcessingElement


class PWXC(ProcessingElement):
    """
    Performs a pairwise cross correlation across a set > 2 signals
    """
    name = "PWXC"

    def __init__(self, clk: int = 0) -> None:
        super().__init__(self.name, clk)

    def run(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"{self.name}"