import asyncio
import difflib
import gc
import importlib
import io
import os
import pkgutil
import re
import threading
import time
import traceback
import wave
from collections import deque
import numpy as np
import sounddevice as sd
from audio.listener import MicListener
from vision.gemini_vision import analyze
from chat.prompts2 import WAKE_REPLIES, build_message, greeting, system_rules
from config import (
    ACTIVE_WINDOW, ASSISTANT_GENDER, ECHO_OVERLAP, ECHO_TAIL, EDGE_RATE, EDGE_TIMEOUT, EDGE_VOICES, EDGE_VOLUME,
    EXIT_WORDS, FASTEST_SPEECH_CPS, GENDER_VOICE_WORDS, GREETING_LANGUAGE, HISTORY_MESSAGES, LANGUAGE,
    MAX_COMPRESSION_RATIO, MAX_FOREIGN_RATIO, MAX_NO_SPEECH_PROB, MIN_AVG_LOGPROB, PAUSE_VISION_WHILE_SPEAKING,
    STT_MODELS, STT_PROMPTS, TTS_ENGINE, VOICE_KEYWORDS, WAKE_FUZZY_RATIO, WAKE_WORD_POSITION,
    WAKE_WORD_REQUIRED, WAKE_WORDS, HINDI_MIN_DEVA_RATIO, HINDI_MIN_LETTERS
)
from llm.prompts import SYSTEM_PROMPT

LOADING = "loading..."
CALIBRATING = "calibrating mic - stay quiet"
LISTENING = "LISTENING - say ARIA, then ask" if WAKE_WORD_REQUIRED else "LISTENING - just ask"
HEARING = "hearing you..."

# ---------------------------------------------------------------- Piper (offline neural voice)
_PIPER = {}
PIPER_MODELS = {
    "en": "~/ARIA/voices/en_US-ryan-medium.onnx",
    "hi": "~/ARIA/voices/hi_IN-pratham-medium.onnx",
}


def piper_available():
    """Piper is usable if the package is installed and the English model exists.
    A missing Hindi model only makes Hindi sentences fall back to Edge."""
    try:
        import piper  # noqa: F401
    except ImportError:
        print("[tts] piper not installed. Run: pip install piper-tts")
        return False
    if not os.path.exists(os.path.expanduser(PIPER_MODELS["en"])):
        print(f"[tts] piper English model not found at {PIPER_MODELS['en']}")
        return False
    return True


def speak_piper(text, language):
    from piper import PiperVoice
    if language not in _PIPER:                      # load once, reuse
        _PIPER[language] = PiperVoice.load(os.path.expanduser(PIPER_MODELS[language]))
    voice = _PIPER[language]
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        try:
            voice.synthesize_wav(text, wf)          # piper-tts >= 1.3
        except AttributeError:
            voice.synthesize(text, wf)              # older piper-tts
    buf.seek(0)
    with wave.open(buf, "rb") as wf:
        rate = wf.getframerate()
        audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    if audio.size == 0:
        raise RuntimeError("piper produced no audio")
    out_rate = int(sd.query_devices(kind="output")["default_samplerate"])
    if out_rate != rate:                            # USB speakers often reject 22050 Hz
        n = int(len(audio) * out_rate / rate)
        audio = np.interp(np.linspace(0, len(audio), n, endpoint=False),
                          np.arange(len(audio)), audio).astype(np.int16)
    sd.play(audio, out_rate, latency="high")
    sd.wait()


# ---------------------------------------------------------------- helpers
def find_class(package, name):
    for info in pkgutil.iter_modules(importlib.import_module(package).__path__):
        mod = importlib.import_module(f"{package}.{info.name}")
        if hasattr(mod, name):
            return getattr(mod, name)
    raise ImportError(f"No file in {package}/ defines {name}")


def _get(obj, key, default=None):
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)


def is_devanagari(c):
    return "\u0900" <= c <= "\u097f"


HINDI_WORDS = {"है", "हैं", "क्या", "मैं", "मुझे", "को", "का", "की", "के", "में", "से", "कर", "करो",
               "तो", "नहीं", "और", "यह", "वह", "था", "हो", "रहा", "रही", "आप", "तुम", "कैसे", "कौन",
               "क्यों", "कब", "कहाँ", "बताओ", "बताइए", "पर", "भी", "ही"}


def _hindi_ok(text):
    letters = [c for c in text if c.isalpha()]
    if len(letters) < HINDI_MIN_LETTERS:
        return False
    if sum(is_devanagari(c) for c in letters) / len(letters) < HINDI_MIN_DEVA_RATIO:
        return False
    return any(w in HINDI_WORDS for w in _tokens(text))


