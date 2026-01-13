# camera.py
import cv2
import time

class CameraManager:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        # Optimizare buffer pentru latență mică
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def get_frame(self):
        if not self.cap.isOpened():
            return None, False
        
        ret, frame = self.cap.read()
        if ret:
            # Redimensionare pentru performanță GUI
            frame = cv2.resize(frame, (640, 480))
        return frame, ret

    def release(self):
        self.cap.release()