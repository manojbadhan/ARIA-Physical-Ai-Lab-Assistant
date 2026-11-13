import os

def open_camera(index=None):
    """Open a UVC camera. RealSense RGB is usually not /dev/video0; find it with v4l2-ctl --list-devices."""
    import cv2
    index = int(os.getenv("CAMERA_INDEX", 0 if index is None else index))
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(index)
    if not cap.isOpened(): raise RuntimeError(f"Cannot open camera index {index}")
    return cap

def grab_jpeg(cap):
    import cv2
    ok, frame = cap.read()
    if not ok: return None
    return cv2.imencode(".jpg", frame)[1].tobytes()
