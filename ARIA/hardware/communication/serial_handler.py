import json

class SerialHandler:
    """Line-based JSON over USB serial to an ESP32/Arduino."""
    def __init__(self, port, baud=115200):
        import serial
        self.ser = serial.Serial(port, baud, timeout=1)
    def send(self, **msg): self.ser.write((json.dumps(msg) + "\n").encode())
    def read(self):
        line = self.ser.readline().decode(errors="ignore").strip()
        try: return json.loads(line) if line else None
        except ValueError: return None
    def close(self): self.ser.close()
