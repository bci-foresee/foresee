# self.num_channels=2
# self.sample_window=10
# self.num_samples=1000
# self.frequencies=[10, 20, 40]
# self.amplitudes=[20, 15, 10]
# self.test_signal = self.sample_signals(num_channels=self.num_channels, 
#                                         sample_window=self.sample_window, 
#                                         num_samples=self.num_samples,
#                                         frequencies=self.frequencies,
#                                         amplitudes=self.amplitudes)

# self.sample_freq = self.num_samples / self.sample_window
# self.berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]

from pipelines import Sandbox_Pipe
from signals.components import Window
import numpy as np

def test_pipeline_basic() -> None:

    # input signal window
    input_window = Window(fs=1000, 
                          channels=2, 
                          samples=1000, 
                          berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)])
    
    input_window.generate_signal(frequencies=[10, 20, 40], amplitudes=[20, 15, 10])

    # create test pipeline
    pipeline = Sandbox_Pipe(input_window=input_window)
    
    output_features = pipeline.run()
    print(output_features)
    assert 1 == 1