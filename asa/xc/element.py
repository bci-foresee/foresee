
import numpy as np
from numpy.typing import NDArray

from asa.parent import ProcessingElement


class XC(ProcessingElement):
    """
    This is the Cross Correlation (XC) PE which is a basic similarity measure 
    between two signals.
    """
    name = "XC"

    def __init__(self, clk: int = 0) -> None:
        super().__init__(self.name, clk)

    def run(self, signal_a: NDArray[np.int16], signal_b: NDArray[np.int16]) -> float:
        assert len(signal_a) == len(signal_b)

        acc: float = 0 # this typing doesnt actually work.
        for i in range(len(signal_a)):
           acc += signal_a[i] * signal_b[i] 

        #print(type(acc)) # comment when done
        return acc

    def __repr__(self) -> str:
        return f"{self.name}"
