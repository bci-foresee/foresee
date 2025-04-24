from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline_api import run_pipeline
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins


@app.route('/run-pipeline', methods=['POST'])
def run_pipeline_api():
    try:
        pipeline_json = request.get_json(force=True)
        print("🧩 Type of pipeline_json:", type(pipeline_json))
        print("🧩 Pipeline received:", pipeline_json)

        result = run_pipeline(pipeline_json)

        if isinstance(result, tuple) and isinstance(result[0], dict):
            return jsonify(result[0]), result[1]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
