from asa import PWXC

from asa.utils import INPUT_PE, generate_signal

import numpy as np

# NO VERILOG IMPLEMENTATION YET


# run the pipeline to test the element
def test_pwxc_basic() -> None:

    # input signal window
    input_fs = 400
    input_channels = 2
    input_samples = 8192

    clk_freq = input_fs * 16 # for 16 input_channels, demo purposes

    # input_signal = generate_signal(frequencies=[10, 20, 40],
    #                                amplitudes=[20, 15, 10],
    #                                fs=input_fs,
    #                                n_channels=input_channels,
    #                                n_samples=input_samples)

    input_signal = np.zeros((input_channels, input_samples))


    input_pe = INPUT_PE(input=input_signal, clk=0)

    pwxc_pe = PWXC(n_channels=input_channels,
                   clk=clk_freq,
                   rtl_sim=True,
                   rtl_power_estimation=True,
                   save_visualization=False)

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

    for key, value in pwxc_pe.simulation_data.items():
        print(f"{element.name}.{key} = {value}")
    print()


    output.shape == (input_channels, 6)
