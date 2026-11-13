from flask import Blueprint, request, jsonify, session
from backend.schemas.chat import validate_chat
from backend.services import chat_service

bp = Blueprint("chat", __name__, url_prefix="/api")

@bp.post("/chat")
def chat():
    text = validate_chat(request.get_json(silent=True) or {})
    return jsonify(chat_service.reply(session.get("user_id"), text))
