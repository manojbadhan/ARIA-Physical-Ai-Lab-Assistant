import os
import cv2
from google import genai
from google.genai import types

# Primary model first, lighter fallback second. Override with env vars if needed.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash-lite")
MODELS = [m for m in (MODEL_NAME, FALLBACK_MODEL) if m]
_client = None

PROMPTS = {
    "identify": (
        "You are ARIA, a visual assistant. Identify the main object in this image. "
        "Explain what it is used for and describe visible features. If uncertain, say so. "
        "Do not invent technical specifications that cannot be verified. "
        "Reply in English, in 2 short spoken sentences, no markdown."
    ),
    "ocr": (
        "Read all legible text in this image exactly as written. "
        "Return only the text. If there is no readable text, say 'No text found'."
    ),
    "ask": (
        "You are ARIA, a visual assistant. Look at this camera image and answer the user's question about it. "
        "Reply in English, in 2 short spoken sentences, no markdown. "
        "If you cannot tell from the image, say so briefly. User's question: {q}"
    ),
}

# Errors worth trying the other model for (overloaded / rate limited / timeout)
_RETRYABLE = ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "overloaded", "DEADLINE")


def _get_client():
    global _client
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        _client = genai.Client(api_key=key)
    return _client


def analyze(frame, mode="identify", question=None):
    h, w = frame.shape[:2]
    max_w = 1600 if mode == "ocr" else 1024
    if w > max_w:
        frame = cv2.resize(frame, (max_w, int(h * max_w / w)))
    cv2.imwrite("last_vision.jpg", frame)   # debug: exactly what Gemini receives
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    if not ok:
        return "Could not encode image."

    prompt = PROMPTS[mode].format(q=question or "describe what you see") if mode == "ask" else PROMPTS[mode]
    contents = [
        prompt,
        types.Part.from_bytes(data=buf.tobytes(), mime_type="image/jpeg"),
    ]
    last_error = None
    for model in MODELS:
        try:
            resp = _get_client().models.generate_content(model=model, contents=contents)
            return resp.text or "No response from model."
        except Exception as e:
            last_error = e
            if any(tag in str(e) for tag in _RETRYABLE):
                print(f"[vision] {model} busy, trying next model")
                continue
            break  # a real error (bad key, bad request): do not hide it behind a fallback
    return f"Vision request failed: {last_error}"