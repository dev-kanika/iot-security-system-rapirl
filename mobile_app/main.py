from flask import Flask, jsonify, request
import random

app = Flask(__name__)

EVENTS = {
    "photo": [
        ("PERSON_DETECTED", "Unrecognized person at the door."),
        ("SUSPICIOUS_OBJECT", "Suspicious object detected."),
        ("LOW_LIGHT", "Low visibility detected."),
        ("NO_MASK", "Face mask not detected."),
        ("CROWD_DENSITY", "High crowd density detected."),
        ("ANIMAL_DETECTED", "Animal intrusion detected.")
    ],
    "audio": [
        ("FIRE_ALARM", "Fire alarm detected! Evacuate now!"),
        ("GLASS_BREAKING", "Glass breaking detected!"),
        ("BABY_CRYING", "Baby crying detected."),
        ("DOORBELL", "Doorbell sound detected."),
        ("GUNSHOT", "Gunshot detected! Call emergency services."),
        ("MOTION_DETECTED", "Motion detected during restricted hours.")
    ]
}

@app.route("/status", methods=["GET"])
def status():
    return "System online"

@app.route("/start_monitoring", methods=["POST"])
def start_monitoring():
    return "Monitoring started"

@app.route("/stop_monitoring", methods=["POST"])
def stop_monitoring():
    return "Monitoring stopped"

@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    return "Heartbeat received"

@app.route("/upload_image", methods=["POST"])
def upload_image():
    event = random.choice(EVENTS["photo"])
    return event[0] + ": " + event[1]

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    event = random.choice(EVENTS["audio"])
    return event[0] + ": " + event[1]

@app.route("/check_alerts", methods=["GET"])
def check_alerts():
    return "No alerts"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
