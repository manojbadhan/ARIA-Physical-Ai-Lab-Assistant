import cv2
from ultralytics import YOLO


# Load YOLO model
model = YOLO("yolo11s.pt")


# Open camera
cap = cv2.VideoCapture(0)

print("Press A to exit")


while True:

    # Capture frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Run YOLO on the frame
    results = model(frame)

    # Draw detection results on the frame
    annotated_frame = results[0].plot()

    # Display frame
    cv2.imshow("AI Lab Assistant - YOLO", annotated_frame)

    # Exit when A is pressed
    if cv2.waitKey(1) & 0xFF == ord("a"):
        break


# Release camera
cap.release()

# Close windows
cv2.destroyAllWindows()