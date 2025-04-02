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

    json_result = run_pipeline(pipeline_data)

    # return the json_result? idk how
    
    return jsonify({"message": "Pipeline run successfully", "metrics": output_data, "storage": storage_data})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
