import logging
import os
import sys
import subprocess
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import jsonify
import json
import numpy as np
from scipy.io import loadmat
from sklearn.metrics import accuracy_score, confusion_matrix

from asa import TKEO, AVG, SVM, THR, FFT, BBF, PWXC
from asa.utils import INPUT_PE, generate_signal

logging.basicConfig(filename='backend.log', level=logging.DEBUG)


class EEGDatasetLoader:
    """Handles loading and processing of EEG datasets from .mat files"""
    
    def __init__(self, dataset_path, info_file_path):
        self.dataset_path = dataset_path
        self.info_file_path = info_file_path
        self.fs = None
        self.seizure_begin = None
        self.seizure_end = None
        self.data = None
        self.load_info()
    
    def load_info(self):
        """Load seizure timing and sampling frequency from .info file"""
        try:
            info_data = loadmat(self.info_file_path)
            self.fs = int(info_data['fs'][0][0])
            self.seizure_begin = info_data['seizure_begin'].flatten()
            self.seizure_end = info_data['seizure_end'].flatten()
            logging.debug(f"Loaded info: fs={self.fs}, seizures={len(self.seizure_begin)}")
        except Exception as e:
            raise RuntimeError(f"Failed to load info file {self.info_file_path}: {e}")
    
    def load_dataset(self):
        """Load EEG data from .mat file"""
        try:
            if os.path.isfile(self.dataset_path):
                # Single file
                data = loadmat(self.dataset_path)
                # Look for common EEG data field names
                possible_keys = ['data', 'signal', 'EEG', 'eeg_data', 'X']
                for key in possible_keys:
                    if key in data:
                        self.data = np.array(data[key])
                        break
                else:
                    # If no common key found, use the first non-metadata key
                    data_keys = [k for k in data.keys() if not k.startswith('__')]
                    if data_keys:
                        self.data = np.array(data[data_keys[0]])
                    else:
                        raise ValueError("No data found in .mat file")
            else:
                raise FileNotFoundError(f"Dataset file not found: {self.dataset_path}")
            
            logging.debug(f"Loaded dataset shape: {self.data.shape}")
            return self.data
            
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset {self.dataset_path}: {e}")
    
    def generate_labels(self, n_samples):
        """Generate binary labels (0=non-seizure, 1=seizure) for each sample"""
        labels = np.zeros(n_samples)
        
        for start_time, end_time in zip(self.seizure_begin, self.seizure_end):
            start_sample = int(start_time * self.fs)
            end_sample = int(end_time * self.fs)
            
            # Ensure indices are within bounds
            start_sample = max(0, min(start_sample, n_samples - 1))
            end_sample = max(0, min(end_sample, n_samples - 1))
            
            labels[start_sample:end_sample + 1] = 1
        
        return labels


def find_terminal_thr_nodes(pipeline_data):
    """Find all THR nodes that are terminal (have no outgoing edges)"""
    # Get all node IDs that are sources of edges
    source_nodes = {edge["source"] for edge in pipeline_data["edges"]}
    
    # Find THR nodes that are NOT sources (i.e., terminal nodes)
    terminal_thr_nodes = []
    for node in pipeline_data["nodes"]:
        if (node.get("label") == "THR" and 
            node["nodeType"] == "module" and 
            node["id"] not in source_nodes):
            terminal_thr_nodes.append(node["id"])
    
    return terminal_thr_nodes


