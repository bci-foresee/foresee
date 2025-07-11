#!/usr/bin/env python3
"""
Test script to demonstrate configurable windowing parameters in EEG dataset processing.
"""

import sys
import os
import json
import numpy as np

# Add the backend directory to the Python path  
sys.path.append('../..')

from run_pipeline import run_pipeline

def test_windowing_parameters():
    """Test different windowing configurations"""
    
    print("=== Testing Configurable Windowing Parameters ===\n")
    
    # Base pipeline configuration
    base_config = {
        "nodes": [
            {
                "id": "eeg_input_1",
                "nodeType": "input",
                "label": "iEEG Dataset",
                "properties": {
                    "Dataset Path": {
                        "value": "/Users/alejo/GitHub/foresee/backend/dev_tests/test_data/test_eeg_data.mat"
                    },
                    "Info File Path": {
                        "value": "/Users/alejo/GitHub/foresee/backend/dev_tests/test_data/test_eeg_info.mat"
                    }
                }
            },
            {
                "id": "tkeo_1", 
                "nodeType": "module",
                "label": "TKEO",
                "properties": {
                    "Number of Channels": {"value": 2},
                    "Clock Frequency": {"value": 100},
                    "Enable RTL Simulation": {"value": False}
                }
            },
            {
                "id": "avg_1",
                "nodeType": "module", 
                "label": "AVG",
                "properties": {
                    "Number of Channels": {"value": 2},
                    "Clock Frequency": {"value": 100},
                    "Enable RTL Simulation": {"value": False}
                }
            },
            {
                "id": "svm_1",
                "nodeType": "module",
                "label": "SVM", 
                "properties": {
                    "Weights": {"value": [1.0, 1.0]},
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
            {"source": "eeg_input_1", "target": "tkeo_1"},
            {"source": "tkeo_1", "target": "avg_1"},
            {"source": "avg_1", "target": "svm_1"},
            {"source": "svm_1", "target": "thr_1"}
        ]
    }
    
    # Test different windowing configurations
    test_configs = [
        {
            "name": "2s windows, no overlap",
            "window_duration": 2.0,
            "window_offset": 2.0,  # No overlap (offset = duration)
        },
        {
            "name": "4s windows, 50% overlap", 
            "window_duration": 4.0,
            "window_offset": 2.0,  # 50% overlap (offset = duration/2)
        },
        {
            "name": "6s windows, 75% overlap",
            "window_duration": 6.0,
            "window_offset": 1.5,  # 75% overlap (offset = duration/4)
        },
        {
            "name": "1s windows, 25% overlap",
            "window_duration": 1.0,
            "window_offset": 0.75,  # 25% overlap (offset = duration*3/4)
        }
    ]
    
    results = []
    
    for i, test_config in enumerate(test_configs):
        print(f"\n--- Test {i+1}: {test_config['name']} ---")
        print(f"   Window Duration: {test_config['window_duration']}s")
        print(f"   Window Offset: {test_config['window_offset']}s")
        
        # Load and modify the pipeline configuration
        config = json.loads(json.dumps(base_config))  # Deep copy
        config["nodes"][0]["properties"]["Window Duration"] = {"value": test_config["window_duration"]}
        config["nodes"][0]["properties"]["Window Offset"] = {"value": test_config["window_offset"]}
        
        try:
            result = run_pipeline(config)
            
            if 'error' in result:
                print(f"   ❌ Error: {result['error']}\n")
                continue
                
            accuracy_info = result.get('accuracy', {})
            accuracy = accuracy_info.get('accuracy', 0.0)
            n_windows = accuracy_info.get('n_windows', 0)
            
            print(f"   ✅ Success!")
            print(f"   Number of windows: {n_windows}")
            print(f"   Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
            print(f"   Message: {accuracy_info.get('message', 'N/A')}")
            
            results.append({
                "config": test_config,
                "accuracy": accuracy,
                "n_windows": n_windows,
                "success": True
            })
            
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results.append({
                "config": test_config,
                "error": str(e),
                "success": False
            })
        
        print()
    
    # Summary
    print("=== Summary ===")
    successful_tests = [r for r in results if r["success"]]
    
    if successful_tests:
        print("Successful configurations:")
        for result in successful_tests:
            config = result["config"]
            print(f"  • {config['name']}: {result['n_windows']} windows, {result['accuracy']:.4f} accuracy")
        
        print(f"\n✅ {len(successful_tests)}/{len(test_configs)} configurations succeeded!")
        print("✅ Windowing parameters are now configurable!")
    else:
        print("❌ No configurations succeeded")

if __name__ == "__main__":
    test_windowing_parameters() 