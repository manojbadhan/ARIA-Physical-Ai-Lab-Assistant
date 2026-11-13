from backend.core.exceptions import AppError

def validate_chat(d):
    msg = (d.get("message") or "").strip()
    if not msg: raise AppError("Message required")
    if len(msg) > 1000: raise AppError("Message too long")
    return msg
