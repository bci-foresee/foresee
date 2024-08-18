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
        numbers = []
        with open(output_file, 'r') as file:
            for line in file:
                # Split each line into words and convert each word from hex to int
                line_numbers = [int(word, base=16) for word in line.split()]
                numbers.extend(line_numbers)
        
        # Convert the list of numbers to a numpy array
        return np.array(numbers)

    def adder(self, a:int, b:int):
        PE_name = "adder"
        verilog_file = "./rtl/" + PE_name + ".v"

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
    
    def clocked_array_adder(self, a:np.ndarray, b:np.ndarray, clk=0):
        PE_name = "clocked_array_adder"
        verilog_file = PE_name + ".v"

        with open(self.input_buffer, 'w') as file:
            # writing input buffer
            for i in range(len(a)):
                file.write(f"{a[i]:08x} {b[i]:08x}\n")

        result = self.run_verilog_simulation(verilog_file, self.output_buffer)
        return result
    
    def spiral_fft_8192(self, a:np.ndarray, clk=0):
        PE_name = "spiral_fft_8192"
        verilog_file = PE_name + ".v"

        # 2048 cycles for 8192 points
        with open(self.input_buffer, 'w') as file:
            # writing input buffer
            for i in range(2048):
                file.write(f"{a[4*i]:08x} {0:08x} {a[4*i+1]:08x} {0:08x} {a[4*i+2]:08x} {0:08x} {a[4*i+3]:08x} {0:08x}\n")

        result = self.run_verilog_simulation(verilog_file, self.output_buffer)
        return result


# maybe an input file generator function? I think that would be good to generalise