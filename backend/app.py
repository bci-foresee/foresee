from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline_api import run_pipeline
import json

app = Flask(__name__)
# Enable CORS for all routes during development with credentials
CORS(app, 
     resources={r"/*": {"origins": "http://localhost:3000"}},
     supports_credentials=True)

@app.route('/run-pipeline', methods=['POST', 'OPTIONS'])
def run_pipeline_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        pipeline_json = request.get_json(force=True)
        print("🧩 Type of pipeline_json:", type(pipeline_json))
        print("🧩 Pipeline received:", pipeline_json)

        result = run_pipeline(pipeline_json)

        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)
    except Exception as e:
        print("❌ Error in pipeline API:", str(e))
        return jsonify({"error": str(e)}), 500


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == '__main__':
    # Disable auto-reloader to prevent spawning multiple processes when launched from Electron
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)
