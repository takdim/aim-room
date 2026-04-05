from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models.user import User
from app.extensions import limiter

auth_bp = Blueprint("auth", __name__)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Silakan login terlebih dahulu.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get("role") not in roles:
                flash("Anda tidak punya akses ke halaman tersebut.", "error")
                return redirect(url_for("main.index"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5/minute")
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Email atau password salah.", "error")
            return render_template("auth/login.html"), 401

        session["user_id"] = user.id
        session["role"] = user.role
        session["full_name"] = user.full_name

        if user.role == "admin":
            return redirect(url_for("dashboard.admin_home"))
        return redirect(url_for("dashboard.staff_home"))

    return render_template("auth/login.html")


@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Anda sudah logout.", "info")
    return redirect(url_for("auth.login"))
