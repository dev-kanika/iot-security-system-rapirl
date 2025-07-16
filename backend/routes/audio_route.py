from flask import Blueprint, request, jsonify
import librosa
import numpy as np
import joblib
import os
from datetime import datetime
from utils.logger import log_event

AUDIO_MODEL_PATH = os.path.join("models", "audio_model.pkl")
audio_model = joblib.load(AUDIO_MODEL_PATH)

label_map = {
    0: "Baby crying detected. Notifying guardian.",
    1: "Doorbell detected. Please check the entrance.",
    2: "Fire alarm detected! Evacuate immediately.",
    3: "Possible intrusion detected! Alerting security.",
    4: "Gunshot detected! Take cover and call emergency services."
}

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=16000, mono=True)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

audio_bp = Blueprint("audio", __name__)

@audio_bp.route("/audio", methods=["POST"])
def predict_audio():
    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    file = request.files['audio_file']
    temp_path = os.path.join("temp_audio.wav")
    file.save(temp_path)

    try:
        features = extract_features(temp_path).reshape(1, -1)
        pred = audio_model.predict(features)[0]
        message = label_map.get(pred, "Unknown sound detected.")

        log_event("audio", label_map.get(pred, "Unknown"))
        return jsonify({"prediction": int(pred), "message": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
