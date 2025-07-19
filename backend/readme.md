# 🧠 Smart Event Detection Backend (Flask + YOLOv5 + Audio)

This is the **Flask-based backend** for the Smart Event Detection System. It processes image and audio data using machine learning models to detect events such as crowd density, animal intrusion, suspicious objects, face mask violations, and emergency audio cues like fire alarms and gunshots.

---

## ✅ Features

| Type   | Detection | Description |
|--------|-----------|-------------|
| 📸 Image | Crowd Density | Detects if too many people are present |
| 📸 Image | Animal Intrusion | Detects animals like dogs, cats, etc. |
| 📸 Image | Suspicious Objects | Detects unknown/unattended objects |
| 📸 Image | Face Mask | Detects if face masks are missing |
| 🔊 Audio | Fire Alarm | Detects loud alarm sounds |
| 🔊 Audio | Glass Break | Intruder Alert |
| 🔊 Audio | Baby Crying | Detects a crying baby |
| 🔊 Audio | Doorbell | Detects doorbell ringing |
| 🔊 Audio | Gunshot | Detects gunshots |

> Returns one string-based alert per request — based on priority:
> **Crowd > Animal > Suspicious > No Mask** (for image)

---

## 🧠 Tech Stack

- 🐍 Python 3.11+
- 🧠 YOLOv5 (`torch.hub`)
- 🔉 Librosa (audio preprocessing)
- 🧪 scikit-learn (audio classification)
- 🖼 OpenCV (image processing)
- 😷 Keras (`.keras` Face Mask Model)
- 🌐 Flask (REST API)

---

## 📦 Folder Structure (Backend)

```

backend/
├── app.py                        # Main Flask application
├── data/                         # Image and Audio for testing
├── routes/
│   ├── audio\_route.py            # Handles /upload\_audio
│   ├── image\_route.py            # Handles /upload\_image
├── models/
│   ├── audio\_model.pkl           # Trained audio classifier
│   ├── mask\_detector.keras       # Face mask classifier (Keras)
│   └── multi\_detector.pt         # YOLOv5 multi-class model
├── haarcascade\_frontalface\_default.xml  # For face detection
├── temp\_audio/                   # Temporary audio file storage
├── utils/
│   └── announcer.py               # (Optional) Speaker integration
├── requirements.txt               # Libraries used
└── README.md

````

---

## ⚙️ Setup & Run Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
````

### 2. Run Flask Server

```bash
python app.py
```

> Server runs at: `http://0.0.0.0:5050`               # Update with your ip address and port

---

## 🔧 API Endpoints

### 📸 Image Event Detection

```
POST /upload_image
Content-Type: multipart/form-data
Form field: image = <your image file>
```

✅ Example response:

```
"Animal intrusion detected."
```

### 🔊 Audio Event Detection

```
POST //upload_audio
Content-Type: multipart/form-data
Form field: file = <your audio file>
```

✅ Example response:

```
"Fire alarm detected! Evacuate now!"
```

---

## 🔁 Event Mapping (Internal Reference)

```python
EVENTS = {
    "photo": {
        "CROWD_DENSITY": "High crowd density detected.",
        "ANIMAL_DETECTED": "Animal intrusion detected.",
        "SUSPICIOUS_OBJECT": "Suspicious object detected.",
        "NO_MASK": "Face mask not detected."
    },
    "audio": {
        "FIRE_ALARM": "Fire alarm detected! Evacuate now!",
        "GLASS_BREAKING": "Glass breaking detected!",
        "BABY_CRYING": "Baby crying detected.",
        "DOORBELL": "Doorbell sound detected.",
        "GUNSHOT": "Gunshot detected! Call emergency services.",
        "MOTION_DETECTED": "Possible intrusion detected during restricted hours."
    }
}
```

---

## 📌 Notes

* Make sure the model files are placed in the `/models/` directory:

  * `multi_detector.pt`
  * `audio_model.pkl`
  * `mask_detector.keras`
* `haarcascade_frontalface_default.xml` is required for face detection.
* All requests return **only one** string response per request — based on priority logic.

---

## 🧹 Clean-up

Temporary uploaded audio files are automatically deleted after processing. No database or stateful storage is used in the backend.

---

## 📄 License

This backend code is licensed for educational and research purposes only. Ensure third-party model usage complies with their respective licenses.
