from verilog_interface import VerilogInterface

import numpy as np

interface = VerilogInterface()
# Example usage
a = 5
b = 2

c = interface.adder(a, b)
print(f"Adder result: {c}")

d = interface.subtractor(a, b)
print(f"Subtractor result: {d}")

a = np.array([5,6,7])
b = np.array([2,3,4])

e = interface.clocked_adder(a, b)
print(f"Inputs: {a}, {b}")
print(f"Clocked adder result: {e}")