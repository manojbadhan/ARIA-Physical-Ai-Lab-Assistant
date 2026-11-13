def record_utterance(rate=16000, frame_ms=30, silence_ms=800, max_s=12, aggressiveness=2):
    """Record from the mic until the speaker stops (webrtcvad). Returns 16-bit mono PCM bytes."""
    import pyaudio, webrtcvad
    vad, n = webrtcvad.Vad(aggressiveness), int(rate * frame_ms / 1000)
    pa = pyaudio.PyAudio()
    st = pa.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=n)
    frames, started, quiet = [], False, 0
    try:
        for _ in range(int(max_s * 1000 / frame_ms)):
            f = st.read(n, exception_on_overflow=False); speech = vad.is_speech(f, rate)
            if speech: started, quiet = True, 0
            elif started: quiet += frame_ms
            if started: frames.append(f)
            if started and quiet >= silence_ms: break
    finally:
        st.close(); pa.terminate()
    return b"".join(frames)

def pcm_to_wav(pcm, rate=16000):
    import io, wave
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
    return buf.getvalue()
