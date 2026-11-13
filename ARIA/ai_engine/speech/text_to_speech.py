import asyncio, os

def synthesize_bytes(text, voice=None):
    """Edge TTS neural voice, returned as mp3 bytes. None if edge-tts is unavailable/offline."""
    if not text: return None
    try:
        import edge_tts
    except ImportError:
        return None
    voice = voice or os.getenv("TTS_VOICE", "en-IN-NeerjaNeural")
    async def run():
        out = b""
        async for ch in edge_tts.Communicate(text, voice).stream():
            if ch["type"] == "audio": out += ch["data"]
        return out
    try:
        return asyncio.run(run()) or None
    except Exception:
        return None
