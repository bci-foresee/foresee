import logging
import os
import sys
import subprocess
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import jsonify
import json
import numpy as np

from asa import TKEO, AVG, SVM, THR, FFT, BBF, PWXC
from asa.utils import INPUT_PE, generate_signal

logging.basicConfig(filename='backend.log', level=logging.DEBUG)


def convert_numpy_to_list(obj):
    # numpy -> python arrays
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {
            key: convert_numpy_to_list(value)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [convert_numpy_to_list(item) for item in obj]
    return obj


def parse_berger_bands(berger_bands_str):
    """
    Parse berger bands from string format to List[Tuple[float, float]]
    Input: "0.1-4, 4-8, 8-12" or "0.1-4,4-8,8-12"
    Output: [(0.1, 4), (4, 8), (8, 12)]
    """
    if isinstance(berger_bands_str, list):
        # Already in correct format (from legacy data)
        return berger_bands_str
    
    if not isinstance(berger_bands_str, str) or not berger_bands_str.strip():
        # Default berger bands if empty or invalid
        return [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]
    
    try:
        bands = []
        # Split by comma and process each range
        for band_str in berger_bands_str.split(','):
            band_str = band_str.strip()
            if '-' in band_str:
                min_val, max_val = band_str.split('-', 1)
                min_val = float(min_val.strip())
                max_val = float(max_val.strip())
                bands.append((min_val, max_val))
        
        if bands:
            return bands
        else:
            # Fallback to default if no valid bands found
            return [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]
            
    except (ValueError, AttributeError) as e:
        logging.error(f"Error parsing berger bands '{berger_bands_str}': {e}")
        # Return default berger bands on error
        return [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]


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
        if "id" not in node or "nodeType" not in node:
            return None, f"Invalid node structure: {node}"

    for edge in pipeline_data["edges"]:
        if "source" not in edge or "target" not in edge:
            return None, f"Invalid edge structure: {edge}"

    return pipeline_data, None


def generate_pipeline(pipeline_data):
    """Generate processing elements with comprehensive error handling."""
    processing_elements = {}

    try:
        # create the processing elements
        for node in pipeline_data["nodes"]:
            try:
                node_id = node["id"]
                node_type = node["nodeType"]
                properties = node.get("properties", {})
                node_label = node.get("label", "Unknown")

                logging.debug(f"Processing node {node_id}: {node_label} ({node_type})")

                # Handle input nodes
                if node_type == "input":
                    try:
                        # Parse frequencies and amplitudes from strings
                        frequencies_str = properties.get("Frequencies", {}).get("value", "10, 20, 40")
                        amplitudes_str = properties.get("Amplitudes", {}).get("value", "20, 15, 10")
                        
                        # Convert string values to lists of integers with error handling
                        logging.debug(f"Frequencies: {frequencies_str}, type: {type(frequencies_str)}")
                        logging.debug(f"Amplitudes: {amplitudes_str}, type: {type(amplitudes_str)}")
                        
                        try:
                            # Split and filter out empty strings, then convert to integers
                            frequencies = [int(f.strip()) for f in frequencies_str.split(',') if f.strip()]
                            amplitudes = [int(a.strip()) for a in amplitudes_str.split(',') if a.strip()]
                            
                            # Ensure we have at least one frequency and amplitude
                            if not frequencies:
                                frequencies = [10, 20, 40]  # Default values
                            if not amplitudes:
                                amplitudes = [20, 15, 10]  # Default values
                                
                        except (ValueError, AttributeError) as e:
                            raise ValueError(f"Invalid frequencies or amplitudes format in Input node {node_id}. Expected comma-separated numbers (e.g., '10, 20, 40'). Error: {e}")

                        # Validate other input parameters
                        try:
                            fs = int(properties.get("Sampling Frequency", {}).get("value", 400))
                            n_channels = int(properties.get("Number of Channels", {}).get("value", 1))
                            n_samples = int(properties.get("Number of Samples", {}).get("value", 8192))
                            
                            if fs <= 0:
                                raise ValueError(f"Sampling frequency must be positive, got {fs}")
                            if n_channels <= 0:
                                raise ValueError(f"Number of channels must be positive, got {n_channels}")
                            if n_samples <= 0:
                                raise ValueError(f"Number of samples must be positive, got {n_samples}")
                                
                        except (ValueError, TypeError) as e:
                            raise ValueError(f"Invalid numeric parameters in Input node {node_id}: {e}")

                        logging.debug(f'input_signal: {frequencies}, {amplitudes}, {fs}, {n_channels}, {n_samples}')
                        
                        try:
                            input_signal = generate_signal(frequencies=frequencies,
                                                         amplitudes=amplitudes,
                                                         fs=fs,
                                                         n_channels=n_channels,
                                                         n_samples=n_samples)
                            processing_elements[node_id] = INPUT_PE(input=input_signal, clk=0)
                        except Exception as e:
                            raise RuntimeError(f"Failed to generate input signal for node {node_id}: {e}")
                            
                    except Exception as e:
                        raise RuntimeError(f"Error creating input node {node_id} ({node_label}): {e}")

                # Handle processing module nodes
                elif node_type == "module":
                    try:
                        # Validate common properties
                        try:
                            clk = properties["Clock Frequency"]["value"]
                            rtl_sim = properties["Enable RTL Simulation"]["value"]
                            rtl_power = properties["Enable RTL Power Estimation"]["value"]
                            
                            if not isinstance(clk, (int, float)) or clk < 0:
                                raise ValueError(f"Clock frequency must be a non-negative number, got {clk}")
                            if not isinstance(rtl_sim, bool):
                                raise ValueError(f"RTL Simulation setting must be true/false, got {rtl_sim}")
                            if not isinstance(rtl_power, bool):
                                raise ValueError(f"RTL Power Estimation setting must be true/false, got {rtl_power}")
                                
                        except KeyError as e:
                            raise ValueError(f"Missing required property in {node_label} node {node_id}: {e}")
                        except (ValueError, TypeError) as e:
                            raise ValueError(f"Invalid property value in {node_label} node {node_id}: {e}")

                        save_viz = False
                        logging.debug(f'{node_label} properties: rtl_sim={rtl_sim}, rtl_power={rtl_power}, clk={clk}')

                        # Create specific PE types with detailed error handling
                        if node_label == "TKEO":
                            try:
                                n_channels = int(properties["Number of Channels"]["value"])
                                if n_channels <= 0:
                                    raise ValueError(f"Number of channels must be positive, got {n_channels}")
                                logging.debug(f'TKEO properties: {n_channels}, {clk}, {rtl_sim}, {rtl_power}, {save_viz}')
                                processing_elements[node_id] = TKEO(
                                    n_channels=n_channels,
                                    clk=clk,
                                    rtl_sim=rtl_sim,
                                    rtl_power_estimation=rtl_power,
                                    save_visualization=save_viz)
                            except Exception as e:
                                raise RuntimeError(f"Failed to create TKEO module: {e}")

                        elif node_label == "AVG":
                            try:
                                n_channels = int(properties["Number of Channels"]["value"])
                                if n_channels <= 0:
                                    raise ValueError(f"Number of channels must be positive, got {n_channels}")
                                processing_elements[node_id] = AVG(
                                    n_channels=n_channels,
                                    clk=clk,
                                    rtl_sim=rtl_sim,
                                    rtl_power_estimation=rtl_power,
                                    save_visualization=save_viz)
                            except Exception as e:
                                raise RuntimeError(f"Failed to create AVG module: {e}")

                        elif node_label == "SVM":
                            try:
                                weights_value = properties["Weights"]["value"]
                                
                                # Parse weights if it's a string representation of an array
                                if isinstance(weights_value, str):
                                    try:
                                        import json
                                        weights_list = json.loads(weights_value)
                                        weights = np.array(weights_list)
                                    except (json.JSONDecodeError, ValueError) as e:
                                        raise ValueError(f"Invalid weights format. Expected JSON array or comma-separated numbers: {e}")
                                else:
                                    weights = np.array(weights_value)
                                    
                                if weights.size == 0:
                                    raise ValueError("Weights array cannot be empty")
                                    
                                processing_elements[node_id] = SVM(
                                    weights=weights,
                                    clk=clk,
                                    rtl_sim=rtl_sim,
                                    rtl_power_estimation=rtl_power,
                                    save_visualization=save_viz)
                            except Exception as e:
                                raise RuntimeError(f"Failed to create SVM module: {e}")

                        elif node_label == "THR":
                            try:
                                lower_bound = float(properties["Lower Bound"]["value"])
                                upper_bound = float(properties["Upper Bound"]["value"])
                                
                                if lower_bound >= upper_bound:
                                    raise ValueError(f"Lower bound ({lower_bound}) must be less than upper bound ({upper_bound})")
                                    
                                processing_elements[node_id] = THR(
                                    lower_bound=lower_bound,
                                    upper_bound=upper_bound,
                                    clk=clk,
                                    rtl_sim=rtl_sim,
                                    rtl_power_estimation=rtl_power,
                                    save_visualization=save_viz)
                            except Exception as e:
                                raise RuntimeError(f"Failed to create THR module: {e}")

                        elif node_label == "FFT":
                            try:
                                berger_bands_raw = properties["Berger Bands"]["value"]
                                berger_bands = parse_berger_bands(berger_bands_raw)
                                logging.debug(f'berger_bands: {berger_bands}, type: {type(berger_bands)}')
                                
                                n_samples = int(properties["Number of Samples"]["value"])
                                if n_samples <= 0:
                                    raise ValueError(f"Number of samples must be positive, got {n_samples}")
                                    
                                logging.debug(f'FFT n_samples: {n_samples}, type: {type(n_samples)}')
                                
                                fs = float(properties["Sampling Frequency"]["value"])
                                if fs <= 0:
                                    raise ValueError(f"Sampling frequency must be positive, got {fs}")
                                    
                                logging.debug(f'FFT fs: {fs}, type: {type(fs)}')
                                
                                processing_elements[node_id] = FFT(berger_bands=berger_bands,
                                                                 n_samples=n_samples,
                                                                 fs=fs,
                                                                 clk=clk,
                                                                 rtl_sim=rtl_sim,
                                                                 save_visualization=save_viz)
                            except Exception as e:
                                raise RuntimeError(f"Failed to create FFT module: {e}")

                        elif node_label == "BBF":
                            try:
                                fs = float(properties["Sampling Frequency"]["value"])
                                if fs <= 0:
                                    raise ValueError(f"Sampling frequency must be positive, got {fs}")
                                    
                                berger_bands_raw = properties["Berger Bands"]["value"]
                                berger_bands = parse_berger_bands(berger_bands_raw)
                                logging.debug(f'BBF berger_bands: {berger_bands}, type: {type(berger_bands)}')
                                
                                processing_elements[node_id] = BBF(
                                    fs=fs,
                                    berger_bands=berger_bands,
                                    clk=clk,
                                    rtl_sim=rtl_sim,
                                    rtl_power_estimation=rtl_power,
                                    save_visualization=save_viz)
                            except Exception as e:
                                raise RuntimeError(f"Failed to create BBF module: {e}")

                        elif node_label == "PWXC":
                            try:
                                n_channels = int(properties["Number of Channels"]["value"])
                                if n_channels <= 0:
                                    raise ValueError(f"Number of channels must be positive, got {n_channels}")
                                    
                                processing_elements[node_id] = PWXC(
                                    n_channels=n_channels,
                                    clk=clk,
                                    save_visualization=save_viz,
                                    rtl_sim=rtl_sim,
                                    rtl_power_estimation=rtl_power)
                            except Exception as e:
                                raise RuntimeError(f"Failed to create PWXC module: {e}")

                        else:
                            raise ValueError(f"Unknown module type '{node_label}' in node {node_id}")
                            
                    except Exception as e:
                        raise RuntimeError(f"Error creating module node {node_id} ({node_label}): {e}")

                else:
                    raise ValueError(f"Unknown node type '{node_type}' in node {node_id}")
                    
            except Exception as e:
                logging.error(f"Failed to create node {node_id}: {e}")
                raise

        # Make the connections with error handling
        try:
            for edge in pipeline_data["edges"]:
                try:
                    source_id = edge["source"]
                    target_id = edge["target"]

                    if source_id not in processing_elements:
                        raise ValueError(f"Source node {source_id} not found in processing elements")
                    if target_id not in processing_elements:
                        raise ValueError(f"Target node {target_id} not found in processing elements")

                    source_pe = processing_elements[source_id]
                    target_pe = processing_elements[target_id]

                    source_pe.add_output(target_pe)
                    target_pe.add_input(source_pe)
                    
                    logging.debug(f"Connected {source_id} -> {target_id}")
                    
                except Exception as e:
                    raise RuntimeError(f"Failed to connect {source_id} -> {target_id}: {e}")
                    
        except Exception as e:
            raise RuntimeError(f"Error creating pipeline connections: {e}")

    except Exception as e:
        logging.error(f"Pipeline generation failed: {e}")
        raise

    return processing_elements


def run_pipeline(pipeline_data):
    """Main pipeline execution function with comprehensive error handling."""
    try:
        # Parse and validate JSON
        try:
            pipeline_data, error = parse_pipeline_config(pipeline_data)
            if error:
                logging.error(f"Pipeline parse error: {error}")
                return {"error": f"Pipeline configuration error: {error}"}
            logging.debug(f'Parsed pipeline data: {pipeline_data}')
        except Exception as e:
            logging.error(f"Failed to parse pipeline data: {e}")
            return {"error": f"Failed to parse pipeline configuration: {e}"}

        # Instantiate processing elements
        try:
            processing_elements = generate_pipeline(pipeline_data)
            logging.debug(f"Created {len(processing_elements)} processing elements")
        except Exception as e:
            logging.error(f"Failed to generate pipeline: {e}")
            return {"error": f"Failed to create pipeline modules: {e}"}

        # Run the processing elements
        try:
            for pe_id, pe in processing_elements.items():
                try:
                    logging.debug(f"Running PE {pe_id}: {pe}")
                    pe.run()
                    logging.debug(f"Successfully ran PE {pe_id}")
                except Exception as e:
                    logging.error(f"Failed to run PE {pe_id}: {e}")
                    raise RuntimeError(f"Processing element '{pe}' (ID: {pe_id}) failed to execute: {e}")
        except Exception as e:
            logging.error(f"Pipeline execution failed: {e}")
            return {"error": f"Pipeline execution failed: {e}"}

        # Generate results
        try:
            results = {
                "message": "Pipeline run successfully",
                "node_properties": {
                    node["id"]: {
                        "label": node["label"],
                        "name": node.get("name", ""),
                        "nodeType": node["nodeType"],
                        "properties": node.get("properties", {})
                    }
                    for node in pipeline_data["nodes"]
                },
                "connections": {
                    edge["source"]: edge["target"]
                    for edge in pipeline_data["edges"]
                },
                "metrics": [],
                "output_data": {}
            }

            # Store simulation data with error handling
            for node_id, pe in processing_elements.items():
                try:
                    results["output_data"][node_id] = convert_numpy_to_list(pe.simulation_data)
                except Exception as e:
                    logging.error(f"Failed to convert simulation data for PE {node_id}: {e}")
                    return {"error": f"Failed to process results from module '{pe}' (ID: {node_id}): {e}"}

            logging.info("Pipeline executed successfully")
            return results
            
        except Exception as e:
            logging.error(f"Failed to generate results: {e}")
            return {"error": f"Failed to generate pipeline results: {e}"}

    except Exception as e:
        logging.error(f"Unexpected error in run_pipeline: {e}")
        return {"error": f"Unexpected error during pipeline execution: {e}"}


def test_pipeline():
    ### this is just for testing, not for production

    top_level_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True,
                                   text=True).stdout.strip()

    # load pipeline file
    pipeline_file = f"{top_level_dir}/backend/dev_tests/simple_fft_pipeline.json"
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
