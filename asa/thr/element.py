
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
                 clk: int = 0, save_visualization: bool = False,
                 rtl_sim: bool = False, rtl_power_estimation: bool = False) -> None:
        
        super().__init__(name=self.name, 
                         clk=clk,
                         save_visualization=save_visualization,
                         rtl_sim=rtl_sim,
                         rtl_power_estimation=rtl_power_estimation)
        
        # no use of window atm
        self.lower_bound: float = lower_bound
        self.upper_bound: float = upper_bound
    
    def load_inputs(self) -> NDArray[np.float32]:
        input_PEs = self.inputs
        # concatenate input data from input PEs
        input_data = []
        for PE in input_PEs:
            input_data.append(PE.run()) # flatten because output of each PE is going to have multiple channels

        # concatenate input data
        # input_data = np.concatenate(input_data, axis=0)
        return np.array(input_data)
    
    def dimension_validate(self, input: NDArray[np.float32]) -> None:
        self.input_dimension = input.shape
        
        self.input_val_size = len(input)
        
        assert self.input_val_size == 1, f"THR only takes one input, got {self.input_val_size}"

    def compute(self, input: NDArray[np.int32]) -> float:

        value = input.item() # there should only be one item at this point

        if (self.lower_bound <= value) and (value <= self.upper_bound):
            return 1
        return 0
    
    def compute_verilog(self, input: NDArray[np.float32]) -> NDArray[np.float32]:
        
        # do if statements to choose between verilog implementations (ie how many points) here
        verilog_file = "thr"

        input_int = input[0].astype(np.int32)

        with open(self.input_buffer, 'w') as file:
            for i in range(1):
                # writing into the buffer in signed hex format
                file.write(f"{self.int_to_signedHex(input_int)} "
                        f"{self.int_to_signedHex(self.lower_bound)} "
                        f"{self.int_to_signedHex(self.upper_bound)}\n")

        verilog_result = self.run_verilog_simulation(verilog_file, self.output_buffer)

        return verilog_result
    
    def visualize(self):
        # nothing to vizualise
        pass

    def __repr__(self) -> str:
        return f"{self.name}"