import sys

sys.path.append("./")

from flask import Flask, jsonify, render_template, request, abort
import os
from visualize.visualize import plot_visualizations
import json
import pandas as pd
from asa.utils import INPUT_PE, generate_signal
from asa import FFT, SVM, THR, PWXC, BBF
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


# TODO: edges are not being saved correctly
@app.route('/save_new_pipeline', methods=['POST'])
def save_new_pipeline():
    new_pipeline_data = request.get_json()

    if not new_pipeline_data or "name" not in new_pipeline_data:
        return jsonify({'error': 'Pipeline name is required'}), 400

    # Sanitize pipeline name
    pipeline_name = new_pipeline_data["name"].lower().replace(' ', '_')
    new_pipeline_data["name"] = pipeline_name

    new_pipeline_directory = os.path.join(BASE_DIR, 'pipelines', pipeline_name)

    # Ensure parent directory exists
    parent_dir = os.path.join(BASE_DIR, 'pipelines')
    if not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir)
        except OSError as error:
            return jsonify(
                {'error':
                 f'Failed to create parent directory: {str(error)}'}), 500

    try:
        if not os.path.exists(new_pipeline_directory):
            os.makedirs(new_pipeline_directory)

        # Create d3 subdirectory for nodes and edges
        d3_directory = os.path.join(new_pipeline_directory, 'd3')
        if not os.path.exists(d3_directory):
            os.makedirs(d3_directory)

        # Save nodes and edges to the d3 directory
        nodes_file = os.path.join(d3_directory, 'nodes.json')
        edges_file = os.path.join(d3_directory, 'edges.json')

        with open(nodes_file, 'w') as f:
            json.dump(new_pipeline_data["nodes"], f, indent=4)

        with open(edges_file, 'w') as f:
            json.dump(new_pipeline_data["edges"], f, indent=4)

    except OSError as error:
        return jsonify({'error': str(error)}), 500

    return jsonify({
        'message': 'Pipeline added successfully',
        'name': new_pipeline_data["name"]
    })


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


# Loads up the pipeline in edit mode
@app.route("/edit_pipeline", methods=['GET'])
def edit_pipeline():
    selected_pipeline = request.args.get('name')
    return render_template('create_pipeline.html',
                           selected_pipeline=selected_pipeline)


def find_pe_by_name(nodes, pe):
    for node in nodes:
        print(node)
        if node['label'] == pe:
            return node
    return None


# Add call that puts the pipeline together and runs it.
@app.route("/run_pipeline", methods=['POST'])
def run_pipeline():
    pipeline_data = request.get_json()
    final_pes = {}
    elements = []

    # Get input node
    input = find_pe_by_name(pipeline_data['nodes'], "Input")
    if input is None:
        abort(400, description="Input PE not found in nodes.")

    # Input signal window
    input_signal = generate_signal(
        frequencies=input.get('frequencies', [10, 20, 40]),
        amplitudes=input.get('amplitudes', [20, 15, 10]),
        fs=input.get('input_fs', 400),
        n_channels=input.get('input_channels', 2),
        n_samples=input.get('input_samples', 8192))

    input_pe = INPUT_PE(input=input_signal, clk=input.get('clk', 0))
    final_pes[input['id']] = input_pe
    elements.append(input_pe)

    for node in pipeline_data['nodes']:
        if node['label'] == "FFT":
            fft_pe = FFT(berger_bands=node.get('berger_bands',
                                               [(0.1, 4), (4, 8), (8, 12),
                                                (12, 30), (30, 80)]),
                         n_samples=node.get('input_samples', 8192),
                         fs=node.get('input_fs', 400),
                         clk=node.get('clk', 1),
                         rtl_sim=node.get('rtl_sim', False),
                         save_visualization=node.get('save_visualization',
                                                     False))
            final_pes[node['id']] = fft_pe
            elements.append(fft_pe)
        elif node['label'] == "BBF":
            bbf_pe = BBF(fs=node.get("input_fs", 400),
                         berger_bands=node.get('berger_bands',
                                               [(0.1, 4), (4, 8), (8, 12),
                                                (12, 30), (30, 80)]),
                         clk=node.get('clk', 1),
                         save_visualization=node.get('save_visualization',
                                                     False))
            final_pes[node['id']] = bbf_pe
            elements.append(bbf_pe)
        elif node['label'] == "PWXC":
            pwxc_pe = PWXC(n_channels=input.get('n_channels', 2),
                           clk=node.get('clk', 1),
                           save_visualization=node.get('save_visualization',
                                                       False),
                           rtl_sim=node.get('rtl_sim', False),
                           rtl_power_estimation=node.get(
                               'rtl_power_estimation', False))
            final_pes[node['id']] = pwxc_pe
            elements.append(pwxc_pe)
        elif node['label'] == "SVM":
            svm_pe = SVM(weights=node.get('weights', np.ones(10)),
                         clk=node.get('clk', 1),
                         rtl_sim=node.get('rtl_sim', False),
                         rtl_power_estimation=node.get('rtl_power_estimation',
                                                       False),
                         save_visualization=node.get('save_visualization',
                                                     False))
            final_pes[node['id']] = svm_pe
            elements.append(svm_pe)
        elif node['label'] == "THR":
            thr_pe = THR(lower_bound=node.get('lower_bound', 0),
                         upper_bound=node.get('upper_bound', 1),
                         clk=node.get('clk', 15_700_000),
                         rtl_sim=node.get('rtl_sim', True),
                         rtl_power_estimation=node.get('rtl_power_estimation',
                                                       False),
                         save_visualization=node.get('save_visualization',
                                                     False))
            final_pes[node['id']] = thr_pe
            elements.append(thr_pe)

    for edge in pipeline_data['edges']:
        final_pes[edge['source']].add_output(final_pes[edge['target']])
        final_pes[edge['target']].add_input(final_pes[edge['source']])

    # Run pipeline
    for pe in elements:
        pe.run()

    output_data = []
    for element in elements:
        element_simulation_data = dict(element.simulation_data.items())
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


@app.route('/available_pipelines')
def get_available_pipelines():
    pipelines_dir = os.path.join(BASE_DIR, 'pipelines')
    pipelines = []

    try:
        for item in os.listdir(pipelines_dir):
            if item in [
                    'create', '__pycache__', '__init__.py', 'README.md',
                    'pipeline.py'
            ]:
                continue

            full_path = os.path.join(pipelines_dir, item)
            # Only include if it's a directory and has a d3 subfolder
            if os.path.isdir(full_path) and os.path.exists(
                    os.path.join(full_path, 'd3')):
                pipelines.append(item)

    except OSError as error:
        return jsonify([])

    return jsonify(pipelines)


@app.route('/create_default/nodes.json')
def get_create_default_nodes_data():
    with open(
            os.path.join(BASE_DIR, 'pipelines', 'create_default',
                         'nodes.json'), 'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/create_default/edges.json')
def get_create_default_edges_data():
    with open(
            os.path.join(BASE_DIR, 'pipelines', 'create_default',
                         'edges.json'), 'r') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
