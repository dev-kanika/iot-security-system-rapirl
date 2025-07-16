#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('pip', 'install opencv-python pyttsx3 torch torchvision')


# In[2]:


get_ipython().run_line_magic('pip', 'install --upgrade torch torchvision')


# In[8]:


get_ipython().system('where python')


# In[9]:


get_ipython().system('python -m venv yolo-env')
get_ipython().system('cd yolo-env\\Scripts')
get_ipython().system('activate')


# In[2]:


get_ipython().run_line_magic('pip', 'install torch torchvision')


# In[1]:


import cv2

cap = cv2.VideoCapture(1)  # or try 0 or 2 if 1 doesn't work
ret, frame = cap.read()

if not ret:
    print("Camera not detected or not returning frames.")
else:
    print("Camera working! Frame shape:", frame.shape)

cap.release()



# In[2]:


get_ipython().run_line_magic('pip', 'install ultralytics')


# #    Crowd  Detection model

# In[2]:


import cv2
import pyttsx3
import torch
import time

# Load YOLOv5 pretrained model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

engine = pyttsx3.init()
cap = cv2.VideoCapture(0)

crowd_threshold = 3
alert_given = False

def speak_alert(msg):
    print(f"[ALERT] {msg}")
    engine.say(msg)
    engine.runAndWait()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    labels = results.pandas().xyxy[0]['name'].tolist()

    person_count = labels.count("person")
    print("People Detected:", person_count)

    if person_count > crowd_threshold:
        if not alert_given:
            speak_alert("High crowd density detected. Maintain social distancing.")
            alert_given = True
    else:
        # Reset when condition is no longer true
        alert_given = False

    annotated = results.render()[0]
    cv2.imshow("Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# #    facemask Detection 

# In[4]:


import cv2
import pyttsx3
import torch
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

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


# In[ ]:





# In[11]:


get_ipython().system('C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\backports\\')


# In[ ]:





# #     Suspicious Object Detection

# In[1]:


import cv2
import torch
import time
import pyttsx3

engine = pyttsx3.init()
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

cap = cv2.VideoCapture(0)
alert_given = False
object_timer = {}

ALERT_DURATION = 10  # seconds

def speak_alert(msg):
    print(f"[ALERT] {msg}")
    engine.say(msg)
    engine.runAndWait()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    df = results.pandas().xyxy[0]

    current_time = time.time()
    for index, row in df.iterrows():
        label = row['name']
        if label not in ['person', 'cat', 'dog']:  # allowed/common classes
            if label not in object_timer:
                object_timer[label] = current_time
            elif current_time - object_timer[label] > ALERT_DURATION and not alert_given:
                speak_alert("Unattended object detected. Please inspect.")
                alert_given = True
        else:
            object_timer.pop(label, None)

    annotated = results.render()[0]
    cv2.imshow("Suspicious Object Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# In[ ]:





# #  Animal Intrusion Detection 

# In[2]:


import cv2
import torch
import pyttsx3

engine = pyttsx3.init()
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
cap = cv2.VideoCapture(0)

animal_classes = ['cat', 'dog', 'bird', 'cow', 'horse', 'sheep']  # YOLO animal labels
alert_given = False

def speak_alert(msg):
    print(f"[ALERT] {msg}")
    engine.say(msg)
    engine.runAndWait()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    labels = results.pandas().xyxy[0]['name'].tolist()

    for label in labels:
        if label in animal_classes and not alert_given:
            speak_alert("Animal intrusion detected! Stay alert.")
            alert_given = True
            break

    if not any(l in animal_classes for l in labels):
        alert_given = False

    annotated = results.render()[0]
    cv2.imshow("Animal Intrusion", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# In[ ]:





# #    Motion detection in restricted hours 

# In[3]:


import cv2
import pyttsx3
import datetime

engine = pyttsx3.init()
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

alert_given = False

def speak_alert(msg):
    print(f"[ALERT] {msg}")
    engine.say(msg)
    engine.runAndWait()

def in_restricted_hours():
    return True

while True:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if in_restricted_hours() and len(contours) > 0 and not alert_given:
        speak_alert("Unauthorized movement detected! Security alert triggered.")
        alert_given = True

    cv2.imshow("Motion Detection", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




