import io, os

def transcribe(audio_bytes, filename="audio.wav", language="en"):
    """Groq Whisper with the language forced (auto-detect wasted a second pass and misheard Norwegian)."""
    if not os.getenv("GROQ_API_KEY"): return ""
    from groq import Groq
    r = Groq().audio.transcriptions.create(file=(filename, io.BytesIO(audio_bytes)), model="whisper-large-v3-turbo",
                                           language=language, temperature=0)
    return clean(r.text)

HALLUCINATIONS = ("thank you for watching", "thanks for watching", "subscribe", "you")

def clean(text):
    t = (text or "").strip()
    return "" if t.lower().strip(" .!") in HALLUCINATIONS or len(t.split()) < 2 else t
