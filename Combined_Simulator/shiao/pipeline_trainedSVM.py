# test pipeimport math
import numpy as np
import matplotlib.pyplot as plt
import math

import os
import torch

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.types import LogicArray

# verilog PE imports
from processing_elements.rtl_wrappers.fft_verilog import fft_verilog

# signal generation import
from signal_gen.simple_signal_gen import sample_signals
from signal_gen.load_ETH_signal import load_ETH_signal

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
    # num_samples = 8000 # how many samples in window
    sample_freq = 512 # sample rate in Hz
    # sample_window = num_samples / sample_freq # how long the window is in seconds
    
    berger_bands = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]
    
    # sample ieeg signals ----------------------------------------------------------------------------
    

    # good demonstration of fft verilog signal and diff to ground truth.
    generated_signal_frequencies = [25, 70, 112, 115, 180]
    generated_signal_amplitudes =  [15, 12, 28, 13, 17]

    sampled_signals = load_ETH_signal(filename="./test_data",
                                     saveGraphs=True)

    # fft --------------------------------------------------------------------------------------------
    
    fft_power_features = fft_py(sampled_signals=sampled_signals, 
                              sample_freq=sample_freq,
                              berger_bands=berger_bands,
                              saveGraphs=True)
    

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

    weights_tensor = torch.load("./processing_elements/python_PEs/SVM_trained_weights/svm_model_weights.pth")
    weights = weights_tensor.numpy()
    
    bias = 0
    svm_output = svm_py(features=features_arr, 
                     weights=weights, 
                     bias=bias)

    # thr ---------------------------------------------------------------------------------------------
    
    upper_bound = 10
    lower_bound = -10
    thr_output = thr_py(val=svm_output, 
                     upper_bound=upper_bound, 
                     lower_bound=lower_bound)
    
    print(thr_output)
    print(svm_output)

    assert 1 == 1
    # assert 2 == 2


