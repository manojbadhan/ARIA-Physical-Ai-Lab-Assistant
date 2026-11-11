import os
import sys
import time
import queue
import threading

import cv2
from ultralytics import YOLO
from google import genai
from google.genai import types


# ---------------- CONFIGURATION ----------------

CAMERA_INDEX = 0

# Your custom-trained model
MODEL_PATH = "runs/detect/aria_baseline/weights/best.pt"

CONFIDENCE = 0.50
IMAGE_SIZE = 640          # use 416 or 320 if Raspberry Pi is slow

# Minimum time between Gemini requests
GEMINI_COOLDOWN = 12

# Choose a model available to your Gemini API key
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash-lite"
)


# ---------------- GEMINI SETUP ----------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Set it first."
    )

client = genai.Client(api_key=api_key)

# Only one pending image is allowed, so the queue cannot grow endlessly.
image_queue = queue.Queue(maxsize=1)

# ---- Shared values: your UI can read these (always use result_lock) ----
result_lock = threading.Lock()
latest_explanation = "Show a lab component to the camera."
gemini_status = "Waiting for an object..."
latest_label = None          # best detected object right now (or None)


def get_state():
    """UI calls this to get (label, status, explanation) as text."""
    with result_lock:
        return latest_label, gemini_status, latest_explanation


# ---------------- GEMINI BACKGROUND WORKER ----------------

def gemini_worker():
    global latest_explanation, gemini_status

    while True:
        item = image_queue.get()

        if item is None:
            image_queue.task_done()
            break

        label, image_bytes = item

        try:
            with result_lock:
                gemini_status = f"Explaining {label}..."

            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    (
                        "You are ARIA, a laboratory assistant. "
                        f"A vision model labelled this object '{label}'. "
                        "Inspect the image and briefly explain what the "
                        "object appears to be and its common use. "
                        "If the label seems incorrect or the image is "
                        "unclear, say so. Do not invent specifications. "
                        "Answer in 2-3 short sentences."
                    ),
                    image_part,
                ],
            )

            explanation = response.text or "Gemini returned no explanation."

            with result_lock:
                latest_explanation = explanation
                gemini_status = f"Last explained: {label}"

            print(f"\nARIA explains [{label}]:\n{explanation}\n")

        except Exception as error:
            with result_lock:
                gemini_status = "Gemini request failed"

            print(f"\nGemini error: {error}\n")

        finally:
            image_queue.task_done()


# ---------------- LOAD TRAINED YOLO MODEL ----------------

print("Loading your trained YOLO model...")

model = YOLO(MODEL_PATH)

print("Trained model ready!")
print("Classes:", model.names)


# ---------------- OPEN CAMERA ----------------

def open_camera(index):
    # CAP_DSHOW works only on Windows. Raspberry Pi uses the default.
    if sys.platform.startswith("win"):
        return cv2.VideoCapture(index, cv2.CAP_DSHOW)
    return cv2.VideoCapture(index)


cap = open_camera(CAMERA_INDEX)

if not cap.isOpened():
    cap.release()
    cap = open_camera(1)

if not cap.isOpened():
    raise RuntimeError(
        "Camera could not open. Check camera connection and permissions."
    )


# ---------------- START GEMINI THREAD ----------------

worker = threading.Thread(
    target=gemini_worker,
    daemon=True
)
worker.start()

print("ARIA live vision started (no camera window). Press Ctrl+C to quit.")


# ---------------- CONTINUOUS DETECTION ----------------

last_submitted_label = None
last_gemini_time = 0

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Could not read camera frame.")
            break

        # YOLO runs continuously on each camera frame.
        results = model.predict(
            source=frame,
            conf=CONFIDENCE,
            imgsz=IMAGE_SIZE,
            verbose=False,
        )

        result = results[0]

        detected_label = None
        best_box = None
        best_score = 0.0

        if result.boxes is not None and len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls[0])
                score = float(box.conf[0])
                label = model.names[class_id]

                print(
                    f"\rDetected: {label} ({score:.0%})          ",
                    end="",
                    flush=True,
                )

                if score > best_score:
                    best_score = score
                    detected_label = label
                    best_box = box

        # Share the current label with the UI
        with result_lock:
            latest_label = detected_label

        # Send a crop to Gemini only when the label changes
        # and the cooldown has elapsed.
        current_time = time.time()

        if detected_label is None:
            last_submitted_label = None

        elif (
            detected_label != last_submitted_label
            and current_time - last_gemini_time >= GEMINI_COOLDOWN
            and best_box is not None
            and image_queue.empty()
        ):
            x1, y1, x2, y2 = map(
                int, best_box.xyxy[0].tolist()
            )

            height, width = frame.shape[:2]

            x1 = max(0, min(x1, width - 1))
            x2 = max(0, min(x2, width))
            y1 = max(0, min(y1, height - 1))
            y2 = max(0, min(y2, height))

            crop = frame[y1:y2, x1:x2]

            if crop.size > 0:
                crop = cv2.resize(crop, (320, 320))

                success, buffer = cv2.imencode(
                    ".jpg",
                    crop,
                    [cv2.IMWRITE_JPEG_QUALITY, 85],
                )

                if success:
                    try:
                        image_queue.put_nowait(
                            (detected_label, buffer.tobytes())
                        )

                        last_submitted_label = detected_label
                        last_gemini_time = current_time

                    except queue.Full:
                        pass

        # No drawing, no imshow, no waitKey: camera stays hidden.
        time.sleep(0.05)   # lets the Pi rest a little

except KeyboardInterrupt:
    pass

finally:
    cap.release()

    # Stop the background worker safely.
    try:
        image_queue.put_nowait(None)
    except queue.Full:
        pass

    print("\nARIA camera closed.")