import os
import sys
import subprocess
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import jsonify
import json
import numpy as np

from asa import TKEO, AVG, SVM, THR, FFT, BBF, PWXC
from asa.utils import INPUT_PE, generate_signal

def convert_numpy_to_list(obj):
    # numpy -> python arrays
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: convert_numpy_to_list(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_to_list(item) for item in obj]
    return obj

def parse_pipeline_config(pipeline_data):
    if isinstance(pipeline_data, str):
        try:
            pipeline_data = json.loads(pipeline_data)
        except json.JSONDecodeError:
            return None, "Invalid JSON string provided"

    # Check for basic structure
    if not isinstance(pipeline_data, dict):
        return None, "Pipeline data is not a dictionary"

    if "nodes" not in pipeline_data or "edges" not in pipeline_data:
        return None, "Missing 'nodes' or 'edges' in pipeline data"
    
    for node in pipeline_data["nodes"]:
        if "id" not in node or "type" not in node:
            return None, f"Invalid node structure: {node}"
    
    for edge in pipeline_data["edges"]:
        if "source" not in edge or "target" not in edge:
            return None, f"Invalid edge structure: {edge}"
    
    return pipeline_data, None

def generate_pipeline(pipeline_data):
    # instantiating python PEs
    processing_elements = {}
    
    # creat ethe processing elements
    for node in pipeline_data["nodes"]:
        node_id = node["id"]
        node_type = node["type"]
        properties = node.get("properties", {})
        
        # bunch of if statements for different types of PEs, input special case
        if node_type == "input":
            frequencies = properties.get("Frequencies", {}).get("value", [10, 20, 40])
            amplitudes = properties.get("Amplitudes", {}).get("value", [20, 15, 10])
            fs = properties.get("Sampling Frequency", {}).get("value", 400)
            n_channels = properties.get("Number of Channels", {}).get("value", 1)
            n_samples = properties.get("Number of Samples", {}).get("value", 8192)
            
            input_signal = generate_signal(
                frequencies=frequencies,
                amplitudes=amplitudes,
                fs=fs,
                n_channels=n_channels,
                n_samples=n_samples
            )            
            processing_elements[node_id] = INPUT_PE(input=input_signal, clk=0)
            
        # all other PEs
        elif node_type == "module":
            clk = properties["Clock Frequency"]["value"]
            rtl_sim = properties["Enable RTL Simulation"]["value"]
            rtl_power = properties["Enable RTL Power Estimation"]["value"]
            save_viz=False

            if node["label"] == "TKEO":
                n_channels = properties["Number of Channels"]["value"]
                processing_elements[node_id] = TKEO(
                    n_channels=n_channels,
                    clk=clk,
                    rtl_sim=rtl_sim,
                    rtl_power_estimation=rtl_power,
                    save_visualization=save_viz
                )
                
            elif node["label"] == "AVG":
                n_channels = properties["Number of Channels"]["value"]
                processing_elements[node_id] = AVG(
                    n_channels=n_channels,
                    clk=clk,
                    rtl_sim=rtl_sim,
                    rtl_power_estimation=rtl_power,
                    save_visualization=save_viz
                )
                
            elif node["label"] == "SVM":
                weights = np.array(properties["Weights"]["value"])
                processing_elements[node_id] = SVM(
                    weights=weights,
                    clk=clk,
                    rtl_sim=rtl_sim,
                    rtl_power_estimation=rtl_power,
                    save_visualization=save_viz
                )
                
            elif node["label"] == "THR":
                lower_bound = properties["Lower Bound"]["value"]
                upper_bound = properties["Upper Bound"]["value"]
                processing_elements[node_id] = THR(
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    clk=clk,
                    rtl_sim=rtl_sim,
                    rtl_power_estimation=rtl_power,
                    save_visualization=save_viz
                )

            elif node["label"] == "FFT":
                berger_bands = properties["Berger Bands"]["value"]
                n_samples = properties["Number of Samples"]["value"]
                fs = properties["Sampling Frequency"]["value"]
                processing_elements[node_id] = FFT(
                    berger_bands=berger_bands,
                    n_samples=n_samples,
                    fs=fs,
                    clk=clk,
                    rtl_sim=rtl_sim,
                    save_visualization=save_viz
                )

            elif node["label"] == "BBF":
                fs = properties["Sampling Frequency"]["value"]
                berger_bands = properties["Berger Bands"]["value"]
                processing_elements[node_id] = BBF(
                    fs=fs,
                    berger_bands=berger_bands,
                    clk=clk,
                    rtl_sim=rtl_sim,
                    rtl_power_estimation=rtl_power,
                    save_visualization=save_viz
                )

            elif node["label"] == "PWXC":
                n_channels = properties["Number of Channels"]["value"]
                processing_elements[node_id] = PWXC(
                    n_channels=n_channels,
                    clk=clk,
                    save_visualization=save_viz,
                    rtl_sim=rtl_sim,
                    rtl_power_estimation=rtl_power
                )

    #make the connections
    for edge in pipeline_data["edges"]:
        source_id = edge["source"]
        target_id = edge["target"]
        
        if source_id in processing_elements and target_id in processing_elements:
            source_pe = processing_elements[source_id]
            target_pe = processing_elements[target_id]
            
            source_pe.add_output(target_pe)
            target_pe.add_input(source_pe)
    
    return processing_elements

def run_pipeline(pipeline_data):
    """Main pipeline execution function that orchestrates the three stages."""
    # parse json
    pipeline_data, error = parse_pipeline_config(pipeline_data)
    if error:
        print("❌ Pipeline parse error:", error)
        return jsonify({"error": error}), 400
    print(f'Parsed pipeline data: {pipeline_data}')

    # instantiate python PEs
    processing_elements = generate_pipeline(pipeline_data)

    # run the PEs
    for pe in processing_elements.values():
        pe.run()
        print(f'RAN {pe}')

    # Get results
    results = {
        "message": "Pipeline run successfully",
        "node_properties": {node["id"]: {
            "label": node["label"],
            "name": node.get("name", ""),
            "type": node["type"],
            "properties": node.get("properties", {})
        } for node in pipeline_data["nodes"]},
        "connections": {edge["source"]: edge["target"] for edge in pipeline_data["edges"]},
        "metrics": [],
        "output_data": {}
    }

    # store sim data
    for node_id, pe in processing_elements.items():
        results["output_data"][node_id] = convert_numpy_to_list(pe.simulation_data)

    return results

def test_pipeline():
    ### this is just for testing, not for production

    top_level_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                       capture_output=True,
                                       text=True).stdout.strip()
    

    # load pipeline file
    pipeline_file = f"{top_level_dir}/backend/dev_tests/neo_pipeline_hardware.json"
    try:
        with open(pipeline_file, 'r') as f:
            pipeline_data = json.load(f)
    except FileNotFoundError:
        print(f"Pipeline configuration file not found: {pipeline_file}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON in pipeline configuration file: {pipeline_file}")
        return None

    result = run_pipeline(pipeline_data)


    


    os.chdir(f"{top_level_dir}/backend/dev_tests/")
    

    output_file = 'pipeline_results.json'
    try:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Pipeline results written to {output_file}")
    except IOError as e:
        print(f"Error writing results to file: {e}")
    
    return result

if __name__ == "__main__":
    test_pipeline()
