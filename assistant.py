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
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import sounddevice as sd
from audio.listener import MicListener
from vision.gemini_vision import analyze
from chat.prompts2 import WAKE_REPLIES, build_message, greeting, system_rules
from config import (
    ACTIVE_WINDOW, ASSISTANT_GENDER, ECHO_OVERLAP, ECHO_TAIL, EDGE_RATE, EDGE_TIMEOUT, EDGE_VOICES, EDGE_VOLUME,
    EXIT_WORDS, FASTEST_SPEECH_CPS, GENDER_VOICE_WORDS, HISTORY_MESSAGES,
    MAX_COMPRESSION_RATIO, MAX_FOREIGN_RATIO, MAX_NO_SPEECH_PROB, MIN_AVG_LOGPROB, PAUSE_VISION_WHILE_SPEAKING,
    STT_MODELS, STT_PROMPTS, TTS_ENGINE, VOICE_KEYWORDS, WAKE_FUZZY_RATIO, WAKE_WORD_POSITION,
    WAKE_WORD_REQUIRED, WAKE_WORDS
)
from llm.prompts import SYSTEM_PROMPT

LANG = "en"        # ARIA is English only

LOADING = "loading..."
CALIBRATING = "calibrating mic - stay quiet"
LISTENING = "LISTENING - say ARIA, then ask" if WAKE_WORD_REQUIRED else "LISTENING - just ask"
HEARING = "hearing you..."

# ---------------------------------------------------------------- conversation mode
# After ARIA answers, the user can keep talking WITHOUT saying "ARIA" for this long.
CONVO_WINDOW = max(ACTIVE_WINDOW, 45)      # seconds, after a normal answer
FOLLOWUP_WINDOW = 90                       # seconds, when ARIA's reply ends with a question

# Even after the window above has closed, phrases that clearly continue the last answer
# ("tell me in detail", "explain more") are accepted for this many seconds after ARIA's reply.
FOLLOWUP_GRACE = 120
FOLLOWUP_STARTS = ("tell me more", "tell me in detail", "in detail", "explain", "give me an example",
                   "what about", "and what", "how come", "why")

# ---------------------------------------------------------------- Piper (offline neural voice)
_PIPER = {}
PIPER_MODEL = "~/ARIA/voices/en_US-ryan-medium.onnx"


def piper_available():
    """Piper is usable if the package is installed and the English model exists."""
    try:
        import piper  # noqa: F401
    except ImportError:
        print("[tts] piper not installed. Run: pip install piper-tts")
        return False
    if not os.path.exists(os.path.expanduser(PIPER_MODEL)):
        print(f"[tts] piper English model not found at {PIPER_MODEL}")
        return False
    return True


def piper_fetch(text):
    """Make the audio for one chunk of text. Returns (int16 samples, sample rate)."""
    from piper import PiperVoice
    if "en" not in _PIPER:                          # load once, reuse
        _PIPER["en"] = PiperVoice.load(os.path.expanduser(PIPER_MODEL))
    voice = _PIPER["en"]
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
    return audio, out_rate


# ---------------------------------------------------------------- helpers
def find_class(package, name):
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
    """Share of characters that are not plain English text (catches Korean/Arabic/other-script junk)."""
    return sum(not c.isascii() for c in text) / len(text)


# ---------------------------------------------------------------- speech to text
def _whisper(stt, path):
    """One Whisper call, language forced to English (no auto-detect, no retry pass)."""
    kwargs = {"model": STT_MODELS.get(LANG, stt.model), "temperature": 0.0,
              "response_format": "verbose_json", "language": LANG}
    if STT_PROMPTS.get(LANG):
        kwargs["prompt"] = STT_PROMPTS[LANG]
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


def transcribe_speech(stt, path):
    """Returns (text, "en") or (None, None)."""
    if not hasattr(stt, "client"):
        text = stt.transcribe(path)
        return (text, LANG) if text else (None, None)
    try:
        text = _text_of(_whisper(stt, path))
        if not text:
            return None, None
        if _foreign_ratio(text) > MAX_FOREIGN_RATIO:
            print(f"[stt] dropped non-English text: {text!r}")
            return None, None
        return text, LANG
    except Exception as error:
        print(f"[STT ERROR] {type(error).__name__}: {error}")
        return None, None


def _tokens(text):
    return re.sub(r"[^\w]+", " ", text.lower()).split()


def looks_like_echo(heard, spoken_texts):
    words = _tokens(heard)
    if len(words) < 3:
        return False
    for text in spoken_texts:
        said = set(_tokens(text))
        if sum(w in said for w in words) / len(words) >= ECHO_OVERLAP:
            return True
    return False


# ---------------------------------------------------------------- wake word
def _clean_word(word):
    return word.strip(" ,.!?-'\"").lower()


def _is_wake(word):
    """Exact or fuzzy match. Used for the first few words of a sentence."""
    w = _clean_word(word)
    if not w:
        return False
    if w in WAKE_WORDS:
        return True
    return w.isascii() and difflib.SequenceMatcher(None, w, "aria").ratio() >= WAKE_FUZZY_RATIO


