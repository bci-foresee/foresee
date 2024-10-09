import sys

sys.path.append("./")

from seizure_shiao import Shiao_Pipe
from asa.utils import Window


def test_thr_basic() -> None:
    # input signal window
    # input signal window
    input_window = Window(fs=400, channels=2, samples=8000)

    input_window.generate_signal(frequencies=[10, 20, 40],
                                 amplitudes=[20, 15, 10])

    # # create test pipeline
    pipeline = Shiao_Pipe(input_window=input_window)
    pipeline.visualize()

    # output = pipeline.run()

    # for element in pipeline.elements:
    #     print(f"Element: {element.name}, visualisation generated: {element.save_visualization}")
    # print()
    # print(f"output:\n {output}")
    # assert 1 == 1, f"Expected 1 (all SVM weights = 0, therefore within threshold), but got {output}"


test_thr_basic()
