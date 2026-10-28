import os
import cv2
from google import genai
from google.genai import types

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
_client = None

PROMPTS = {
    "identify": (
        "You are ARIA, a visual assistant. Identify the main object in this image. "
        "Explain what it is used for and describe visible features. If uncertain, say so. "
        "Do not invent technical specifications that cannot be verified. "
        "Reply in English, in 3-4 short sentences."
    ),
    "ocr": (
        "Read all legible text in this image exactly as written. "
        "Return only the text. If there is no readable text, say 'No text found'."
    ),
}


def _get_client():
    global _client
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        _client = genai.Client(api_key=key)
    return _client


def analyze(frame, mode="identify"):
    h, w = frame.shape[:2]
    if w > 1024:
        frame = cv2.resize(frame, (1024, int(h * 1024 / w)))
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    if not ok:
        return "Could not encode image."
    try:
        resp = _get_client().models.generate_content(
            model=MODEL_NAME,
            contents=[
                PROMPTS[mode],
                types.Part.from_bytes(data=buf.tobytes(), mime_type="image/jpeg"),
            ],
        )
        return resp.text or "No response from model."
    except Exception as e:
        return f"Vision request failed: {e}"