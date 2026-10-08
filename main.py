import threading
import cv2
from assistant import Session, voice_worker
from vision.display import draw_frame
from vision.live_detector import LiveDetector
 
CAMERA_INDEX = 0
 
 
def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("ERROR: Could not open camera")
        return
 
    s = Session()
    s.detector = LiveDetector()
    s.detector.start()
    threading.Thread(target=voice_worker, args=(s,), daemon=True).start()
 
    while not s.quit.is_set():
        ok, frame = cap.read()
        if not ok:
            print("ERROR: Failed to capture frame")
            break
        s.detector.frame = frame
        cv2.imshow("ARIA", draw_frame(frame, s))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
 
    s.quit.set()
    cap.release()
    cv2.destroyAllWindows()
 
 
if __name__ == "__main__":
    main()