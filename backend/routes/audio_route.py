from flask import Blueprint, request
import librosa
import numpy as np
import joblib
import os
import base64
import re
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from config.events import EVENTS

audio_bp = Blueprint('audio_bp', __name__)

# Load model once
model = joblib.load("models/audio_model.pkl")

# Label-to-event mapping
label_map = {
    0: EVENTS["audio"]["BABY_CRYING"],
    1: EVENTS["audio"]["DOORBELL"],
    2: EVENTS["audio"]["FIRE_ALARM"],
    3: EVENTS["audio"]["MOTION_DETECTED"],
    4: EVENTS["audio"]["GUNSHOT"]
}

def clean_base64_string(data):
    """Clean and validate base64 string"""
    # Remove whitespace
    data = re.sub(r'\s+', '', data)
    
    # Remove data URL prefix if present
    if data.startswith("data:"):
        data = data.split(",")[1]
    
    # Add padding if needed
    padding_needed = 4 - (len(data) % 4)
    if padding_needed != 4:
        data += '=' * padding_needed
    
    return data

# Convert 3GP to WAV using ffmpeg
def convert_3gp_to_wav(input_path, output_path):
    import subprocess
    try:
        # Use ffmpeg to convert 3GP to WAV
        subprocess.run([
            'ffmpeg', '-i', input_path, 
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',      # mono
            '-y',            # overwrite output
            output_path
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        # ffmpeg not available, try alternative
        return False

# Extract MFCC features from audio file
def extract_features(file_path):
    wav_path = None
    try:
        # If it's a 3GP file, try to convert it first
        if file_path.endswith('.3gp'):
            wav_path = file_path.replace('.3gp', '.wav')
            if convert_3gp_to_wav(file_path, wav_path):
                file_path = wav_path
            else:
                # Try to load 3GP directly with librosa (may fail)
                pass
        
        y, sr = librosa.load(file_path, sr=16000, mono=True)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfcc.T, axis=0)
        
    except Exception as e:
        print(f"Error extracting features: {e}")
        # Return zero features as fallback
        return np.zeros(13)
    finally:
        # Clean up converted WAV file
        if wav_path and os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except:
                pass

@audio_bp.route('/upload_audio', methods=['POST'])
def predict_audio_event():
    print("\n=== AUDIO UPLOAD ENDPOINT HIT ===")
    print(f"Content-Type: {request.content_type}")
    print(f"Request method: {request.method}")
    
    try:
        temp_path = None
        encoded_str = None
        
        # Check content type and extract data accordingly
        if request.content_type and 'application/json' in request.content_type:
            # Handle JSON payload
            json_data = request.get_json()
            if json_data:
                encoded_str = json_data.get("data")
                print("Extracted base64 from JSON payload")
                
        elif request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
            # Handle form data
            encoded_str = request.form.get("data")
            print("Extracted base64 from form data")
            
        elif request.data:
            # Handle raw data
            raw_data = request.data.decode('utf-8')
            if raw_data.startswith('{"') and raw_data.endswith('}'):
                # It's JSON
                json_data = json.loads(raw_data)
                encoded_str = json_data.get("data")
            else:
                # Assume it's form data or raw base64
                if 'data=' in raw_data:
                    encoded_str = raw_data.split('data=')[1].split('&')[0]
                else:
                    encoded_str = raw_data
            print("Extracted base64 from raw data")
            
        if not encoded_str:
            print("❗ No base64 data found in request")
            return "No audio data provided", 400
        
        print(f"Base64 string length: {len(encoded_str)}")
        print(f"First 50 chars: {encoded_str[:50]}...")
        
        # Clean and decode base64
        try:
            cleaned_b64 = clean_base64_string(encoded_str)
            audio_data = base64.b64decode(cleaned_b64, validate=True)
            print(f"Successfully decoded {len(audio_data)} bytes of audio data")
        except Exception as decode_error:
            print(f"❗ Base64 decode error: {decode_error}")
            return "Invalid base64 audio data", 400
        
        # Save to temporary file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"audio_{timestamp}.3gp"  # Use 3gp as that's what MIT App Inventor records
        temp_path = os.path.join("temp_audio", filename)
        os.makedirs("temp_audio", exist_ok=True)
        
        with open(temp_path, "wb") as f:
            f.write(audio_data)
        
        print(f"Audio saved to: {temp_path}")
        
        # Extract features and predict
        features = extract_features(temp_path).reshape(1, -1)
        pred = model.predict(features)[0]
        print(f"Model Prediction: {pred}")
        
        # Return the event message
        message = label_map.get(pred, "Unknown sound detected.")
        print(f"Returning message: {message}")
        return message, 200
        
    except Exception as e:
        print(f"❗ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        return "Error processing audio", 500
        
    finally:
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                print(f"Temp file deleted: {temp_path}")
            except Exception as cleanup_error:
                print(f"Cleanup error: {cleanup_error}")
