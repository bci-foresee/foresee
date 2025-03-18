from flask import Flask, request, jsonify, abort
import numpy as np
import os
import csv
import math

# Mock classes for processing elements (replace with actual implementations)
class PE:
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.simulation_data = {
            "output_data": np.random.rand(10),
            "latency": np.random.randint(10, 100),
            "power_dict": np.random.rand(10),
            "name": name,
            "output_dimensions": (2, 2),
        }

    def add_input(self, pe):
        self.inputs.append(pe)

    def add_output(self, pe):
        self.outputs.append(pe)

    def run(self):
        print(f"Running {self.name}")

class INPUT_PE(PE):
    def __init__(self, input):
        super().__init__("Input")

class FFT(PE):
    def __init__(self):
        super().__init__("FFT")

class BBF(PE):
    def __init__(self):
        super().__init__("BBF")

class PWXC(PE):
    def __init__(self):
        super().__init__("PWXC")

class SVM(PE):
    def __init__(self):
        super().__init__("SVM")

class THR(PE):
    def __init__(self):
        super().__init__("THR")

class StorageModel:
    def __init__(self):
        self.result = {"TOTAL_POWER": np.random.rand()}

    def run(self):
        pass

    def get_result(self, field):
        return self.result.get(field, 0)

# Flask App
app = Flask(__name__)

@app.route('/process-graph', methods=['POST'])
def run_pipeline():
    pipeline_data = request.get_json()
    if not pipeline_data or "nodes" not in pipeline_data or "edges" not in pipeline_data:
        return jsonify({"error": "Invalid pipeline data"}), 400

    nodes = pipeline_data["nodes"]
    edges = pipeline_data["edges"]
    final_pes = {}

    # Find input and storage nodes
    input_nodes = [n for n in nodes if n["label"] == "Input"]
    storage_nodes = [n for n in nodes if n["label"] == "Storage"]

    if len(input_nodes) != 1 or len(storage_nodes) != 1:
        return jsonify({"error": "Exactly one Input and one Storage node required"}), 400

    input_node = input_nodes[0]
    storage_node = storage_nodes[0]

    # Initialize processing elements
    pe_types = {
        "FFT": FFT,
        "BBF": BBF,
        "PWXC": PWXC,
        "SVM": SVM,
        "THR": THR,
    }

    for node in nodes:
        if node["label"] == "Input":
            final_pes[node["id"]] = INPUT_PE(input={})
        elif node["label"] == "Storage":
            final_pes[node["id"]] = StorageModel()
        elif node["label"] in pe_types:
            final_pes[node["id"]] = pe_types[node["label"]]()
        else:
            return jsonify({"error": f"Unknown node type: {node['label']}"}), 400

    # Connect edges
    for edge in edges:
        if edge["source"] in final_pes and edge["target"] in final_pes:
            final_pes[edge["source"]].add_output(final_pes[edge["target"]])
            final_pes[edge["target"]].add_input(final_pes[edge["source"]])
        else:
            return jsonify({"error": f"Invalid edge: {edge}"}), 400

    # Run the pipeline
    for pe in final_pes.values():
        if isinstance(pe, PE):  # Avoid running StorageModel
            pe.run()

    # Compute output metrics
    output_data = []
    for pe_id, pe in final_pes.items():
        if isinstance(pe, PE):  # Skip StorageModel
            accuracy = np.mean(pe.simulation_data["output_data"])
            latency = pe.simulation_data["latency"]
            power = np.mean(pe.simulation_data["power_dict"]) if pe.simulation_data["power_dict"] is not None else 0
            output_data.append({"PE": pe.name, "Accuracy": accuracy, "Latency": latency, "Power": power})

    # Compute storage metrics
    storage = final_pes[storage_node["id"]]
    storage.run()
    storage_data = {"TOTAL_POWER": storage.get_result("TOTAL_POWER")}

    # Save to CSV
    csv_filename = "output_data.csv"
    try:
        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["PE", "Accuracy", "Latency", "Power"])
            writer.writeheader()
            writer.writerows(output_data)
        print(f"CSV file '{csv_filename}' created successfully.")
    except Exception as e:
        return jsonify({"error": f"Error creating CSV: {e}"}), 500

    return jsonify({"message": "Pipeline run successfully", "metrics": output_data, "storage": storage_data})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
