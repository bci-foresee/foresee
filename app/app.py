import sys

sys.path.append("./")

from flask import Flask, jsonify, render_template, request
import os
from visualize.visualize import plot_visualizations
import json
import pandas as pd

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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
