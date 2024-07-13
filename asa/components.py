"""
This file defines the base class for all hardware components
"""

class ProcessingElement:
    def __init__(self, name: str, clk: int = 0):
        self.name = name

        self.clk = clk
        self.inputs = []
        self.outputs = []
    
    def add_input(self, node: 'ProcessingElement') -> None:
        if node not in self.inputs:
            self.inputs.append(node)

    def add_output(self, node: 'ProcessingElement') -> None:
        if node not in self.outputs:
            self.outputs.append(node)