def compute_pipeline_accuracy(pipeline_data, processing_elements, dataset_loader):
    """Compute accuracy for pipelines ending with THR nodes using windowed approach with pipeline reuse"""
    terminal_thr_nodes = find_terminal_thr_nodes(pipeline_data)
    
    if not terminal_thr_nodes:
        logging.debug("No terminal THR nodes found, returning default accuracy")
        return {"accuracy": 1.0, "message": "No terminal THR found, defaulting to 100% accuracy"}
    
    try:
        # Load the actual dataset
        eeg_data = dataset_loader.load_dataset()
        
        # Get windowing parameters from dataset loader (with fallback defaults)
        window_duration = getattr(dataset_loader, 'window_duration', 4.0)  # 4-second windows 
        overlap_ratio = getattr(dataset_loader, 'overlap_ratio', 0.5)  # 50% overlap
        fs = dataset_loader.fs
        
        window_samples = int(window_duration * fs)
        step_samples = int(window_samples * (1 - overlap_ratio))
        
        n_samples = eeg_data.shape[-1] if len(eeg_data.shape) > 1 else len(eeg_data)
        
        # Generate windows
        windows = []
        window_labels = []
        
        for start_idx in range(0, n_samples - window_samples + 1, step_samples):
            end_idx = start_idx + window_samples
            
            # Extract window data
            if len(eeg_data.shape) > 1:
                window_data = eeg_data[:, start_idx:end_idx]
            else:
                window_data = eeg_data[start_idx:end_idx]
            
            windows.append(window_data)
            
            # Generate window label (seizure if majority of window overlaps with seizure)
            window_time_start = start_idx / fs
            window_time_end = end_idx / fs
            
            # Check overlap with seizure periods
            seizure_overlap = 0
            for seizure_start, seizure_end in zip(dataset_loader.seizure_begin, dataset_loader.seizure_end):
                overlap_start = max(window_time_start, seizure_start)
                overlap_end = min(window_time_end, seizure_end)
                if overlap_start < overlap_end:
                    seizure_overlap += overlap_end - overlap_start
            
            # Label as seizure if >50% of window overlaps with seizure
            is_seizure = (seizure_overlap / window_duration) > 0.5
            window_labels.append(1 if is_seizure else 0)
        
        logging.debug(f"Generated {len(windows)} windows of {window_duration}s each")
        logging.debug(f"Window labels: {sum(window_labels)} seizure windows out of {len(window_labels)} total")
        
        # Find the input node ID
        input_node_id = None
        for node in pipeline_data["nodes"]:
            if node["nodeType"] == "input":
                input_node_id = node["id"]
                break
        
        if not input_node_id or input_node_id not in processing_elements:
            raise ValueError("No input node found in pipeline or processing elements")
        
        # Get the input processing element
        input_pe = processing_elements[input_node_id]
        
        # Process each window through the existing pipeline
        all_predictions = {}
        all_accuracies = {}
        
        for thr_node_id in terminal_thr_nodes:
            if thr_node_id in processing_elements:
                window_predictions = []
                
                for i, window_data in enumerate(windows):
                    try:
                        # Reset the input data for this window
                        input_pe.input = window_data
                        
                        # Clear simulation data from all processing elements to reset state
                        for pe_id, pe in processing_elements.items():
                            if str(pe_id).endswith("_dataset_loader"):
                                continue  # Skip dataset loaders
                            pe.simulation_data = {}
                            pe.output_data = None
                            # Reset any other state if needed
                            if hasattr(pe, 'reset'):
                                pe.reset()
                        
                        # Re-run the pipeline with the new window data
                        for pe_id, pe in processing_elements.items():
                            if str(pe_id).endswith("_dataset_loader"):
                                continue  # Skip dataset loaders
                            pe.run()
                            
                            # Log SVM outputs during windowed accuracy computation
                            if hasattr(pe, 'name') and pe.name == 'SVM' and i < 3:  # Only log first 3 windows to avoid spam
                                svm_output = pe.simulation_data.get('output_data', 'No output_data')
                                logging.info(f"🔍 WINDOW {i} SVM OUTPUT {pe_id}: {svm_output}")
                        
                        # Get THR prediction for this window
                        thr_pe = processing_elements[thr_node_id]
                        if hasattr(thr_pe, 'simulation_data') and thr_pe.simulation_data is not None:
                            output_data = thr_pe.simulation_data.get('output_data', 0)
                            
                            # Debug logging
                            if i < 3:  # Only log first 3 windows
                                logging.info(f"🔍 WINDOW {i} THR DEBUG - output_data: {output_data}, type: {type(output_data)}")
                            
                            # Handle both scalar and array outputs
                            output_array = np.array(output_data)
                            
                            if output_array.ndim > 0 and output_array.size > 0:
                                # Multi-dimensional or 1D array
                                prediction = output_array[0]
                            else:
                                # Scalar output (0-dimensional)
                                prediction = float(output_array)
                            
                            # Log THR input vs output for first few windows
                            if i < 3:
                                # Find SVM node that feeds into this THR
                                svm_pe_id = None
                                for edge in pipeline_data["edges"]:
                                    if edge["target"] == thr_node_id:
                                        for node in pipeline_data["nodes"]:
                                            if node["id"] == edge["source"] and node.get("label") == "SVM":
                                                svm_pe_id = edge["source"]
                                                break
                                
                                if svm_pe_id and svm_pe_id in processing_elements:
                                    svm_pe = processing_elements[svm_pe_id]
                                    svm_value = svm_pe.simulation_data.get('output_data', 'No data')
                                    logging.info(f"🎯 WINDOW {i} THR INPUT: {svm_value} → THR OUTPUT: {prediction}")
                            
                            # THR nodes output binary values directly (0 or 1)
                            binary_prediction = int(prediction)
                            window_predictions.append(binary_prediction)
                            
                            if i < 3:  # Only log first 3 windows
                                logging.info(f"🔍 WINDOW {i} THR DEBUG - final binary_prediction: {binary_prediction}")
                        else:
                            if i < 3:
                                logging.info(f"🔍 WINDOW {i} THR DEBUG - no simulation_data, defaulting to 0")
                            window_predictions.append(0)  # Default to non-seizure
                            
                    except Exception as e:
                        logging.warning(f"Failed to process window {i}: {e}")
                        logging.warning(f"Exception type: {type(e)}")
                        import traceback
                        logging.warning(f"Traceback: {traceback.format_exc()}")
                        window_predictions.append(0)  # Default to non-seizure on error
                
                # Compute accuracy for this THR node
                if len(window_predictions) == len(window_labels):
                    accuracy = accuracy_score(window_labels, window_predictions)
                    all_predictions[thr_node_id] = window_predictions
                    all_accuracies[thr_node_id] = accuracy
                    
                    logging.debug(f"THR node {thr_node_id} window-wise accuracy: {accuracy:.4f}")
                    logging.debug(f"Predictions: {window_predictions[:10]}... (showing first 10)")
                    logging.debug(f"True labels: {window_labels[:10]}... (showing first 10)")
                else:
                    logging.warning(f"Mismatch in predictions/labels length for THR {thr_node_id}")
                    all_accuracies[thr_node_id] = 0.0
        
        # Restore original input data after windowed processing
        input_pe.input = eeg_data
        
        # Clear and re-run the pipeline with original data to restore state
        for pe_id, pe in processing_elements.items():
            if str(pe_id).endswith("_dataset_loader"):
                continue  # Skip dataset loaders
            pe.simulation_data = {}
            pe.output_data = None
            if hasattr(pe, 'reset'):
                pe.reset()
        
        for pe_id, pe in processing_elements.items():
            if str(pe_id).endswith("_dataset_loader"):
                continue  # Skip dataset loaders
            pe.run()
        
        if all_accuracies:
            # Return average accuracy across all terminal THR nodes
            overall_accuracy = np.mean(list(all_accuracies.values()))
            return {
                "accuracy": overall_accuracy,
                "individual_accuracies": all_accuracies,
                "predictions": all_predictions,
                "true_labels": window_labels,
                "n_windows": len(window_labels),
                "window_duration": window_duration,
                "overlap_ratio": overlap_ratio,
                "message": f"Computed windowed accuracy from {len(terminal_thr_nodes)} terminal THR node(s) using {len(window_labels)} windows"
            }
        else:
            return {"accuracy": 0.0, "message": "Failed to compute windowed accuracy from THR predictions"}
            
    except Exception as e:
        logging.error(f"Error computing pipeline accuracy: {e}")
        return {"accuracy": 0.0, "error": f"Failed to compute accuracy: {e}"}


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


