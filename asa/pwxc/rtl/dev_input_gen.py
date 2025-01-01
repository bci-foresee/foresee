import numpy as np

def generate_input_buffers(x_data, y_data, x_filename="input_x_buffer.txt", y_filename="input_y_buffer.txt"):
    """Generates input buffers for the Verilog testbench.

    Args:
        x_data: A list or numpy array of 16-bit signed integers for x.
        y_data: A list or numpy array of 16-bit signed integers for y.
        x_filename: The filename for the x buffer.
        y_filename: The filename for the y buffer.
    """

    if len(x_data) != len(y_data):
        raise ValueError("x_data and y_data must have the same length.")

    if len(x_data) != 8192:
        raise ValueError("x_data and y_data must have length 8192")

    with open(x_filename, "w") as x_file, open(y_filename, "w") as y_file:
        for x, y in zip(x_data, y_data):
            # Ensure values are within the 16-bit signed range (-32768 to 32767)
            x = np.int16(x)
            y = np.int16(y)
            x_file.write(f"{x:04x}\n")  # Write as hexadecimal
            y_file.write(f"{y:04x}\n")  # Write as hexadecimal

# Example usage (Constant inputs):
x_const = np.full(8192, 5, dtype=np.int16)
y_const = np.full(8192, 3, dtype=np.int16)
# generate_input_buffers(x_const, y_const)

# Example usage (Sine wave autocorrelation):
amplitude = 1000
period = 100
x_sine = np.array([int(np.sin(2 * np.pi * i / period) * amplitude) for i in range(8192)], dtype=np.int16)
y_sine = x_sine.copy()  # For autocorrelation
# generate_input_buffers(x_sine, y_sine)

# Example usage (Sequence):
x_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_seq = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
x_seq_padded = np.pad(x_seq, (0, 8192 - len(x_seq)), 'constant')
y_seq_padded = np.pad(y_seq, (0, 8192 - len(y_seq)), 'constant')

generate_input_buffers(x_seq_padded, y_seq_padded)

# Example usage (Impulse):

x_impulse = np.zeros(8192, dtype = np.int16)
x_impulse[0] = 1
y_impulse = np.zeros(8192, dtype = np.int16)

# generate_input_buffers(x_impulse, y_impulse)

print("Input buffer files generated successfully.")