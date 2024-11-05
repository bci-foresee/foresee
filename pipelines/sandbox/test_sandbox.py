import sys

sys.path.append("./")

from sandbox import Sandbox_Pipe
from signals.parent import Window
import numpy as np


def test_pipeline_basic() -> None:

    # input signal window
    input_window = Window(fs=1000, channels=2, samples=1000)

    input_window.generate_signal(frequencies=[10, 20, 40],
                                 amplitudes=[20, 15, 10])

    # create test pipeline
    pipeline = Sandbox_Pipe(input_window=input_window)

    output_features = pipeline.run()
    print(output_features)
    pipeline.visualize()
    assert 1 == 1


test_pipeline_basic()
