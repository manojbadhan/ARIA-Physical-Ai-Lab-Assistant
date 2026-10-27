
import os
import cv2
from google import genai
from google.genai import types

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Set it in PowerShell."
    )

# You can override this model name in PowerShell if needed.
model_name = "gemini-2.5-flash"
client = genai.Client(api_key=api_key)

# Open Camo Studio camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    cap.release()
    cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise RuntimeError(
        "Could not open camera. Check that Camo Studio is running."
    )

print("ARIA Visual Assistant is running.")
print("Press SPACE to identify an object.")
print("Press Q to quit.")

try:
    while True:
        success, frame = cap.read()

        if not success:
            print("Could not read camera frame.")
            break

        cv2.imshow("ARIA Visual Assistant", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        if key == 32:  # Spacebar
            print("\nAnalyzing image with Gemini...")

            height, width = frame.shape[:2]
            if width > 1024:
                new_height = int(height * 1024 / width)
                frame = cv2.resize(frame, (1024, new_height))

            success, buffer = cv2.imencode(
                ".jpg",
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, 85],
            )

            if not success:
                print("Could not encode camera image.")
                continue

            try:
                image_part = types.Part.from_bytes(
                    data=buffer.tobytes(),
                    mime_type="image/jpeg",
                )

                response = client.models.generate_content(
                    model=model_name,
                    contents=[
                        (
                            "You are ARIA, a visual assistant. Identify "
                            "the main object in this image. Explain what "
                            "it is used for and describe visible features. "
                            "If uncertain, say so. Do not invent technical "
                            "specifications that cannot be verified."
                        ),
                        image_part,
                    ],
                )

                print("\n--- ARIA's Answer ---")
                print(response.text or "Gemini returned no text.")
                print("---------------------\n")

            except Exception as error:
                print("Gemini request failed:", error)

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("ARIA stopped.")