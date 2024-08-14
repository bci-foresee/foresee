from verilog_interface import VerilogInterface

interface = VerilogInterface()
# Example usage
a = 5
b = 2

c = interface.adder(a, b)
print(f"Adder result: {c}")

d = interface.subtractor(a, b)
print(f"Subtractor result: {d}")

e = interface.clocked_adder(a, b)
print(f"Clocked adder result: {e}")