from flask import Blueprint, request
import librosa
import numpy as np
import joblib
import os
from werkzeug.utils import secure_filename
from config.events import EVENTS

audio_bp = Blueprint('audio_bp', __name__)

# Load model once
model = joblib.load("models/audio_model.pkl")

# Label-to-event mapping (match index with model output)
label_map = {
    0: EVENTS["audio"]["BABY_CRYING"],
    1: EVENTS["audio"]["DOORBELL"],
    2: EVENTS["audio"]["FIRE_ALARM"],
    3: EVENTS["audio"]["MOTION_DETECTED"],  # Replacing intrusion with "Motion Detected"
    4: EVENTS["audio"]["GUNSHOT"]
}

# Extract MFCC features
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=16000, mono=True)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

# Prediction Endpoint
@audio_bp.route('/upload_audio', methods=['POST'])
def predict_audio_event():
    print("\n=== AUDIO UPLOAD ENDPOINT HIT ===")

    # Validate uploaded file
    if 'file' not in request.files:
        print("❌ 'file' not found in request.files")
        return "No audio file provided", 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    temp_path = os.path.join("temp_audio", filename)
    os.makedirs("temp_audio", exist_ok=True)
    file.save(temp_path)

    try:
        # Extract features and predict
        features = extract_features(temp_path).reshape(1, -1)
        pred = model.predict(features)[0]
        print(f"🧠 Model Prediction: {pred}")

        # Return mapped message or fallback
        message = label_map.get(pred, "Unknown sound detected.")
        return message, 200

    except Exception as e:
        print(f"❗ Error during prediction: {e}")
        return str(e), 500

    finally:
        try:
            os.remove(temp_path)
            print(f"🧹 Temp file deleted: {temp_path}")
        except Exception as cleanup_error:
            print(f"⚠️ Cleanup error: {cleanup_error}")