def script_language(text):
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "en"
    return "hi" if sum(is_devanagari(c) for c in letters) / len(letters) > 0.3 else "en"


def _trusted(seg):
    return ((_get(seg, "no_speech_prob", 0) or 0) <= MAX_NO_SPEECH_PROB
            and (_get(seg, "avg_logprob", 0) or 0) >= MIN_AVG_LOGPROB
            and (_get(seg, "compression_ratio", 0) or 0) <= MAX_COMPRESSION_RATIO)


def _foreign_ratio(text):
    def expected(c):
        return c.isascii() or (LANGUAGE in ("hi", "auto") and is_devanagari(c))
    return sum(not expected(c) for c in text) / len(text)


# ---------------------------------------------------------------- speech to text
def _whisper(stt, path, language):
    kwargs = {"model": STT_MODELS.get(language, stt.model), "temperature": 0.0, "response_format": "verbose_json"}
    if language != "auto":
        kwargs["language"] = language
    if STT_PROMPTS.get(language):
        kwargs["prompt"] = STT_PROMPTS[language]
    with open(path, "rb") as audio_file:
        return stt.client.audio.transcriptions.create(file=audio_file, **kwargs)


def _text_of(result):
    segments = _get(result, "segments") or []
    if not segments:
        return (_get(result, "text", "") or "").strip()
    text = " ".join((_get(s, "text", "") or "").strip() for s in segments if _trusted(s)).strip()
    if not text:
        said = " ".join((_get(s, "text", "") or "").strip() for s in segments).strip()
        print(f"[stt] dropped low-confidence: {said!r}")
    return text


def _detected(result):
    value = (_get(result, "language", "") or "").lower()
    if value in ("en", "english"):
        return "en"
    if value in ("hi", "hindi", "ur", "urdu"):
        return "hi"
    return value or None


def transcribe_speech(stt, path):
    if not hasattr(stt, "client"):
        text = stt.transcribe(path)
        return (text, script_language(text)) if text else (None, None)
    try:
        result = _whisper(stt, path, LANGUAGE)
        text = _text_of(result)
        if LANGUAGE == "auto" and text:
            detected = _detected(result)
            arabic_script = any("\u0600" <= c <= "\u06ff" for c in text)
            if detected not in (None, "en", "hi") and not arabic_script:
                print(f"[stt] heard {detected}, retrying as English: {text!r}")
                text = _text_of(_whisper(stt, path, "en"))
            if arabic_script or (detected == "hi" and script_language(text) == "en"):
                text = _text_of(_whisper(stt, path, "hi"))
        if LANGUAGE == "auto" and text and script_language(text) == "hi" and not _hindi_ok(text):
            print(f"[stt] weak Hindi, retrying as English: {text!r}")
            text = _text_of(_whisper(stt, path, "en"))
        if not text:
            return None, None
        if _foreign_ratio(text) > MAX_FOREIGN_RATIO:
            print(f"[stt] dropped wrong-language text: {text!r}")
            return None, None
        return text, (script_language(text) if LANGUAGE == "auto" else LANGUAGE)
    except Exception as error:
        print(f"[STT ERROR] {type(error).__name__}: {error}")
        return None, None


def _tokens(text):
    return re.sub(r"[^\w\u0900-\u097F]+", " ", text.lower()).split()


def looks_like_echo(heard, spoken_texts):
    words = _tokens(heard)
    if len(words) < 3:
        return False
    for text in spoken_texts:
        said = set(_tokens(text))
        if sum(w in said for w in words) / len(words) >= ECHO_OVERLAP:
            return True
    return False


def _is_wake(word):
    w = word.strip(" ,.!?।-'\"").lower()
    if not w:
        return False
    if w in WAKE_WORDS:
        return True
    return w.isascii() and difflib.SequenceMatcher(None, w, "aria").ratio() >= WAKE_FUZZY_RATIO


def apply_wake_word(query, now, active_until):
    words = query.split()
    woke = any(_is_wake(w) for w in words[:WAKE_WORD_POSITION])
    if not woke and WAKE_WORD_REQUIRED and now > active_until:
        return None
    if not woke:
        return query
    kept = [w for i, w in enumerate(words) if not (i < WAKE_WORD_POSITION and _is_wake(w))]
    return " ".join(kept).strip(" ,.!?।-")


# ---------------------------------------------------------------- text to speech
_SPEECH_MAP = str.maketrans({"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
                             "\u2014": ", ", "\u2013": ", ", "\u2011": "-", "\u2026": "...", "\u00a0": " "})


def clean_for_speech(text):
    text = text.translate(_SPEECH_MAP)
    text = re.sub(r"[*#`_]+", "", text)
    text = "".join(c for c in text if c.isascii() or is_devanagari(c))
    return " ".join(text.split())


