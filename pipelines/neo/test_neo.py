from asa import TKEO, AVG, SVM, THR

from asa.utils import INPUT_PE, generate_signal

import numpy as np


# run the pipeline to test the element
def test_sandbox_pipeline() -> None:

    # input signal window
    input_fs = 400
    # input_channels = 16
    input_channels = 2  # 1 for demonstration (speed)
    input_samples = 8192

    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=input_fs,
                                   n_channels=input_channels,
                                   n_samples=input_samples)

    input_pe = INPUT_PE(input=input_signal, clk=0)

    tkeo_pe = TKEO(n_channels=input_channels,
                   clk=1,
                   rtl_sim=False,
                   rtl_power_estimation=False,
                   save_visualization=False)

    avg_pe = AVG(n_channels=input_channels,
                 clk=1,
                 rtl_sim=False,
                 rtl_power_estimation=False,
                 save_visualization=False)

    some_weights = np.ones(input_channels)

    svm_pe = SVM(weights=some_weights,
                 clk=1,
                 rtl_sim=False,
                 rtl_power_estimation=False,
                 save_visualization=False)

    thr_pe = THR(lower_bound=0,
                 upper_bound=1,
                 clk=15_700_000,
                 rtl_sim=False,
                 rtl_power_estimation=False,
                 save_visualization=False)

    # connect PEs
    input_pe.add_output(tkeo_pe)

    tkeo_pe.add_input(input_pe)
    tkeo_pe.add_output(avg_pe)

    avg_pe.add_input(tkeo_pe)
    avg_pe.add_output(svm_pe)

    svm_pe.add_input(avg_pe)
    svm_pe.add_output(thr_pe)

    thr_pe.add_input(svm_pe)

    # run end PE which recursively runs all previous PEs
    # output = thr_pe.run()

    # for element in elements, run

    elements = [input_pe, tkeo_pe, avg_pe, svm_pe, thr_pe]

    for pe in elements:
        pe.run()

    output = thr_pe.simulation_data['output_data']

    # print("--------------------")
    # print(output)
    # print("--------------------")

    for element in elements:
        print(
            f"Element: {element.name}, visualisation generated: {element.save_visualization}"
        )

    print()
    print(f"assert test case not implemented yet, output:\n {output}")
    print()

    for element in elements:
        for key, value in element.simulation_data.items():
            print(f"{element.name}.{key} = {value}")
        print()

    # Save CSV

    assert 1 == 1
