from asa import PWXC

from asa.utils import INPUT_PE, generate_signal

import numpy as np

# NO VERILOG IMPLEMENTATION YET


# run the pipeline to test the element
def test_pwxc_basic() -> None:

    # input signal window
    input_fs = 400
    input_channels = 16
    input_samples = 8192

    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=input_fs,
                                   n_channels=input_channels,
                                   n_samples=input_samples)

    input_pe = INPUT_PE(input=input_signal, clk=0)

    pwxc_pe = PWXC(n_channels=16, clk=1, rtl_sim=True, save_visualization=True)

    # connect PEs
    input_pe.add_output(pwxc_pe)
    pwxc_pe.add_input(input_pe)

    # run end PE which recursively runs all previous PEs
    # output = pwxc_pe.run()

    elements = [input_pe, pwxc_pe]

    for pe in elements:
        pe.run()

    output = elements[-1].simulation_data['output_data']

    for element in elements:
        print(
            f"Element: {element.name}, visualisation generated: {element.save_visualization}"
        )
    print()
    print(f"assert test case not implemented yet, output:\n {output}")
    assert 1 == 1
