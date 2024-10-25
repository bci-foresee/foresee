from asa import FFT, BBF, PWXC, SVM, THR

from asa.utils import INPUT_PE, generate_signal

import numpy as np


# run the pipeline to test the element
def test_pwxc_basic() -> None:

    # input signal window
    input_fs = 400
    # input_channels = 16
    input_channels = 1 # 1 for demonstration (speed)
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
    
    some_weights = np.ones(5)

    svm_pe = SVM(weights=some_weights,
                 clk=1,
                #  rtl_sim=False,
                 save_visualization=False)
    
    thr_pe = THR(lower_bound=0,
                 upper_bound=1,
                 clk=1,
                 rtl_sim=True,
                 rtl_power_estimation=True,
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
    assert 1 == 1
