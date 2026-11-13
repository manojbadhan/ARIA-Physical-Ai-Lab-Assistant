import os

_model = None

def detect(image_bytes, conf=0.4):
    """Run the YOLO model (best.pt). Returns [(label, confidence), ...]; [] if model missing."""
    global _model
    path = os.getenv("YOLO_WEIGHTS", "ai_engine/vision/best.pt")
    if not os.path.exists(path): return []
    import numpy as np, cv2
    from ultralytics import YOLO
    if _model is None: _model = YOLO(path)
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    r = _model(img, conf=conf, verbose=False)[0]
    boxes = r.obb if getattr(r, "obb", None) is not None else r.boxes
    return [(r.names[int(c)], float(p)) for c, p in zip(boxes.cls, boxes.conf)] if boxes is not None else []
