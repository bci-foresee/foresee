from asa import TKEO

from asa.utils import INPUT_PE, generate_signal


# run the pipeline to test the element
def test_tkeo_basic() -> None:

    # input signal window
    input_fs = 400
    input_channels = 2
    input_samples = 8192

    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=input_fs,
                                   n_channels=input_channels,
                                   n_samples=input_samples)

    input_pe = INPUT_PE(input=input_signal, clk=0)

    tkeo_pe = TKEO(n_channels=input_channels,
                   clk=1,
                   rtl_sim=True,
                   rtl_power_estimation=True,
                   save_visualization=False)

    # connect PEs
    input_pe.add_output(tkeo_pe)
    tkeo_pe.add_input(input_pe)

    # run end PE which recursively runs all previous PEs
    # output = fft_pe.run()

    elements = [input_pe, tkeo_pe]

    for pe in elements:
        pe.run()

    output = elements[-1].simulation_data['output_data']

    for element in elements:
        print(
            f"Element: {element.name}, visualisation generated: {element.save_visualization}"
        )
    print()
    print(
        f"assert test case not implemented yet, output shape:\n {output.shape}"
    )
    assert output.shape == (input_channels, input_samples)
