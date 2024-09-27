from flask import Flask, render_template, request
import os
import visualize
import visualize.visualize

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/output', methods=['POST'])
def output():
    # Get form data
    pipeline = request.form['pipeline']
    num_runs = int(request.form['numberRuns'])
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
    visualize_filename = "app/visualize/input_csv/dummy.csv"
    visualize.visualize.plot_visualizations(visualize_filename, accuracy=accuracy_selected, time=latency_selected, power=power_selected, custom=custom_selected)
   
    return render_template('output.html', accuracy_selected=accuracy_selected, latency_selected=latency_selected, power_selected=power_selected, custom_selected=custom_selected)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
