from verilog_interface import VerilogInterface

import numpy as np

interface = VerilogInterface()

def generic_display(PE_name, inputs, outputs):
    print()
    print(f" ------------- {PE_name} ------------- ")
    print("Inputs:")
    for i in range(len(inputs)):
        print(f"in[{i}] = {inputs[i]}")
    print("Outputs:")
    for i in range(len(outputs)):
        print(f"out[{i}] = {outputs[i]}")
    print(" ------------------------------------ ")
    print()

# Example usage
a = 5
b = 2

c = interface.adder(a, b)
generic_display("Adder", [a, b], [c])

d = interface.subtractor(a, b)
generic_display("Subtractor", [a, b], [d])

a = np.array([5,6,7])
b = np.array([2,3,4])
e = interface.clocked_array_adder(a, b)
generic_display("Clocked Array Adder", [a, b], [e])
    
arr = np.zeros(8192, dtype=np.int16)
out = interface.spiral_fft_8192(arr)
print(out)