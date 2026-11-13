from flask import Blueprint, request, jsonify
from ai_engine.vision.classifier import identify
from backend.repositories import equipment_repository as repo
from backend.services import inventory_service

bp = Blueprint("vision", __name__, url_prefix="/api/vision")

@bp.post("/identify")
def identify_route():
    f = request.files.get("image")
    if not f: return jsonify(error="image required"), 400
    data = f.read(); f.stream.seek(0)
    label = identify(data)
    photo = inventory_service.save_photo(f, "frame")
    if label: repo.add_detection(label, photo, "detected")
    return jsonify(label=label or "I could not recognise that", photo=photo)
