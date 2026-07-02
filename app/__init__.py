import os

from flask import Flask
from app.extensions import db, migrate

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


def create_app(config_object: str = "config.DevelopmentConfig") -> Flask:
    if load_dotenv:
        load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    try:
        app.config.from_pyfile("config.py", silent=True)
    except OSError:
        pass

    # Ensure upload folder exists
    os.makedirs(app.config.get("UPLOAD_FOLDER", "instance/uploads"), exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    from app.extensions import limiter
    limiter.init_app(app)

    # Ensure models are imported so metadata is registered.
    from app import models  # noqa: F401
    from app.cli import register_commands
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.main import main_bp
    from app.routes.approval import approval_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(approval_bp)
    register_commands(app)

    return app
