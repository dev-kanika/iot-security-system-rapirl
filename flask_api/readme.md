#  Smart Event Detection System with Raspberry Pi & Computer Vision

This project is part of **IoT Case Study 2 (RaPiRL)** and implements **real-time event detection** using a webcam and YOLOv5, with alerts announced through a speaker. It focuses on enhancing surveillance and safety in smart environments using Raspberry Pi.

## ✅ Features Implemented

###  Real-time Event Detection (with Audio Alerts)
The following models are implemented in Python using OpenCV, PyTorch, and `pyttsx3`:

| Task | Description | Triggered Announcement |
|------|-------------|------------------------|
| 👥 Crowd Density Monitoring | Detects if number of people exceeds a threshold | “High crowd density detected. Maintain social distancing.” |
|     Face Mask detection |  Detects if person wears mask or not | if not then instruct please wear mask.
| 📦 Suspicious Object Detection | Detects unattended or unknown objects in a zone | “Unattended object detected. Please inspect.” |
| 🐶 Animal Intrusion Detection | Detects animals like dogs, cats, etc. in restricted areas | “Animal intrusion detected! Stay alert.” |
| 🕵️ Motion Detection in Restricted Hours | Detects motion during night/off-hours | “Unauthorized movement detected! Security alert triggered.” |

Each model uses a `alert_given` reset logic to enable **multiple alerts** if the condition reoccurs after being resolved.

---

## 🧠 Tech Stack

- 🐍 Python
- 🎥 OpenCV
- 🧠 YOLOv5 (torch.hub)
- 🗣️ pyttsx3 (Text-to-Speech)
- 🧠 Pre-trained models used directly from `ultralytics/yolov5`

- 
---

## 🧑‍💻 Flask Integration (To Be Done by Collaborator)

### What Needs to Be Done

Your job is to wrap each event detection model into **Flask APIs** so that they can be triggered from a web/mobile frontend or dashboard.

#### Suggested API Structure

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/detect/crowd` | GET or POST | Start crowd detection camera stream |
| `/detect/animal` | GET or POST | Start animal intrusion detection |
| `/detect/object` | GET or POST | Start suspicious object detection |
| `/detect/motion` | GET or POST | Start motion detection in restricted hours |
| `/stop` | POST | Stop the camera/detection service |

#### How to Proceed

1. Use **Flask or FastAPI** to create endpoints.
2. Import each detection script and run it as a subprocess or thread.
3. Return a success message (or logs/stats) from the API call.
4. Make sure the camera resource isn’t shared across concurrent endpoints.

---

## 📝 Example (crowd_density.py wrapped into Flask)

```python
@app.route("/detect/crowd", methods=["GET"])
def detect_crowd():
    subprocess.Popen(["python", "crowd_density.py"])
    return jsonify({"status": "Crowd detection started"})


---

## 📂 Folder Structure

