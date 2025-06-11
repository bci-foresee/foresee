# EEG Dataset Testing Suite

This directory contains a comprehensive testing suite for EEG dataset processing functionality with the Foresee pipeline system.

## Directory Structure

```
dev_tests/
├── pipelines/           # JSON pipeline configurations
│   ├── test_eeg_pipeline.json      # Main EEG dataset test pipeline
│   ├── simple_fft_pipeline.json    # FFT-based pipeline
│   ├── neo_pipeline.json           # Neo architecture pipeline
│   ├── neo_pipeline_hardware.json  # Hardware-optimized Neo pipeline
│   └── shiao_pipeline.json         # Shiao architecture pipeline
├── test_scripts/        # Python test scripts
│   ├── test_eeg_functionality.py   # Comprehensive EEG testing
│   ├── simple_pipeline_test.py     # Quick pipeline validation
│   ├── test_different_windowing.py # Windowing parameter tests
│   ├── debug_accuracy.py           # Debug accuracy computation
│   └── create_test_eeg_data.py     # Generate synthetic EEG data
├── test_data/          # Test datasets
│   ├── test_eeg_data.mat           # Synthetic EEG data (60s, 2 channels)
│   └── test_eeg_info.mat           # Seizure timing and metadata
├── results/            # Generated outputs and logs
│   ├── backend.log                 # Pipeline execution logs
│   ├── pipeline_results_hardware.json # Hardware pipeline results
│   └── __pycache__/               # Python cache files
└── README_EEG_TESTS.md # This documentation
```

## Overview

The EEG testing suite implements **windowed seizure detection analysis** following the methodology used in the SWEC_ETHZ_iEEG dataset research. This includes:

- **Configurable windowing parameters** (window duration, overlap ratio)
- **Realistic accuracy computation** for seizure detection pipelines
- **Support for real EEG datasets** (.mat format with timing info)
- **Backward compatibility** with synthetic signal processing

## Quick Start

### 1. Run Basic Pipeline Test
```bash
cd test_scripts
python simple_pipeline_test.py
```

### 2. Test Different Windowing Configurations
```bash
cd test_scripts
python test_different_windowing.py
```

### 3. Run Comprehensive Test Suite
```bash
cd test_scripts
python test_eeg_functionality.py
```

## EEG Dataset Pipeline Configuration

### Required Node Properties

**EEG Dataset Input Node:**
- `Dataset Path`: Path to .mat data file
- `Info File Path`: Path to .mat info file with seizure timing
- `Window Duration (seconds)`: Configurable window size (default: 4.0)
- `Overlap Ratio`: Configurable overlap ratio (default: 0.5)

### Example Pipeline Structure
```
EEG Dataset → TKEO → AVG → SVM
```

## Test Data Format

### Data File (.mat)
- **`data`**: EEG signal array (channels × samples)
- **`fs`**: Sampling frequency
- **`duration`**: Signal duration in seconds

### Info File (.mat) 
- **`fs`**: Sampling frequency [[512]]
- **`seizure_begin`**: Array of seizure start times (seconds)
- **`seizure_end`**: Array of seizure end times (seconds)

## Windowing Analysis

The system implements **overlapping window analysis** for realistic seizure detection:

1. **Signal Segmentation**: EEG data split into overlapping windows
2. **Per-Window Processing**: Each window processed through the entire pipeline
3. **Window-Wise Classification**: Each window classified as seizure/non-seizure
4. **Ground Truth Labeling**: Windows labeled based on >50% overlap with seizure periods
5. **Accuracy Computation**: Window-wise predictions vs ground truth

### Example Results
- **2s windows, no overlap**: 30 windows, 100.0% accuracy
- **4s windows, 50% overlap**: 29 windows, 93.1% accuracy  
- **6s windows, 75% overlap**: 37 windows, 89.2% accuracy
- **1s windows, 25% overlap**: 79 windows, 98.7% accuracy

## Pipeline Behavior

### EEG Dataset + SVM Pipeline
- ✅ **Computes real accuracy** using windowed analysis
- ✅ **Returns per-window predictions** vs ground truth
- ✅ **Configurable windowing parameters**

### Synthetic Signal + SVM Pipeline  
- ✅ **Returns 100% default accuracy** (no ground truth available)
- ✅ **Maintains backward compatibility**

### Non-SVM Pipelines
- ✅ **Returns `accuracy: null`** (no classification endpoint)

## File Usage

### Running Tests from Root Directory
All test scripts can be run from the dev_tests directory:
```bash
# From backend/dev_tests/
python test_scripts/simple_pipeline_test.py
python test_scripts/test_different_windowing.py
```

### Running Tests from test_scripts Directory
```bash
# From backend/dev_tests/test_scripts/
python simple_pipeline_test.py
python test_different_windowing.py
```

## Dependencies

Ensure the following packages are available:
- `numpy`
- `scipy` 
- `scikit-learn`
- `flask-cors`

## Research Integration

This implementation follows the **SWEC_ETHZ_iEEG dataset methodology** for seizure detection research:

- **Dataset**: http://ieeg-swez.ethz.ch/
- **Approach**: Windowed analysis with TKEO, AVG, SVM processing
- **Validation**: Window-wise accuracy computation
- **Flexibility**: Configurable windowing for different research requirements

The testing suite provides a foundation for evaluating seizure detection algorithms using both synthetic and real EEG datasets with proper temporal analysis. 