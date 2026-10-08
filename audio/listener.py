import queue
import tempfile
import time
import wave
from collections import deque
 
import numpy as np
import sounddevice as sd
 
RATE = 16000
BLOCK = RATE * 30 // 1000       # 30 ms audio blocks
MIC_THRESHOLD = None            # None = auto-calibrate; or set a number (see the level bar)
START_BLOCKS = 2                # loud blocks in a row that count as "started talking"
END_SILENCE_BLOCKS = 25         # ~0.75 s of quiet ends the question
MIN_VOICED_BLOCKS = 8           # ignore clicks and coughs shorter than this
MAX_RECORD_SECONDS = 30
WAV_PATH = tempfile.gettempdir() + "/aria_input.wav"
 
 
def _rms(block):
    return float(np.sqrt(np.mean(block.astype(np.float32) ** 2)))
 
 
class MicListener:
    def __init__(self):
        self.q = queue.Queue()
        self.level = 0.0
        self.threshold = 1e9     # nothing counts as speech until calibrate() runs
        self._stream = None
 
    def __enter__(self):
        self._stream = sd.InputStream(
            samplerate=RATE, channels=1, dtype="int16", blocksize=BLOCK,
            callback=lambda data, *_: self.q.put(data.copy()),
        )
        self._stream.start()
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
 
    def calibrate(self, seconds=1.0):
        """Measure room noise and set the speech threshold from it."""
        levels, end = [], time.time() + seconds
        while time.time() < end:
            try:
                levels.append(_rms(self.q.get(timeout=0.2)))
            except queue.Empty:
                pass
        floor = float(np.median(levels)) if levels else 0.0
        self.threshold = MIC_THRESHOLD or max(floor * 3, 200)
        print(f"[mic] noise floor {floor:.0f}, speech threshold {self.threshold:.0f}")
 
    def listen(self, quit_event, on_speech_start=None):
        """Wait until the user speaks and finishes. Returns a wav path, or None."""
        pre = deque(maxlen=10)           # ~0.3 s before speech starts, so the first word isn't cut
        chunks, collecting = [], False
        loud_run = silent_run = voiced = 0
 
        while not quit_event.is_set():
            try:
                block = self.q.get(timeout=0.2)
            except queue.Empty:
                continue
            self.level = _rms(block)
            loud = self.level > self.threshold
 
            if not collecting:
                pre.append(block)
                loud_run = loud_run + 1 if loud else 0
                if loud_run >= START_BLOCKS:
                    collecting, chunks, voiced = True, list(pre), loud_run
                    if on_speech_start:
                        on_speech_start()
            else:
                chunks.append(block)
                voiced, silent_run = (voiced + 1, 0) if loud else (voiced, silent_run + 1)
                if silent_run >= END_SILENCE_BLOCKS or len(chunks) * BLOCK > MAX_RECORD_SECONDS * RATE:
                    break
 
        if not collecting or voiced < MIN_VOICED_BLOCKS:
            return None
        with wave.open(WAV_PATH, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes(np.concatenate(chunks).tobytes())
        return WAV_PATH