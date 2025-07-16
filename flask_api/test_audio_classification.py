import librosa
import numpy as np
import joblib

# Load model
model = joblib.load("audio_model.pkl")

# Label-to-alert mapping
label_map = {
    0: "Baby crying detected. Notifying guardian.",
    1: "Doorbell detected. Please check the entrance.",
    2: "Fire alarm detected! Evacuate immediately.",
    3: "Possible intrusion detected! Alerting security.",
    4: "Gunshot detected! Take cover and call emergency services."
}

# Feature extraction
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=16000, mono=True)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

# Update this path with the new file you want to test
file_path = r"data\baby-cry.wav"

# Predict
features = extract_features(file_path).reshape(1, -1)
pred = model.predict(features)[0]

# Output
message = label_map.get(pred, "Unknown sound detected.")
print(f"Prediction: {pred} → {message}")