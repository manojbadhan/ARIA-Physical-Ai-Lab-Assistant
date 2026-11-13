import re
from backend.core.exceptions import AppError

def validate_signup(d):
    name, email, pw = (d.get("name") or "").strip(), (d.get("email") or "").strip().lower(), d.get("password") or ""
    role = d.get("role", "student")
    if not name: raise AppError("Name required")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email): raise AppError("Valid email required")
    if len(pw) < 8: raise AppError("Password must be at least 8 characters")
    if role not in ("student", "faculty"): raise AppError("Invalid role")
    return {"name": name, "email": email, "password": pw, "role": role}
