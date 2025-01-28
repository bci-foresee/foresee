from asa import AVG

from asa.utils import INPUT_PE, generate_signal


# run the pipeline to test the element
def test_avg_basic() -> None:

    # input signal window
    input_fs = 400
    input_channels = 2
    input_samples = 8192

    hardware_runs = 8192 # for demonstration, how many times the hardware runs for one valid output signal

    clk_freq = input_fs * input_channels

    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=input_fs,
                                   n_channels=input_channels,
                                   n_samples=input_samples)

    input_pe = INPUT_PE(input=input_signal, clk=0)

    avg_pe = AVG(n_channels=input_channels,
                 clk=clk_freq,
                 rtl_sim=True,
                 rtl_power_estimation=True,
                 save_visualization=False)

    # connect PEs
    input_pe.add_output(avg_pe)
    avg_pe.add_input(input_pe)

    # run end PE which recursively runs all previous PEs
    # output = fft_pe.run()

    elements = [input_pe, avg_pe]

    for pe in elements:
        pe.run()

    output = elements[-1].simulation_data['output_data']

    for element in elements:
        print(
            f"Element: {element.name}, visualisation generated: {element.save_visualization}"
        )
    print()
    for element in elements:
        for key, value in element.simulation_data.items():
            print(f"{element.name}.{key} = {value}")
        print()

    print(output)
    assert output.shape == (input_channels, )
