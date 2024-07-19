"""
This file defines the base class for all hardware components
"""

# from pipelines.components import Pipeline

class ProcessingElement:
    def __init__(self, 
                name: str,
                #pipeline: Pipeline, # possible in future
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

        # define parent pipeline.
        # needed to get information like sampling rate
        # self.pipeline = pipeline
    
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
        # load input data
        # validate dimensions
        # compute
        # vizualise
        # return data
        raise NotImplementedError("run method not implemented")
    
    # necessary method to load input data from input processing elements
    def load_inputs(self):
        raise NotImplementedError("run method not implemented")
    
    # necessary method to calculate processing element's computation
    def compute(self):
        raise NotImplementedError("run method not implemented")
    
    # necessary method to validate the dimensions of the input data
    def vizualise(self):
        raise NotImplementedError("run method not implemented")

