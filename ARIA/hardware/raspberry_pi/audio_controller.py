import os, subprocess, tempfile
from ai_engine.speech.audio_processor import record_utterance, pcm_to_wav
from ai_engine.speech.speech_to_text import transcribe
from ai_engine.speech.text_to_speech import synthesize_bytes

def listen():
    pcm = record_utterance()
    return transcribe(pcm_to_wav(pcm)) if pcm else ""

def speak(text):
    audio = synthesize_bytes(text)
    if not audio:
        subprocess.run(["espeak", text], check=False); return
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(audio); path = f.name
    subprocess.run(["mpg123", "-q", path], check=False); os.unlink(path)
