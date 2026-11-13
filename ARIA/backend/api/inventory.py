from flask import Blueprint, jsonify
from backend.repositories import equipment_repository as repo
from backend.services import inventory_service

bp = Blueprint("inventory", __name__, url_prefix="/api/inventory")

@bp.get("")
def items(): return jsonify(items=repo.all_items())

@bp.get("/stats")
def stats(): return jsonify(inventory_service.stats())