def choose_voice(tts, language):
    words = VOICE_KEYWORDS.get(language, ())
    gender_words = GENDER_VOICE_WORDS.get(ASSISTANT_GENDER, ())
    try:
        voices = list(tts.engine.getProperty("voices"))
    except Exception as error:
        print(f"[tts] could not list voices: {error}")
        return language == "en"
    best = None
    for i, voice in enumerate(voices):
        label = f"{voice.id} {voice.name}".lower()
        if words and not any(w in label for w in words):
            continue
        if gender_words and any(w in label for w in gender_words):
            best = (i, voice)
            break
        best = best or (i, voice)
    if best:
        tts.set_voice(best[0])
        print(f"[tts] system voice for {language}: {best[1].name}")
        return True
    return language == "en"


def edge_available():
    try:
        import edge_tts  # noqa: F401
        import miniaudio  # noqa: F401
        return True
    except ImportError as error:
        print(f"[tts] online voices are not installed ({error}). Run: pip install edge-tts miniaudio")
        return False


async def _edge_audio(text, voice):
    import edge_tts
    data = bytearray()
    async for chunk in edge_tts.Communicate(text, voice, rate=EDGE_RATE, volume=EDGE_VOLUME).stream():
        if chunk["type"] == "audio":
            data += chunk["data"]
    return bytes(data)


def speak_edge(text, language):
    import miniaudio
    voices = EDGE_VOICES.get(ASSISTANT_GENDER) or EDGE_VOICES["male"]
    mp3 = asyncio.run(asyncio.wait_for(_edge_audio(text, voices[language]), EDGE_TIMEOUT))
    if not mp3:
        raise RuntimeError("no audio came back")
    rate = int(sd.query_devices(kind="output")["default_samplerate"])
    decoded = miniaudio.decode(mp3, output_format=miniaudio.SampleFormat.SIGNED16, nchannels=1, sample_rate=rate)
    sd.play(np.frombuffer(decoded.samples, dtype=np.int16), rate, latency="high")
    sd.wait()


def speak_system(box, tts_cls, text, language):
    for attempt in (1, 2):
        if box["language"] != language:
            choose_voice(box["tts"], language)
            box["language"] = language
        started = time.time()
        box["tts"].speak(text)
        took = time.time() - started
        if len(text) < 15 or took >= max(0.3, len(text) / FASTEST_SPEECH_CPS):
            return
        print(f"[tts] the speech engine came back after {took:.1f} s for {len(text)} characters, "
              "so it did not really speak.")
        if attempt == 1:
            print("[tts] restarting it and trying again")
            box["tts"] = None
            gc.collect()
            box["tts"] = tts_cls()
            box["language"] = None
    print("[tts] still silent after a restart. Check the output device and the volume.")


def say(box, tts_cls, text):
    """Order: Piper (offline) -> Edge (online) -> system voice."""
    text = clean_for_speech(text)
    if not text:
        return
    language = script_language(text)
    if box.get("piper"):
        try:
            speak_piper(text, language)
            return
        except Exception as error:
            print(f"[tts] piper failed ({type(error).__name__}: {error})")
    if box["edge"]:
        try:
            speak_edge(text, language)
            return
        except Exception as error:
            print(f"[tts] online voice failed ({type(error).__name__}: {error}); using the system voice")
    if language == "hi" and not box["hindi_system"]:
        print("[tts] cannot speak Hindi on this machine (no Hindi voice and no online voice).")
        return
    speak_system(box, tts_cls, text, language)


# ---------------------------------------------------------------- vision with retry
def analyze_retry(frame, mode, tries=3):
    """analyze() returns the error text instead of raising, so check the returned string."""
    for i in range(tries):
        text = analyze(frame, mode)
        if "503" not in text and "UNAVAILABLE" not in text:
            return text
        print(f"[vision] service busy, retry {i + 1}/{tries}")
        time.sleep(1.5 * (2 ** i))
    return "The vision service is busy right now. Please ask again in a moment."


class Session:
    def __init__(self):
        self.status = LOADING
        self.heard = ""
        self.quit = threading.Event()
        self.detector = None
        self.mic = None
        self.frame = None
        self.last_vision = {"mode": None, "text": "", "ts": 0}


def vision_intent(query):
    t = query.lower()
    words = set(re.findall(r"[a-z']+", t))
    if ("read" in words or "written" in words or "writing" in words) \
       or "what does it say" in t or "what does this say" in t:
        return "ocr"
    if any(p in t for p in ("what is this", "what's this", "what is that", "what's that",
                            "what am i holding", "in my hand", "identify", "what do you see", "look at this")):
        return "identify"
    return None


