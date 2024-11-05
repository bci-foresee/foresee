from flask import Flask, jsonify, render_template, request
import os
import visualize
import visualize.visualize
import json

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test():
    return render_template("test.html")


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
    with open(
            '/workspaces/aloha-verilog/app/static/pipelines/create/nodes.json',
            'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/create/update_nodes', methods=['POST'])
def update_create_nodes_data():
    new_node_data = request.get_json()

    with open(
            '/workspaces/aloha-verilog/app/static/pipelines/create/nodes.json',
            'w') as f:
        json.dump(new_node_data, f, indent=4)

    return jsonify({'message': 'Node added successfully'})


@app.route('/create/edges.json')
def get_create_edges_data():
    with open(
            '/workspaces/aloha-verilog/app/static/pipelines/create/edges.json',
            'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/create/update_edges', methods=['POST'])
def update_create_edges_data():
    new_edges_data = request.get_json()

    with open(
            '/workspaces/aloha-verilog/app/static/pipelines/create/edges.json',
            'w') as f:
        json.dump(new_edges_data, f, indent=4)

    return jsonify({'message': 'Node added successfully'})


@app.route('/pe.json')
def get_pe_data():
    with open(
            '/workspaces/aloha-verilog/app/static/processing_elements/pe.json',
            'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/create_pipeline', methods=['POST'])
def save_new_pipeline():
    new_pipeline_data = request.get_json()

    # Create pipeline directory
    # Reset the nodes and edges in the pipeline creator canvas
    # Make sure that the new pipeline is good to go

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
    visualize_filename = "/workspaces/aloha-verilog/app/visualize/input_csv/dummy_accuracy.csv"
    visualize.visualize.plot_visualizations(visualize_filename,
                                            accuracy=accuracy_selected,
                                            time=latency_selected,
                                            power=power_selected,
                                            custom=custom_selected)

    return render_template('output.html',
                           accuracy_selected=accuracy_selected,
                           latency_selected=latency_selected,
                           power_selected=power_selected,
                           custom_selected=custom_selected)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
