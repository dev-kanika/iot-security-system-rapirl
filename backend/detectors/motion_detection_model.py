#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


import cv2
import pyttsx3
import datetime

cap = cv2.VideoCapture(1)  # or try 0 or 2 if 1 doesn't work
ret, frame = cap.read()

if not ret:
    print("Camera not detected or not returning frames.")
else:
    print("Camera working! Frame shape:", frame.shape)

cap.release()


# In[ ]:


engine = pyttsx3.init()
engine.say("This is a test. Can you hear me?")
engine.runAndWait()

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




