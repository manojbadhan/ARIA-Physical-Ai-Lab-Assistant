import cv2
from ultralytics import YOLO


# Load YOLO model
model = YOLO("yolo11s.pt")


def detect_objects(camera_index=0):

    # Open camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("ERROR: Could not open camera")
        return

    print("Camera opened successfully")
    print("Press A to exit")

    while True:

        # Capture frame
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Failed to capture frame")
            break

        # Run YOLO
        results = model(frame)

        # Draw detections
        annotated_frame = results[0].plot()

        # Display
        cv2.imshow(
            "ARIA - Object Detection",
            annotated_frame
        )

        # Exit when A is pressed
        if cv2.waitKey(1) & 0xFF == ord("a"):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_objects()