
import threading
import time
import traceback
from collections import Counter, deque
from pathlib import Path

from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent.parent

YOLO_WEIGHTS = (
    PROJECT_ROOT
    / "vision"
    / "Datasets"
    / "runs"
    / "obb"
    / "aria_combined_13_classes"
    / "weights"
    / "best.pt"
)

CONF = 0.25
IMGSZ = 640


class LiveDetector(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)

        self.ready = False
        self.error = False
        self.frame = None

        # Compatible with ARIA code that expects rectangular boxes.
        self.boxes = []

        # Oriented polygons used by the updated display.py.
        self.obb_polygons = []

        self.recent = deque(maxlen=15)
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def run(self):
        try:
            if not YOLO_WEIGHTS.exists():
                raise FileNotFoundError(
                    f"Trained model not found: {YOLO_WEIGHTS}"
                )

            print(f"Loading 13-class OBB model: {YOLO_WEIGHTS}")
            model = YOLO(str(YOLO_WEIGHTS))
            print("Model classes:", model.names)

            if len(model.names) != 13:
                raise ValueError(
                    f"Expected 13 classes, found {len(model.names)}"
                )

            self.ready = True
            last_frame = None

            while not self._stop_event.is_set():
                frame = self.frame

                if frame is None or frame is last_frame:
                    time.sleep(0.005)
                    continue

                last_frame = frame

                result = model.predict(
                    source=frame,
                    imgsz=IMGSZ,
                    conf=CONF,
                    verbose=False,
                )[0]

                polygons = []
                boxes = []

                obb = result.obb

                if obb is not None and len(obb) > 0:
                    corners = obb.xyxyxyxy.cpu().numpy()
                    class_ids = obb.cls.int().cpu().tolist()
                    confidences = obb.conf.cpu().tolist()

                    for points, class_id, confidence in zip(
                        corners, class_ids, confidences
                    ):
                        label = result.names[int(class_id)]
                        points = points.astype(int)

                        polygons.append({
                            "points": points.tolist(),
                            "label": label,
                            "confidence": float(confidence),
                        })

                        # Axis-aligned envelope for legacy ARIA consumers.
                        x1 = int(points[:, 0].min())
                        y1 = int(points[:, 1].min())
                        x2 = int(points[:, 0].max())
                        y2 = int(points[:, 1].max())

                        boxes.append((x1, y1, x2, y2, label))

                with self._lock:
                    self.obb_polygons = polygons
                    self.boxes = boxes
                    self.recent.append({item["label"] for item in polygons})

        except Exception:
            traceback.print_exc()
            self.error = True
            self.ready = False

    def stable_labels(self, min_count=4):
        """Return labels observed repeatedly in recent frames."""
        with self._lock:
            counts = Counter(
                label
                for labels in self.recent
                for label in labels
            )

        return sorted(
            label for label, count in counts.items()
            if count >= min_count
        )

    def stop(self):
        """Ask the background detection thread to stop."""
        self._stop_event.set()
