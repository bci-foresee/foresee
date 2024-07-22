from pipelines.parent import Pipeline
from signals.parent import Window
from asa import FFT, LOADER

from asa.utils import create_testing_pipeline, generate_signal
    

# run the pipeline to test the element
def test_fft_v4() -> None:

    # input signal window
    # need to define signal properties for the input signal
    input_window = Window(fs=400, channels=2, samples=8000)
    
    # generate an input signal
    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=400,
                                   n_channels=2,
                                   n_samples=8000)
    
    # create the PE you want to test
    fft_pe = FFT(n_samples=8000,
                 fs=400,
                 berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)],
                 clk=1,
                 save_vizualisation=True)
    
    # run the pipeline
    output = fft_pe.compute(input=input_signal)

    print()
    print(f"assert test case not implemented yet, output shape:\n {output.shape}")
    assert 1 == 1