def _is_wake_exact(word):
    """Exact match only. Used for ARIA anywhere else in the sentence (no fuzzy = fewer false wakes)."""
    w = _clean_word(word)
    return bool(w) and w in WAKE_WORDS


def apply_wake_word(query, started_at, active_until, last_reply_at=0.0):
    """started_at = when the user STARTED speaking (not when transcription finished).
    Inside the conversation window no wake word is needed. After it closes, a phrase that clearly
    continues ARIA's last answer ("tell me in detail...") is still accepted for FOLLOWUP_GRACE seconds."""
    words = query.split()
    lead = any(_is_wake(w) for w in words[:WAKE_WORD_POSITION])
    anywhere = lead or any(_is_wake_exact(w) for w in words)
    if not anywhere and WAKE_WORD_REQUIRED and started_at > active_until:
        low = query.lower().strip(" ,.!?-")
        if (last_reply_at and started_at - last_reply_at <= FOLLOWUP_GRACE
                and low.startswith(FOLLOWUP_STARTS)):
            return query
        return None
    if not lead:
        return query                      # keep "ARIA" if it was said at the end, it is part of the question
    kept = [w for i, w in enumerate(words) if not (i < WAKE_WORD_POSITION and _is_wake(w))]
    return " ".join(kept).strip(" ,.!?-")


# ---------------------------------------------------------------- text to speech
_SPEECH_MAP = str.maketrans({"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
                             "\u2014": ", ", "\u2013": ", ", "\u2011": "-", "\u2026": "...", "\u00a0": " "})


def clean_for_speech(text):
    text = text.translate(_SPEECH_MAP)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)      # never read links aloud
    text = re.sub(r"[*#`_]+", "", text)
    text = "".join(c for c in text if c.isascii())
    return " ".join(text.split())


def split_sentences(text):
    """One chunk per sentence (very short ones are merged), so audio starts after the first sentence
    and every online request is short enough not to time out."""
    parts = [p for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p]
    chunks = []
    for p in parts:
        if chunks and len(chunks[-1]) < 40:
            chunks[-1] += " " + p
        else:
            chunks.append(p)
    return chunks


def choose_voice(tts):
    """Pick an English system voice that matches ASSISTANT_GENDER where possible."""
    words = VOICE_KEYWORDS.get(LANG, ())
    gender_words = GENDER_VOICE_WORDS.get(ASSISTANT_GENDER, ())
    try:
        voices = list(tts.engine.getProperty("voices"))
    except Exception as error:
        print(f"[tts] could not list voices: {error}")
        return True
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
        print(f"[tts] system voice: {best[1].name}")
    return True


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


def edge_fetch(text):
    """Make the audio for one chunk of text. Returns (int16 samples, sample rate)."""
    import miniaudio
    voices = EDGE_VOICES.get(ASSISTANT_GENDER) or EDGE_VOICES["male"]
    mp3 = asyncio.run(asyncio.wait_for(_edge_audio(text, voices[LANG]), EDGE_TIMEOUT))
    if not mp3:
        raise RuntimeError("no audio came back")
    rate = int(sd.query_devices(kind="output")["default_samplerate"])
    decoded = miniaudio.decode(mp3, output_format=miniaudio.SampleFormat.SIGNED16, nchannels=1, sample_rate=rate)
    return np.frombuffer(decoded.samples, dtype=np.int16), rate


def _play(samples, rate):
    sd.play(samples, rate, latency="high")
    sd.wait()


def _play_chunks(chunks, fetch, progress):
    """Play chunk i while chunk i+1 is already being made. progress[] records what was really spoken,
    so a failure half-way only re-speaks the rest."""
    pool = ThreadPoolExecutor(max_workers=1)
    try:
        nxt = pool.submit(fetch, chunks[0])
        for i in range(len(chunks)):
            samples, rate = nxt.result()
            if i + 1 < len(chunks):
                nxt = pool.submit(fetch, chunks[i + 1])
            _play(samples, rate)
            progress.append(i)
    finally:
        pool.shutdown(wait=False)


def speak_system(box, tts_cls, text):
    for attempt in (1, 2):
        if box["voice_ready"] is False:
            choose_voice(box["tts"])
            box["voice_ready"] = True
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
            box["voice_ready"] = False
    print("[tts] still silent after a restart. Check the output device and the volume.")


