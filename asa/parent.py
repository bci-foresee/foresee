"""
This file defines the base class for all hardware components
"""

import subprocess
import numpy as np
import struct

class ProcessingElement:
    def __init__(self, 
                name: str,
                clk: int = 0,
                rtl_sim: bool = False,
                save_visualization: bool = False) -> None:

        # name of the processing element
        self.name = name

        # clock frequency
        self.clk = clk

        # False means run python implementation, True means run verilog implementation
        self.rtl_sim = rtl_sim

        # save vizualisation of processing element
        self.save_visualization = save_visualization
        
        # i/o
        self.inputs = []
        self.outputs = []

        # name the input and output buffers - used for the verilog simulation
        self.input_buffer = "input_buffer.txt"
        self.output_buffer = "output_buffer.txt"
    
    # add inputs to the processing element
    def add_input(self, node: 'ProcessingElement') -> None:
        if node not in self.inputs:
            self.inputs.append(node)

    # add outputs from the processing element
    def add_output(self, node: 'ProcessingElement') -> None:
        if node not in self.outputs:
            self.outputs.append(node)

    # to run the PE's verilog implementation
    def run_verilog_simulation(self, verilog_file, output_file):
        # Run the Verilog simulation using Icarus Verilog or another Verilog simulator
        subprocess.run(["iverilog", "-o", "sim", verilog_file])
        subprocess.run(["vvp", "sim"])
        
        # Read the output
        numbers = []
        with open(output_file, 'r') as file:
            for line in file:
                # Split each line into words and convert each word from hex to int
                line_numbers = [int(word, base=16) for word in line.split()]
                numbers.extend(line_numbers)
        
        # Convert the list of numbers to a numpy array
        return np.array(numbers)

    # necessary method to run the processing element
    def run(self):
        # load input data
        # validate dimensions
        # compute
        # visualize
        # return data
        raise NotImplementedError("run method not implemented")
    
    def int_to_signedHex(self, value: int) -> str:
        item = f"{struct.unpack('I', struct.pack('i', value))[0]:08x}"
        return item
    
    # necessary method to load input data from input processing elements
    def load_inputs(self):
        raise NotImplementedError("run method not implemented")
    
    # necessary method to validate the dimensions of the input data
    def dimension_validate(self):
        raise NotImplementedError("run method not implemented")
    
    # necessary method to calculate processing element's computation
    def compute(self):
        raise NotImplementedError("run method not implemented")
    
    # method to compute using the verilog implementation of PE
    def compute_verilog(self):
        raise NotImplementedError("run method not implemented")
    
    # necessary method to validate the dimensions of the input data
    def vizualise(self):
        raise NotImplementedError("run method not implemented")

    # return way to identify the processing element
    def __repr__(self) -> str:
        return f"{self.name}"
