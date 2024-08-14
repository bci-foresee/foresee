import subprocess

def run_verilog_simulation(verilog_file, input_file, output_file):
    # Run the Verilog simulation using Icarus Verilog or another Verilog simulator
    subprocess.run(["iverilog", "-o", "sim", verilog_file])
    subprocess.run(["vvp", "sim"])
    
    # Read the output
    with open(output_file, 'r') as file:
        result = int(file.read().strip(), 16)  # Assuming hexadecimal format
    return result

def adder(a, b):
    with open("adder_input.txt", 'w') as file:
        file.write(f"{a:08x} {b:08x}\n")  # Write inputs in hexadecimal

    result = run_verilog_simulation("adder.v", "adder_input.txt", "adder_output.txt")
    return result

def subtractor(a, b):
    with open("subtractor_input.txt", 'w') as file:
        file.write(f"{a:08x} {b:08x}\n")  # Write inputs in hexadecimal

    result = run_verilog_simulation("subtractor.v", "subtractor_input.txt", "subtractor_output.txt")
    return result

# Example usage
a = 5
b = 2

c = adder(a, b)
print(f"Adder result: {c}")

d = subtractor(a, b)
print(f"Subtractor result: {d}")
