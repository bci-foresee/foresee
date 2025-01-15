# from asa import SVM

# from asa.utils import INPUT_PE, generate_signal

# import numpy as np


# # run the pipeline to test the element
# def test_pwxc_basic() -> None:

#     # input
#     input_arr = np.ones(10)

#     # input weights
#     input_weights = np.ones(10)

#     input_pe = INPUT_PE(input=input_arr, clk=0)

#     svm_pe = SVM(weights=input_weights,
#                  clk=1,
#                  rtl_sim=True,
#                  rtl_power_estimation=False,
#                  save_visualization=True)

#     # connect PEs
#     input_pe.add_output(svm_pe)
#     svm_pe.add_input(input_pe)

#     # run end PE which recursively runs all previous PEs
#     # output = svm_pe.run()

#     elements = [input_pe, svm_pe]

#     # elements = [input_pe, fft_pe]

#     for pe in elements:
#         pe.run()

#     output = elements[-1].simulation_data['output_data']

#     for element in elements:
#         print(
#             f"Element: {element.name}, visualisation generated: {element.save_visualization}"
#         )
#     print()
#     print(f"assert test case not implemented yet, output:\n {output}")
#     print(f"input_arr: {input_arr}")
#     print(f"input_weights: {input_weights}")

#     assert 1 == 1
