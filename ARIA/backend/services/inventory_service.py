import re, time
from pathlib import Path
from backend.config import Config
from backend.repositories import equipment_repository as repo

def save_photo(file, prefix="tool"):
    if not file or not file.filename: return None
    Config.DETECTIONS.mkdir(parents=True, exist_ok=True)
    name = f"{prefix}_{int(time.time())}_{re.sub(r'[^A-Za-z0-9._-]', '_', file.filename)}"
    file.save(Config.DETECTIONS / name)
    return f"/media/{name}"

def stats():
    s = repo.counts()
    s["recent"] = [{"photo": r["photo"] or "", "label": r["label"], "when": (r["created_at"] or "")[:16]} for r in repo.detections("detected", 8)]
    return s

def usage():
    return [{"photo": r["photo"] or "", "tool": r["label"], "when": (r["created_at"] or "")[:16]} for r in repo.detections("usage", 12)]
