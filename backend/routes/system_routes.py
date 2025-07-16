from flask import Blueprint, jsonify, request

system_bp = Blueprint("system", __name__)

@system_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "System online"})

@system_bp.route("/start_monitoring", methods=["POST"])
def start_monitoring():
    return jsonify({"message": "Monitoring started"})

@system_bp.route("/stop_monitoring", methods=["POST"])
def stop_monitoring():
    return jsonify({"message": "Monitoring stopped"})

@system_bp.route("/heartbeat", methods=["POST"])
def heartbeat():
    return jsonify({"message": "Heartbeat received"})