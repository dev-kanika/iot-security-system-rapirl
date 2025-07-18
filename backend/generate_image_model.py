import torch
import os
import requests

output_path = "models/multi_detector.pt"
model_url = "https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5s.pt"

os.makedirs("models", exist_ok=True)

print("[⏳] Downloading YOLOv5s model (no cache)...")
response = requests.get(model_url, stream=True)
with open(output_path, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

print(f"[✔] Model downloaded and saved as: {output_path}")

print("[🔍] Verifying model with torch.hub.load...")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=output_path, source='github', force_reload=True)
print("[✅] Model verified and ready.")
