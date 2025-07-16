import cv2
import pyttsx3
import torch
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

cap = cv2.VideoCapture(1)  # or try 0 or 2 if 1 doesn't work
ret, frame = cap.read()

if not ret:
    print("Camera not detected or not returning frames.")
else:
    print("Camera working! Frame shape:", frame.shape)

cap.release()

# Load YOLOv5 for general object detection
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Load Face Detector + Mask Classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
mask_model = load_model('mask_detector.model')

# TTS engine
engine = pyttsx3.init()

cap = cv2.VideoCapture(0)
crowd_threshold = 3

def speak_alert(msg):
    print(f"[ALERT] {msg}")
    engine.say(msg)
    engine.runAndWait()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO Detection
    results = model(frame)
    labels = results.pandas().xyxy[0]['name'].tolist()
    person_count = labels.count("person")

    if person_count > crowd_threshold:
        speak_alert("High crowd density detected.")

    # FACE MASK DETECTION
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (224, 224))
        face_img = img_to_array(face_img)
        face_img = np.expand_dims(face_img, axis=0)
        face_img = face_img / 255.0

        (mask, no_mask) = mask_model.predict(face_img)[0]

        label = "Mask" if mask > no_mask else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        if label == "No Mask":
            speak_alert("Face mask not detected! Please wear a mask.")

        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    # Show annotated frame
    annotated = results.render()[0]
    combined = cv2.addWeighted(annotated, 0.7, frame, 0.3, 0)
    cv2.imshow("Detection with Mask & Crowd", combined)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()