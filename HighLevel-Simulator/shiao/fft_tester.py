import numpy as np
import matplotlib.pyplot as plt

# Example signal: 1 second of a 5 Hz sine wave sampled at 50 Hz
sampling_rate = 50
t = np.linspace(0, 1, sampling_rate, endpoint=False)
samples = np.sin(2 * np.pi * 5 * t)

# Perform FFT
fft_output = np.fft.fft(samples)

# Frequency bins
freqs = np.fft.fftfreq(len(samples), d=1/sampling_rate)

# Separate positive and negative frequencies
positive_freqs = freqs[:len(freqs)//2]
negative_freqs = freqs[len(freqs)//2:]

positive_fft_output = fft_output[:len(fft_output)//2]
negative_fft_output = fft_output[len(fft_output)//2:]

# Plot the original signal
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.plot(t, samples)
plt.title("Original Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot the FFT magnitudes (positive frequencies)
plt.subplot(2, 2, 2)
plt.stem(positive_freqs, np.abs(positive_fft_output))
plt.title("Positive Frequencies")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")

# Plot the FFT magnitudes (negative frequencies)
plt.subplot(2, 2, 3)
plt.stem(negative_freqs, np.abs(negative_fft_output))
plt.title("Negative Frequencies")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")

# Combine positive and negative frequency magnitudes for a full spectrum plot
plt.subplot(2, 2, 4)
full_spectrum_freqs = np.fft.fftshift(freqs)
full_spectrum_magnitudes = np.fft.fftshift(np.abs(fft_output))
plt.stem(full_spectrum_freqs, full_spectrum_magnitudes)
plt.title("Full Spectrum")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")

plt.tight_layout()
plt.savefig("plots/fft_example.png")

