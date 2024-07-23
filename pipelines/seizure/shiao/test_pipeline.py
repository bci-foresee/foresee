
from pipelines.parent import Pipeline
from pipelines import Shiao_Pipe
from asa.utils import Window

def test_thr_basic() -> None:
    print()

    # input signal window
    # input signal window
    input_window = Window(fs=400, 
                          channels=2, 
                          samples=8000)
    
    input_window.generate_signal(frequencies=[10, 20, 40], 
                                 amplitudes=[20, 15, 10])

    # create test pipeline
    pipeline = Shiao_Pipe(input_window=input_window)
    
    output = pipeline.run()
    for element in pipeline.elements:
        print(f"Element: {element.name}, visualisation generated: {element.save_visualization}")
    print()
    print(f"output:\n {output}")
    assert output == 1, f"Expected 1 (all SVM weights = 0, therefore within threshold), but got {output}"