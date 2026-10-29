from pathlib import Path

import cv2
from ultralytics import YOLO


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Your trained 13-class OBB model
MODEL_PATH = (
    PROJECT_ROOT
    / "vision"
    / "Datasets"
    / "runs"
    / "obb"
    / "aria_combined_13_classes"
    / "weights"
    / "best.pt"
)

CAMERA_INDEX = 0
CONFIDENCE = 0.25
IMAGE_SIZE = 640


def main():
    if not MODEL_PATH.exists():
        print(f"Model not found: {MODEL_PATH}")
        print("Check that best.pt exists at the expected location.")
        return

    print(f"Loading model: {MODEL_PATH}")
    model = YOLO(str(MODEL_PATH))

    print("Detected model classes:")
    print(model.names)

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera started. Press Q to quit.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read a frame from the camera.")
                break

            results = model.predict(
                source=frame,
                imgsz=IMAGE_SIZE,
                conf=CONFIDENCE,
                verbose=False,
            )

            # Ultralytics plots oriented bounding boxes (OBB)
            annotated_frame = results[0].plot()

            cv2.imshow("ARIA - 13 Class Object Detection", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
