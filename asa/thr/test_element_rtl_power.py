from asa import THR

from asa.utils import INPUT_PE

import numpy as np


# run the pipeline to test the element
def test_thr_basic() -> None:

    input_val = 50
    input_val = np.array([50])

    input_pe = INPUT_PE(input=input_val, clk=0)

    thr_pe = THR(lower_bound=0,
                 upper_bound=100,
                 rtl_sim=True,
                 clk=16_000_000,
                 rtl_power_estimation=True,
                 save_visualization=True)

    # connect PEs
    input_pe.add_output(thr_pe)
    thr_pe.add_input(input_pe)

    # run end PE which recursively runs all previous PEs
    # output = thr_pe.run()

    elements = [input_pe, thr_pe]

    for pe in elements:
        pe.run()

    output = elements[-1].simulation_data['output_data']

    for element in elements:
        print(
            f"Element: {element.name}, visualisation generated: {element.save_visualization}"
        )

    power_dict = elements[-1].simulation_data["power_dict"]

    print(elements[-1].rtl_module_runs)

    for key, value in power_dict.items():
        print(f"{key}: {value}")


    print()
    print(f"assert test case not implemented yet, output:\n {output}")
    assert 1 == 1
