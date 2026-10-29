<<<<<<< HEAD

from pathlib import Path
import cv2
from ultralytics import YOLO

# Locate the project and trained model
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = (
    PROJECT_ROOT
    / "runs"
    / "detect"
    / "aria_baseline"
    / "weights"
    / "best.pt"
)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Trained model not found: {MODEL_PATH}")

print("Loading ARIA's trained detector...")
model = YOLO(str(MODEL_PATH))
print("Model loaded:", model.names)

# Open your Camo Studio camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    cap.release()
    cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise RuntimeError(
        "Camera could not be opened. Check Camo Studio and camera index."
    )

print("Live detection started. Press Q to quit.")

try:
    while True:
        success, frame = cap.read()

        if not success:
            print("Could not read a camera frame.")
            break

        # Run object detection on the live frame using your GPU
        results = model.predict(
               source=frame,
               imgsz=640,
               conf=0.25,
               device=0,
               verbose=False,
           )

        
        # Draw YOLO detections first
        annotated_frame = results[0].plot()

        cv2.imshow("ARIA - Live Object Detection", annotated_frame)

        # Press Q to close the live feed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Live detection stopped.")
=======

from pathlib import Path
import cv2
from ultralytics import YOLO


# Locate the project and the new trained OBB model
PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT
    / "vision"
    / "Datasets"
    / "aria_combined_obb_dataset"
    / "runs"
    / "obb"
    / "runs"
    / "obb"
    / "aria_objects-2"
    / "weights"
    / "best.pt"
)


if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Trained model not found: {MODEL_PATH}")

print("Loading ARIA's trained detector...")
model = YOLO(str(MODEL_PATH))
print("Model loaded:", model.names)

# Open your Camo Studio camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    cap.release()
    cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise RuntimeError(
        "Camera could not be opened. Check Camo Studio and camera index."
    )

print("Live detection started. Press Q to quit.")

try:
    while True:
        success, frame = cap.read()

        if not success:
            print("Could not read a camera frame.")
            break

        # Run object detection on the live frame using your GPU
        results = model.predict(
               source=frame,
               imgsz=640,
               conf=0.65,
               device=0,
               verbose=False,
           )

        
        # Draw YOLO detections first
        annotated_frame = results[0].plot()

        cv2.imshow("ARIA - Live Object Detection", annotated_frame)

        # Press Q to close the live feed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Live detection stopped.")
>>>>>>> visual-assistant
