from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
from utils.logger import log_event

IMAGE_MODEL_PATH = os.path.join("models", "mask_detector.model")
FACE_CASCADE_PATH = os.path.join("models", "haarcascade_frontalface_default.xml")

image_model = load_model(IMAGE_MODEL_PATH)
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

image_bp = Blueprint("image", __name__)

@image_bp.route("/image", methods=["POST"])
def predict_image():
    if 'image_file' not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files['image_file']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    predictions = []

    for (x, y, w, h) in faces:
        face_img = img[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (128, 128)) / 255.0
        face_img = np.expand_dims(face_img, axis=0)

        pred = image_model.predict(face_img)[0][0]
        label = "No Mask" if pred > 0.5 else "Mask"
        predictions.append(label)
        log_event("image", label)

    if not predictions:
        return jsonify({"message": "No faces detected."})

    return jsonify({"predictions": predictions})