from functools import wraps
from flask import session
from backend.config import Config
from backend.core.exceptions import Unauthorized, Forbidden

def require_role(role):
    def deco(fn):
        @wraps(fn)
        def inner(*a, **k):
            if not Config.DEV_OPEN_ACCESS:
                if "user_id" not in session: raise Unauthorized("Login required")
                if session.get("role") != role: raise Forbidden("Faculty only")
            return fn(*a, **k)
        return inner
    return deco
