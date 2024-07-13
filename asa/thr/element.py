
from asa.components import ProcessingElement


class THR(ProcessingElement):
    """
    Thresholding element
    """
    name = "THR"

    def __init__(self, lower_bound: float, upper_bound: float, clk: int = 0):
        super().__init__(self.name, clk)

        self.lower_bound: float = lower_bound
        self.upper_bound: float = upper_bound

    def run(self, value: float):
        if (self.lower_bound <= value) and (value <= self.upper_bound):
            return 1
        return 0
