import os
from ai_engine.vision.detector import detect

def identify(image_bytes):
    """YOLO first (offline, fast), Gemini as fallback for anything unknown."""
    try:
        hits = detect(image_bytes)
        if hits: return max(hits, key=lambda h: h[1])[0]
    except Exception:
        pass
    if os.getenv("GEMINI_API_KEY"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            m = genai.GenerativeModel("gemini-2.5-flash")
            r = m.generate_content(["Name the main electronics or lab object in this image in 1 to 3 words.",
                                    {"mime_type": "image/jpeg", "data": image_bytes}])
            return r.text.strip()
        except Exception:
            return None
    return None
