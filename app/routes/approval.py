import os

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from sqlalchemy import or_, and_

from app.extensions import db
from app.models.room_booking import RoomBooking
from app.models.user import ROLE_STATUS_MAP, NEXT_STATUS_MAP
from app.routes.auth import login_required, role_required

# Statuses that come AFTER each role's approval (used for history)
_HISTORY_STATUSES = {
    "kasubag": ["Menunggu KTU", "Menunggu WD2", "Menunggu Dekan", "Disetujui"],
    "ktu":     ["Menunggu WD2", "Menunggu Dekan", "Disetujui"],
    "wd2":     ["Menunggu Dekan", "Disetujui"],
    "dekan":   ["Disetujui"],
}

approval_bp = Blueprint("approval", __name__, url_prefix="/approval")

_APPROVAL_ROLES = ("kasubag", "ktu", "wd2", "dekan")


@approval_bp.get("/")
@login_required
@role_required(*_APPROVAL_ROLES)
def approval_home():
    role = session.get("role")
    my_status = ROLE_STATUS_MAP.get(role)
    bookings = (
        RoomBooking.query.filter_by(status=my_status)
        .order_by(RoomBooking.booking_date.asc())
        .all()
    )

    # History: bookings approved by this role (moved to later stage) OR rejected by this role
    later_statuses = _HISTORY_STATUSES.get(role, [])
    history = (
        RoomBooking.query.filter(
            or_(
                RoomBooking.status.in_(later_statuses),
                and_(RoomBooking.status == "Ditolak", RoomBooking.rejected_by == role),
            )
        )
        .order_by(RoomBooking.booking_date.desc())
        .all()
    )

    return render_template(
        "approval/home.html",
        bookings=bookings,
        history=history,
        role=role,
        my_status=my_status,
        full_name=session.get("full_name"),
    )


@approval_bp.get("/detail/<int:booking_id>")
@login_required
@role_required(*_APPROVAL_ROLES)
def approval_detail(booking_id: int):
    role = session.get("role")
    booking = RoomBooking.query.get_or_404(booking_id)
    return render_template(
        "approval/detail.html",
        booking=booking,
        role=role,
        full_name=session.get("full_name"),
    )


@approval_bp.post("/action/<int:booking_id>")
@login_required
@role_required(*_APPROVAL_ROLES)
def approval_action(booking_id: int):
    role = session.get("role")
    booking = RoomBooking.query.get_or_404(booking_id)
    expected_status = ROLE_STATUS_MAP.get(role)

    if booking.status != expected_status:
        flash("Peminjaman ini bukan di tahap Anda.", "error")
        return redirect(url_for("approval.approval_home"))

    action = request.form.get("action")
    if action == "approve":
        booking.status = NEXT_STATUS_MAP.get(role, "Disetujui")
        flash("Peminjaman berhasil disetujui.", "info")
    elif action == "reject":
        booking.status = "Ditolak"
        booking.rejection_note = request.form.get("rejection_note", "").strip() or None
        booking.rejected_by = role
        flash("Peminjaman ditolak.", "info")
    else:
        abort(400)

    db.session.commit()
    return redirect(url_for("approval.approval_home"))


@approval_bp.get("/file/<int:booking_id>/<field>")
@login_required
@role_required(*_APPROVAL_ROLES, "staff", "admin")
def serve_file(booking_id: int, field: str):
    """Serve uploaded booking files to authorised users."""
    if field not in ("pakta_integritas_path", "surat_permohonan_path"):
        abort(404)
    booking = RoomBooking.query.get_or_404(booking_id)
    file_path = getattr(booking, field, None)
    if not file_path:
        abort(404)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, file_path, as_attachment=False)
