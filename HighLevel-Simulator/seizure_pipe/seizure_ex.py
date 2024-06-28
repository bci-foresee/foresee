import numpy as np
import matplotlib.pyplot as plt
import os
import ctypes
from PE_library import PE_algorithms

# init with the shared object file
PE_algorithms = PE_algorithms('lib_cmodels.so')


# pipe = ADC -> FFT -> SVM -> THR

#create samples (ie ADC info)
def sample_function(x):
    return np.sin(x) + 3

num_samples = 1024

sample_positions = np.linspace(0, 2*np.pi, num_samples)
samples = sample_function(sample_positions)

# process FFT
spectrum = PE_algorithms.fft(signal_in=samples, num_points=num_samples)

# show FFT results
# plot the results
plt.figure()
plt.plot(sample_positions, samples)
plt.title('FFT signal in')
plt.xlabel('time')
plt.ylabel('amplitude')
plt.savefig('./plots/pipe_fft.png')

plt.figure()
plt.plot(np.abs(spectrum))
plt.title('Spectrum out')
plt.xlabel('frequency')
plt.ylabel('magnitude')
plt.savefig('./plots/pipe_spectrum.png')

# Create example weights
size = len(spectrum)
model = np.array([], dtype=np.float64)
for i in range(size):
    np.append(model,1)

values = np.array(spectrum, dtype=np.uint16) # casting complex to real discards im part, fix w np.abs

# put through svm
svm_out = PE_algorithms.svm_predict(model, values, size)

#threshold
value = svm_out
low_bound = 0
high_bound = 10
result = PE_algorithms.threshold(value, low_bound, high_bound)

print(f"Result: {result}")