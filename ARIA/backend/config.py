import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    DEBUG = os.getenv("DEBUG", "1") == "1"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    DEV_OPEN_ACCESS = os.getenv("DEV_OPEN_ACCESS", "1") == "1"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    STORAGE = ROOT / "storage"
    DETECTIONS = STORAGE / "detections"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
