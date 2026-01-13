# main.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import config
from serial_comm import SerialManager
from camera import CameraManager
from ai_inference import AIModel

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AOI PCB Inspection System - NextLab")
        self.root.geometry("1000x700")
        
        # 1. Inițializare Module
        self.serial = SerialManager(config.SERIAL_PORT, config.BAUD_RATE)
        self.cam = CameraManager(config.CAMERA_URL)
        self.ai = AIModel(config.MODEL_PATH, config.CONFIDENCE_THRESHOLD)
        
        self.inspecting = False # Dacă AI-ul scanează activ
        self.conveyor_active = False

        # 2. Interfața Grafică (GUI)
        self.setup_gui()

        # 3. Conectare Serială Automată
        if self.serial.connect():
            self.lbl_status.config(text="Status: CONECTAT", fg="green")
        else:
            self.lbl_status.config(text="Status: EROARE SERIAL", fg="red")

        # 4. Loop Video
        self.video_loop()

    def setup_gui(self):
        # Frame Stânga (Video)
        self.frame_video = tk.Frame(self.root, bg="black", width=640, height=480)
        self.frame_video.pack(side=tk.LEFT, padx=10, pady=10)
        self.lbl_video = tk.Label(self.frame_video)
        self.lbl_video.pack()

        # Frame Dreapta (Controale)
        self.frame_ctrl = tk.Frame(self.root)
        self.frame_ctrl.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(self.frame_ctrl, text="Panou Control", font=("Arial", 16, "bold")).pack(pady=20)

        # Butoane
        btn_start = tk.Button(self.frame_ctrl, text="START BANDĂ", command=self.start_conveyor, 
                              bg="#2ecc71", fg="white", font=("Arial", 12), height=2, width=20)
        btn_start.pack(pady=5)

        btn_stop = tk.Button(self.frame_ctrl, text="STOP", command=self.stop_conveyor, 
                             bg="#e74c3c", fg="white", font=("Arial", 12), height=2, width=20)
        btn_stop.pack(pady=5)

        # Log Defecte
        tk.Label(self.frame_ctrl, text="Jurnal Inspecție:", font=("Arial", 12)).pack(pady=(20, 5))
        self.log_box = tk.Text(self.frame_ctrl, height=15, width=35)
        self.log_box.pack()

        # Status Bar
        self.lbl_status = tk.Label(self.root, text="Inițializare...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def start_conveyor(self):
        self.serial.send_command('S')
        self.conveyor_active = True
        self.log("Comandă: Start Bandă")

    def stop_conveyor(self):
        self.serial.send_command('O')
        self.conveyor_active = False
        self.log("Comandă: Stop Bandă")

    def log(self, msg):
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)

    def video_loop(self):
        # 1. Citire Arduino (Verificăm dacă s-a oprit singur la obstacol)
        arduino_msg = self.serial.read_line()
        if arduino_msg == "OBSTACOL":
            self.conveyor_active = False
            self.log("ALERTĂ: PCB Detectat! Analiză AI...")
            # Aici am putea declanșa o logică automată de analiză
        
        # 2. Citire Cadru Cameră
        frame, ret = self.cam.get_frame()
        if ret:
            # 3. AI Inference (Doar dacă vrem să vedem detecțiile live)
            # Rulăm AI pe fiecare frame pentru demo (poate reduce FPS)
            annotated_frame, defect_found, detections = self.ai.predict(frame)
            
            # Dacă banda e oprită și avem defecte, logăm
            if not self.conveyor_active and defect_found:
                 # Evităm spam-ul în log (logică simplificată)
                 pass 

            # 4. Conversie pentru Tkinter
            img = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lbl_video.imgtk = imgtk
            self.lbl_video.configure(image=imgtk)

        self.root.after(30, self.video_loop) # ~30 FPS

    def on_close(self):
        self.stop_conveyor()
        self.serial.close()
        self.cam.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()