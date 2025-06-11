#!/usr/bin/env python3

import sys
import os
import json
import numpy as np

# Add the backend directory to the Python path
sys.path.append('../..')

from run_pipeline import run_pipeline

def debug_accuracy():
    print("=== Debug Accuracy Computation ===")
    
    # Load and run pipeline
    with open('../pipelines/test_eeg_pipeline.json') as f:
        config = json.load(f)
    
    result = run_pipeline(config)
    
    if 'error' in result:
        print(f"❌ Pipeline failed: {result['error']}")
        return
    
    print("✅ Pipeline succeeded!")
    
    # Check SVM output
    svm_output = result['output_data']['svm_1']
    print(f"SVM output keys: {list(svm_output.keys())}")
    
    if 'output_data' in svm_output:
        svm_data = svm_output['output_data']
        print(f"SVM output_data: {svm_data}")
        print(f"SVM output_data type: {type(svm_data)}")
        if isinstance(svm_data, (list, np.ndarray)):
            print(f"SVM output_data shape: {np.array(svm_data).shape}")
    
    if 'predictions' in svm_output:
        predictions = np.array(svm_output['predictions'])
        print(f"SVM predictions shape: {predictions.shape}")
        print(f"SVM predictions: {predictions}")
        print(f"SVM prediction unique values: {np.unique(predictions)}")
    else:
        print("❌ No 'predictions' field in SVM output")
    
    # Let's also print all SVM output for debugging
    print(f"\nFull SVM output:")
    for key, value in svm_output.items():
        print(f"  {key}: {value}")
    
    # Check accuracy details
    accuracy_info = result.get('accuracy', {})
    print(f"\nAccuracy info: {accuracy_info}")
    
    if 'true_labels' in accuracy_info:
        true_labels = np.array(accuracy_info['true_labels'])
        print(f"True labels shape: {true_labels.shape}")
        print(f"True labels unique values: {np.unique(true_labels)}")
        print(f"True labels sum (should be > 0): {np.sum(true_labels)}")
    
    if 'predictions' in accuracy_info:
        pred_labels = accuracy_info['predictions']
        for node_id, preds in pred_labels.items():
            print(f"Predictions for {node_id}: {np.array(preds)}")
    
    # Debug TKEO and AVG outputs
    tkeo_output = result['output_data']['tkeo_1']
    avg_output = result['output_data']['avg_1']
    
    print(f"\nTKEO output keys: {list(tkeo_output.keys())}")
    print(f"AVG output keys: {list(avg_output.keys())}")
    
    if 'processed_data' in tkeo_output:
        tkeo_data = np.array(tkeo_output['processed_data'])
        print(f"TKEO data shape: {tkeo_data.shape}")
        print(f"TKEO data range: {np.min(tkeo_data):.2f} to {np.max(tkeo_data):.2f}")
    
    if 'processed_data' in avg_output:
        avg_data = np.array(avg_output['processed_data'])
        print(f"AVG data: {avg_data}")

if __name__ == "__main__":
    debug_accuracy() 