import sys, re, math, threading, time
from PySide6.QtCore import Qt, QTimer, Signal, QObject
from PySide6.QtGui import QPainter, QColor, QPainterPath, QLinearGradient, QPen, QBrush, QFont
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

# ---- connect YOUR project code here -----------------------------------------
try:
    from assistant import process_command      # your function: question text -> reply text
except Exception:
    def process_command(text):
        return f"You asked: {text}. Connect assistant.process_command to get real answers."
try:
    import speech_recognition as sr
except Exception:
    sr = None
try:
    import pyttsx3
except Exception:
    pyttsx3 = None
# ------------------------------------------------------------------------------

ROBOT_NAME = "ARIA"
TITLE = "ARIA - Lab Assistant"
WAKE = re.compile(r"\b(aria|arya|ariya|aaria|ariah)\b")   # spellings the recogniser may return

# state: (label, colour, wave height, wave speed)
STATES = {
    "idle":         ("Say “ARIA” to wake me", "#8fa3c7", .05, .02),
    "listening":    ("Listening", "#2ee6ff", .60, .09),
    "transcribing": ("Transcribing", "#b58cff", .30, .20),
    "thinking":     ("Thinking", "#ffb84d", .18, .14),
    "speaking":     ("Speaking", "#ff4f9a", .75, .12),
}


