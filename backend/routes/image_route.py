from flask import Blueprint, request
import torch
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from config.events import EVENTS

image_bp = Blueprint('image_bp', __name__)

# Load YOLOv5 model for image classification
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/multi_detector.pt', source='github')

# Load face detection model (Haarcascade)
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

# Load face mask detection model
try:
    mask_classifier = load_model('models/mask_detector.h5')
except Exception as e:
    print(f"[!] Failed to load mask detector model: {e}")
    mask_classifier = None

# Detection route
@image_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]
    npimg = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Run YOLOv5 detection
    results = model(frame)
    labels = results.pandas().xyxy[0]['name'].tolist()

    # Define detection categories
    animal_classes = ['cat', 'dog', 'cow', 'horse', 'sheep', 'elephant', 'bird']
    suspicious_exclude = ['person', 'cat', 'dog']
    crowd_threshold = 3
    person_count = labels.count("person")

    # Priority 1: Crowd
    if person_count > crowd_threshold:
        return EVENTS['photo']["CROWD_DENSITY"]

    # Priority 2: Animal Intrusion
    if any(label in animal_classes for label in labels):
        return EVENTS['photo']["ANIMAL_DETECTED"]

    # Priority 3: Suspicious Object
    if any(label not in suspicious_exclude for label in labels):
        return EVENTS['photo']["SUSPICIOUS_OBJECT"]

    # Priority 4: Face Mask
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (224, 224))
            face_img = img_to_array(face_img)
            face_img = np.expand_dims(face_img, axis=0) / 255.0

            if mask_classifier is not None:
                (mask, no_mask) = mask_classifier.predict(face_img)[0]
                if no_mask > mask:
                    return EVENTS['photo']["NO_MASK"]
    except Exception as e:
        print(f"[!] Face mask detection failed: {e}")

    return "Nothing detected"
