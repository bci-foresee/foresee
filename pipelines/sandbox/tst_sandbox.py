import sys

sys.path.append("./")

# from sandbox import Sandbox_Pipe

from signals.parent import Window
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

    fft_pe = FFT(berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80)],
                 n_samples=input_samples,
                 fs=input_fs,
                 clk=1,
                 rtl_sim=False,
                 save_visualization=False)

    some_weights = np.ones(10)

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
    input_pe.add_output(fft_pe)

    fft_pe.add_input(input_pe)
    fft_pe.add_output(svm_pe)

    svm_pe.add_input(fft_pe)
    svm_pe.add_output(thr_pe)

    thr_pe.add_input(svm_pe)

    # run end PE which recursively runs all previous PEs
    output = thr_pe.run()

    elements = [input_pe, fft_pe, svm_pe, thr_pe]

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

    output_features = pipeline.run()
    print(output_features)
    pipeline.visualize()
    assert 1 == 1


test_sandbox_pipeline()
