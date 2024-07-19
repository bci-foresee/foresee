
from pipelines.components import Pipeline
from asa import FFT, LOADER
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt


class Sandbox_Pipe(Pipeline):

    def __init__(self, 
                 num_channels:int,
                 sample_window:int,
                 num_samples:int,
                 input_signal:NDArray[np.float32],
                 berger_bands: list[tuple[int, int]]):
        
        super().__init__()
        
        self.num_channels=num_channels
        self.sample_window=sample_window
        self.num_samples=num_samples
        
        self.test_signal = input_signal

        self.sample_freq = self.num_samples / self.sample_window
        self.berger_bands=berger_bands

        self.loader = LOADER(input=self.test_signal,
                      save_vizualisation=True)
        
        self.fft = FFT(points=self.num_samples, 
                       sample_freq=self.sample_freq, 
                       berger_bands=self.berger_bands,
                       save_vizualisation=True)
       

        self.add_elements([self.loader, self.fft])

        self.add_edge(from_node=self.loader, to_node=self.fft)




    def run(self):
        return self.fft.run()



