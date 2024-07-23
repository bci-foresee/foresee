
from asa.parent import ProcessingElement
from signals.parent import Window

import numpy as np
from numpy.typing import NDArray

class THR(ProcessingElement):
    """
    Thresholding element
    """
    name = "THR"

    def __init__(self, lower_bound: float, upper_bound: float, 
                 clk: int = 0, save_visualization: bool = False) -> None:
        
        super().__init__(name=self.name, 
                         clk=clk,
                         save_visualization=save_visualization)
        
        # no use of window atm
        self.lower_bound: float = lower_bound
        self.upper_bound: float = upper_bound

    def run(self) -> NDArray[np.float32]:
        # load input data
        input_data = self.load_inputs()
        # validate dimensions
        self.dimension_validate(input=input_data)
        # compute
        output = self.compute(input=input_data)
        # vizualise
        if self.save_visualization:
            self.visualize()
        # return data
        return output
    
    def load_inputs(self) -> NDArray[np.float32]:
        input_PEs = self.inputs
        # concatenate input data from input PEs
        input_data = []
        for PE in input_PEs:
            input_data.append(PE.run().flatten()) # flatten because output of each PE is going to have multiple channels

        # concatenate input data
        input_data = np.concatenate(input_data, axis=0)
        return input_data
    
    def dimension_validate(self, input: NDArray[np.float32]) -> None:
        self.input_dimension = input.shape
        
        self.input_val_size = len(input)
        
        assert self.input_val_size == 1, f"THR only takes one input, got {self.input_val_size}"

    def compute(self, input: NDArray[np.int32]) -> float:

        value = input.item() # there should only be one item at this point

        if (self.lower_bound <= value) and (value <= self.upper_bound):
            return 1
        return 0
    
    def visualize(self):
        # nothing to vizualise
        pass

    def __repr__(self) -> str:
        return f"{self.name}"