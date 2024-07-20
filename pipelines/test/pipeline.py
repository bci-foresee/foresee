
from pipelines.components import Pipeline
from signals.components import Window
from asa import FFT, LOADER
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt


class Sandbox_Pipe(Pipeline):

    def __init__(self, 
                 input_window: Window):
        
        super().__init__(input_window=input_window)
        
        # self.num_channels=num_channels
        # self.sample_window=sample_window
        # self.num_samples=num_samples
        
        # self.test_signal = input_signal

        # self.sample_freq = self.num_samples / self.sample_window
        # self.berger_bands=berger_bands

        self.loader = LOADER(input=input_window.load_signal(),
                      save_vizualisation=True)
        
        self.fft = FFT(points=input_window.n_samples, 
                       sample_freq=input_window.fs, 
                       berger_bands=input_window.berger_bands,
                       save_vizualisation=True)
       

        self.add_elements([self.loader, self.fft])

        self.add_edge(from_node=self.loader, to_node=self.fft)




    def run(self):
        return self.fft.run()



