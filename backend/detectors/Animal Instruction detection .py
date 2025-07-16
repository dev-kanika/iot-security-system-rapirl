#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


import cv2

cap = cv2.VideoCapture(1)  # or try 0 or 2 if 1 doesn't work
ret, frame = cap.read()

if not ret:
    print("Camera not detected or not returning frames.")
else:
    print("Camera working! Frame shape:", frame.shape)

cap.release()


# In[ ]:


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

