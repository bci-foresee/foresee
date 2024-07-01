import math
import numpy as np
import matplotlib.pyplot as plt

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.types import LogicArray

@cocotb.test()
async def test_fft_verilog(dut):
    # pipe setup -------------------------------------------------------------------------------------
    # Sample information
    num_channels = 16 # 1 for now, will be 16 in the future.
    # 1024 samples and 400Hz =>
    num_samples = 8000 # how many samples in window
    sample_rate = 400 # sample rate in Hz
    sample_window = num_samples / sample_rate # how long the window is in seconds
    
    sample_freq = sample_rate # sample frequency in Hz (how many samples/second)
    
    nyquist_freq = sample_freq / 2 # Nyquist frequency, max frequency that can be represented in the signal
    
    # berger bands
    berger_bands = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]
    
    # sample ieeg signals ----------------------------------------------------------------------------
    
    sampled_signals = sample_signals(num_signals=num_channels, 
                                     sample_window=sample_window, 
                                     num_samples=num_samples,
                                     saveGraphs=True)
    
    # fft verilog -------------------------------------------------------------------------------------

    fft_temp_out = await fft_verilog(dut=dut,
                                     sampled_signals=sampled_signals, 
                                     num_samples=num_samples, 
                                     sample_freq=sample_freq,
                                     nyquist_freq=nyquist_freq,
                                     berger_bands=berger_bands,
                                     saveGraphs=True)

    print(fft_temp_out[0:10])

    assert 1 == 1

# fft verilog -----------------------------------------------------------------------------------------
async def fft_verilog(dut,
                      sampled_signals, 
                      num_samples, 
                      sample_freq, 
                      nyquist_freq, 
                      berger_bands,
                      saveGraphs=False):
    
    # zero pad the sampled signals to 8192 samples
    for i in range(len(sampled_signals)):
        sampled_signals[i] = np.pad(sampled_signals[i], (0, 8192 - len(sampled_signals[i])), 'constant', constant_values=(0, 0))

    num_samples = 8192

    print(f"sampled signal: {sampled_signals[0][0:10]}")
    
    # helper functions ---------

    def HzToPeriodNs(freq):
        period_unrounded = ((1 / freq) * 1e9)
        return math.ceil(period_unrounded)
    
    def setInputs(dut, input_real, input_imag):
        # 4 concurrent inputs

        # print(f"full val: {input_real[0]}, int val: {int(input_real[0])}") # issues here...

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
    fft_clk_freq = 15_700_000 # 15.7 MHz
    fft_clk_period = HzToPeriodNs(fft_clk_freq) # period in ns

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
    dut.fft_next.value = 1 # set the flag to 1
    await RisingEdge(dut.fft_clk) # wait for rising edge
    dut.fft_next.value = 0 # reset the flag

    # input loop while the input loop exists
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

    # data ready check -------------------

    is_data_ready = False # flag set by dut.next_out
    while not is_data_ready:
        await RisingEdge(dut.fft_clk)
        cycles_run += 1
        is_data_ready = LogicArray(dut.fft_next_out.value) == LogicArray("1") # checking if data ready, but also able to deal with "X" and "Z" outputs
        # print(cycles_run, is_data_ready)
        # is_data_ready = LogicArray(dut.fft_next_out.value) == LogicArray("1") # checking if data ready, but also able to deal with "X" and "Z" outputs

    # fft output loop -------------------

    # now data is ready
    real_output = []
    imag_output = []

    # read the output, 256 cycles for 1024 values
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
        # debug_print(cycles_run, dut)

    output_spectrum = np.zeros(num_samples)
    np_real_output = np.array(real_output)
    np_imag_output = np.array(imag_output)

    for i in range(len(real_output)):
        output_spectrum[i] = np.sqrt(np_real_output[i]**2 + np_imag_output[i]**2)
    
    # midpoint = len(output_spectrum) // 2

    # reverse upper half
    # output_spectrum[:midpoint] = output_spectrum[:midpoint][::-1]

    positive_freqs = output_spectrum[len(output_spectrum)//2:][::-1]

    sample_spacing = 1/sample_freq # how much time between samples
    freq_bins = np.fft.fftfreq(num_samples, sample_spacing) # provide a frequency for each index of the fft output
    positive_freq_bins = freq_bins[:num_samples // 2] # only positive frequencies bins

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
        plt.savefig('plots/seizure_pipe/fft_magnitude_spectrum.png')


        plt.figure(figsize=(12, 6))
        plt.plot(freq_bins, output_spectrum)
        plt.title('Output Spectrum')
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')
        plt.grid()
        plt.savefig('plots/seizure_pipe/output_spectrum')

    return output_spectrum


# sample signals -------------------------------------------------------------------------------------
def sample_signals(num_signals, sample_window, num_samples, saveGraphs=False):

    # define a sampled function, and the sample
    def signal1(t):
        frequencies = [10, 50, 80, 125]
        amplitudes =  [50,  15,  15,  5]
        # frequencies = [50, 100]
        # amplitudes =  [5, 10]
        returnSignal = 0
        for i in range(len(frequencies)):
            returnSignal += amplitudes[i] * np.sin(2*np.pi*frequencies[i]*t)  
        return (returnSignal)
    
    def randomvals(t):
        return np.ones_like(t)
    
    sampled_signals = []
    for i in range(num_signals):
        x = np.linspace(start=0, stop=sample_window, num=num_samples, endpoint=False)
        if i == 0:
            sampled_signals.append(signal1(x))
            # display 1st sampled signal
            if saveGraphs:
                plt.figure(figsize=(12, 6))
                plt.plot(x, sampled_signals[0])
                plt.title('Sampled Signal')
                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')
                plt.grid()
                plt.savefig('plots/seizure_pipe/sampled_signal.png')

                # also printing int converted graph
                int_sampled_signal = [int(sampled_signals[0][i]) for i in range(len(sampled_signals[0]))]
                plt.figure(figsize=(12, 6))
                plt.plot(x, int_sampled_signal)
                plt.title('Sampled Signal int conversion')
                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')
                plt.grid()
                plt.savefig('plots/seizure_pipe/sampled_signal_int.png')
        else:
            sampled_signals.append(randomvals(x))

    return sampled_signals

# fft helper stuff -----------------------------------------------------------------------------------

