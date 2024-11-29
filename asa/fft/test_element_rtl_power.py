from pipelines.pipeline import Pipeline
from signals.parent import Window
from asa import FFT, LOADER

from asa.utils import INPUT_PE, generate_signal


# run the pipeline to test the element
def test_fft_basic() -> None:

    # input signal window
    input_fs = 400
    input_channels = 1
    input_samples = 8192

    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=input_fs,
                                   n_channels=input_channels,
                                   n_samples=input_samples)

    input_pe = INPUT_PE(input=input_signal, clk=0)

    fft_pe = FFT(n_samples=input_samples,
                 fs=input_fs,
                 berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80),
                               (80, 180)],
                 clk=15_700_000,
                 rtl_sim=True,
                 rtl_power_estimation=True,
                 save_visualization=True)

    # connect PEs
    input_pe.add_output(fft_pe)
    fft_pe.add_input(input_pe)

    # run end PE which recursively runs all previous PEs
    output = fft_pe.run()

    elements = [input_pe, fft_pe]

    for element in elements:
        print(
            f"Element: {element.name}, visualisation generated: {element.save_visualization}"
        )
    print()
    print(
        f"assert test case not implemented yet, output shape:\n {output.shape}"
    )
    assert 1 == 1
