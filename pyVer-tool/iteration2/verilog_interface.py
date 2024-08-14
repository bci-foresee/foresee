import subprocess

import subprocess

class VerilogInterface:

    def run_verilog_simulation(self, verilog_file, output_file):
        # Run the Verilog simulation using Icarus Verilog or another Verilog simulator
        subprocess.run(["iverilog", "-o", "sim", verilog_file])
        subprocess.run(["vvp", "sim"])
        
        # Read the output
        with open(output_file, 'r') as file:
            result = int(file.read().strip(), 16)  # Assuming hexadecimal format
        return result

    def adder(self, a, b):
        with open("adder_input.txt", 'w') as file:
            file.write(f"{a:08x} {b:08x}\n")  # Write inputs in hexadecimal

        result = self.run_verilog_simulation("adder.v", "adder_output.txt")
        return result

    def subtractor(self, a, b):
        with open("subtractor_input.txt", 'w') as file:
            file.write(f"{a:08x} {b:08x}\n")  # Write inputs in hexadecimal

        result = self.run_verilog_simulation("subtractor.v", "subtractor_output.txt")
        return result
    
    def clocked_adder(self, a, b, clk=0):
        with open("clocked_adder_input.txt", 'w') as file:
            file.write(f"{a:08x} {b:08x}\n")

        result = self.run_verilog_simulation("clocked_adder.v", "clocked_adder_output.txt")
        return result
