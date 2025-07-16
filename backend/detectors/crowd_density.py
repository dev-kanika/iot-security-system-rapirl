import cv2
import pyttsx3
import torch
import time

get_ipython().run_line_magic('pip', 'install opencv-python pyttsx3 torch torchvision')
get_ipython().run_line_magic('pip', 'install --upgrade torch torchvision')
get_ipython().system('where python')
get_ipython().system('python -m venv yolo-env')
get_ipython().system('cd yolo-env\\Scripts')
get_ipython().system('activate')
get_ipython().run_line_magic('pip', 'install torch torchvision')

cap = cv2.VideoCapture(1)  # or try 0 or 2 if 1 doesn't work
ret, frame = cap.read()

if not ret:
    print("Camera not detected or not returning frames.")
else:
    print("Camera working! Frame shape:", frame.shape)

cap.release()

get_ipython().run_line_magic('pip', 'install ultralytics')


# Crowd Detection model
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
