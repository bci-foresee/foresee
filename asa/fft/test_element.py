import numpy as np

from asa import FFT, LOADER

def test_fft_basic() -> None:

    # generate signal into system
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

    #initialize loader block to provide inputs for fft
    loader = LOADER(input=test_signal,
        save_vizualisation=True)

    # initialize fft block
    fft = FFT(points=num_samples, 
              sample_freq=sample_freq, 
              berger_bands=berger_bands,
              save_vizualisation=True)

    # add inputs to fft
    fft.add_input(loader)

    # run fft block
    output_features = fft.run()

    # expected result

    # assert np.allclose(result, expected_result), f"Expected {expected_result}, but got {result}"
    
    '''IMPLEMENT TEST CASE'''
    assert 1 == 1


import numpy as np
import matplotlib.pyplot as plt

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