def generate_pipeline(pipeline_data, run_power_latency=True):
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
                    # Check if this is an EEG dataset input or synthetic signal input
                    if node_label == "EEG Dataset" or "Dataset Path" in properties:
                        # EEG Dataset Input Node
                        try:
                            dataset_path = properties.get("Dataset Path", {}).get("value", "")
                            info_file_path = properties.get("Info File Path", {}).get("value", "")
                            
                            # Get windowing parameters (with defaults)
                            window_duration = float(properties.get("Window Duration", {}).get("value", 4.0))
                            window_offset = float(properties.get("Window Offset", {}).get("value", 2.0))
                            
                            # Validate parameters
                            if window_duration <= 0:
                                raise ValueError(f"Window duration must be positive, got {window_duration}")
                            if window_offset < 0 or window_offset > window_duration:
                                raise ValueError(f"Window offset must be between 0 and window duration ({window_duration}), got {window_offset}")
                            
                            # Convert window offset to overlap ratio for internal calculations
                            overlap_ratio = 1.0 - (window_offset / window_duration)
                            
                            if not dataset_path:
                                raise ValueError(f"Dataset Path is required for EEG Dataset input node {node_id}")
                            if not info_file_path:
                                raise ValueError(f"Info File Path is required for EEG Dataset input node {node_id}")
                            
                            # Validate file paths
                            if not os.path.exists(dataset_path):
                                raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
                            if not os.path.exists(info_file_path):
                                raise FileNotFoundError(f"Info file not found: {info_file_path}")
                            
                            # Load EEG dataset
                            dataset_loader = EEGDatasetLoader(dataset_path, info_file_path)
                            eeg_data = dataset_loader.load_dataset()
                            
                            # Store windowing parameters in the dataset loader
                            dataset_loader.window_duration = window_duration
                            dataset_loader.overlap_ratio = overlap_ratio
                            
                            logging.debug(f'EEG dataset loaded: shape={eeg_data.shape}, fs={dataset_loader.fs}')
                            logging.debug(f'Windowing params: duration={window_duration}s, overlap={overlap_ratio}')
                            
                            # Store dataset loader for later accuracy computation
                            processing_elements[f"{node_id}_dataset_loader"] = dataset_loader
                            
                            # Create INPUT_PE with EEG data
                            processing_elements[node_id] = INPUT_PE(input=eeg_data, clk=0)
                            
                        except Exception as e:
                            raise RuntimeError(f"Error creating EEG dataset input node {node_id}: {e}")
                    
                    else:
                        # Synthetic Signal Input Node (existing functionality)
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
                            raise RuntimeError(f"Error creating synthetic input node {node_id} ({node_label}): {e}")

                # Handle processing module nodes
                elif node_type == "module":
                    try:
                        # Validate common properties
                        try:
                            clk = properties["Clock Frequency"]["value"]
                            rtl_sim = properties["Enable RTL Simulation"]["value"]
                            
                            # Power estimation is enabled only if BOTH RTL simulation is enabled AND run_power_latency is True
                            rtl_power = rtl_sim and run_power_latency
                            
                            if not isinstance(rtl_sim, bool):
                                raise ValueError(f"RTL Simulation setting must be true/false, got {rtl_sim}")
                            if not isinstance(clk, (int, float)) or clk < 0:
                                raise ValueError(f"Clock frequency must be a non-negative number, got {clk}")
                                
                        except KeyError as e:
                            raise ValueError(f"Missing required property in {node_label} node {node_id}: {e}")
                        except (ValueError, TypeError) as e:
                            raise ValueError(f"Invalid property value in {node_label} node {node_id}: {e}")

                        save_viz = False
                        logging.debug(f'{node_label} properties: rtl_sim={rtl_sim}, rtl_power={rtl_power}, clk={clk} (user_rtl_sim={rtl_sim}, run_power_latency={run_power_latency})')

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


