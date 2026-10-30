import os
import platform
import sys

if platform.system() != "Windows":
    os.environ.setdefault("QT_QPA_PLATFORM", "xcb")   # must be before import cv2

import threading
import time

import cv2
import numpy as np

from assistant import Session, voice_worker, analyze_retry
from config import CAMERA_INDEX, DETECT_FPS_PC, DETECT_FPS_PI, FRAME_SIZE_PC, FRAME_SIZE_PI
from vision.display import draw_frame
from vision.live_detector import LiveDetector

ON_PI = platform.system() == "Linux" and platform.machine().lower().startswith(("aarch64", "armv"))
FRAME_SIZE = FRAME_SIZE_PI if ON_PI else FRAME_SIZE_PC
DETECT_FPS = DETECT_FPS_PI if ON_PI else DETECT_FPS_PC
BACKEND = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_V4L2


class ARIA:
    def __init__(self):
        self.s = Session()
        self.cap = None
        self.latest_jpeg = None
        self.latest_frame = None
        self.latest_display = None            # the main loop reads this
        self.lock = threading.Lock()
        self.vision_busy = threading.Event()
        self.s.last_vision = {"mode": None, "text": "", "ts": 0}

    def _is_color(self, frame):
        """IR/depth streams have identical B, G, R channels. Real color frames don't."""
        if frame is None or frame.ndim != 3:
            return False
        b = frame[..., 0].astype(int)
        g = frame[..., 1].astype(int)
        r = frame[..., 2].astype(int)
        return (np.abs(b - g).mean() + np.abs(g - r).mean()) > 2.0

    def _open_camera(self):
        # 1) If CAMERA_INDEX in config.py is a number, trust it
        if isinstance(CAMERA_INDEX, int) and CAMERA_INDEX >= 0:
            cap = cv2.VideoCapture(CAMERA_INDEX, BACKEND)
            if cap.isOpened():
                return cap, CAMERA_INDEX
            cap.release()

        # 2) Otherwise auto-scan, skipping grayscale (IR/depth) nodes
        for index in range(10):
            cap = cv2.VideoCapture(index, BACKEND)
            if not cap.isOpened():
                cap.release()
                continue
            ok, frame = False, None
            for _ in range(5):                 # warm up
                ok, frame = cap.read()
                time.sleep(0.05)
            if ok and self._is_color(frame):
                return cap, index
            print(f"[camera] index {index} skipped (no frame or grayscale/IR stream)")
            cap.release()
        return None, None

    def start(self):
        self.cap, index = self._open_camera()
        if self.cap is None:
            raise RuntimeError("No working color camera found. "
                               "Windows: set CAMERA_INDEX = 0 in config.py. Pi: run v4l2-ctl --list-devices")
        print(f"[camera] Using color camera at index {index}")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])

        self.s.detector = LiveDetector()
        self.s.detector.start()
        threading.Thread(target=voice_worker, args=(self.s,), daemon=True).start()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        last_fed = 0.0
        fails = 0
        while not self.s.quit.is_set():
            ok, frame = self.cap.read()
            if not ok or frame is None:
                # cameras drop a frame now and then (and DSHOW fails during warm-up);
                # only give up if it keeps failing
                fails += 1
                if fails > 30:
                    print("ERROR: camera stopped giving frames")
                    break
                time.sleep(0.05)
                continue
            fails = 0

            self.latest_frame = frame
            self.s.frame = frame          # the voice thread reads this for "read this" / "what is this"

            now = time.time()
            if now - last_fed >= 1.0 / DETECT_FPS:
                self.s.detector.frame = frame
                last_fed = now

            out = draw_frame(frame, self.s)
            self.latest_display = out
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
                text = analyze_retry(frame, mode)
                self.s.last_vision = {"mode": mode, "text": text, "ts": time.time()}
                if on_done:
                    on_done(text)
            except Exception as e:
                print(f"[vision ERROR] {type(e).__name__}: {e}")
                if on_done:
                    on_done("Sorry, I couldn't analyze the image.")
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


def run_cv_window(aria):
    """Old mode: OpenCV window. Run with:  python main.py --cv"""
    aria.start()
    try:
        while not aria.s.quit.is_set():
            img = aria.latest_display
            if img is not None:
                cv2.imshow("ARIA", img)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
    except KeyboardInterrupt:
        pass
    finally:
        aria.stop()
        cv2.destroyAllWindows()
        time.sleep(0.5)
        os._exit(0)


def run_ui(aria):
    """New mode: ARIA screen (ui.py). Run with:  python main.py [--windowed]"""
    aria.start()
    import ui                              # imported late so --cv mode never loads PySide6
    try:
        ui.show(aria.s, get_frame=lambda: aria.latest_display)
    except KeyboardInterrupt:
        pass
    finally:
        aria.stop()
        time.sleep(0.5)
        os._exit(0)


if __name__ == "__main__":
    aria = ARIA()
    if "--cv" in sys.argv:
        run_cv_window(aria)
    else:
        run_ui(aria)
