from asa import FFT, BBF, PWXC, SVM, THR

from asa.utils import INPUT_PE, generate_signal

import numpy as np


# run the pipeline to test the element
def test_sandbox_pipeline() -> None:

    # input signal window
    input_fs = 400
    # input_channels = 16
    input_channels = 16  # 1 for demonstration (speed)
    input_samples = 8192

    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=input_fs,
                                   n_channels=input_channels,
                                   n_samples=input_samples)

    input_pe = INPUT_PE(input=input_signal, clk=0)

    # bbf
    # def __init__(self,
    #              fs: int,
    #              berger_bands: List[Tuple[int, int]],
    #              clk: int = 0,
    #              save_visualization: bool = False) -> None:
    #     super().__init__(name=self.name,
    #                      clk=clk,
    #                      save_visualization=save_visualization)

    bbf_pe = BBF(fs=input_fs,
                 berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80),
                               (80, 180)],
                 clk=1,
                 save_visualization=False)

    # pwxc
    #  def __init__(self,
    #              n_channels: int,
    #              clk: int = 0,
    #              save_visualization: bool = False,
    #              rtl_sim: bool = False,
    #              rtl_power_estimation: bool = False) -> None:

    #     super().__init__(name=self.name,
    #                      clk=clk,
    #                      save_visualization=save_visualization,
    #                      rtl_sim=rtl_sim,
    #                      rtl_power_estimation=rtl_power_estimation)

    pwxc_pe = PWXC(n_channels=input_channels,
                   clk=1,
                   save_visualization=False,
                   rtl_sim=False,
                   rtl_power_estimation=False)

    # input_pe.run()
    # bbf_pe.run()
    # pwxc_pe.run()

    # make PWXC work for 2 channel correlation
    # repeat

    #

    # check output dimensions
    # print(f"BBF output shape: {bbf_pe.simulation_data['output_data'].shape}")
    # print(f"PWXC output shape: {pwxc_pe.simulation_data['output_data'].shape}")

    fft_pe = FFT(berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80),
                               (80, 180)],
                 n_samples=input_samples,
                 fs=input_fs,
                 clk=1,
                 rtl_sim=False,
                 save_visualization=False)

    some_weights = np.ones(312)

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

    bbf_pe.add_input(input_pe)
    bbf_pe.add_output(svm_pe)

    pwxc_pe.add_input(input_pe)
    pwxc_pe.add_output(svm_pe)

    fft_pe.add_input(input_pe)
    fft_pe.add_output(svm_pe)

    svm_pe.add_input(fft_pe)
    svm_pe.add_input(pwxc_pe)
    svm_pe.add_input(bbf_pe)

    svm_pe.add_output(thr_pe)

    thr_pe.add_input(svm_pe)

    # run end PE which recursively runs all previous PEs
    # output = thr_pe.run()

    # for element in elements, run

    elements = [input_pe, bbf_pe, pwxc_pe, fft_pe, svm_pe, thr_pe]

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
