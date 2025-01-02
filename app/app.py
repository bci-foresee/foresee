import sys

sys.path.append("./")

from flask import Flask, jsonify, render_template, request
import os
from visualize.visualize import plot_visualizations
import json
import pandas as pd
from asa.utils import INPUT_PE, generate_signal
from asa import FFT, SVM, THR
import numpy as np
import csv

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

BASE_DIR = os.getenv(
    'PROJECT_ROOT',
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/pipeline', methods=['POST'])
def pipeline():
    selected_pipeline = request.form['selectPipeline'].lower().replace(
        ' ', '_')
    if selected_pipeline != "":
        return render_template('pipeline.html',
                               selected_pipeline=selected_pipeline)
    return render_template('index.html')


@app.route('/create_pipeline', methods=['POST'])
def create_pipeline():
    return render_template('create_pipeline.html')


@app.route('/create/nodes.json')
def get_create_nodes_data():
    with open(os.path.join(BASE_DIR, 'pipelines', 'create', 'nodes.json'),
              'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/create/update_nodes', methods=['POST'])
def update_create_nodes_data():
    new_node_data = request.get_json()

    with open(os.path.join(BASE_DIR, 'pipelines', 'create', 'nodes.json'),
              'w') as f:
        json.dump(new_node_data, f, indent=4)

    return jsonify({'message': 'Node added successfully'})


@app.route('/create/edges.json')
def get_create_edges_data():
    with open(os.path.join(BASE_DIR, 'pipelines', 'create', 'edges.json'),
              'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/create/update_edges', methods=['POST'])
def update_create_edges_data():
    new_edges_data = request.get_json()

    with open(os.path.join(BASE_DIR, 'pipelines', 'create', 'edges.json'),
              'w') as f:
        json.dump(new_edges_data, f, indent=4)

    return jsonify({'message': 'Node added successfully'})


@app.route('/pe.json')
def get_pe_data():
    with open(os.path.join(BASE_DIR, 'asa', 'pe.json'), 'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/pipeline/<pipeline_name>/d3/nodes')
def get_pipeline_nodes(pipeline_name):
    try:
        pipeline_path = os.path.join(BASE_DIR, 'pipelines', pipeline_name,
                                     'd3', 'nodes.json')
        with open(pipeline_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([])


@app.route('/pipeline/<pipeline_name>/d3/edges')
def get_pipeline_edges(pipeline_name):
    try:
        pipeline_path = os.path.join(BASE_DIR, 'pipelines', pipeline_name,
                                     'd3', 'edges.json')
        with open(pipeline_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([])


@app.route('/save_new_pipeline', methods=['POST'])
def save_new_pipeline():
    new_pipeline_data = request.get_json()

    new_pipeline_directory = os.path.join(BASE_DIR, 'app', 'static',
                                          'pipelines',
                                          new_pipeline_data["name"])

    try:
        os.makedirs(new_pipeline_directory)
        print(f"Directory '{new_pipeline_directory}' created successfully.")
    except OSError as error:
        print(f"Error creating directory: {error}")

    # TODO: write function that reads the nodes and edges and creates the pipeline.py file accordingly.

    # Reset edges and nodes after pipeline has been saved.
    with open(os.path.join(BASE_DIR, 'pipelines', 'create', 'edges.json'),
              'w') as f:
        json.dump([], f, indent=4)
    with open(os.path.join(BASE_DIR, 'pipelines', 'create', 'nodes.json'),
              'w') as f:
        json.dump([{
            'color': 'red',
            'id': 'loader',
            'label': 'Loader',
            'layer': 1,
            'x': 50,
            'y': 200
        }],
                  f,
                  indent=4)

    return jsonify({'message': 'Pipeline added successfully'})


@app.route('/output', methods=['POST'])
def output():
    # Get form data
    # num_runs = int(request.form['numberRuns'])
    accuracy_selected = False
    latency_selected = False
    power_selected = False
    custom_selected = None

    if 'accuracy' in request.form:
        accuracy_selected = True
    if 'latency' in request.form:
        latency_selected = True
    if 'power' in request.form:
        power_selected = True
    if 'custom' in request.form:
        custom_path = request.form['customPathInput']
        custom_selected = custom_path

    # Perform simulation or processing here using the data
    # TODO(btrevisan): connect with Shaan's logic.
    # simulation_result = simulate(pipeline, num_runs)

    # Create visualizations based on selected options
    # visualize_filename = os.path.join('data', f"{pipeline}_{num_runs}.csv")
    # TODO(btrevisan): Find ways to optimize data organization here.
    visualize_filename = os.path.join(BASE_DIR, "visualize", "input_csv",
                                      "dummy_accuracy.csv")
    plot_visualizations(visualize_filename,
                        accuracy=accuracy_selected,
                        time=latency_selected,
                        power=power_selected,
                        custom=custom_selected)

    return render_template('output.html',
                           accuracy_selected=accuracy_selected,
                           latency_selected=latency_selected,
                           power_selected=power_selected,
                           custom_selected=custom_selected)


@app.route("/dummy_data")
def get_dummy_data():
    try:
        df = pd.read_csv(
            os.path.join(BASE_DIR, 'app', 'dummy_data', 'pipeline_output.csv'))
        dummy_data = df.to_dict(orient="records")
        return jsonify(dummy_data)
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404


@app.route('/pipeline/<pipeline_name>/d3/output_data')
def get_pipeline_data(pipeline_name):
    try:
        df = pd.read_csv(
            os.path.join(BASE_DIR, 'pipelines', pipeline_name, 'd3',
                         'output_data.csv'))
        dummy_data = df.to_dict(orient="records")
        return jsonify(dummy_data)
    except FileNotFoundError:
        df = pd.read_csv(
            os.path.join(BASE_DIR, 'app', 'dummy_data', 'pipeline_output.csv'))
        dummy_data = df.to_dict(orient="records")
        return jsonify(dummy_data)


# Add call that puts the pipeline together and runs it.
@app.route("/run_pipeline", methods=['POST'])
def run_pipeline():
    pipeline_data = request.get_json()

    # input signal window
    input_fs = 400
    input_channels = 2  # 1 for demonstration (speed)
    input_samples = 8192

    input_signal = generate_signal(frequencies=[10, 20, 40],
                                   amplitudes=[20, 15, 10],
                                   fs=input_fs,
                                   n_channels=input_channels,
                                   n_samples=input_samples)

    # TODO: once the PEs are set up correctly with all of their inputs set, fix this to be more scalable.

    input_pe = INPUT_PE(input=input_signal, clk=0)

    fft_pe = FFT(berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80)],
                 n_samples=input_samples,
                 fs=input_fs,
                 clk=1,
                 rtl_sim=False,
                 save_visualization=False)

    some_weights = np.ones(10)

    svm_pe = SVM(weights=some_weights,
                 clk=1,
                 rtl_sim=False,
                 rtl_power_estimation=False,
                 save_visualization=False)

    thr_pe = THR(lower_bound=0,
                 upper_bound=1,
                 clk=15_700_000,
                 rtl_sim=True,
                 rtl_power_estimation=False,
                 save_visualization=False)

    input_pe.add_output(fft_pe)
    fft_pe.add_input(input_pe)
    fft_pe.add_output(svm_pe)
    svm_pe.add_input(fft_pe)
    svm_pe.add_output(thr_pe)
    thr_pe.add_input(svm_pe)

    elements = [input_pe, fft_pe, svm_pe, thr_pe]

    # Run pipeline
    for pe in elements:
        pe.run()

    output_data = []
    for element in elements:
        element_simulation_data = dict(element.simulation_data.items())
        print(element_simulation_data)
        accuracy_value = np.mean(
            np.array(element_simulation_data['output_data']))
        latency_value = element_simulation_data['latency']
        power_value = np.mean(
            np.array(element_simulation_data['power_dict'])
        ) if element_simulation_data['power_dict'] is not None else 0
        accuracy = accuracy_value if accuracy_value is not None else 0
        latency = latency_value if latency_value is not None else 0
        power = power_value if power_value is not None else 0
        element_output = {
            "PE": element_simulation_data['name'],
            "Accuracy": accuracy,
            "Latency": latency,
            "Power": power
        }
        output_data.append(element_output)

    # Save output
    filename = os.path.join(BASE_DIR, "pipelines", pipeline_data['name'], "d3",
                            "output_data.csv")

    fieldnames = ["PE", "Accuracy", "Latency", "Power"]

    try:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(output_data)

        print(f"CSV file '{filename}' created successfully.")

    except (ValueError, TypeError) as e:  #Catch data format errors
        print(f"Error with input data: {e}")
        raise
    except OSError as e:
        print(f"Error creating file: {e}")
        raise

    return jsonify({'message': 'Pipeline run successfully'})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
