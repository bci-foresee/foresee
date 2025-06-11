#!/usr/bin/env python3
"""
Script to create test EEG data files for testing the EEG dataset functionality.
This creates .mat files similar to the SWEC_ETHZ_iEEG format.
"""

import numpy as np
from scipy.io import savemat
import os

def create_test_eeg_data():
    """Create synthetic EEG data with seizure periods for testing"""
    
    # Simplified approach: create signal where seizure periods have much higher average energy
    fs = 512  # Sampling frequency (Hz)
    duration = 60  # Duration in seconds
    n_channels = 2  # Number of EEG channels
    n_samples = fs * duration
    
    # Create time array
    t = np.linspace(0, duration, n_samples)
    
    # Initialize signal
    signal = np.zeros((n_channels, n_samples))
    
    # Define seizure period (20-30 seconds)
    seizure_start_time = 20
    seizure_end_time = 30
    seizure_start_idx = int(seizure_start_time * fs)
    seizure_end_idx = int(seizure_end_time * fs)
    
    for ch in range(n_channels):
        # Normal periods: low amplitude baseline activity
        normal_signal = np.zeros(n_samples)
        normal_signal += 0.5 * np.sin(2 * np.pi * 10 * t + ch * np.pi/4)  # Alpha waves
        normal_signal += 0.3 * np.sin(2 * np.pi * 20 * t + ch * np.pi/3)  # Beta waves
        normal_signal += 0.2 * np.random.randn(n_samples)  # Low noise
        
        # Seizure period: dramatically higher amplitude
        seizure_amplitude_multiplier = 20  # Make seizure 20x stronger
        seizure_signal = np.zeros(seizure_end_idx - seizure_start_idx)
        seizure_t = t[seizure_start_idx:seizure_end_idx]
        
        # High amplitude seizure pattern
        seizure_signal += seizure_amplitude_multiplier * 2.0 * np.sin(2 * np.pi * 15 * seizure_t + ch * np.pi/2)
        seizure_signal += seizure_amplitude_multiplier * 1.5 * np.sin(2 * np.pi * 25 * seizure_t + ch * np.pi/3)
        seizure_signal += seizure_amplitude_multiplier * 1.0 * np.sin(2 * np.pi * 35 * seizure_t + ch * np.pi/4)
        seizure_signal += seizure_amplitude_multiplier * 0.5 * np.random.randn(len(seizure_signal))
        
        # Combine normal and seizure periods
        signal[ch] = normal_signal
        signal[ch, seizure_start_idx:seizure_end_idx] = seizure_signal
    
    print(f"Normal period RMS: {np.sqrt(np.mean(signal[:, :seizure_start_idx]**2)):.2f}")
    print(f"Seizure period RMS: {np.sqrt(np.mean(signal[:, seizure_start_idx:seizure_end_idx]**2)):.2f}")
    
    return signal, fs, seizure_start_time, seizure_end_time

def save_test_data():
    """Save test EEG data and info files"""
    
    # Create test data directory within dev_tests
    test_dir = "../test_data"
    os.makedirs(test_dir, exist_ok=True)
    
    # Generate test data
    signal, fs, seizure_start, seizure_end = create_test_eeg_data()
    
    # Save EEG data file
    data_file = os.path.join(test_dir, "test_eeg_data.mat")
    savemat(data_file, {
        'data': signal,  # EEG data (channels x samples)
        'fs': fs,
        'duration': signal.shape[1] / fs
    })
    
    # Save info file
    info_file = os.path.join(test_dir, "test_eeg_info.mat")
    savemat(info_file, {
        'fs': np.array([[fs]]),
        'seizure_begin': np.array([[seizure_start]]),
        'seizure_end': np.array([[seizure_end]])
    })
    
    print(f"Test EEG data saved to {data_file}")
    print(f"Test EEG info saved to {info_file}")
    print(f"Data shape: {signal.shape}")
    print(f"Sampling frequency: {fs} Hz")
    print(f"Total duration: {signal.shape[1] / fs:.1f} seconds")
    print(f"Seizure period: {seizure_start}s to {seizure_end}s")
    
    return data_file, info_file

if __name__ == "__main__":
    save_test_data() 