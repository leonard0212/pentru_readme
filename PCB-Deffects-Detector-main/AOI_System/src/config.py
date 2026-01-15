# config.py

# --- Setări Serial ---
SERIAL_PORT = 'COM4'   # <--- VERIFICĂ în Device Manager!
BAUD_RATE = 9600

# --- Setări Cameră (iPhone) ---

CAMERA_URL = 0  #0 pentru webcam laptop sau "http://192.168.1.x:8080/video" pt IP Camera

# --- Setări AI ---
MODEL_PATH = "models/optimized_model.pt" # Actualizat Etapa 6
CONFIDENCE_THRESHOLD = 0.45 # Cât de sigur să fie AI-ul (0-1)
IMG_SIZE = 640