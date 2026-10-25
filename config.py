import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "openai/gpt-oss-120b"
STT_MODEL = "whisper-large-v3-turbo"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
NOTES_DIR = "notes/"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
TOP_K = 3
SIMILARITY_THRESHOLD = 0.35
STORE_DIR = "rag/store/"
CHUNKS_PATH = STORE_DIR + "chunks.pkl"
EMBEDDINGS_PATH = STORE_DIR + "embeddings.npy"
LANGUAGE = "auto"
GREETING_LANGUAGE = "en"
ASSISTANT_GENDER = "male"
STT_MODELS = {"auto": "whisper-large-v3", "hi": "whisper-large-v3"}
STT_PROMPTS = {"auto": "Hello ARIA. हेलो आरिया।", "hi": "हेलो आरिया।", "en": "Hello ARIA."}
TTS_ENGINE = "edge"
EDGE_VOICES = {
    "male": {"en": "en-IN-PrabhatNeural", "hi": "hi-IN-MadhurNeural"},
    "female": {"en": "en-IN-NeerjaNeural", "hi": "hi-IN-SwaraNeural"},
}
EDGE_RATE = "+0%"
EDGE_VOLUME = "+0%"
EDGE_TIMEOUT = 8
VOICE_KEYWORDS = {"en": ("english", "en-", "/en"), "hi": ("hindi", "hi-in", "/hi")}
GENDER_VOICE_WORDS = {
    "male": ("david", "mark", "george", "ravi", "hemant", "madhur", "prabhat", "guy", "male"),
    "female": ("zira", "hazel", "susan", "heera", "kalpana", "swara", "neerja", "jenny", "female"),
}
PAUSE_VISION_WHILE_SPEAKING = True
WAKE_WORD_REQUIRED = True
WAKE_WORDS = ("aria", "arya", "ariya", "आरिया", "अरिया", "आर्या", "अर्या", "आरीया",
              "लेजिया", "लेज़िया", "लीजिया")
WAKE_FUZZY_RATIO = 0.7
WAKE_WORD_POSITION = 4
ACTIVE_WINDOW = 12.0
EXIT_WORDS = ("exit", "quit", "stop", "goodbye", "अलविदा", "बाय", "बाय बाय", "बंद करो", "रुको", "बस")
HISTORY_MESSAGES = 20
ECHO_TAIL = 0.8
ECHO_OVERLAP = 0.7
FASTEST_SPEECH_CPS = 60
MAX_NO_SPEECH_PROB = 0.6
MIN_AVG_LOGPROB = -1.2
MAX_COMPRESSION_RATIO = 2.4
MAX_FOREIGN_RATIO = 0.2
MIC_DEVICE = None
MIC_CHANNELS = 1
MIC_THRESHOLD = None
CALIBRATION_SECONDS = 2.0
THRESHOLD_FACTOR_VAD = 2.0
THRESHOLD_FACTOR_NO_VAD = 3.5
MIN_THRESHOLD = 150
VAD_AGGRESSIVENESS = 2
START_WINDOW = 6
START_VOTES = 5
END_SILENCE_BLOCKS = 25
MIN_VOICED_BLOCKS = 8
MIN_SPEECH_RATIO = 0.3
MAX_RECORD_SECONDS = 30
IDLE_REPORT_SECONDS = 15
CAMERA_INDEX = 0
FRAME_SIZE_PC = (1280, 720)
FRAME_SIZE_PI = (640, 480)
DETECT_FPS_PC = 15
DETECT_FPS_PI = 4
YOLO_WEIGHTS = "yolo11s.pt"
YOLO_CONF = 0.4
YOLO_IMGSZ = 480
YOLO_IGNORE_LABELS = {"person"}
DETECT_HISTORY = 15
STABLE_MIN_COUNT = 4