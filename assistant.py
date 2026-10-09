import importlib
import pkgutil
import threading
import time
import traceback
 
from audio.listener import MicListener
from chat.prompts2 import GREETING, VOICE_RULES, build_message
from llm.prompts import SYSTEM_PROMPT
 
LOADING = "loading..."
CALIBRATING = "calibrating mic - stay quiet"
LISTENING = "LISTENING - just ask"
HEARING = "hearing you..."
EXIT_WORDS = ("exit", "quit", "stop", "goodbye")
 
# --- speech-to-text settings -------------------------------------------------
STT_LANGUAGE = "en"          # Whisper guesses the language if you don't fix it, and guesses wrong on noise
MAX_NO_SPEECH_PROB = 0.6     # Whisper's own "this is probably silence" score
MIN_AVG_LOGPROB = -1.2       # Whisper's confidence in its words (closer to 0 = more confident)
MAX_COMPRESSION_RATIO = 2.4  # very repetitive text is a classic hallucination
MAX_NON_ASCII_RATIO = 0.2    # leftover foreign-script text
ENGLISH_RULE = ("Always reply in English, even if the user's words look like another language. "
                "If a message is garbled or makes no sense, say you didn't catch that and ask "
                "them to repeat instead of guessing.")
 
 
def find_class(package, name):
    """Import the class `name` from whichever file in `package/` defines it."""
    for info in pkgutil.iter_modules(importlib.import_module(package).__path__):
        mod = importlib.import_module(f"{package}.{info.name}")
        if hasattr(mod, name):
            return getattr(mod, name)
    raise ImportError(f"No file in {package}/ defines {name}")
 
 
def _get(obj, key, default=None):
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)
 
 
def _trusted(seg):
    return ((_get(seg, "no_speech_prob", 0) or 0) <= MAX_NO_SPEECH_PROB
            and (_get(seg, "avg_logprob", 0) or 0) >= MIN_AVG_LOGPROB
            and (_get(seg, "compression_ratio", 0) or 0) <= MAX_COMPRESSION_RATIO)
 
 
def transcribe_english(stt, path):
    """
    Same job as stt.transcribe(path) (it reuses your SpeechToText object's client and model),
    but English-only and it drops what Whisper "hears" in noise. Returns text or None.
    Dropped results are printed as [stt] ... so you can tune the numbers above.
    """
    if not hasattr(stt, "client"):
        return stt.transcribe(path)
    try:
        with open(path, "rb") as audio_file:
            result = stt.client.audio.transcriptions.create(
                file=audio_file,
                model=stt.model,
                language=STT_LANGUAGE,
                temperature=0.0,
                response_format="verbose_json",
            )
        segments = _get(result, "segments") or []
        if segments:
            text = " ".join((_get(s, "text", "") or "").strip() for s in segments if _trusted(s)).strip()
            if not text:
                said = " ".join((_get(s, "text", "") or "").strip() for s in segments).strip()
                print(f"[stt] dropped low-confidence: {said!r}")
                return None
        else:                                        # no segment details returned
            text = (_get(result, "text", "") or "").strip()
 
        if not text:
            return None
        if sum(ord(c) > 127 for c in text) / len(text) > MAX_NON_ASCII_RATIO:
            print(f"[stt] dropped non-English: {text!r}")
            return None
        return text
    except Exception as error:
        print(f"[STT ERROR] {type(error).__name__}: {error}")
        return None
 
 
class Session:
    """State shared by the camera window (main thread) and the voice thread."""
 
    def __init__(self):
        self.status = LOADING
        self.heard = ""
        self.quit = threading.Event()
        self.detector = None     # set by main.py
        self.mic = None          # set by voice_worker
 
 
def voice_worker(s):
    try:
        # built inside this thread so pyttsx3 is used from the thread that created it
        llm = find_class("llm", "LabAssistantLLM")()
        stt = find_class("audio", "SpeechToText")()
        tts = find_class("audio", "TextToSpeech")()
        history = []
 
        with MicListener() as mic:
            s.mic = mic
 
            def speak(text):
                s.status = "speaking..."
                tts.speak(text)         # blocks until finished
                time.sleep(0.3)
                mic.drain()             # drop audio recorded while ARIA was talking
                s.status = LISTENING
 
            speak(GREETING)
            s.status = CALIBRATING      # after the greeting, so her voice isn't counted as noise
            mic.calibrate()
            s.status = LISTENING
 
            while not s.quit.is_set():
                path = mic.listen(s.quit, on_speech_start=lambda: setattr(s, "status", HEARING))
                if not path:
                    s.status = LISTENING
                    continue
 
                s.status = "transcribing..."
                query = transcribe_english(stt, path)
                if not query or len(query.strip(" .!?")) < 2:
                    mic.drain()
                    s.status = LISTENING
                    continue
                s.heard = query
                print(f"\nYou: {query}")
 
                if query.lower().strip(" .!?") in EXIT_WORDS:
                    speak("Goodbye.")
                    s.quit.set()
                    break
 
                objects = s.detector.stable_labels()
                print(f"[camera sees: {', '.join(objects) or 'nothing recognizable'}]")
 
                s.status = "thinking..."
                reply = llm.generate_response(
                    user_message=build_message(query, objects),
                    system_prompt=SYSTEM_PROMPT + "\n\n" + VOICE_RULES + " " + ENGLISH_RULE,
                    conversation_history=history,
                    max_history_turns=20,       # last 10 exchanges, so follow-ups make sense
                )
                history += [{"role": "user", "content": query},
                            {"role": "assistant", "content": reply}]
                print(f"ARIA: {reply}")
                speak(reply)
    except Exception:
        traceback.print_exc()
        s.status = "VOICE ERROR - see terminal"