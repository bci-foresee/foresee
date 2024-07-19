
import numpy as np
from numpy.typing import NDArray

from asa.components import ProcessingElement

import matplotlib.pyplot as plt

import os


class LOADER(ProcessingElement):
    """
    Loader

    Loads in the generated signal so it can be given to output PEs
    
    Special unit that does not take in any input PEs, only output PEs
    """
    name = "Loader"

    def __init__(self, input: NDArray[np.float32],
                  clk: int = 0, save_vizualisation: bool = False) -> None:
        super().__init__(name = self.name, 
                         clk = clk,
                         save_vizualisation = save_vizualisation)
        self.input = input
        

    # takes in a signal 2d array (channels, num_samples) and returns itself.
    def run(self) -> NDArray[np.float32]:
        input = self.input
        # validate the input signal
        self.dimension_validate(input=input)
        # compute output
        output = self.compute(input=input)
        # vizualise the output (only if save_vizualisation is True)
        if self.save_vizualisation:
            self.vizualise(output)
        return output

    # function that gets the dimension of the input signal
    # in future can be used to validate input sizes
    def dimension_validate(self, input: NDArray[np.float32]) -> None:
        self.input_dimension = input.shape
        self.channels = self.input_dimension[0]
        self.num_samples = self.input_dimension[1]

    # this will compute on the input PEs and provide an output
    # loader is special case where inputs are not provided by PEs
    def compute(self, input: NDArray[np.float32]) -> NDArray[np.float32]:
        return input

    # vizualises data flow through PE and stores in /plots/ directory
    def vizualise(self, data: NDArray[np.float32]) -> None:
        # Create a figure and subplots for each channel
        fig, axs = plt.subplots(self.channels, 1, figsize=(10, 20), sharex=True)

        # Plot each channel
        for i in range(self.channels):
            axs[i].plot(data[i])
            axs[i].set_ylabel(f'Channel {i+1}')

        # Set common labels
        axs[-1].set_xlabel('Time (ms)')
        fig.suptitle(f'iEEG Data Visualization shape: {self.input_dimension}')

        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Ensure the directory exists
        output_dir = 'plots'
        os.makedirs(output_dir, exist_ok=True)

        # Save the figure in the plots/ directory
        plt.savefig(os.path.join(output_dir, 'input_signal.png'))

    def __repr__(self) -> str:
        return f"{self.name}"
