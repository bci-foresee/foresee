# test pipeimport math
import numpy as np
import matplotlib.pyplot as plt
import math

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.types import LogicArray

# verilog PE imports
from processing_elements.rtl_wrappers.fft_verilog import fft_verilog

# signal generation import
from signal_gen.simple_signal_gen import sample_signals

# python high level PE imports
from processing_elements.python_PEs.fft import fft_py
from processing_elements.python_PEs.xcorr import xcorr_py
from processing_elements.python_PEs.bbf import bbf_py
from processing_elements.python_PEs.svm import svm_py
from processing_elements.python_PEs.thr import thr_py

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


