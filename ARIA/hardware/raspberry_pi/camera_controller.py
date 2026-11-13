from ai_engine.vision.camera import open_camera, grab_jpeg
from ai_engine.vision.classifier import identify

class CameraController:
    def __init__(self, index=None): self.cap = open_camera(index)
    def snapshot(self): return grab_jpeg(self.cap)
    def identify(self):
        img = self.snapshot()
        return identify(img) if img else None
    def close(self): self.cap.release()
