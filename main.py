import platform
import threading
import time
import numpy as np

import cv2

from assistant import Session, voice_worker
from config import CAMERA_INDEX, DETECT_FPS_PC, DETECT_FPS_PI, FRAME_SIZE_PC, FRAME_SIZE_PI
from vision.display import draw_frame
from vision.gemini_vision import analyze
from vision.live_detector import LiveDetector

ON_PI = platform.system() == "Linux" and platform.machine().lower().startswith(("aarch64", "armv"))
FRAME_SIZE = FRAME_SIZE_PI if ON_PI else FRAME_SIZE_PC
DETECT_FPS = DETECT_FPS_PI if ON_PI else DETECT_FPS_PC


class ARIA:
    def __init__(self):
        self.s = Session()
        self.cap = None
        self.latest_jpeg = None
        self.latest_frame = None
        self.lock = threading.Lock()
        self.vision_busy = threading.Event()
        self.s.last_vision = {"mode": None, "text": "", "ts": 0}

    def start(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

        self.s.detector = LiveDetector()
        self.s.detector.start()
        threading.Thread(target=voice_worker, args=(self.s,), daemon=True).start()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        last_fed = 0.0
        while not self.s.quit.is_set():
            ok, frame = self.cap.read()
            if not ok:
                print("ERROR: Failed to capture frame")
                break

            self.latest_frame = frame  # used by analyze_async

            now = time.time()
            if now - last_fed >= 1.0 / DETECT_FPS:
                self.s.detector.frame = frame
                last_fed = now

            out = draw_frame(frame, self.s)
            ok, buf = cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ok:
                with self.lock:
                    self.latest_jpeg = buf.tobytes()
        self.stop()

    def analyze_async(self, mode="identify", on_done=None):
        if self.vision_busy.is_set() or self.latest_frame is None:
            return False
        frame = self.latest_frame.copy()
        self.vision_busy.set()

        def work():
            try:
                text = analyze(frame, mode)
                self.s.last_vision = {"mode": mode, "text": text, "ts": time.time()}
                if on_done:
                    on_done(text)
            finally:
                self.vision_busy.clear()

        threading.Thread(target=work, daemon=True).start()
        return True

    def get_jpeg(self):
        with self.lock:
            return self.latest_jpeg

    def stop(self):
        self.s.quit.set()
        if self.cap:
            self.cap.release()

if __name__ == "__main__":
    aria = ARIA()
    aria.start()
    try:
        while not aria.s.quit.is_set():
            jpg = aria.get_jpeg()
            if jpg is not None:
                img = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow("ARIA", img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        aria.stop()
        cv2.destroyAllWindows()