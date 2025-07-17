import cv2
import torch
import time
from utils.announcer import speak_alert


cap = cv2.VideoCapture(1)  # or try 0 or 2 if 1 doesn't work
ret, frame = cap.read()

if not ret:
    print("Camera not detected or not returning frames.")
else:
    print("Camera working! Frame shape:", frame.shape)

cap.release()

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

cap = cv2.VideoCapture(0)
alert_given = False
object_timer = {}

ALERT_DURATION = 10  # seconds

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