from pipelines.parent import Pipeline
from signals.parent import Window
from asa import FFT, LOADER

from asa.utils import INPUT_PE, generate_signal
    

# run the pipeline to test the element
def test_fft_basic() -> None:

    # input signal window
    input_window = Window(fs=400, 
                          channels=2, 
                          samples=8000)
    
    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=400,
                                   n_channels=2,
                                   n_samples=8000)

    input_pe = INPUT_PE(input=input_signal,
                        clk=0)
    
    fft_pe = FFT(window=input_window,
                 berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)],
                 clk=1,
                 save_vizualisation=True)
    
    # connect PEs
    input_pe.add_output(fft_pe)
    fft_pe.add_input(input_pe)
    
    # run end PE which recursively runs all previous PEs
    output = fft_pe.run()

    elements = [input_pe, fft_pe]

    for element in elements:
        print(f"Element: {element.name}, visualisation generated: {element.save_vizualisation}")
    print()
    print(f"assert test case not implemented yet, output shape:\n {output.shape}")
    assert 1 == 1