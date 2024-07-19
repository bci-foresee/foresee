
import numpy as np
from numpy.typing import NDArray

from asa.components import ProcessingElement


class LOADER(ProcessingElement):
    """
    Loader

    Loads in the generated signal so it can be given to output PEs
    
    Special unit that does not take in any input PEs, only output PEs
    """
    name = "Loader"

    def __init__(self, clk: int = 0, save_vizualisation: bool = False) -> None:
        super().__init__(name = self.name, 
                         clk = clk,
                         save_vizualisation = False)
        

    # takes in a signal 2d array (channels, num_samples) and returns itself.
    def run(self, input: NDArray[np.float32]) -> NDArray[np.float32]:

        # validate the input signal
        self.dimension_validate(input=input)

        # compute output
        output = self.compute(input=input)

        return output


    # function that gets the dimension of the input signal
    # in future can be used to validate input sizes
    def dimension_validate(self, input: NDArray[np.float32]) -> None:
        self.input_dimension = input.shape

    # this will compute on the input PEs and provide an output
    # loader is special case where inputs are not provided by PEs
    def compute(self, input: NDArray[np.float32]) -> NDArray[np.float32]:
        return input

    def vizualise(): # need to make these necessary functions
        pass

    def __repr__(self) -> str:
        return f"{self.name}"
