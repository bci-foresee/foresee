import numpy as np
import matplotlib.pyplot as plt

# Parameters
fs = 400  # Sampling frequency
t_window = 20  # Sample window in seconds
num_samples = fs * t_window  # Total number of samples

# Create a time array
t = np.linspace(0, t_window, num_samples, endpoint=False)

# Create a sample signal: sum of two sine waves, one below and one above Nyquist frequency
signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

# Perform FFT
fft_output = np.fft.fft(signal)
freqs = np.fft.fftfreq(num_samples, 1/fs)

# Plotting the magnitude spectrum
magnitude = np.abs(fft_output)

plt.figure(figsize=(12, 6))
plt.plot(freqs[:num_samples // 2], magnitude[:num_samples // 2])  # Plot only positive frequencies
plt.axvline(x=fs / 2, color='r', linestyle='--', label='Nyquist Frequency')
plt.title('Magnitude Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.grid()
plt.savefig('plots/nyquist_example.png')
