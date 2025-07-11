#!/usr/bin/env python3
"""
Test script for the new EEG dataset functionality.
This script creates test data and runs a pipeline to verify accuracy computation.
"""

import json
import os
import sys

# Add the backend directory to the Python path
sys.path.append('../..')

from run_pipeline import run_pipeline

def test_eeg_dataset_functionality():
    """Comprehensive test of EEG dataset processing functionality"""
    
    print("=== Testing iEEG Dataset Pipeline Functionality ===\n")
    
    # 1. Create test data
    print("1. Creating test EEG data...")
    try:
        # Import and run test data creation
        from create_test_eeg_data import save_test_data
        data_file, info_file = save_test_data()
        print("✓ Test data created successfully")
        print(f"  Data file: {data_file}")
        print(f"  Info file: {info_file}")
    except Exception as e:
        print(f"✗ Failed to create test data: {e}")
        return False
    
    # 2. Load and test pipeline configuration
    print("\n2. Loading test pipeline configuration...")
    pipeline_file = "../pipelines/test_eeg_pipeline.json"
    try:
        with open(pipeline_file, 'r') as f:
            pipeline_data = json.load(f)
        print("✓ Pipeline configuration loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load pipeline configuration: {e}")
        return False
    
    # Step 3: Run the pipeline
    print("3. Running EEG dataset pipeline...")
    try:
        result = run_pipeline(pipeline_data)
        
        if "error" in result:
            print(f"✗ Pipeline execution failed: {result['error']}")
            return False
        else:
            print("✓ Pipeline executed successfully")
            
            # Display results
            print(f"  Message: {result.get('message', 'N/A')}")
            print(f"  Nodes processed: {len(result.get('node_properties', {}))}")
            print(f"  Output data keys: {list(result.get('output_data', {}).keys())}")
            
            # Display accuracy results
            accuracy_info = result.get('accuracy', {})
            if accuracy_info:
                print(f"\n  Accuracy Results:")
                if 'accuracy' in accuracy_info:
                    print(f"    Overall Accuracy: {accuracy_info['accuracy']:.4f}")
                if 'individual_accuracies' in accuracy_info:
                    print(f"    Individual Accuracies: {accuracy_info['individual_accuracies']}")
                if 'message' in accuracy_info:
                    print(f"    Message: {accuracy_info['message']}")
                if 'error' in accuracy_info:
                    print(f"    Error: {accuracy_info['error']}")
            else:
                print("  No accuracy information available")
            
            print("\n✓ Test completed successfully!")
            return True
            
    except Exception as e:
        print(f"✗ Pipeline execution failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_synthetic_pipeline():
    """Test synthetic signal pipeline for comparison"""
    
    print("=== Testing Synthetic Pipeline (Default Accuracy) ===\n")
    
    # Simple synthetic pipeline that should default to 100% accuracy
    synthetic_config = {
        "nodes": [
            {
                "id": "input_1",
                "nodeType": "input", 
                "label": "Input",
                "properties": {
                    "Frequencies": {"value": "10, 20"},
                    "Amplitudes": {"value": "5, 3"},
                    "Sampling Frequency": {"value": 400},
                    "Number of Channels": {"value": 1},
                    "Number of Samples": {"value": 100}
                }
            },
            {
                "id": "avg_1",
                "nodeType": "module",
                "label": "AVG",
                "properties": {
                    "Number of Channels": {"value": 1},
                    "Clock Frequency": {"value": 100},
                    "Enable RTL Simulation": {"value": False}
                }
            },
            {
                "id": "svm_1", 
                "nodeType": "module",
                "label": "SVM",
                "properties": {
                    "Weights": {"value": [0.5]},
                    "Clock Frequency": {"value": 100},
                    "Enable RTL Simulation": {"value": False}
                }
            },
            {
                "id": "thr_1",
                "nodeType": "module",
                "label": "THR",
                "properties": {
                    "Lower Bound": {"value": 0},
                    "Upper Bound": {"value": 10},
                    "Clock Frequency": {"value": 100},
                    "Enable RTL Simulation": {"value": False}
                }
            }
        ],
        "edges": [
            {"source": "input_1", "target": "avg_1"},
            {"source": "avg_1", "target": "svm_1"},
            {"source": "svm_1", "target": "thr_1"}
        ]
    }
    
    try:
        result = run_pipeline(synthetic_config)
        
        if "error" in result:
            print(f"✗ Synthetic pipeline failed: {result['error']}")
            return False
        
        accuracy_info = result.get('accuracy', {})
        if accuracy_info and accuracy_info.get('accuracy') == 1.0:
            print("✓ Synthetic pipeline correctly defaults to 100% accuracy")
            return True
        else:
            print(f"✗ Synthetic pipeline accuracy issue: {accuracy_info}")
            return False
            
    except Exception as e:
        print(f"✗ Synthetic pipeline failed: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    eeg_success = test_eeg_dataset_functionality()
    synthetic_success = test_synthetic_pipeline()
    
    if eeg_success and synthetic_success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1) 