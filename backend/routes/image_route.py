from flask import Blueprint, request
import torch
import cv2
import numpy as np
import base64
import re
import json
from datetime import datetime
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from config.events import EVENTS

image_bp = Blueprint('image_bp', __name__)

# Load models
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/multi_detector.pt', source='github')
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

try:
    mask_classifier = load_model('models/mask_detector.h5')
except Exception as e:
    print(f"[!] Failed to load mask detector model: {e}")
    mask_classifier = None

# Clean and validate base64 string
def clean_base64_string(data):
    data = re.sub(r'\s+', '', data)
    
    if data.startswith("data:"):
        data = data.split(",")[1]
    
    padding_needed = 4 - (len(data) % 4)
    if padding_needed != 4:
        data += '=' * padding_needed
    
    return data

@image_bp.route('/upload_image', methods=['POST'])
def detect_image():
    print("\n=== IMAGE UPLOAD ENDPOINT HIT ===")
    print(f"Content-Type: {request.content_type}")
    
    try:
        frame = None
        encoded_str = None
        
        # Check content type and extract data accordingly
        if request.content_type and 'application/json' in request.content_type:
            json_data = request.get_json()
            if json_data:
                encoded_str = json_data.get("data")
                print("Extracted base64 from JSON payload")
                
        elif request.content_type and 'text/plain' in request.content_type:
            # Handle raw base64 data with custom headers
            encoded_str = request.data.decode('utf-8')
            print("Extracted base64 from raw data with headers")
            
        elif request.data and len(request.data) > 100:
            raw_data = request.data.decode('utf-8')
            if raw_data.startswith('{"') and raw_data.endswith('}'):
                json_data = json.loads(raw_data)
                encoded_str = json_data.get("data")
            else:
                encoded_str = raw_data
            print("Extracted base64 from raw data")
            
        elif request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
            # Handle form data - but check size first
            try:
                encoded_str = request.form.get("data")
                print("Extracted base64 from form data")
            except Exception as form_error:
                print(f"Form data too large: {form_error}")
                return "Request too large - try using JSON format", 413
            
        if not encoded_str:
            print("❗ No base64 data found in request")
            return "No image data provided", 400
        
        print(f"Base64 string length: {len(encoded_str)}")
        print(f"First 50 chars: {encoded_str[:50]}...")
        
        # Clean and decode base64
        try:
            cleaned_b64 = clean_base64_string(encoded_str)
            image_data = base64.b64decode(cleaned_b64, validate=True)
            print(f"Successfully decoded {len(image_data)} bytes of image data")
        except Exception as decode_error:
            print(f"❗ Base64 decode error: {decode_error}")
            return "Invalid base64 image data", 400
        
        # Convert to OpenCV image
        npimg = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        if frame is None:
            print("❗ Failed to decode image data to OpenCV format")
            return "Failed to decode image data", 400
        
        print(f"Image shape: {frame.shape}")
        
        # Run YOLOv5 detection
        results = model(frame)
        labels = results.pandas().xyxy[0]['name'].tolist()
        print(f"Detected objects: {labels}")
        
        # Detection logic (same as before)
        animal_classes = ['cat', 'dog', 'cow', 'horse', 'sheep', 'elephant', 'bird']
        suspicious_exclude = ['person', 'cat', 'dog']
        crowd_threshold = 3
        person_count = labels.count("person")
        
        # Priority 1: Crowd
        if person_count > crowd_threshold:
            return EVENTS['photo']["CROWD_DENSITY"]
        
        # Priority 2: Animal Intrusion
        detected_animals = [label for label in labels if label in animal_classes]
        if detected_animals:
            return EVENTS['photo']["ANIMAL_DETECTED"]
        
        # Priority 3: Suspicious Object
        suspicious_objects = [label for label in labels if label not in suspicious_exclude]
        if suspicious_objects:
            return EVENTS['photo']["SUSPICIOUS_OBJECT"]
        
        # Priority 4: Face Mask Detection
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
        
        return "Nothing detected", 200
        
    except Exception as e:
        print(f"❗ Error during image processing: {e}")
        import traceback
        traceback.print_exc()
        return "Error processing image", 500
