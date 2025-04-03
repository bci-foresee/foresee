from flask import Flask, request, jsonify
from pipeline_api import run_pipeline

app = Flask(__name__)

@app.route('/run-pipeline', methods=['POST'])
def run_pipeline_api():
    try:
        pipeline_json = request.get_json(force=True)
        result = run_pipeline(pipeline_json)

        # If run_pipeline already returns a Response (like with jsonify + status), pass it through
        if isinstance(result, tuple) and isinstance(result[0], dict):
            return jsonify(result[0]), result[1]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