def run_pipeline(pipeline_data, run_power_latency=True, run_accuracy=True):
    """Main pipeline execution function with comprehensive error handling and optional analysis."""
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
            processing_elements = generate_pipeline(pipeline_data, run_power_latency=run_power_latency)
            logging.debug(f"Created {len(processing_elements)} processing elements")
        except Exception as e:
            logging.error(f"Failed to generate pipeline: {e}")
            return {"error": f"Failed to create pipeline modules: {e}"}

        # Run the processing elements
        try:
            for pe_id, pe in processing_elements.items():
                # Skip dataset loaders (they're not actual processing elements)
                if str(pe_id).endswith("_dataset_loader"):
                    continue
                try:
                    logging.debug(f"Running PE {pe_id}: {pe}")
                    pe.run()
                    logging.debug(f"Successfully ran PE {pe_id}")
                    
                    # Log SVM outputs for debugging
                    if hasattr(pe, 'name') and pe.name == 'SVM':
                        svm_output = pe.simulation_data.get('output_data', 'No output_data')
                        logging.info(f"🔍 SVM OUTPUT {pe_id}: {svm_output}")
                        
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
                "output_data": {},
                "accuracy": None,
                "analysis_settings": {
                    "run_power_latency": run_power_latency,
                    "run_accuracy": run_accuracy
                }
            }

            # Store simulation data with error handling
            for node_id, pe in processing_elements.items():
                # Skip dataset loaders when storing simulation data
                if str(node_id).endswith("_dataset_loader"):
                    continue
                try:
                    results["output_data"][node_id] = convert_numpy_to_list(pe.simulation_data)
                except Exception as e:
                    logging.error(f"Failed to convert simulation data for PE {node_id}: {e}")
                    return {"error": f"Failed to process results from module '{pe}' (ID: {node_id}): {e}"}

            # Conditionally compute accuracy
            if run_accuracy:
                # Compute accuracy if EEG dataset is used and pipeline has terminal THR nodes
                dataset_loaders = {k: v for k, v in processing_elements.items() if str(k).endswith("_dataset_loader")}
                if dataset_loaders:
                    logging.debug(f"Found {len(dataset_loaders)} dataset loader(s), computing accuracy")
                    try:
                        # Use the first dataset loader found (assuming single dataset input for now)
                        dataset_loader = list(dataset_loaders.values())[0]
                        accuracy_results = compute_pipeline_accuracy(pipeline_data, processing_elements, dataset_loader)
                        results["accuracy"] = accuracy_results
                        logging.debug(f"Accuracy computation result: {accuracy_results}")
                    except Exception as e:
                        logging.error(f"Failed to compute accuracy: {e}")
                        results["accuracy"] = {
                            "accuracy": 0.0,
                            "error": f"Failed to compute accuracy: {e}"
                        }
                else:
                    # Default to 100% accuracy if no EEG dataset is used
                    terminal_thr_nodes = find_terminal_thr_nodes(pipeline_data)
                    if terminal_thr_nodes:
                        results["accuracy"] = {
                            "accuracy": 1.0,
                            "message": "No EEG dataset found, defaulting to 100% accuracy for synthetic data"
                        }
            else:
                logging.debug("Accuracy analysis disabled by settings")
                results["accuracy"] = {
                    "message": "Accuracy analysis disabled"
                }

            logging.info("Pipeline executed successfully")
            return results
            
        except Exception as e:
            logging.error(f"Failed to generate results: {e}")
            return {"error": f"Failed to generate pipeline results: {e}"}

    except Exception as e:
        logging.error(f"Unexpected error in run_pipeline: {e}")
        return {"error": f"Unexpected error during pipeline execution: {e}"}