def say(box, tts_cls, text):
    """Order: Piper (offline) -> Edge (online) -> system voice. Sentence by sentence."""
    text = clean_for_speech(text)
    if not text:
        return
    chunks = split_sentences(text)

    if box.get("piper") and chunks:
        progress = []
        try:
            _play_chunks(chunks, piper_fetch, progress)
            return
        except Exception as error:
            print(f"[tts] piper failed ({type(error).__name__}: {error})")
            chunks = chunks[len(progress):]

    if box["edge"] and chunks and time.time() >= box.get("edge_off_until", 0):
        progress = []
        try:
            _play_chunks(chunks, edge_fetch, progress)
            box["edge_fails"] = 0
            return
        except Exception as error:
            print(f"[tts] online voice failed ({type(error).__name__}: {error}); using the system voice")
            chunks = chunks[len(progress):]
            box["edge_fails"] = box.get("edge_fails", 0) + 1
            if box["edge_fails"] >= 2:      # do not wait for a timeout on every single reply
                box["edge_off_until"] = time.time() + 300
                box["edge_fails"] = 0
                print("[tts] online voice keeps failing, skipping it for 5 minutes")

    if not chunks:
        return
    speak_system(box, tts_cls, " ".join(chunks))


# ---------------------------------------------------------------- vision with retry
def analyze_retry(frame, mode, question=None, tries=3):
    """analyze() returns the error text instead of raising, so check the returned string."""
    for i in range(tries):
        text = analyze(frame, mode, question)
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
        self.reply = ""
        self.reply_n = 0
        self.heard_n = 0

def vision_intent(query):
    t = query.lower()
    words = set(re.findall(r"[a-z']+", t))
    if (words & {"read", "written", "writing", "label"}
            or any(p in t for p in ("what does it say", "what does this say", "what does that say",
                                    "what's written", "what is written", "text on", "any text"))):
        return "ocr"
    if any(p in t for p in ("what is this", "what's this", "what is that", "what's that",
                            "what am i holding", "identify", "what do you see", "look at this")):
        return "identify"
    if any(p in t for p in ("can you see", "do you see", "look at", "in my hand", "on my screen",
                            "on my phone", "on this screen", "on the screen", "in front of you",
                            "behind this")):
        return "ask"                  # free question about what the camera sees
    return None


# ---------------------------------------------------------------- main voice loop
def voice_worker(s):
    try:
        llm = find_class("llm", "LabAssistantLLM")()
        stt = find_class("audio", "SpeechToText")()
        tts_cls = find_class("audio", "TextToSpeech")
        box = {"tts": tts_cls(), "voice_ready": False,
               "edge": TTS_ENGINE == "edge" and edge_available(),
               "piper": piper_available()}
        voice_kind = ("offline neural voices" if box["piper"]
                      else "online neural voices" if box["edge"] else "system voices")
        print(f"[ARIA] language: English | voice: {ASSISTANT_GENDER}, {voice_kind} | wake word: "
              + (f"say ARIA first, then talk freely ({CONVO_WINDOW} s after each reply, "
                 f"{FOLLOWUP_WINDOW} s after a question)" if WAKE_WORD_REQUIRED else "off, answers everything"))
        history = []
        active_until = 0.0
        speech_started = [0.0]
        last_reply = [0.0]
        spoken = deque(maxlen=3)
        with MicListener() as mic:
            s.mic = mic

            def on_speech_start():
                speech_started[0] = time.time()
                s.status = HEARING

            def speak(text):
                nonlocal active_until
                s.status = "speaking..."
                s.reply = text
                s.reply_n += 1
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
                time.sleep(ECHO_TAIL)
                mic.drain()
                # a reply that ends with a question keeps the conversation open longer
                asks = "?" in text[-120:]
                active_until = time.time() + (FOLLOWUP_WINDOW if asks else CONVO_WINDOW)
                last_reply[0] = time.time()
                s.status = LISTENING

            speak(greeting(LANG, ASSISTANT_GENDER))
            s.status = CALIBRATING
            mic.calibrate()
            s.status = LISTENING
            while not s.quit.is_set():
                path = mic.listen(s.quit, on_speech_start=on_speech_start)
                if not path:
                    s.status = LISTENING
                    continue
                s.status = "transcribing..."
                heard, _ = transcribe_speech(stt, path)
                if not heard or len(heard.strip(" .!?")) < 2:
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
                started = speech_started[0] or time.time()
                query = apply_wake_word(heard, started, active_until, last_reply[0])
                if query is None:
                    gap = started - active_until
                    print(f"[wake] ignored (window closed {gap:.0f}s before you spoke; "
                          f"{started - last_reply[0]:.0f}s after ARIA's last reply): {heard!r}")
                    s.heard = f"(ignored, no ARIA) {heard}"
                    s.status = LISTENING
                    continue
                if query == "":
                    speak(WAKE_REPLIES[LANG])
                    continue
                s.heard = query
                s.heard_n += 1
                print(f"\nYou: {query}")
                if query.lower().strip(" .!?") in EXIT_WORDS:
                    speak("Goodbye.")
                    s.quit.set()
                    break
                objects = s.detector.stable_labels()
                mode = vision_intent(query)
                print(f"[intent] {mode}")
                if mode:
                    if s.frame is None:
                        speak("I can't see anything yet.")
                        continue
                    s.status = "looking..."
                    reply = analyze_retry(s.frame.copy(), mode, question=query)
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
                    system_prompt=SYSTEM_PROMPT + "\n\n" + system_rules(LANG, ASSISTANT_GENDER),
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
