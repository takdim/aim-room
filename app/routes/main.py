from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import and_

from app.extensions import db
from app.models.class_schedule import ClassSchedule
from app.models.lecturer import Lecturer
from app.models.reference import Building, Course
from app.models.semester import Semester
from app.models.room import Room
from app.models.room_booking import RoomBooking

main_bp = Blueprint("main", __name__)


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
        db.session.query(ClassSchedule, Course, Lecturer, Room)
        .join(Course, ClassSchedule.course_id == Course.id)
        .join(Lecturer, ClassSchedule.lecturer_id == Lecturer.id)
        .join(Room, ClassSchedule.room_id == Room.id)
        .filter(ClassSchedule.day_name == selected_day)
    )
    if active_semester:
        schedule_query = schedule_query.filter(ClassSchedule.semester_id == active_semester.id)

    schedule_rows = schedule_query.all()

    has_schedule_by_room = {room.id: True for _, _, _, room in schedule_rows}

    current_by_room = {}
    if show_live:
        for sched, course, lecturer, room in schedule_rows:
            if sched.start_time and sched.end_time and sched.start_time <= now_time < sched.end_time:
                if room.id not in current_by_room:
                    current_by_room[room.id] = {
                        "time_range": f"{sched.start_time.strftime('%H:%M')} - {sched.end_time.strftime('%H:%M')}",
                        "course_name": course.course_name,
                        "lecturer_name": lecturer.lecturer_name,
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
        db.session.query(ClassSchedule, Lecturer, Course)
        .join(Lecturer, ClassSchedule.lecturer_id == Lecturer.id)
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
    room = Room.query.get_or_404(room_id)
    building_name = None
    if room.building_id:
        building = Building.query.get(int(room.building_id))
        if building:
            building_name = building.building_name

    if request.method == "POST":
        borrower_name = request.form.get("borrower_name", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        borrower_email = request.form.get("borrower_email", "").strip()
        organization = request.form.get("organization", "").strip()
        purpose = request.form.get("purpose", "").strip()
        booking_date = request.form.get("booking_date", "").strip()
        start_time = request.form.get("start_time", "").strip()
        end_time = request.form.get("end_time", "").strip()
        notes = request.form.get("notes", "").strip()

        if not (borrower_name and phone_number and organization and purpose and booking_date and start_time and end_time):
            return render_template(
                "main/booking_form.html",
                room=room,
                building_name=building_name,
                last_booking=_get_last_booking(room_id),
                error="Semua field wajib diisi.",
            )

        parsed_date = _parse_date(booking_date)
        parsed_start = _parse_time(start_time)
        parsed_end = _parse_time(end_time)
        if not (parsed_date and parsed_start and parsed_end):
            return render_template(
                "main/booking_form.html",
                room=room,
                building_name=building_name,
                last_booking=_get_last_booking(room_id),
                error="Format tanggal atau waktu tidak valid.",
            )

        booking = RoomBooking(
            room_id=room.id,
            borrower_name=borrower_name,
            phone_number=phone_number,
            borrower_email=borrower_email or None,
            organization=organization,
            purpose=purpose,
            booking_date=parsed_date,
            start_time=parsed_start,
            end_time=parsed_end,
            notes=notes or None,
            status="Menunggu",
        )
        db.session.add(booking)
        db.session.commit()
        flash("Permintaan berhasil dikirim, silahkan tunggu kabar via email, WA.", "info")
        return redirect(url_for("main.index"))

    return render_template(
        "main/booking_form.html",
        room=room,
        building_name=building_name,
        last_booking=_get_last_booking(room_id),
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
    return render_template(
        "main/booking_index.html",
        rooms=rooms,
        building_map=building_map,
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
