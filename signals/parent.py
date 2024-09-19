import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple


# this class holds the input data dimensions and is capable of generating & holding the input data.
class Window:

    def __init__(self, fs: int, channels: int, samples: int) -> None:
        self.fs = fs
        self.n_channels = channels
        self.n_samples = samples
        self.sample_time = self.n_samples / self.fs  # how long the signal sampled is

    # set the input signal to some value
    def set_input_signal(self, input_signal: NDArray[np.float32]) -> None:
        self.input_signal = input_signal

    # generate a superposition of sinusoidal signals as the input
    def generate_signal(self, frequencies: list[int],
                        amplitudes: list[int]) -> NDArray[np.float32]:

        sample_window = self.sample_time

        def signal1(t):
            returnSignal = 0
            for i in range(len(frequencies)):
                returnSignal += amplitudes[i] * np.sin(
                    2 * np.pi * frequencies[i] * t)

            return returnSignal

        def constant_signal(t):
            return np.ones_like(t) * 2

        sampled_signals = []
        for i in range(self.n_channels):
            x = np.linspace(start=0,
                            stop=sample_window,
                            num=self.n_samples,
                            endpoint=False)
            if i == 0:
                sampled_signals.append(signal1(x))
            else:
                sampled_signals.append(constant_signal(x))
        self.input_signal = np.array(sampled_signals)

    # return the input value
    def load_signal(self) -> NDArray[np.float32]:
        if self.input_signal is None:
            raise ValueError("No input signal has been set")
        return self.input_signal
