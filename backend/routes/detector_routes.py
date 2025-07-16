from flask import Blueprint, jsonify
import subprocess
import os

detector_bp = Blueprint("detector", __name__)

SCRIPTS = {
    "crowd": "crowd_density.py",
    "animal": "animal_intrusion.py",
    "object": "suspicious_object.py",
    "motion": "motion_detector.py"
}

@detector_bp.route("/<event>", methods=["GET"])
def start_detection(event):
    script = SCRIPTS.get(event)
    if not script:
        return jsonify({"error": "Invalid event type"}), 400

    script_path = os.path.join("detectors", script)
    try:
        subprocess.Popen(["python", script_path])
        return jsonify({"status": f"{event} detection started."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
