
import cv2
from ultralytics import YOLO

# Load the trained 13-class OBB model
model = YOLO(
    r"vision\Datasets\runs\obb\aria_combined_13_classes\weights\best.pt"
)

# Open the default webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    raise SystemExit

print("Webcam started. Press Q to quit.")

while True:
    success, frame = cap.read()

    if not success:
        print("Error: Could not read camera frame.")
        break

    # Run oriented bounding box detection
    results = model.predict(
        source=frame,
        imgsz=640,
        conf=0.25,
        verbose=False
    )

    # Draw detections, including rotated boxes
    annotated_frame = results[0].plot()

    cv2.imshow("ARIA - 13 Class OBB Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
