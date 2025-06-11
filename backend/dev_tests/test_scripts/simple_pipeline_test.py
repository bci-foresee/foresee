#!/usr/bin/env python3

import sys
import json
import os

# Add the backend directory to the Python path
sys.path.append('../..')

from run_pipeline import run_pipeline

def test_simple_pipeline():
    print("=== Simple Pipeline Test ===")
    
    try:
        print("✅ Successfully imported pipeline_api")
        
        # Load pipeline configuration
        with open('../pipelines/test_eeg_pipeline.json') as f:
            config = json.load(f)
        print(f"✅ Successfully loaded config with {len(config['nodes'])} nodes")
        
        # Check if dataset files exist
        dataset_path = "/Users/alejo/GitHub/foresee/backend/dev_tests/test_data/test_eeg_data.mat"
        info_path = "/Users/alejo/GitHub/foresee/backend/dev_tests/test_data/test_eeg_info.mat"
        
        if os.path.exists(dataset_path):
            print(f"✅ Dataset file exists: {dataset_path}")
        else:
            print(f"❌ Dataset file missing: {dataset_path}")
            return
            
        if os.path.exists(info_path):
            print(f"✅ Info file exists: {info_path}")
        else:
            print(f"❌ Info file missing: {info_path}")
            return
        
        # Test running pipeline
        print("🔄 Running pipeline...")
        result = run_pipeline(config)
        
        if 'error' in result:
            print(f"❌ Pipeline failed: {result['error']}")
            return False
        else:
            print("✅ Pipeline succeeded!")
            print(f"   Output nodes: {list(result.get('output_data', {}).keys())}")
            accuracy = result.get('accuracy', {})
            if accuracy:
                print(f"   Accuracy: {accuracy.get('accuracy', 'N/A')}")
                if 'message' in accuracy:
                    print(f"   Message: {accuracy['message']}")
                if 'error' in accuracy:
                    print(f"   Accuracy Error: {accuracy['error']}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple_pipeline() 