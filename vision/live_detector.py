import threading
import time
import traceback
from collections import Counter, deque
 
YOLO_WEIGHTS = "yolo11s.pt"     # swap for your own trained weights later
CONF = 0.4
IMGSZ = 480                     # smaller = faster detection (default is 640)
IGNORE_LABELS = {"person"}      # you're always in frame
 
 
class LiveDetector(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.ready = False
        self.error = False
        self.frame = None
        self.boxes = []
        self.recent = deque(maxlen=15)   # label sets from recent detections
 
    def run(self):
        try:
            from ultralytics import YOLO     # slow import, kept off the main thread
            model = YOLO(YOLO_WEIGHTS)
            self.ready = True
            last = None
            while True:
                frame = self.frame
                if frame is None or frame is last:
                    time.sleep(0.005)
                    continue
                last = frame
                r = model(frame, verbose=False, conf=CONF, imgsz=IMGSZ)[0]
                boxes = [(*map(int, b.xyxy[0]), r.names[int(b.cls)]) for b in r.boxes]
                self.boxes = [b for b in boxes if b[4] not in IGNORE_LABELS]
                self.recent.append({b[4] for b in self.boxes})
        except Exception:
            traceback.print_exc()
            self.error = True
 
    def stable_labels(self, min_count=4):
        """Labels seen in several recent detections (ignores one-frame flicker)."""
        counts = Counter(l for labels in list(self.recent) for l in labels)
        return sorted(l for l, c in counts.items() if c >= min_count)
 