import importlib
import pkgutil
import re
import threading
import time
import traceback
from collections import deque
 
from audio.listener import MicListener
from chat.prompts2 import GREETINGS, LANGUAGE_RULES, VOICE_RULES, WAKE_REPLIES, build_message
from llm.prompts import SYSTEM_PROMPT
 
# --- language ----------------------------------------------------------------
LANGUAGE = "hi"              # "hi" = Hindi (Devanagari), "en" = English
STT_MODELS = {"hi": "whisper-large-v3"}   # more accurate than turbo for Hindi; English uses your config's model
VOICE_KEYWORDS = {"hi": ("hindi", "hi-in", "/hi")}    # how a Hindi voice shows up in the voice list
 
# --- wake word: ARIA only answers when addressed -----------------------------
# Whisper spells the name in different ways, so list the likely ones.
WAKE_WORDS = ("aria", "arya", "ariya", "आरिया", "अरिया", "आर्या", "अर्या", "आरीया")
ACTIVE_WINDOW = 12.0         # seconds after ARIA speaks during which no wake word is needed
WAKE_RE = re.compile("|".join(re.escape(w) for w in WAKE_WORDS), re.IGNORECASE)
 
# --- speaker next to the mic: stop ARIA hearing herself ------------------------
ECHO_TAIL = 0.8             # seconds the mic stays deaf after she stops talking (room echo; use ~1.5 for a Bluetooth speaker)
ECHO_OVERLAP = 0.7          # if this share of the words heard was in her own recent speech, it was her echo
 
LOADING = "loading..."
CALIBRATING = "calibrating mic - stay quiet"
LISTENING = "LISTENING - say ARIA, then ask"
HEARING = "hearing you..."
EXIT_WORDS = ("exit", "quit", "stop", "goodbye", "अलविदा", "बाय", "बाय बाय", "बंद करो", "रुको", "बस")
 
# --- speech-to-text filtering ------------------------------------------------
MAX_NO_SPEECH_PROB = 0.6     # Whisper's own "this is probably silence" score
MIN_AVG_LOGPROB = -1.2       # Whisper's confidence in its words (closer to 0 = more confident)
MAX_COMPRESSION_RATIO = 2.4  # very repetitive text is a classic hallucination
MAX_FOREIGN_RATIO = 0.2      # share of characters from a script we don't expect
 
 
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
 
 
def _foreign_ratio(text):
    """Share of characters outside the scripts we expect (Latin, plus Devanagari in Hindi mode)."""
    def expected(c):
        return c.isascii() or (LANGUAGE == "hi" and "\u0900" <= c <= "\u097f")
    return sum(not expected(c) for c in text) / len(text)
 
 
def transcribe_speech(stt, path):
    """
    Same job as stt.transcribe(path) (it reuses your SpeechToText object's client), but the
    language is fixed and it drops what Whisper "hears" in noise. Returns text or None.
    Dropped results are printed as [stt] ... so you can tune the numbers above.
    """
    if not hasattr(stt, "client"):
        return stt.transcribe(path)
    try:
        with open(path, "rb") as audio_file:
            result = stt.client.audio.transcriptions.create(
                file=audio_file,
                model=STT_MODELS.get(LANGUAGE, stt.model),
                language=LANGUAGE,
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
        if _foreign_ratio(text) > MAX_FOREIGN_RATIO:
            print(f"[stt] dropped wrong-language text: {text!r}")
            return None
        return text
    except Exception as error:
        print(f"[STT ERROR] {type(error).__name__}: {error}")
        return None
 
 
def _tokens(text):
    # the Devanagari block is listed because \w alone splits Hindi words at vowel signs
    return re.sub(r"[^\w\u0900-\u097F]+", " ", text.lower()).split()
 
 
def looks_like_echo(heard, spoken_texts):
    """True if `heard` is mostly made of words ARIA herself just said (her voice came back into the mic)."""
    words = _tokens(heard)
    if len(words) < 3:                     # too short to judge; "yes" or "ok" could be a real answer
        return False
    for text in spoken_texts:
        said = set(_tokens(text))
        if sum(w in said for w in words) / len(words) >= ECHO_OVERLAP:
            return True
    return False
 
 
def apply_wake_word(query, now, active_until):
    """
    Returns the question to answer, "" if the user only said the wake word,
    or None if the speech wasn't meant for ARIA and should be ignored.
    """
    woke = bool(WAKE_RE.search(query))
    if not woke and now > active_until:
        return None
    if not woke:
        return query
    return " ".join(WAKE_RE.sub(" ", query).split()).strip(" ,.!?।-")
 
 
def choose_voice(tts):
    """Switch your TextToSpeech to a voice for LANGUAGE, if the system has one."""
    words = VOICE_KEYWORDS.get(LANGUAGE)
    if not words:
        return
    try:
        for i, voice in enumerate(tts.engine.getProperty("voices")):
            label = f"{voice.id} {voice.name}".lower()
            if any(w in label for w in words):
                tts.set_voice(i)
                print(f"[tts] using voice: {voice.name}")
                return
    except Exception as error:
        print(f"[tts] could not list voices: {error}")
    print("[tts] WARNING: no Hindi voice found. Pi: sudo apt install espeak-ng. "
          "Windows: install the Hindi language pack. Until then she will mispronounce Hindi.")
 
 
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
        choose_voice(tts)
        history = []
        active_until = 0.0
        spoken = deque(maxlen=3)        # what ARIA said most recently, to spot her own echo
 
        with MicListener() as mic:
            s.mic = mic
 
            def speak(text):
                nonlocal active_until
                s.status = "speaking..."
                spoken.append(text)
                tts.speak(text)         # blocks until finished
                time.sleep(ECHO_TAIL)   # let the room echo die away before listening again
                mic.drain()             # drop audio recorded while ARIA was talking
                active_until = time.time() + ACTIVE_WINDOW
                s.status = LISTENING
 
            speak(GREETINGS[LANGUAGE])
            s.status = CALIBRATING      # after the greeting, so her voice isn't counted as noise
            mic.calibrate()
            s.status = LISTENING
 
            while not s.quit.is_set():
                path = mic.listen(s.quit, on_speech_start=lambda: setattr(s, "status", HEARING))
                if not path:
                    s.status = LISTENING
                    continue
 
                s.status = "transcribing..."
                heard = transcribe_speech(stt, path)
                if not heard or len(heard.strip(" .!?।")) < 2:
                    mic.drain()
                    s.status = LISTENING
                    continue
 
                if looks_like_echo(heard, spoken):
                    print(f"[echo] ignored (that was ARIA's own voice): {heard!r}")
                    mic.drain()
                    s.status = LISTENING
                    continue
 
                query = apply_wake_word(heard, time.time(), active_until)
                if query is None:
                    print(f"[wake] ignored (not addressed to ARIA): {heard!r}")
                    s.status = LISTENING
                    continue
                if query == "":                      # only the wake word
                    speak(WAKE_REPLIES[LANGUAGE])
                    continue
 
                s.heard = query
                print(f"\nYou: {query}")
 
                if query.lower().strip(" .!?।") in EXIT_WORDS:
                    speak("Goodbye." if LANGUAGE == "en" else "अलविदा!")
                    s.quit.set()
                    break
 
                objects = s.detector.stable_labels()
                print(f"[camera sees: {', '.join(objects) or 'nothing recognizable'}]")
 
                s.status = "thinking..."
                reply = llm.generate_response(
                    user_message=build_message(query, objects),
                    system_prompt=SYSTEM_PROMPT + "\n\n" + VOICE_RULES + " " + LANGUAGE_RULES[LANGUAGE],
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