from backend.core.exceptions import AppError, Unauthorized
from backend.core.security import hash_password, verify_password
from backend.repositories import user_repository as users
from backend.schemas.user import validate_signup

def signup(data):
    d = validate_signup(data)
    if users.by_email(d["email"]): raise AppError("Email already registered", 409)
    uid = users.create(d["name"], d["email"], hash_password(d["password"]), d["role"])
    return {"id": uid, "role": d["role"]}

def login(email, password):
    u = users.by_email((email or "").strip().lower())
    if not u or not verify_password(password or "", u["password_hash"]): raise Unauthorized("Wrong email or password")
    return {"id": u["id"], "role": u["role"], "name": u["name"]}
