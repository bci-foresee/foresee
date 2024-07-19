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
import numpy as np

def test_pipeline_basic() -> None:
    num_channels=2
    sample_window=10
    num_samples=1000
    frequencies=[10, 20, 40]
    amplitudes=[20, 15, 10]
    test_signal = sample_signals(num_channels=num_channels, 
                                            sample_window=sample_window, 
                                            num_samples=num_samples,
                                            frequencies=frequencies,
                                            amplitudes=amplitudes)

    sample_freq = num_samples / sample_window
    berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]

    pipeline = Sandbox_Pipe(num_channels=num_channels,
                    sample_window=sample_window,
                    num_samples=num_samples,
                    input_signal=test_signal,
                    berger_bands=berger_bands)
    
    output_features = pipeline.run()
    print(output_features)
    assert 1 == 1

# for testing purposes
# generates some sample signals
def sample_signals(num_channels, 
                sample_window, 
                num_samples,
                frequencies,
                amplitudes):

    # define a sampled function, and the sample
    def signal1(t):
        returnSignal = 0
        for i in range(len(frequencies)):
            returnSignal += amplitudes[i] * np.sin(2*np.pi*frequencies[i]*t)  

        return returnSignal
    
    def constant_signal(t):
        return np.ones_like(t) * 100
    
    def randomvals(t):
        return np.ones_like(t)
    
    sampled_signals = []
    for i in range(num_channels):
        x = np.linspace(start=0, stop=sample_window, num=num_samples, endpoint=False)
        if i == 0:
            sampled_signals.append(signal1(x))
        else:
            sampled_signals.append(randomvals(x))

    return np.array(sampled_signals)