class Assistant(QObject):
    """Wake word -> listen -> transcribe -> think -> speak. Runs in a thread."""
    state = Signal(str)
    user_text = Signal(str)
    bot_text = Signal(str)
    busy = False
    _trig = False
    _awake = False

    def start_wake(self):
        if sr:
            threading.Thread(target=self._wake_loop, daemon=True).start()

    def trigger(self):                       # tap / Space = say "ARIA"
        if self._awake:
            self._trig = True
        elif not self.busy:
            threading.Thread(target=self._run, args=(None,), daemon=True).start()

    def _wake_loop(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as src:
                r.adjust_for_ambient_noise(src, 1)
                self._awake = True
                while True:
                    if self._trig:
                        self._trig = False
                        self._run(None, r, src)
                        continue
                    try:
                        audio = r.listen(src, timeout=2, phrase_time_limit=6)
                        heard = r.recognize_google(audio).lower()
                    except Exception:
                        continue
                    m = WAKE.search(heard)
                    if m:                    # "ARIA, <question>" skips the listening step
                        self._run(heard[m.end():].strip(" ,.?!") or None, r, src)
        except Exception as e:
            self._awake = False
            self.bot_text.emit(f"Microphone problem: {e}")

    def _run(self, text, r=None, src=None):
        self.busy = True
        try:
            if text is None:
                self.state.emit("listening")
                text = self._hear(r, src)
                if not text:
                    self.bot_text.emit("I didn't catch that. Say ARIA to try again.")
                    return
            self.user_text.emit(text)
            self.state.emit("thinking")
            reply = str(process_command(text))
            self.bot_text.emit(reply)
            self.state.emit("speaking")
            self._say(reply)
        except Exception as e:
            self.bot_text.emit(f"Something went wrong: {e}")
        finally:
            self.busy = False
            self.state.emit("idle")

    def _hear(self, r=None, src=None):
        if not sr:                           # demo mode if SpeechRecognition isn't installed
            time.sleep(2.5); self.state.emit("transcribing"); time.sleep(1.2)
            return "What is the pH of distilled water?"
        try:
            if src is None:
                r = sr.Recognizer()
                with sr.Microphone() as s:
                    r.adjust_for_ambient_noise(s, .4)
                    audio = r.listen(s, timeout=6, phrase_time_limit=12)
            else:
                audio = r.listen(src, timeout=6, phrase_time_limit=12)
            self.state.emit("transcribing")
            return r.recognize_google(audio)
        except Exception:
            return ""

    def _say(self, text):
        if pyttsx3:
            e = pyttsx3.init(); e.say(text); e.runAndWait()
        else:
            time.sleep(min(6, .07 * len(text)))


class Wave(QWidget):
    """Layered translucent ribbons that move with the assistant's state."""
    COLORS = [(0, 122, 255), (0, 220, 255), (255, 45, 130), (0, 230, 190), (160, 90, 255)]

    def __init__(self):
        super().__init__()
        self.state, self.t, self.ph, self.amp = "idle", 0, 0.0, .05
        self.setMinimumHeight(120)
        tm = QTimer(self); tm.timeout.connect(self.tick); tm.start(16)

    def tick(self):
        self.t += 1
        _, _, tg, sp = STATES[self.state]
        if self.state == "speaking":
            m = .35 + .65 * abs(math.sin(self.t * .21)) * (.6 + .4 * math.sin(self.t * .07))
        elif self.state == "listening":
            m = .45 + .55 * abs(math.sin(self.t * .08) * math.cos(self.t * .031))
        else:
            m = 1
        self.amp += (tg * m - self.amp) * .1
        self.ph += sp
        self.update()

    def paintEvent(self, _):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height(); cy = h / 2; N = 90
        p.setCompositionMode(QPainter.CompositionMode_Plus)
        for i, (r, g, b) in enumerate(self.COLORS):
            c = .5 + .22 * math.sin(self.ph * .4 + i * 1.9)
            wd, f, A = .16 + .03 * i, 1.5 + .55 * i, self.amp * h * .42
            pts = []
            for j in range(N + 1):
                u = j / N
                env = math.exp(-((u - c) / wd) ** 2)
                pts.append((w * u, A * env * math.sin(6.283 * f * u + self.ph * (-1) ** i + i * 1.3)))
            path = QPainterPath(); path.moveTo(pts[0][0], cy - pts[0][1])
            for x, y in pts[1:]: path.lineTo(x, cy - y)
            for x, y in reversed(pts): path.lineTo(x, cy + y)
            path.closeSubpath()
            p.fillPath(path, QColor(r, g, b, 120))
        g = QLinearGradient(0, 0, w, 0)
        g.setColorAt(0, QColor(255, 255, 255, 0)); g.setColorAt(.5, QColor(255, 255, 255, 170))
        g.setColorAt(1, QColor(255, 255, 255, 0))
        p.setCompositionMode(QPainter.CompositionMode_SourceOver)
        p.setPen(QPen(QBrush(g), 1.5)); p.drawLine(0, int(cy), w, int(cy))


def lbl(text="", size=20, color="white", bold=False, sp=0):
    l = QLabel(text); f = QFont("Segoe UI"); f.setPixelSize(size); f.setBold(bold)
    f.setLetterSpacing(QFont.AbsoluteSpacing, sp); l.setFont(f)
    l.setStyleSheet(f"color:{color};"); l.setWordWrap(True); l.setAlignment(Qt.AlignCenter)
    return l


def setcol(label, color):
    label.setStyleSheet(f"color:{color};")


def reveal(label, text, ms=50):
    """Types text into a label word by word (live transcription effect)."""
    words, n = text.split(), [0]
    if hasattr(label, "_tm"): label._tm.stop()
    label._tm = t = QTimer(label); label.setText("")
    def step():
        n[0] += 1; label.setText(" ".join(words[:n[0]]))
        if n[0] >= len(words): t.stop()
    t.timeout.connect(step); t.start(ms)


class Aurora(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("root"); self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("#root{background:qradialgradient(cx:.5,cy:.45,radius:.85,"
                           "fx:.5,fy:.45,stop:0 #172a63,stop:1 #04061a);}")
        self.wave, self.bot = Wave(), Assistant()
        self.bot.state.connect(self.on_state)
        self.bot.user_text.connect(self.on_user)
        self.bot.bot_text.connect(self.on_bot)

        title = lbl(TITLE, 26, "#9fb4e6", True, 3)
        self.status = lbl("", 24, "#8fa3c7", True, 2)
        self.cap = lbl("Say “ARIA” and ask me anything about the lab.", 32, "#cfe3ff")
        self.cap.setMinimumHeight(170)

        lay = QVBoxLayout(self); lay.setContentsMargins(50, 26, 50, 40)
        lay.addWidget(title); lay.addWidget(self.wave, 3)
        lay.addWidget(self.status); lay.addWidget(self.cap, 1)

        self.x = QPushButton("✕", self); self.x.setFixedSize(52, 52); self.x.clicked.connect(self.close)
        self.x.setStyleSheet("QPushButton{background:rgba(128,128,128,70);color:white;border:none;"
                             "border-radius:26px;font-size:20px;}")
        self.on_state("idle")
        self.bot.start_wake()                # begin listening for "ARIA"

    def on_state(self, st):
        text, color, *_ = STATES[st]
        self.wave.state = st
        self.status.setText(text + ("…" if st != "idle" else "")); setcol(self.status, color)

    def on_user(self, text):                 # the question, typed out live
        setcol(self.cap, "#cfe3ff"); reveal(self.cap, f"“{text}”", 60)

    def on_bot(self, text):                  # the answer
        setcol(self.cap, "#ffd6e8"); reveal(self.cap, text, 45)

    def mousePressEvent(self, e): self.bot.trigger()
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space: self.bot.trigger()

    def resizeEvent(self, e):
        super().resizeEvent(e); self.x.move(self.width() - 68, 16); self.x.raise_()


def show(windowed=None):
    """Open the ARIA screen. Blocks until the window is closed."""
    if windowed is None:
        windowed = "--windowed" in sys.argv
    app = QApplication(sys.argv); w = Aurora()
    if windowed:
        w.resize(1100, 650); w.show()
    else:
        app.setOverrideCursor(Qt.BlankCursor); w.showFullScreen()
    app.exec()


if __name__ == "__main__":
    show()
