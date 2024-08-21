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

    num_channels = 16 # 16 channels of ieeg data
    num_samples = 8192 # how many samples in window
    sample_rate = 400 # sample rate in Hz
    sample_window = num_samples / sample_rate # how long the window is in seconds
    
    sample_freq = sample_rate # sample frequency in Hz (how many samples/second)
    
#     nyquist_freq = sample_freq / 2 # Nyquist frequency, max frequency that can be represented in the signal
    
    # berger bands
    berger_bands = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]
    
    # sample ieeg signals ----------------------------------------------------------------------------
    
    # to show bbf alg issues
    # generated_signal_frequencies = [2, 25, 70, 112, 115]    
    # generated_signal_amplitudes =  [15, 15, 12, 28, 13]

    # good demonstration of fft verilog signal and diff to ground truth.
    # generated_signal_frequencies = [25, 70, 112, 115, 180]
    # generated_signal_amplitudes =  [15, 12, 28, 13, 17]

    generated_signal_frequencies = [10, 20, 40]
    generated_signal_amplitudes =  [20, 15, 10]

    sampled_signals = sample_signals(num_channels=num_channels, 
                                     sample_window=sample_window, 
                                     num_samples=num_samples,
                                     frequencies=generated_signal_frequencies,
                                     amplitudes=generated_signal_amplitudes,
                                     saveGraphs=True)

    # fft --------------------------------------------------------------------------------------------
    
    fft_power_features = fft_py(sampled_signals=sampled_signals, 
                              sample_freq=sample_freq,
                              berger_bands=berger_bands,
                              saveGraphs=True)
    
    # spiral fft
    fft_power_features_v = await fft_verilog(dut=dut,
                                     fft_clk_freq=15_700_000, # simulation clock frequency
                                    sampled_signals=sampled_signals, 
                                    sample_freq=sample_freq,
                                    berger_bands=berger_bands,
                                    saveGraphs=True)
    
    # make a feature gen for fft_verilog.

    # bbf --------------------------------------------------------------------------------------------

    # note look at fix for setting inf/nan values to 0

    bbf_power_features = bbf_py(sampled_signals=sampled_signals,
                             sample_freq=sample_freq, 
                             berger_bands=berger_bands, 
                             saveGraphs=True)

    # xcorr --------------------------------------------------------------------------------------------

    xcorr_features = xcorr_py(sampled_signals=sampled_signals, 
                              num_channels=num_channels, 
                              saveGraphs=True)
    
    # data manipulation -------------------------------------------------------------------------------

    fft_power_features_arr = np.array(fft_power_features)
    bbf_power_features_arr = np.array(bbf_power_features)
    xcorr_features_arr = np.array(xcorr_features)
    
    fft_features_flat = fft_power_features_arr.flatten()
    bbf_features_flat = bbf_power_features_arr.flatten()
    xcorr_features_flat = xcorr_features_arr.flatten()

    # 312 features in one array
    features_arr = np.concatenate((fft_features_flat, bbf_features_flat, xcorr_features_flat))
    
    # svm ---------------------------------------------------------------------------------------------

    weights = np.random.rand(312)
    bias = np.random.rand(1)
    print(weights.shape,bias.shape)
    svm_output = svm_py(features=features_arr, 
                     weights=weights, 
                     bias=bias)

    # thr ---------------------------------------------------------------------------------------------
    
    upper_bound = 1
    lower_bound = 0
    thr_output = thr_py(val=svm_output, 
                     upper_bound=upper_bound, 
                     lower_bound=lower_bound)
    
    print(thr_output)
    print(svm_output)

    assert thr_output == 0
    # assert 2 == 2


