
import cv2
from ultralytics import YOLOWorld

CAMERA_INDEX = 0
MODEL_PATH = "yolov8s-worldv2.pt"
CONFIDENCE = 0.10

TARGET_CLASSES = [
    "box",
    "red product box",
    "computer",
    "circuit board",
    "electronic device",
]

print("Loading YOLO-World...")
model = YOLOWorld(MODEL_PATH)
model.set_classes(TARGET_CLASSES)
print("Model ready!")

cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera could not open.")
    raise SystemExit(1)

print("Live detection started. Press Q to quit.")

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Could not read frame.")
            break

        results = model.predict(
            source=frame,
            conf=CONFIDENCE,
            imgsz=640,
            verbose=False,
        )

        result = results[0]
        annotated = result.plot()

        if result.boxes is not None and len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls[0])
                score = float(box.conf[0])
                label = model.names[class_id]

                print(
                    f"\rDetected: {label} "
                    f"({score:.0%})          ",
                    end="",
                    flush=True,
                )

        cv2.imshow("ARIA - Live YOLO-World Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("\nCamera closed.")
