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
 
 
def find_class(package, name):
    """Import the class `name` from whichever file in `package/` defines it."""
    for info in pkgutil.iter_modules(importlib.import_module(package).__path__):
        mod = importlib.import_module(f"{package}.{info.name}")
        if hasattr(mod, name):
            return getattr(mod, name)
    raise ImportError(f"No file in {package}/ defines {name}")
 
 
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
                query = stt.transcribe(path)
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
                    system_prompt=SYSTEM_PROMPT + "\n\n" + VOICE_RULES,
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