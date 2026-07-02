import io
import os
import datetime as dt
from datetime import datetime

import qrcode
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    session,
    url_for,
)
from sqlalchemy import and_
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.class_schedule import ClassSchedule
from app.models.holiday import Holiday
from app.models.lecturer import Lecturer
from app.models.pakta_template import PaktaTemplate
from app.models.reference import Building, Course
from app.models.semester import Semester
from app.models.room import Room
from app.models.room_booking import RoomBooking

main_bp = Blueprint("main", __name__)

# Time slots for event booking: 08:00 – 16:00, hourly
EVENT_TIME_SLOTS = [
    ("08:00", "09:00"),
    ("09:00", "10:00"),
    ("10:00", "11:00"),
    ("11:00", "12:00"),
    ("12:00", "13:00"),
    ("13:00", "14:00"),
    ("14:00", "15:00"),
    ("15:00", "16:00"),
]


def _allowed_file(filename: str) -> bool:
    allowed = current_app.config.get("ALLOWED_EXTENSIONS", {"pdf", "jpg", "jpeg", "png"})
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def _save_upload(file, subfolder: str) -> str | None:
    """Save uploaded file, return relative path or None."""
    if not file or not file.filename:
        return None
    if not _allowed_file(file.filename):
        return None
    upload_root = current_app.config["UPLOAD_FOLDER"]
    dest_dir = os.path.join(upload_root, subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    filename = secure_filename(file.filename)
    unique_name = f"{int(datetime.utcnow().timestamp())}_{filename}"
    file.save(os.path.join(dest_dir, unique_name))
    return os.path.join(subfolder, unique_name)


@main_bp.get("/")
def index():
    day_map = {
        0: "Senin",
        1: "Selasa",
        2: "Rabu",
        3: "Kamis",
        4: "Jumat",
        5: "Sabtu",
        6: "Minggu",
    }
    today_name = day_map[datetime.now().weekday()]
    selected_day = request.args.get("day", today_name)
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    active_semester = Semester.query.filter_by(is_active=True).order_by(Semester.id.desc()).first()
    now_time = datetime.now().time()
    show_live = selected_day == today_name

    rooms = (
        Room.query.filter(Room.room_type == "Ruang Kelas")
        .order_by(Room.room_name.asc())
        .all()
    )

    schedule_query = (
        db.session.query(ClassSchedule, Course, Room)
        .join(Course, ClassSchedule.course_id == Course.id)
        .join(Room, ClassSchedule.room_id == Room.id)
        .filter(ClassSchedule.day_name == selected_day)
    )
    if active_semester:
        schedule_query = schedule_query.filter(ClassSchedule.semester_id == active_semester.id)

    schedule_rows = schedule_query.all()

    has_schedule_by_room = {room.id: True for _, _, room in schedule_rows}

    current_by_room = {}
    if show_live:
        for sched, course, room in schedule_rows:
            if sched.start_time and sched.end_time and sched.start_time <= now_time < sched.end_time:
                if room.id not in current_by_room:
                    lecturer_names = ", ".join(l.lecturer_name for l in sched.lecturers) if sched.lecturers else "-"
                    current_by_room[room.id] = {
                        "time_range": f"{sched.start_time.strftime('%H:%M')} - {sched.end_time.strftime('%H:%M')}",
                        "course_name": course.course_name,
                        "lecturer_name": lecturer_names,
                    }

    return render_template(
        "main/index.html",
        rooms=rooms,
        days=days,
        selected_day=selected_day,
        show_live=show_live,
        now_time=now_time.strftime("%H:%M"),
        current_by_room=current_by_room,
        has_schedule_by_room=has_schedule_by_room,
    )


@main_bp.get("/ruangan/<int:room_id>")
def room_schedule(room_id: int):
    room = Room.query.get_or_404(room_id)
    building_name = None
    if room.building_id:
        building = Building.query.get(int(room.building_id))
        if building:
            building_name = building.building_name

    day_map = {
        0: "Senin",
        1: "Selasa",
        2: "Rabu",
        3: "Kamis",
        4: "Jumat",
        5: "Sabtu",
        6: "Minggu",
    }
    today_name = day_map[datetime.now().weekday()]

    active_semester = Semester.query.filter_by(is_active=True).order_by(Semester.id.desc()).first()

    selected_day = request.args.get("day", today_name)
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

    schedule_rows = (
        db.session.query(ClassSchedule, Course)
        .join(Course, ClassSchedule.course_id == Course.id)
        .filter(
            and_(
                ClassSchedule.room_id == room.id,
                ClassSchedule.day_name == selected_day,
            )
        )
        .order_by(ClassSchedule.start_time.asc())
        .all()
    )
    if active_semester:
        schedule_rows = [
            row for row in schedule_rows if row[0].semester_id == active_semester.id
        ]

    return render_template(
        "main/room_schedule.html",
        room=room,
        building_name=building_name,
        today_name=selected_day,
        days=days,
        selected_day=selected_day,
        schedule_rows=schedule_rows,
        active_semester=active_semester,
    )


@main_bp.route("/peminjaman/<int:room_id>", methods=["GET", "POST"])
def room_booking(room_id: int):
    """Unified booking form — semua peminjaman wajib pakta integritas & surat permohonan."""
    room = Room.query.get_or_404(room_id)
    building_name = None
    if room.building_id:
        building = Building.query.get(int(room.building_id))
        if building:
            building_name = building.building_name

    pakta_template = PaktaTemplate.query.order_by(PaktaTemplate.id.desc()).first()
    error = None

    if request.method == "POST":
        borrower_name    = request.form.get("borrower_name", "").strip()
        name_on_pakta    = request.form.get("name_on_pakta", "").strip()
        phone_number     = request.form.get("phone_number", "").strip()
        borrower_email   = request.form.get("borrower_email", "").strip()
        organization     = request.form.get("organization", "").strip()
        purpose          = request.form.get("purpose", "").strip()
        booking_date     = request.form.get("booking_date", "").strip()
        start_time       = request.form.get("start_time", "").strip()
        end_time         = request.form.get("end_time", "").strip()
        notes            = request.form.get("notes", "").strip()

        pakta_file = request.files.get("pakta_integritas")
        surat_file = request.files.get("surat_permohonan")

        parsed_date = parsed_start = parsed_end = None
        if not (borrower_name and name_on_pakta and phone_number and organization
                and purpose and booking_date and start_time and end_time):
            error = "Semua field wajib diisi."
        elif not (pakta_file and pakta_file.filename):
            error = "File pakta integritas wajib diunggah."
        elif not (surat_file and surat_file.filename):
            error = "Surat permohonan organisasi wajib diunggah."
        elif not _allowed_file(pakta_file.filename):
            error = "Format file pakta integritas tidak didukung (PDF, JPG, PNG)."
        elif not _allowed_file(surat_file.filename):
            error = "Format file surat permohonan tidak didukung (PDF, JPG, PNG)."
        else:
            parsed_date  = _parse_date(booking_date)
            parsed_start = _parse_time(start_time)
            parsed_end   = _parse_time(end_time)
            if not (parsed_date and parsed_start and parsed_end):
                error = "Format tanggal atau waktu tidak valid."

        if not error:
            pakta_path = _save_upload(pakta_file, "pakta")
            surat_path = _save_upload(surat_file, "surat")
            booking = RoomBooking(
                room_id=room.id,
                booking_type="event",
                borrower_name=borrower_name,
                name_on_pakta=name_on_pakta,
                phone_number=phone_number,
                borrower_email=borrower_email or None,
                organization=organization,
                purpose=purpose,
                booking_date=parsed_date,
                start_time=parsed_start,
                end_time=parsed_end,
                notes=notes or None,
                pakta_integritas_path=pakta_path,
                surat_permohonan_path=surat_path,
                submission_date=dt.date.today(),
                status="Menunggu Staff",
            )
            db.session.add(booking)
            db.session.commit()
            flash(
                "Pengajuan berhasil dikirim! Staff akan memeriksa dokumen Anda. "
                "Tunggu konfirmasi via email atau WhatsApp.",
                "info",
            )
            return redirect(url_for("main.booking_index"))

    return render_template(
        "main/booking_form.html",
        room=room,
        building_name=building_name,
        last_booking=_get_last_booking(room_id),
        pakta_template=pakta_template,
        time_slots=EVENT_TIME_SLOTS,
        error=error,
    )


@main_bp.get("/peminjaman")
def booking_index():
    rooms = (
        Room.query.filter(Room.room_type.in_(["Aula", "Ruang Senat"]))
        .order_by(Room.room_name.asc())
        .all()
    )
    building_map = {
        building.id: building.building_name
        for building in Building.query.order_by(Building.id.asc()).all()
    }
    pakta_template = PaktaTemplate.query.order_by(PaktaTemplate.id.desc()).first()
    return render_template(
        "main/booking_index.html",
        rooms=rooms,
        building_map=building_map,
        pakta_template=pakta_template,
    )


@main_bp.route("/peminjaman-event/<int:room_id>", methods=["GET", "POST"])
def event_booking(room_id: int):
    """Special event booking form with file uploads for big events & holidays."""
    room = Room.query.get_or_404(room_id)
    building_name = None
    if room.building_id:
        building = Building.query.get(int(room.building_id))
        if building:
            building_name = building.building_name

    pakta_template = PaktaTemplate.query.order_by(PaktaTemplate.id.desc()).first()
    error = None

    if request.method == "POST":
        borrower_name = request.form.get("borrower_name", "").strip()
        name_on_pakta = request.form.get("name_on_pakta", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        borrower_email = request.form.get("borrower_email", "").strip()
        organization = request.form.get("organization", "").strip()
        purpose = request.form.get("purpose", "").strip()
        booking_date = request.form.get("booking_date", "").strip()
        start_time = request.form.get("start_time", "").strip()
        end_time = request.form.get("end_time", "").strip()
        notes = request.form.get("notes", "").strip()

        pakta_file = request.files.get("pakta_integritas")
        surat_file = request.files.get("surat_permohonan")

        parsed_date = parsed_start = parsed_end = None
        if not (borrower_name and name_on_pakta and phone_number and organization
                and purpose and booking_date and start_time and end_time):
            error = "Semua field wajib diisi."
        elif not (pakta_file and pakta_file.filename):
            error = "File pakta integritas wajib diunggah."
        elif not (surat_file and surat_file.filename):
            error = "Surat permohonan organisasi wajib diunggah."
        elif not _allowed_file(pakta_file.filename):
            error = "Format file pakta integritas tidak didukung (PDF, JPG, PNG)."
        elif not _allowed_file(surat_file.filename):
            error = "Format file surat permohonan tidak didukung (PDF, JPG, PNG)."
        else:
            parsed_date = _parse_date(booking_date)
            parsed_start = _parse_time(start_time)
            parsed_end = _parse_time(end_time)
            if not (parsed_date and parsed_start and parsed_end):
                error = "Format tanggal atau waktu tidak valid."

        if not error:
            pakta_path = _save_upload(pakta_file, "pakta")
            surat_path = _save_upload(surat_file, "surat")
            booking = RoomBooking(
                room_id=room.id,
                booking_type="event",
                borrower_name=borrower_name,
                name_on_pakta=name_on_pakta,
                phone_number=phone_number,
                borrower_email=borrower_email or None,
                organization=organization,
                purpose=purpose,
                booking_date=parsed_date,
                start_time=parsed_start,
                end_time=parsed_end,
                notes=notes or None,
                pakta_integritas_path=pakta_path,
                surat_permohonan_path=surat_path,
                submission_date=dt.date.today(),
                status="Menunggu Staff",
            )
            db.session.add(booking)
            db.session.commit()
            flash(
                "Pengajuan event berhasil dikirim! Staff akan memeriksa dokumen Anda. "
                "Tunggu konfirmasi via email atau WhatsApp.",
                "info",
            )
            return redirect(url_for("main.booking_index"))

    return render_template(
        "main/event_booking_form.html",
        room=room,
        building_name=building_name,
        pakta_template=pakta_template,
        time_slots=EVENT_TIME_SLOTS,
        error=error,
    )


@main_bp.get("/daftar-peminjaman")
def public_booking_list():
    bookings = (
        RoomBooking.query
        .order_by(RoomBooking.booking_date.asc())
        .all()
    )
    return render_template("main/public_booking_list.html", bookings=bookings)


@main_bp.get("/pakta-template/download")
def download_pakta_template():
    template = PaktaTemplate.query.order_by(PaktaTemplate.id.desc()).first()
    if not template:
        flash("Template pakta integritas belum tersedia.", "error")
        return redirect(url_for("main.booking_index"))
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    dir_path = os.path.dirname(os.path.join(upload_folder, template.file_path))
    filename = os.path.basename(template.file_path)
    return send_from_directory(
        dir_path,
        filename,
        as_attachment=True,
        download_name=template.original_filename or filename,
    )


@main_bp.get("/qr/<int:room_id>")
def room_qr(room_id: int):
    """Return a PNG QR code image for the event booking form of this room."""
    Room.query.get_or_404(room_id)
    target_url = url_for("main.event_booking", room_id=room_id, _external=True)
    img = qrcode.make(target_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png", download_name=f"qr_room_{room_id}.png")


@main_bp.get("/qr-page/<int:room_id>")
def room_qr_page(room_id: int):
    """Display QR code on a printable page."""
    room = Room.query.get_or_404(room_id)
    qr_url = url_for("main.room_qr", room_id=room_id)
    booking_url = url_for("main.event_booking", room_id=room_id, _external=True)
    return render_template(
        "main/qr_page.html",
        room=room,
        qr_url=qr_url,
        booking_url=booking_url,
    )


def _get_last_booking(room_id: int):
    return (
        RoomBooking.query.filter_by(room_id=room_id)
        .order_by(RoomBooking.booking_date.desc(), RoomBooking.start_time.desc(), RoomBooking.id.desc())
        .first()
    )


def _parse_date(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _parse_time(value: str):
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError:
        return None
