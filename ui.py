import sys, math
from PySide6.QtCore import Qt, QTimer, Signal, QObject, QSize
from PySide6.QtGui import QPainter, QColor, QPainterPath, QLinearGradient, QPen, QBrush, QFont, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

ROBOT_NAME = "ARIA"
TITLE = "ARIA - Lab Assistant"

# state: (label, colour, wave height, wave speed)
STATES = {
    "idle":         ("Say “ARIA” to wake me", "#8fa3c7", .05, .02),
    "listening":    ("Listening", "#2ee6ff", .60, .09),
    "transcribing": ("Transcribing", "#b58cff", .30, .20),
    "thinking":     ("Thinking", "#ffb84d", .18, .14),
    "speaking":     ("Speaking", "#ff4f9a", .75, .12),
}


def ui_state(status):
    """Map voice_worker's s.status text to one of the UI states."""
    st = (status or "").lower()
    if st.startswith("hearing"):
        return "listening"
    if st.startswith("transcrib"):
        return "transcribing"
    if st.startswith(("thinking", "looking")):
        return "thinking"
    if st.startswith("speaking"):
        return "speaking"
    return "idle"


class Assistant(QObject):
    """Only watches the Session that voice_worker fills. No mic / TTS here."""
    state = Signal(str)
    user_text = Signal(str)
    bot_text = Signal(str)

    def __init__(self, session):
        super().__init__()
        self.s = session
        self._st = None
        self._hn = 0
        self._rn = 0
        self._tm = QTimer(self)
        self._tm.timeout.connect(self.poll)
        self._tm.start(100)

    def poll(self):
        s = self.s
        if s.quit.is_set():                # "Goodbye" or camera failure -> close the screen
            QApplication.quit()
            return
        if s.status != self._st:
            self._st = s.status
            self.state.emit(ui_state(s.status))
        if s.heard_n != self._hn:          # counters, so the same question twice still shows
            self._hn = s.heard_n
            self.user_text.emit(s.heard)
        if s.reply_n != self._rn:
            self._rn = s.reply_n
            self.bot_text.emit(s.reply)


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


class CameraView(QLabel):
    """Live camera feed (with detection boxes). get_frame() must return a BGR numpy image or None."""
    def __init__(self, get_frame):
        super().__init__()
        self.get_frame, self._last = get_frame, None
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(320, 240)
        self.setText("Camera starting...")
        self.setStyleSheet("background:#02040f;color:#8fa3c7;font-size:18px;"
                           "border:2px solid #2a3f7a;border-radius:14px;")
        self._pm = None
        tm = QTimer(self); tm.timeout.connect(self.refresh); tm.start(40)    # ~25 fps

    def refresh(self):
        frame = self.get_frame()
        if frame is None or frame is self._last:
            return
        self._last = frame
        h, w = frame.shape[:2]
        img = QImage(frame.data, w, h, frame.strides[0], QImage.Format_BGR888).copy()
        self._pm = QPixmap.fromImage(img)
        self.show_scaled()

    def show_scaled(self):
        if self._pm is not None:
            self.setPixmap(self._pm.scaled(self.size() - QSize(6, 6),
                                           Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, e):
        super().resizeEvent(e); self.show_scaled()


class Aurora(QWidget):
    def __init__(self, session, get_frame=None):
        super().__init__()
        self.setObjectName("root"); self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("#root{background:qradialgradient(cx:.5,cy:.45,radius:.85,"
                           "fx:.5,fy:.45,stop:0 #172a63,stop:1 #04061a);}")
        self.wave, self.bot = Wave(), Assistant(session)
        self.bot.state.connect(self.on_state)
        self.bot.user_text.connect(self.on_user)
        self.bot.bot_text.connect(self.on_bot)

        title = lbl(TITLE, 26, "#9fb4e6", True, 3)
        self.status = lbl("", 24, "#8fa3c7", True, 2)
        self.cap = lbl("Say “ARIA” and ask me anything about the lab.", 28, "#cfe3ff")
        self.cap.setMinimumHeight(170)

        right = QVBoxLayout()
        right.addWidget(self.wave, 3); right.addWidget(self.status); right.addWidget(self.cap, 2)
        body = QHBoxLayout(); body.setSpacing(30)
        if get_frame is not None:                       # camera on the left, ARIA on the right
            self.cam = CameraView(get_frame)
            body.addWidget(self.cam, 5)
        body.addLayout(right, 6)
        lay = QVBoxLayout(self); lay.setContentsMargins(40, 26, 40, 30)
        lay.addWidget(title); lay.addLayout(body, 1)

        self.x = QPushButton("✕", self); self.x.setFixedSize(52, 52); self.x.clicked.connect(self.close)
        self.x.setStyleSheet("QPushButton{background:rgba(128,128,128,70);color:white;border:none;"
                             "border-radius:26px;font-size:20px;}")
        self.on_state("idle")

    def on_state(self, st):
        text, color, *_ = STATES[st]
        self.wave.state = st
        self.status.setText(text + ("…" if st != "idle" else "")); setcol(self.status, color)

    def on_user(self, text):                 # the question, typed out live
        setcol(self.cap, "#cfe3ff"); reveal(self.cap, f"“{text}”", 60)

    def on_bot(self, text):                  # the answer
        setcol(self.cap, "#ffd6e8"); reveal(self.cap, text, 45)

    def resizeEvent(self, e):
        super().resizeEvent(e); self.x.move(self.width() - 68, 16); self.x.raise_()


def show(session, get_frame=None, windowed=None):
    """Open the ARIA screen. Blocks until the window is closed."""
    if windowed is None:
        windowed = "--windowed" in sys.argv
    app = QApplication(sys.argv); w = Aurora(session, get_frame)
    if windowed:
        w.resize(1100, 650); w.show()
    else:
        app.setOverrideCursor(Qt.BlankCursor); w.showFullScreen()
    app.exec()
