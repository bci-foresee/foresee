"""
This file defines the base class for all hardware components
"""

class ProcessingElement:
    def __init__(self, name: str,
                clk: int = 0,
                save_vizualisation: bool = False) -> None:

        # name of the processing element
        self.name = name

        # clock frequency
        self.clk = clk

        # save vizualisation of processing element
        self.save_vizualisation = save_vizualisation
        
        # i/o
        self.inputs = []
        self.outputs = []
    
    # add inputs to the processing element
    def add_input(self, node: 'ProcessingElement') -> None:
        if node not in self.inputs:
            self.inputs.append(node)

    # add outputs from the processing element
    def add_output(self, node: 'ProcessingElement') -> None:
        if node not in self.outputs:
            self.outputs.append(node)

    # necessary method to run the processing element
    def run(self):
        raise NotImplementedError("run method not implemented")

