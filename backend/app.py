from flask import Flask, request, jsonify
from flask_cors import CORS
from run_pipeline import run_pipeline
import json
import logging

app = Flask(__name__)
# Accept any http://localhost:<port> origin, keep credentials support
CORS(
    app,
    resources={r"/*": {"origins": r"http://localhost:\d+"}},
    supports_credentials=True,
)

logging.basicConfig(filename='backend.log', level=logging.DEBUG)

@app.route('/run-pipeline', methods=['POST', 'OPTIONS'])
def run_pipeline_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        request_data = request.get_json(force=True)
        
        # Extract analysis settings (with defaults)
        analysis_settings = request_data.pop('analysis_settings', {})
        run_power_latency = analysis_settings.get('run_power_latency', True)
        run_accuracy = analysis_settings.get('run_accuracy', True)
        
        # The remaining data is the pipeline configuration
        pipeline_json = request_data
        
        logging.debug("🧩 Pipeline received: %s", pipeline_json)
        logging.debug("⚙️ Analysis settings: power_latency=%s, accuracy=%s", run_power_latency, run_accuracy)

        result = run_pipeline(pipeline_json, 
                            run_power_latency=run_power_latency,
                            run_accuracy=run_accuracy)

        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)
    except Exception as e:
        logging.error("❌ Error in pipeline API: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == '__main__':
    # Disable auto-reloader to prevent spawning multiple processes when launched from Electron
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)
