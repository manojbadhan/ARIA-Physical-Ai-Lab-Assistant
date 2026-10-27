import os, sys, time, threading, runpy
import cv2

EXISTING_MAIN = "main.py"        # <-- change to the file name of your current YOLO main file

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)                   # so model paths like "yolov8n.pt" still resolve

# 1) Stop OpenCV from opening any window. Detection keeps running, nothing is drawn.
_noop = lambda *a, **k: None
for name in ("imshow", "namedWindow", "resizeWindow", "moveWindow",
             "setWindowProperty", "destroyAllWindows", "destroyWindow"):
    setattr(cv2, name, _noop)

def _wait_key(delay=1):          # keeps loops that call waitKey(1) from spinning at 100% CPU
    time.sleep(max(int(delay), 1) / 1000)
    return -1
cv2.waitKey = _wait_key

# 2) Run your existing main file in a background thread, exactly as if you ran it yourself.
windowed = "--windowed" in sys.argv
if windowed:
    sys.argv.remove("--windowed")        # so your own argument parser doesn't see it

def run_existing():
    try:
        runpy.run_path(os.path.join(HERE, EXISTING_MAIN), run_name="__main__")
    except SystemExit:
        pass
    except Exception as e:
        print(f"[run_aria] {EXISTING_MAIN} stopped: {e!r}")

threading.Thread(target=run_existing, daemon=True).start()

# 3) Show the ARIA screen (must be on the main thread). Closing it ends everything.
import aria_ui
aria_ui.show(windowed)
