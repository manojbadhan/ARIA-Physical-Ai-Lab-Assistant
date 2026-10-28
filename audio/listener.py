import queue
import tempfile
import time
import wave
from collections import deque
 
import numpy as np
import sounddevice as sd
from config import (
    MIC_DEVICE, MIC_CHANNELS, MIC_THRESHOLD, VAD_AGGRESSIVENESS,
    START_WINDOW, START_VOTES, END_SILENCE_BLOCKS, MIN_VOICED_BLOCKS,
    MIN_SPEECH_RATIO, MAX_RECORD_SECONDS, CALIBRATION_SECONDS,
    THRESHOLD_FACTOR_VAD, THRESHOLD_FACTOR_NO_VAD, MIN_THRESHOLD,
)
 
try:
    import webrtcvad
except ImportError:
    webrtcvad = None
 
RATE = 16000
BLOCK = RATE * 30 // 1000       # 30 ms audio blocks (a size WebRTC VAD accepts)

WAV_PATH = tempfile.gettempdir() + "/aria_input.wav"
 
 
def _rms(block):
    return float(np.sqrt(np.mean(block.astype(np.float32) ** 2)))
 
 
class MicListener:
    def __init__(self):
        self.q = queue.Queue()
        self.level = 0.0
        self.threshold = 1e9     # nothing counts as speech until calibrate() runs
        self.overflows = 0       # audio blocks the system dropped because the CPU was busy
        self._stream = None
        self._vad = webrtcvad.Vad(VAD_AGGRESSIVENESS) if webrtcvad else None
        if self._vad is None:
            print("[mic] webrtcvad not installed: using loudness only, which picks up noise. "
                  "Run: pip install webrtcvad-wheels")
 
    def _on_audio(self, data, frames, time_info, status):
        if status:                       # sounddevice reports dropped audio here
            self.overflows += 1
        self.q.put(data[:, :1].copy())
 
    def __enter__(self):
        self._stream = sd.InputStream(samplerate=RATE, channels=MIC_CHANNELS, dtype="int16", device=MIC_DEVICE,
                                      blocksize=BLOCK, callback=self._on_audio)
        self._stream.start()
        try:
            print(f"[mic] input device: {sd.query_devices(MIC_DEVICE, 'input')['name']}")
        except Exception:
            pass
        return self
 
    def __exit__(self, *exc):
        self._stream.stop()
        self._stream.close()
 
    def drain(self):
        while True:
            try:
                self.q.get_nowait()
            except queue.Empty:
                return
 
    def calibrate(self, seconds=None):
        
        self.drain()                     # throw away audio queued during the greeting
        seconds = seconds or CALIBRATION_SECONDS
        levels, end = [], time.time() + seconds
        while time.time() < end:
            try:
                levels.append(_rms(self.q.get(timeout=0.2)))
            except queue.Empty:
                pass
        floor = float(np.median(levels)) if levels else 0.0
        factor = THRESHOLD_FACTOR_VAD if self._vad else THRESHOLD_FACTOR_NO_VAD
        self.threshold = MIC_THRESHOLD or max(floor * factor, MIN_THRESHOLD)
        print(f"[mic] noise floor {floor:.0f}, loudness threshold {self.threshold:.0f}")
    
    def _is_speech(self, block, level):
        if level <= self.threshold:
            return False
        if self._vad is None:
            return True
        try:
            return self._vad.is_speech(block.tobytes(), RATE)
        except Exception:
            return True                  # unexpected block size: fall back to loudness
 
    def listen(self, quit_event, on_speech_start=None):
        """Wait until the user speaks and finishes. Returns a wav path, or None."""
        pre = deque(maxlen=10)           # ~0.3 s before speech starts, so the first word isn't cut
        votes = deque(maxlen=START_WINDOW)
        chunks, collecting = [], False
        silent_run = voiced = 0
        dropped_before = self.overflows
 
        while not quit_event.is_set():
            try:
                block = self.q.get(timeout=0.2)
            except queue.Empty:
                continue
            self.level = _rms(block)
            speech = self._is_speech(block, self.level)
 
            if not collecting:
                pre.append(block)
                votes.append(speech)
                if sum(votes) >= START_VOTES:
                    collecting, chunks, voiced = True, list(pre), sum(votes)
                    dropped_before = self.overflows
                    if on_speech_start:
                        on_speech_start()
            else:
                chunks.append(block)
                voiced, silent_run = (voiced + 1, 0) if speech else (voiced, silent_run + 1)
                if silent_run >= END_SILENCE_BLOCKS or len(chunks) * BLOCK > MAX_RECORD_SECONDS * RATE:
                    break
 
        if not collecting:
            return None
        active = max(len(chunks) - silent_run, 1)        # the clip without the trailing silence
        if voiced < MIN_VOICED_BLOCKS or voiced / active < MIN_SPEECH_RATIO:
            print(f"[mic] ignored a noise clip ({voiced} speech blocks out of {active})")
            return None
        if self.overflows > dropped_before:
            print("[mic] WARNING: audio was dropped while recording (CPU overloaded), "
                  "so the transcript may be garbage. Lower the detection load.")
        with wave.open(WAV_PATH, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes(np.concatenate(chunks).tobytes())
        return WAV_PATH