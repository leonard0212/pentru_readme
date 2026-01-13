# serial_comm.py
import serial
import time
import threading

class SerialManager:
    def __init__(self, port, baud):
        self.ser = None
        self.port = port
        self.baud = baud
        self.is_connected = False

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2) # Așteptare reset Arduino
            self.is_connected = True
            print(f"[Serial] Conectat la {self.port}")
            return True
        except Exception as e:
            print(f"[Serial] Eroare: {e}")
            return False

    def send_command(self, cmd):
        if self.is_connected and self.ser:
            try:
                self.ser.write(cmd.encode())
                print(f"[Serial] Trimis: {cmd}")
            except Exception as e:
                print(f"[Serial] Eroare trimitere: {e}")

    def read_line(self):
        if self.is_connected and self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                return line
            except:
                return None
        return None

    def close(self):
        if self.ser:
            self.ser.close()