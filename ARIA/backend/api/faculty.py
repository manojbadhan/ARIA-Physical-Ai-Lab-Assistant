from flask import Blueprint, request, jsonify, session
from backend.core.permissions import require_role
from backend.repositories import equipment_repository as repo
from backend.schemas.equipment import validate_tool
from backend.services import inventory_service
from ai_engine.vision.classifier import identify

bp = Blueprint("faculty", __name__, url_prefix="/api/faculty")

@bp.post("/tools")
@require_role("faculty")
def add_tool():
    form = request.form
    loc = validate_tool(form)
    photo_file = request.files.get("photo")
    name = loc["name"]
    if not name and photo_file:
        name = identify(photo_file.read()) or ""; photo_file.stream.seek(0)
    if not name: return jsonify(error="Tool name needed (or enable vision to detect it)"), 400
    repo.upsert(name, loc["location"], inventory_service.save_photo(photo_file))
    return jsonify(ok=True, name=name, location=loc["location"])

@bp.get("/usage")
@require_role("faculty")
def usage(): return jsonify(items=inventory_service.usage())

@bp.post("/usage")
def log_usage():
    """Called by the robot when it sees someone using a tool."""
    photo = inventory_service.save_photo(request.files.get("photo"), "use")
    repo.add_detection(request.form.get("tool", "unknown"), photo, "usage")
    return jsonify(ok=True)
