from flask import Blueprint, request, jsonify
from ai_engine.speech.speech_to_text import transcribe
from ai_engine.speech.text_to_speech import synthesize_bytes

bp = Blueprint("voice", __name__, url_prefix="/api/voice")

@bp.post("/stt")
def stt():
    f = request.files.get("audio")
    if not f: return jsonify(error="audio required"), 400
    return jsonify(text=transcribe(f.read()))

@bp.post("/tts")
def tts():
    text = (request.get_json(silent=True) or {}).get("text", "")
    audio = synthesize_bytes(text)
    return (audio, 200, {"Content-Type": "audio/mpeg"}) if audio else (jsonify(error="tts unavailable"), 503)
