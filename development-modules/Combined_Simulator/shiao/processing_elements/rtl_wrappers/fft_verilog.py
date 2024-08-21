import numpy as np
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.types import LogicArray
import matplotlib.pyplot as plt
import math

'''
##################################

This module takes in a sampled signal and performs the dft to provide a frequency domain representation of the signal.

This module is an interface for the hardware level fft module.

It provides an abstraction for the fft module, allowing it to be easily used in the pipeline for testing.
It is logically identical, however makes use of pre and post buffering to allow for easy logical testing.

This module in particular is heavily commented to provide guidance for the development of other rtl wrappers.

These wrappers heavily depend on the context of the rtl module they are interfacing with, 
so it is important to thoroughly understand the rtl module before developing the wrapper.

Also look at the cocotb documentation.

# Inputs
- dut [cocotb handle]                   handle to the "design under test", in this case the fft (this is a cocotb feature)
- sampled_signals [np.array::float]     list of sampled signals
- sample_freq [float]                   frequency of the samples taken (Hz)
- berger_bands [List::Tuple]            list of tuples of the berger bands (Hz)
- saveGraphs [Bool]                     boolean determining if graphs are generated

# Outputs
- fft_power_features [np.array::float]  list of power estimates in the berger bands for each signal
- output_spectrum [png]                 plot of the output spectrum
- magnitude_spectrum [png]              plot of the magnitude spectrum
- power_in_berger_bands [png]           plot of the power in the berger bands

##################################
'''

