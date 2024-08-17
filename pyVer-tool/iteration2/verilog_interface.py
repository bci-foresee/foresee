import subprocess

import numpy as np

class VerilogInterface:

    input_buffer = "input_buffer.txt"
    output_buffer = "output_buffer.txt"

    def run_verilog_simulation(self, verilog_file, output_file):
        # Run the Verilog simulation using Icarus Verilog or another Verilog simulator
        subprocess.run(["iverilog", "-o", "sim", verilog_file])
        subprocess.run(["vvp", "sim"])
        
        # Read the output
        with open(output_file, 'r') as file:
            # Read all lines and strip whitespace
            lines = [line.strip() for line in file]
            
            # Convert each line from hex to int and create a NumPy array
            output_array = np.array([int(line, base=16) for line in lines])
        
        return output_array

    def adder(self, a:int, b:int):
        PE_name = "adder"
        verilog_file = PE_name + ".v"

        with open(self.input_buffer, 'w') as file:
            file.write(f"{a:08x} {b:08x}\n")  # Write inputs in hexadecimal

        result = self.run_verilog_simulation(verilog_file, self.output_buffer)
        return result

    def subtractor(self, a:int, b:int):
        PE_name = "subtractor"
        verilog_file = PE_name + ".v"
        with open(self.input_buffer, 'w') as file:
            file.write(f"{a:08x} {b:08x}\n")  # Write inputs in hexadecimal

        result = self.run_verilog_simulation(verilog_file, self.output_buffer)
        return result
    
    def clocked_adder(self, a:np.ndarray, b:np.ndarray, clk=0):
        PE_name = "clocked_adder"
        verilog_file = PE_name + ".v"

        with open(self.input_buffer, 'w') as file:
            # writing input buffer
            for i in range(len(a)):
                file.write(f"{a[i]:08x} {b[i]:08x}\n")

        result = self.run_verilog_simulation(verilog_file, self.output_buffer)
        return result


# maybe an input file generator function? I think that would be good to generalise