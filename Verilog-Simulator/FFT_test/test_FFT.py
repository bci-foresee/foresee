# test_dff.py

import math

import matplotlib.pyplot as plt
import numpy as np

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.types import LogicArray

def HzToPeriodNs(freq):
    period_unrounded = ((1 / freq) * 1e9)
    return math.ceil(period_unrounded)

def setInputs(dut, input_real, input_imag):

    # 4 concurrent inputs

    dut.X0.value = input_real[0]
    dut.X1.value = input_imag[0]

    dut.X2.value = input_real[1]
    dut.X3.value = input_imag[1]

    dut.X4.value = input_real[2]
    dut.X5.value = input_imag[2]

    dut.X6.value = input_real[3]
    dut.X7.value = input_imag[3]

    # print(dut.X0.value)

def frequency_spectrum_mag(real_output, imag_output):
    N = len(real_output)
    mag = []
    for i in range(N):
        mag.append( math.sqrt( real_output[i]**2 + imag_output[i]**2 ) )
    return mag

def debug_print(cycles, dut):
    print(f"cycles run: {cycles}, reset: {dut.reset.value}, dut.next_out.value: {dut.next_out.value}, Y0: {dut.Y0.value}")

@cocotb.test()
async def fft_test(dut):
    """Test the FFT"""

    #setting up arrays to store the output
    out_real = [] # real part of output
    out_imag = [] # imaginary part of output

    # setting up the clock
    fft_clk_freq = 15_700_000 # 15.7 MHz
    fft_clk_period = HzToPeriodNs(fft_clk_freq) # period in ns

    # starting the clock
    fft_clk = Clock(dut.clk, fft_clk_period, units="ns")  # Create a clock for dut
    cocotb.start_soon(fft_clk.start(start_high=False))

    # initial setups
    dut.reset.value = 0 # reset the fft module
    dut.next.value = 0 # no new input data coming in, so flag = 0
    is_data_ready = False # flag set by dut.next_out
    cycles_run = 0 # counter for cycles

    input_real = []
    input_imag = []

    for i in range(1024):
        input_real.append(100)
        input_imag.append(0)
    # input_real = [100, 100, 100, 100]
    # input_imag = [0, 0, 0, 0]
    setInputs(dut, input_real[0:4], input_imag[0:4]) # set the input data
    # await Timer(20, units="ns")

    # release the reset
    # dut.reset.value = 0
    # await Timer(20, units="ns")

    # reset for 5 cycles
    
    for i in range(5):
        cycles_run += 1
        dut.reset.value = 1
        await RisingEdge(dut.clk)

    dut.reset.value = 0

    # initial input on cycle 10

    for i in range(5):
        cycles_run += 1
        await RisingEdge(dut.clk)
    
    dut.next.value = 1 # set the flag to 1

    await RisingEdge(dut.clk) # wait for rising edge

    setInputs(dut, input_real[0:4], input_imag[0:4]) # set the input data

    # await RisingEdge(dut.clk) # wait for rising edge

    dut.next.value = 0 # reset the flag

    await RisingEdge(dut.clk) # wait for rising edge

    # loop to run fft until output is ready
    while not is_data_ready:
        await FallingEdge(dut.clk) # this was it <----------------- when to latch data
        setInputs(dut, input_real[0:4], input_imag[0:4])
        cycles_run += 1
        is_data_ready = LogicArray(dut.next_out.value) == LogicArray("1") # checking if data ready, but also able to deal with "X" and "Z" outputs

        # debug_print(cycles_run, dut)

        await RisingEdge(dut.clk)

        # assert LogicArray(dut.next_out.value) == LogicArray("1")

    # now data is ready
    real_output = []
    imag_output = []

    #await RisingEdge(dut.clk)

    # read the output, 256 cycles for 1024 values
    for i in range(256):
        await RisingEdge(dut.clk)
        cycles_run += 1

        real_output.append(dut.Y0.value)
        imag_output.append(dut.Y1.value)
        real_output.append(dut.Y2.value)
        imag_output.append(dut.Y3.value)
        real_output.append(dut.Y4.value)
        imag_output.append(dut.Y5.value)
        real_output.append(dut.Y6.value)
        imag_output.append(dut.Y7.value)
        #print(f"cycles run: {cycles_run}, dut.next_out.value: {dut.next_out.value}, next: {dut.next.value}")
        # debug_print(cycles_run, dut)

    await RisingEdge(dut.clk)

    # now do plotting:

    print( "Len real_in: " + str( len(input_real) ) )
    print( "Len real_out: " + str( len(real_output) ) )

    plt.plot(input_real)
    plt.xlabel('Sample')
    plt.ylabel('Signal Value')
    plt.title('Input Signal (real part)')
    plt.ylim(0, 120)  # Set y-axis limit from 0 to 120
    plt.savefig('/workspaces/aloha-verilog/SCALO_sim/FFT_test/plots/input_plot.png')
    plt.close()

    frequency_amplitudes = frequency_spectrum_mag(real_output, imag_output)

    plt.plot(frequency_amplitudes)
    plt.xlabel('Freq/Sample (check)')
    plt.ylabel('Amplitude')
    plt.title('Frequency Spectrum')
    plt.savefig('/workspaces/aloha-verilog/SCALO_sim/FFT_test/plots/frequency_spectrum.png')
    plt.close()

    maxRealVal = max(real_output)

    assert maxRealVal > 0, f"maxRealVal was {maxRealVal} on the {cycles_run}th cycle"