async def fft_verilog(dut,
                      fft_clk_freq,
                      sampled_signals, 
                      sample_freq, 
                      berger_bands,
                      saveGraphs=False):
    

    # initial setup --------------------
    nyquist_freq = sample_freq / 2 # Nyquist frequency, max frequency that can be represented in the signal
    num_samples = sampled_signals[0].shape[0] # how many samples given

    # spiral fft requires a power of 2 number of samples
    # so we zero pad 8000 samples to 8192 because a signal of zero does not affect the frequency domain
    for i in range(len(sampled_signals)):
        sampled_signals[i] = np.pad(sampled_signals[i], (0, 8192 - len(sampled_signals[i])), 'constant', constant_values=(0, 0))

    # updating num_samples from 8000 to 8192
    num_samples = sampled_signals[0].shape[0]

    # print(f"sampled signal: {sampled_signals[0][0:10]}") debug
    
    # helper functions ---------

    # convert frequency to period in ns, useful for clock setup
    def HzToPeriodNs(freq):
        period_unrounded = ((1 / freq) * 1e9)
        return math.ceil(period_unrounded)
    
    # helper function to assign inputs to fft module
    # as the fft module can only take 4 inputs at a time, we need to assign them in groups of 4
    def setInputs(dut, input_real, input_imag):
        dut.fft_X0.value = int(input_real[0])
        dut.fft_X1.value = int(input_imag[0])
        dut.fft_X2.value = int(input_real[1])
        dut.fft_X3.value = int(input_imag[1])
        dut.fft_X4.value = int(input_real[2])
        dut.fft_X5.value = int(input_imag[2])
        dut.fft_X6.value = int(input_real[3])
        dut.fft_X7.value = int(input_imag[3])


    # setup --------------------

    # clock
    fft_clk_period = HzToPeriodNs(fft_clk_freq) # clock frequency -> period in ns for cocotb interface

    # starting the clock
    fft_clk = Clock(dut.fft_clk, fft_clk_period, units="ns")  # Create a clock for dut
    cocotb.start_soon(fft_clk.start(start_high=False))

    # i/o setups
    dut.fft_reset.value = 0 # reset the fft module
    dut.fft_next.value = 0 # no new input data coming in, so flag = 0
    cycles_run = 0 # counter for cycles

    # initial input data = 0
    setInputs(dut=dut,
              input_real=[0, 0, 0, 0],
              input_imag=[0, 0, 0, 0])
    
    # reset for 5 cycles to make sure everything is clear
    for i in range(5):
        cycles_run += 1
        dut.fft_reset.value = 1
        await RisingEdge(dut.fft_clk)

    # release the reset
    dut.fft_reset.value = 0
    cycles_run += 1
    await RisingEdge(dut.fft_clk)

    # fft input loop --------------------

    # testing one signal for now:
    signal_in = sampled_signals[0]

    # input flag = 1
    dut.fft_next.value = 1 # set the flag to 1, this means data in from next cycle onwards
    await RisingEdge(dut.fft_clk) # wait for rising edge
    dut.fft_next.value = 0 # reset the flag

    print()
    print(f"input signal: {signal_in[0:10]}") # debug

    # input loop while the input data exists, keep inputting data until there is no more.
    while len(signal_in) >= 4:
        # wait for falling edge to latch inputs
        await FallingEdge(dut.fft_clk)
        setInputs(dut=dut,
                input_real=[signal_in[0], signal_in[1], signal_in[2], signal_in[3]],
                input_imag=[0, 0, 0, 0])
        
        # Remove the first 4 items
        signal_in = signal_in[4:]

        await RisingEdge(dut.fft_clk)
        cycles_run += 1

    # when all input data has been inputted, set input data = 0 so no artifacts
    setInputs(dut=dut,
            input_real=[0, 0, 0, 0],
            input_imag=[0, 0, 0, 0])

    # data ready check -------------------
    is_data_ready = False # flag set by dut.next_out
    while not is_data_ready:
        await RisingEdge(dut.fft_clk)
        cycles_run += 1
        is_data_ready = LogicArray(dut.fft_next_out.value) == LogicArray("1") # checking if data ready, but also able to deal with "X" and "Z" outputs

    # fft output loop -------------------

    # now data is ready
    # arrays to store output data
    real_output = []
    imag_output = []

    # read the output, 2048 cycles for 8192 values
    for i in range(2048):
        await RisingEdge(dut.fft_clk)
        cycles_run += 1
        real_output.append(dut.fft_Y0.value.integer)
        imag_output.append(dut.fft_Y1.value.integer)
        real_output.append(dut.fft_Y2.value.integer)
        imag_output.append(dut.fft_Y3.value.integer)
        real_output.append(dut.fft_Y4.value.integer)
        imag_output.append(dut.fft_Y5.value.integer)
        real_output.append(dut.fft_Y6.value.integer)
        imag_output.append(dut.fft_Y7.value.integer)
        #print(f"cycles run: {cycles_run}, dut.next_out.value: {dut.next_out.value}, next: {dut.next.value}")
        #debug_print(cycles_run, dut)

    # converting to numpy arrays for easier analysis of work done
    output_spectrum = np.zeros(num_samples)
    np_real_output = np.array(real_output)
    np_imag_output = np.array(imag_output)

    # helpful debugging code
    # print(np_real_output)
    # num_inf_nan = np.count_nonzero(np.isnan(np_real_output) | np.isinf(np_real_output))
    # print(f"Number of values in np_real_output that are inf or nan: {num_inf_nan}")

    # print(np_imag_output)
    # num_inf_nan = np.count_nonzero(np.isnan(np_imag_output) | np.isinf(np_imag_output))
    # print(f"Number of values in np_imag_output that are inf or nan: {num_inf_nan}")

    # data cleanup -------------------

    # replac vals in np_real and np_imag that are above a certain threshold with 0
    # this is likely due to overflow in the fft module
    threshold = (2**31) - 1000
    np_real_output = np.where(np_real_output > threshold, 0, np_real_output)
    np_imag_output = np.where(np_imag_output > threshold, 0, np_imag_output)

    # convert to magnitude spectrum from real and imaginary numbers
    for i in range(len(real_output)):
        output_spectrum[i] = np.sqrt(np_real_output[i]**2 + np_imag_output[i]**2)

    print(f"output_spectrum[0:10] = {output_spectrum[0:10]}") # debug
    # helpful debugging code
    # print(output_spectrum)
    # num_inf_nan = np.count_nonzero(np.isnan(output_spectrum) | np.isinf(output_spectrum))
    # print(f"Number of values in output_spectrum that are inf or nan: {num_inf_nan}")
    

    # frequency spectrum -------------------

    # the fft module seems to produce better results in the negative frequencies
    # as the negative frequencies are a mirror of the positive frequencies, we can just reverse the positive frequencies
    # so we take avg of positive and negative frequencies to ensure a lower probability of error
    neg_freqs = output_spectrum[len(output_spectrum)//2:][::-1]
    pos_freqs = output_spectrum[:len(output_spectrum)//2]

    # take avg of positive and negative frequencies
    positive_freqs = (neg_freqs + pos_freqs) / 2

    # calculate the frequency bins
    sample_spacing = 1/sample_freq # how much time between samples

    # provide a frequency for each index of the fft output
    freq_bins = np.fft.fftfreq(num_samples, sample_spacing) 
    positive_freq_bins = freq_bins[:num_samples // 2] # only positive frequencies bins


    # power estimate in berger bands from fft
        # shiao - sum of the magnitudes of the fft output in the berger bands

    fft_power_features = []

    fft_power = np.zeros(len(berger_bands))
    for band in berger_bands:
        band_magnitudes = np.abs(positive_freqs[(positive_freq_bins >= band[0]) & (positive_freq_bins < band[1])])
        band_power = np.sum(band_magnitudes)
        fft_power[berger_bands.index(band)] = band_power
    
    fft_power_features.append(fft_power)

    # plotting the output spectrum
    if saveGraphs:
        # Plotting the magnitude spectrum
        plt.figure(figsize=(12, 6))
        # x-axis is the frequency bins,
        plt.plot(positive_freq_bins, positive_freqs)  # Plot only positive frequencies
        plt.axvline(x=nyquist_freq, color='r', linestyle='--', label='Nyquist Frequency')
        plt.title('Magnitude Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid()
        plt.savefig('plots/rtl_PEs/fft_magnitude_spectrum.png')


        plt.figure(figsize=(12, 6))
        plt.plot(freq_bins, output_spectrum)
        plt.title('Output Spectrum')
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')
        plt.grid()
        plt.savefig('plots/rtl_PEs/fft_output_spectrum')

        # Plotting the power in the berger bands
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(berger_bands)), fft_power)
        plt.xticks(ticks=range(len(berger_bands)), labels=[str(band) for band in berger_bands])
        plt.title('Power in Berger Bands')
        plt.xlabel('Band')
        plt.ylabel('Power')
        plt.grid()
        plt.savefig('plots/rtl_PEs/fft_power_in_berger_bands.png')

    return fft_power_features
