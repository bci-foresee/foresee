import numpy as np
import matplotlib.pyplot as plt
import os
import ctypes
from PE_library import PE_algorithms

# init with the shared object file

PE_algorithms = PE_algorithms('lib_cmodels.so')

# Create sample data
model = np.array([0.1, 0.2, 0.3, 0.4, 0.5], dtype=np.float64)
values = np.array([1, 2, 3, 4, 5], dtype=np.uint16)
size = len(values)

# Call the function
result = PE_algorithms.svm_predict(model, values, size)


#fft
def sample_function(x):
    return np.sin(x) + 3

num_samples = 1024

# sample_positions = np.linspace(0, 2*np.pi, num_samples) # over 1 second
sample_positions = np.linspace(0, 10*2*np.pi, num_samples) # over 10 seconds
samples = sample_function(sample_positions)

spectrum = PE_algorithms.fft(signal_in=samples, num_points=num_samples)

print(len(samples))
print(len(spectrum))

# plot the results
plt.figure()
plt.plot(sample_positions, samples)
plt.title('Signal in')
plt.xlabel('time')
plt.ylabel('amplitude')
plt.savefig('./plots/fft2.png')

plt.figure()
plt.plot(np.abs(spectrum))
plt.title('Spectrum out')
plt.xlabel('frequency')
plt.ylabel('magnitude')
plt.savefig('./plots/spectrum2.png')

#print(np.abs(spectrum[0:15]))

#threshold
value = 5
low_bound = 0
high_bound = 10
result = PE_algorithms.threshold(value, low_bound, high_bound)

print(f"Result: {result}")