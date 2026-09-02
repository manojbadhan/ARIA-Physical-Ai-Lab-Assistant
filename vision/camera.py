import cv2
import time

cap = cv2.VideoCapture(0)

# Request Full HD
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Get actual resolution
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Camera Resolution: {width} x {height}")

# FPS calculation variables
frame_count = 0
start_time = time.time()
fps = 0

print("Press Q to exit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    frame_count += 1

    # Calculate FPS every 1 second
    elapsed_time = time.time() - start_time

    if elapsed_time >= 1:
        fps = frame_count / elapsed_time

        frame_count = 0
        start_time = time.time()

    # Display FPS
    cv2.putText(
        frame,
        f"FPS: {fps:.2f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("AI Lab Assistant - Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()