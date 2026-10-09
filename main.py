import platform
import threading
import time
 
import cv2
 
from assistant import Session, voice_worker
from vision.display import draw_frame
from vision.live_detector import LiveDetector
 
CAMERA_INDEX = 0
 
# On a Raspberry Pi, YOLO can eat every CPU core and starve the microphone, which drops
# audio and makes speech-to-text hear garbage. So on a Pi: smaller frames, fewer detections.
ON_PI = platform.system() == "Linux" and platform.machine().lower().startswith(("aarch64", "armv"))
FRAME_SIZE = (640, 480) if ON_PI else (1280, 720)
DETECT_FPS = 4 if ON_PI else 15     # how often a frame is handed to YOLO
 
 
def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])
    if not cap.isOpened():
        print("ERROR: Could not open camera")
        return
 
    s = Session()
    s.detector = LiveDetector()
    s.detector.start()
    threading.Thread(target=voice_worker, args=(s,), daemon=True).start()
 
    last_fed = 0.0
    while not s.quit.is_set():
        ok, frame = cap.read()
        if not ok:
            print("ERROR: Failed to capture frame")
            break
 
        now = time.time()
        if now - last_fed >= 1.0 / DETECT_FPS:      # the video stays smooth; only YOLO is throttled
            s.detector.frame = frame
            last_fed = now
 
        cv2.imshow("ARIA", draw_frame(frame, s))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
 
    s.quit.set()
    cap.release()
    cv2.destroyAllWindows()
 
 
if __name__ == "__main__":
    main()
 