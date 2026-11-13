from flask import Blueprint, request, jsonify, session, redirect
from backend.services import auth_service

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

def _data():
    return request.get_json(silent=True) or request.form.to_dict()

def _done(user, is_json):
    session.update(user_id=user["id"], role=user["role"])
    if is_json: return jsonify(user)
    return redirect("/faculty" if user["role"] == "faculty" else "/dashboard")

@bp.post("/signup")
def signup():
    d = _data(); user = auth_service.signup(d)
    return _done(user, request.is_json)

@bp.post("/login")
def login():
    d = _data(); user = auth_service.login(d.get("email"), d.get("password"))
    return _done(user, request.is_json)

@bp.post("/logout")
def logout():
    session.clear(); return jsonify(ok=True)
