from flask import Flask, render_template, send_from_directory
from backend.config import Config
from backend.extensions import init_extensions
from backend.core.logging import setup_logging
from backend.core.middleware import init_middleware
from backend.api import register_blueprints

ROOT = Config.STORAGE.parent

def create_app():
    app = Flask(__name__, template_folder=str(ROOT / "frontend" / "templates"),
                static_folder=str(ROOT / "frontend" / "static"))
    app.config.from_object(Config)
    setup_logging(); init_extensions(app); init_middleware(app); register_blueprints(app)

    def page(t, active=None, nav=True): return render_template(t, active=active, show_nav=nav)

    app.add_url_rule("/", "index", lambda: page("index.html", nav=False))
    app.add_url_rule("/login", "login_page", lambda: page("login.html", nav=False))
    app.add_url_rule("/signup", "signup_page", lambda: page("signup.html", nav=False))
    app.add_url_rule("/dashboard", "dashboard", lambda: page("dashboard.html", "dashboard"))
    app.add_url_rule("/chat", "chat_page", lambda: page("chat.html", "chat"))
    app.add_url_rule("/inventory", "inventory_page", lambda: page("inventory.html", "inventory"))
    app.add_url_rule("/faculty", "faculty_page", lambda: page("faculty_dashboard.html", "faculty"))
    app.add_url_rule("/media/<path:name>", "media", lambda name: send_from_directory(Config.DETECTIONS, name))

    @app.errorhandler(404)
    def nf(_): return render_template("error.html", code=404, message="Page not found"), 404
    return app

app = create_app() if __name__ == "__main__" else None
