import pyttsx3

engine = pyttsx3.init()

def speak_alert(msg):
    try:
        print(f"[ALERT] {msg}")
        engine.say(msg)
        engine.runAndWait()
    except Exception as e:
        print(f"[Announcer Error] {e}")