# ---------------------------------------------------------------- main voice loop
def voice_worker(s):
    global LANGUAGE
    try:
        llm = find_class("llm", "LabAssistantLLM")()
        stt = find_class("audio", "SpeechToText")()
        tts_cls = find_class("audio", "TextToSpeech")
        box = {"tts": tts_cls(), "language": None,
               "edge": TTS_ENGINE == "edge" and edge_available(),
               "piper": piper_available()}
        box["hindi_system"] = hasattr(box["tts"], "engine") and choose_voice(box["tts"], "hi")
        box["language"] = None
        any_hindi = box["piper"] or box["edge"] or box["hindi_system"]
        if LANGUAGE != "en" and not any_hindi:
            LANGUAGE = "en"
            print("[ARIA] No Hindi voice available, so Hindi is switched off and she will use English only.")
        greet_language = LANGUAGE if LANGUAGE in ("en", "hi") else GREETING_LANGUAGE
        if greet_language == "hi" and not any_hindi:
            greet_language = "en"
        voice_kind = ("offline neural voices" if box["piper"]
                      else "online neural voices" if box["edge"] else "system voices")
        print(f"[ARIA] language: {LANGUAGE} | voice: {ASSISTANT_GENDER}, {voice_kind} | wake word: "
              + ("say ARIA first, then ask (12 s follow-up window)" if WAKE_WORD_REQUIRED else "off, answers everything"))
        history = []
        active_until = 0.0
        spoken = deque(maxlen=3)
        with MicListener() as mic:
            s.mic = mic

            def speak(text):
                nonlocal active_until
                s.status = "speaking..."
                spoken.append(text)
                if PAUSE_VISION_WHILE_SPEAKING and s.detector is not None:
                    s.detector.paused = True
                t = time.time()
                try:
                    say(box, tts_cls, text)
                finally:
                    if s.detector is not None:
                        s.detector.paused = False
                print(f"[time] tts {time.time() - t:.2f}s")
                t = time.time()
                time.sleep(ECHO_TAIL)
                mic.drain()
                print(f"[time] echo-tail+drain {time.time() - t:.2f}s")

            speak(greeting(greet_language, ASSISTANT_GENDER))
            s.status = CALIBRATING
            mic.calibrate()
            s.status = LISTENING
            while not s.quit.is_set():
                path = mic.listen(s.quit, on_speech_start=lambda: setattr(s, "status", HEARING))
                if not path:
                    s.status = LISTENING
                    continue
                s.status = "transcribing..."
                heard, language = transcribe_speech(stt, path)
                if not heard or len(heard.strip(" .!?।")) < 2:
                    s.heard = "(could not make out any words)"
                    mic.drain()
                    s.status = LISTENING
                    continue
                if looks_like_echo(heard, spoken):
                    print(f"[echo] ignored (that was ARIA's own voice): {heard!r}")
                    s.heard = "(ignored: her own echo)"
                    mic.drain()
                    s.status = LISTENING
                    continue
                query = apply_wake_word(heard, time.time(), active_until)
                if query is None:
                    print(f"[wake] ignored (not addressed to ARIA): {heard!r}")
                    s.heard = f"(ignored, no ARIA) {heard}"
                    s.status = LISTENING
                    continue
                if query == "":
                    speak(WAKE_REPLIES[language])
                    continue
                s.heard = query
                print(f"\nYou ({language}): {query}")
                if query.lower().strip(" .!?।") in EXIT_WORDS:
                    speak("Goodbye." if language == "en" else "अलविदा!")
                    s.quit.set()
                    break
                objects = s.detector.stable_labels()
                mode = vision_intent(query)
                if mode:
                    if s.frame is None:
                        speak("I can't see anything yet.")
                        continue
                    s.status = "looking..."
                    reply = analyze_retry(s.frame.copy(), mode)
                    s.last_vision = {"mode": mode, "text": reply, "ts": time.time()}
                    history += [{"role": "user", "content": query},
                                {"role": "assistant", "content": reply}]
                    print(f"ARIA (vision/{mode}): {reply}")
                    speak(reply)
                    continue
                print(f"[camera sees: {', '.join(objects) or 'nothing recognizable'}]")
                s.status = "thinking..."
                reply = llm.generate_response(
                    user_message=build_message(query, objects),
                    system_prompt=SYSTEM_PROMPT + "\n\n" + system_rules(language, ASSISTANT_GENDER),
                    conversation_history=history,
                    max_history_turns=HISTORY_MESSAGES,
                )
                history += [{"role": "user", "content": query},
                            {"role": "assistant", "content": reply}]
                print(f"ARIA: {reply}")
                speak(reply)
    except Exception:
        traceback.print_exc()
        s.status = "VOICE ERROR - see terminal"