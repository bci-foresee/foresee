import subprocess
import os

class VerilogModule:
    def __init__(self, verilog_file):
        self.verilog_file = verilog_file

    def run(self, inputs):
        # Create input and output files in the current directory
        input_file_name = 'input.txt'
        output_file_name = 'output.txt'

        try:
            # Write inputs to the input file
            with open(input_file_name, 'w') as input_file:
                for key, value in inputs.items():
                    input_file.write(f"{key} {value}\n")

            # Run the Verilog simulation
            subprocess.run(['iverilog', '-o', 'sim', self.verilog_file], check=True)
            subprocess.run(['vvp', 'sim'], check=True)

            # Read the output
            with open(output_file_name, 'r') as output_file:
                outputs = {}
                for line in output_file:
                    key, value = line.strip().split()
                    outputs[key] = int(value)

            return outputs

        except subprocess.CalledProcessError as e:
            print(f"Error running Verilog simulation: {e}")
            return None
        except IOError as e:
            print(f"Error handling files: {e}")
            return None
        finally:
            # Clean up files
            if os.path.exists(input_file_name):
                os.remove(input_file_name)
            if os.path.exists(output_file_name):
                os.remove(output_file_name)

# Usage
adder = VerilogModule('adder.v')
result = adder.run({'a': 5, 'b': 2})
if result:
    print(f"Verilog adder result: {result.get('sum', 'No sum found')}")
else:
    print("Failed to run Verilog simulation")