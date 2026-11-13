from backend.api.chat import bp as chat_bp
from backend.api.authentication import bp as auth_bp
from backend.api.inventory import bp as inventory_bp
from backend.api.vision import bp as vision_bp
from backend.api.voice import bp as voice_bp
from backend.api.faculty import bp as faculty_bp

def register_blueprints(app):
    for b in (chat_bp, auth_bp, inventory_bp, vision_bp, voice_bp, faculty_bp):
        app.register_blueprint(b)
