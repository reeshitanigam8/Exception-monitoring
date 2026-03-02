from flask import Flask, render_template, jsonify, request
import os
import json
import threading
import sys
import io
import monitor
from monitor import main as run_monitoring_engine, load_config

app = Flask(__name__, template_folder='../templates')

# In-memory storage for logs and findings
logs = []
current_status = "Idle"
last_findings = {}
waiting_for_input = False
input_prompt = ""

class LogCapturer:
    def write(self, message):
        if message.strip():
            logs.append(message.strip())
    def flush(self):
        pass

def run_pipeline():
    global current_status, last_findings, waiting_for_input, input_prompt
    current_status = "Running"
    
    # Override monitor's input with web-based waiting state
    def web_input(prompt):
        global waiting_for_input, input_prompt
        input_prompt = prompt
        waiting_for_input = True
        while waiting_for_input:
            import time
            time.sleep(1)
        return ""

    monitor.get_user_input = web_input

    old_stdout = sys.stdout
    sys.stdout = LogCapturer()
    try:
        run_monitoring_engine()
        current_status = "Completed"
    except Exception as e:
        logs.append(f"ERROR: {str(e)}")
        current_status = "Error"
    finally:
        sys.stdout = old_stdout

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    return jsonify({
        "status": current_status,
        "logs": logs[-30:], 
        "waiting": waiting_for_input,
        "prompt": input_prompt
    })

@app.route('/api/respond', methods=['POST'])
def respond_input():
    global waiting_for_input
    waiting_for_input = False
    return jsonify({"message": "Resumed"})

@app.route('/api/run', methods=['POST'])
def trigger_run():
    global logs, current_status
    if current_status == "Running":
        return jsonify({"message": "Monitoring is already running"}), 400
    
    logs = [] # Clear logs for new run
    thread = threading.Thread(target=run_pipeline)
    thread.daemon = True
    thread.start()
    return jsonify({"message": "Monitoring started"})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    target_name = request.form.get('target', 'INPUT_CSV') # Default to INPUT_CSV
    
    config = load_config()
    filename = config.get(target_name)
    
    if file and filename:
        save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config.get("DATA_DIR", "data"), filename)
        file.save(save_path)
        logs.append(f"Successfully uploaded: {filename}")
        return jsonify({"message": f"Uploaded {filename} successfully"})
    return jsonify({"message": "Target name not found in config"}), 400

@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    if request.method == 'POST':
        new_config = request.json
        with open(config_path, 'w') as f:
            json.dump(new_config, f, indent=4)
        return jsonify({"message": "Config updated"})
    
    with open(config_path, 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    # Ensure templates directory exists
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), exist_ok=True)
    app.run(debug=True, port=5000)