def save_pipeline_results(result, output_dir="dev_tests", filename="pipeline_results.json"):
    """Save pipeline execution results to a JSON file"""
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Pipeline results written to {output_path}")
        return output_path
    except IOError as e:
        print(f"Error writing results to file: {e}")
        return None


def load_pipeline_config(pipeline_file):
    """Load pipeline configuration from JSON file"""
    try:
        with open(pipeline_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Pipeline configuration file not found: {pipeline_file}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON in pipeline configuration file: {pipeline_file}")
        return None


def test_pipeline():
    """Test pipeline execution with default configuration"""
    top_level_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True,
                                   text=True).stdout.strip()

    # Load pipeline file
    pipeline_file = f"{top_level_dir}/backend/dev_tests/simple_fft_pipeline.json"
    pipeline_data = load_pipeline_config(pipeline_file)
    
    if pipeline_data is None:
        return None

    # Run the pipeline with default analysis settings
    result = run_pipeline(pipeline_data, run_power_latency=True, run_accuracy=True)

    # Save results
    os.chdir(f"{top_level_dir}/backend/dev_tests/")
    save_pipeline_results(result)

    return result


def run_and_save_pipeline(pipeline_config_path, output_dir=None, output_filename=None, 
                         run_power_latency=True, run_accuracy=True):
    """Convenience function to run a pipeline and save results"""
    # Load configuration
    pipeline_data = load_pipeline_config(pipeline_config_path)
    if pipeline_data is None:
        return None
    
    # Run pipeline with specified analysis settings
    result = run_pipeline(pipeline_data, 
                         run_power_latency=run_power_latency, 
                         run_accuracy=run_accuracy)
    
    # Save results
    if output_dir is None:
        output_dir = os.path.dirname(pipeline_config_path)
    if output_filename is None:
        config_name = os.path.splitext(os.path.basename(pipeline_config_path))[0]
        output_filename = f"{config_name}_results.json"
    
    save_pipeline_results(result, output_dir, output_filename)
    return result


if __name__ == "__main__":
    test_pipeline()
