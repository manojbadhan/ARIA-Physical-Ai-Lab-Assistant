import logging
from logging.handlers import RotatingFileHandler
from backend.config import Config

def setup_logging():
    Config.STORAGE.joinpath("logs").mkdir(parents=True, exist_ok=True)
    h = RotatingFileHandler(Config.STORAGE / "logs" / "aria.log", maxBytes=1_000_000, backupCount=3)
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not any(isinstance(x, RotatingFileHandler) for x in root.handlers):
        root.addHandler(h)
