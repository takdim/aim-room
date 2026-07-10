import os

from flask import Flask, render_template
from app.extensions import db, migrate, csrf

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
    csrf.init_app(app)
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

    # ── Error handlers ──────────────────────────────────────────
    @app.errorhandler(400)
    def bad_request(e):
        return render_template(
            "errors/error.html",
            error_code="400",
            error_icon="warning",
            error_title="Permintaan Tidak Valid",
            error_description="Server tidak dapat memproses permintaan karena data yang dikirimkan tidak valid. Periksa kembali inputan Anda.",
        ), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template(
            "errors/error.html",
            error_code="403",
            error_icon="lock",
            error_title="Akses Ditolak",
            error_description="Anda tidak memiliki izin untuk mengakses halaman ini. Silakan hubungi administrator jika Anda merasa ini adalah kesalahan.",
        ), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template(
            "errors/error.html",
            error_code="404",
            error_icon="search_off",
            error_title="Halaman Tidak Ditemukan",
            error_description="Halaman yang Anda cari tidak tersedia atau telah dipindahkan. Periksa kembali alamat URL yang Anda masukkan.",
        ), 404

    @app.errorhandler(429)
    def too_many_requests(e):
        return render_template(
            "errors/error.html",
            error_code="429",
            error_icon="timer_off",
            error_title="Terlalu Banyak Permintaan",
            error_description="Anda telah mengirimkan terlalu banyak permintaan dalam waktu singkat. Harap tunggu beberapa saat sebelum mencoba kembali.",
        ), 429

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template(
            "errors/error.html",
            error_code="500",
            error_icon="error",
            error_title="Kesalahan Server",
            error_description="Terjadi kesalahan pada server kami. Tim teknis telah diberitahu. Silakan coba lagi beberapa saat.",
        ), 500

    @app.errorhandler(503)
    def service_unavailable(e):
        return render_template(
            "errors/error.html",
            error_code="503",
            error_icon="cloud_off",
            error_title="Layanan Tidak Tersedia",
            error_description="Server sedang dalam pemeliharaan atau kelebihan beban. Silakan coba beberapa saat lagi.",
        ), 503
    # ─────────────────────────────────────────────────────────────

    return app
