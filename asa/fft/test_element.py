from pipelines.parent import Pipeline
from signals.parent import Window
from asa import FFT, LOADER
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt

# define the pipeline to test the fft PE
class FFT_Pipe(Pipeline):

    def __init__(self, 
                 input_window: Window):
        
        super().__init__(input_window=input_window)

        self.loader = LOADER(input=input_window.load_signal(),
                      save_vizualisation=True)
        
        self.fft = FFT(window=input_window,
                       berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)],
                       save_vizualisation=True)
       
        self.add_elements([self.loader, self.fft])

        self.add_edge(from_node=self.loader, to_node=self.fft)

    def run(self):
        return self.fft.run()
    

# test the pipeline
def test_fft_basic() -> None:

    # input signal window
    input_window = Window(fs=1000, 
                          channels=2, 
                          samples=1000)
    
    input_window.generate_signal(frequencies=[10, 20, 40], 
                                 amplitudes=[20, 15, 10])

    # create test pipeline
    pipeline = FFT_Pipe(input_window=input_window)
    
    output_features = pipeline.run()
    print(output_features)
    assert 1 == 1