import numpy as np
from numpy.typing import NDArray

from asa.processing_element import ProcessingElement

from signals.parent import Window
from pipelines.pipeline import Pipeline


def create_testing_pipeline(test_pe: ProcessingElement,
                            input_signal: NDArray[np.float32],
                            input_window: Window) -> Pipeline:

    # define the pipeline to test the fft PE
    class Standard_Pipe(Pipeline):

        def __init__(self):

            # initialise the parent class
            super().__init__(input_window=input_window)

            # add processing elements to the pipeline
            self.input_pe = INPUT_PE(input=input_signal)

            self.test_pe = test_pe

            # add PEs to list of elements
            self.add_elements([self.input_pe, self.test_pe])

            # define relationship between PEs
            self.add_edge(from_node=self.input_pe, to_node=self.test_pe)

        # run the end node of the pipeline, recursively running all the previous nodes
        def run(self):
            return self.test_pe.run()

    # create test pipeline
    pipeline = Standard_Pipe()
    return pipeline


class INPUT_PE(ProcessingElement):
    """
    Input PE

    Returns exactly what was input into the PE, allows for PE testing
    """
    name = "Input PE"

    def __init__(self, input: NDArray[np.float32], clk: int = 0) -> None:
        super().__init__(name=self.name, clk=clk, save_visualization=False)
        self.input = input

    def run(self) -> NDArray[np.float32]:
        input = self.input
        return input

    def __repr__(self) -> str:
        return f"{self.name}"


def generate_signal(frequencies: list[int], amplitudes: list[int], fs: int,
                    n_channels: int, n_samples: int) -> NDArray[np.float32]:

    sample_time = n_samples / fs

    sample_window = sample_time

    def signal1(t):
        returnSignal = 0
        for i in range(len(frequencies)):
            returnSignal += amplitudes[i] * np.sin(
                2 * np.pi * frequencies[i] * t)

        return returnSignal

    def constant_signal(t):
        return np.ones_like(t) * 2

    sampled_signals = []
    for i in range(n_channels):
        x = np.linspace(start=0,
                        stop=sample_window,
                        num=n_samples,
                        endpoint=False)
        if i == 0:
            sampled_signals.append(signal1(x))
        else:
            sampled_signals.append(constant_signal(x))

    return np.array(sampled_signals)
