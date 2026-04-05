from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.reference import Building, Course
from app.models.class_schedule import ClassSchedule
from app.models.lecturer import Lecturer
from app.models.room import Room
from app.models.room_booking import RoomBooking
from app.models.user import User
from app.models.semester import Semester
from app.routes.auth import login_required, role_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


def _get_active_semester():
    """Get semester from session, fallback to is_active=True for schedules."""
    semester_id = session.get("active_semester_id")
    if semester_id:
        semester = Semester.query.get(int(semester_id))
        if semester:
            return semester
    return Semester.query.filter_by(is_active=True).order_by(Semester.id.desc()).first()


def _get_selected_semester():
    """Get semester from session only. Return None if not selected."""
    semester_id = session.get("active_semester_id")
    if semester_id:
        semester = Semester.query.get(int(semester_id))
        if semester:
            return semester
    return None


@dashboard_bp.route("/admin", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_home():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not full_name or not email or not password:
            flash("Nama, email, dan password wajib diisi.", "error")
            return redirect(url_for("dashboard.admin_home"))

        if password != confirm_password:
            flash("Konfirmasi password tidak cocok.", "error")
            return redirect(url_for("dashboard.admin_home"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email sudah digunakan.", "error")
            return redirect(url_for("dashboard.admin_home"))

        staff_user = User(full_name=full_name, email=email, role="staff")
        staff_user.set_password(password)
        db.session.add(staff_user)
        db.session.commit()
        flash("Akun staff berhasil dibuat.", "info")
        return redirect(url_for("dashboard.admin_home"))

    staff_users = User.query.filter_by(role="staff").order_by(User.id.desc()).all()
    total_users = User.query.count()
    admin_count = User.query.filter_by(role="admin").count()
    return render_template(
        "dashboard/admin.html",
        full_name=session.get("full_name"),
        staff_users=staff_users,
        total_users=total_users,
        staff_count=len(staff_users),
        admin_count=admin_count,
    )


@dashboard_bp.get("/staff")
@login_required
@role_required("staff")
def staff_home():
    semesters = Semester.query.order_by(Semester.id.desc()).all()
    active_semester = _get_active_semester()
    
    # Filter stats berdasarkan semester yang dipilih
    if active_semester:
        # Courses yang ada di schedule semester ini
        total_courses = db.session.query(ClassSchedule.course_id).filter(
            ClassSchedule.semester_id == active_semester.id
        ).distinct().count()
        
        # Lecturers yang mengajar di semester ini
        total_lecturers = db.session.query(ClassSchedule.lecturer_id).filter(
            ClassSchedule.semester_id == active_semester.id
        ).distinct().count()
        
        # Rooms yang digunakan di semester ini
        total_rooms = db.session.query(ClassSchedule.room_id).filter(
            ClassSchedule.semester_id == active_semester.id
        ).distinct().count()
    else:
        # Jika tidak ada semester yang dipilih, tampilkan 0
        total_courses = 0
        total_lecturers = 0
        total_rooms = 0
    
    return render_template(
        "dashboard/staff.html",
        full_name=session.get("full_name"),
        total_courses=total_courses,
        total_lecturers=total_lecturers,
        total_rooms=total_rooms,
        semesters=semesters,
        active_semester=active_semester,
    )


@dashboard_bp.route("/staff/courses", methods=["GET", "POST"])
@login_required
@role_required("staff")
def staff_courses():
    if request.method == "POST":
        action = request.form.get("action", "add")
        course_id = request.form.get("course_id", "").strip()
        course_name = request.form.get("course_name", "").strip()
        course_code = request.form.get("course_code", "").strip().upper()

        if action == "delete":
            if course_id:
                Course.query.filter_by(id=int(course_id)).delete()
                db.session.commit()
                flash("Kelas berhasil dihapus.", "info")
            return redirect(url_for("dashboard.staff_courses"))

        if not course_name:
            flash("Nama kelas wajib diisi.", "error")
            return redirect(url_for("dashboard.staff_courses"))

        if action == "update":
            course = Course.query.get(int(course_id)) if course_id else None
            if not course:
                flash("Kelas tidak ditemukan.", "error")
                return redirect(url_for("dashboard.staff_courses"))
            if course_code and Course.query.filter(Course.course_code == course_code, Course.id != course.id).first():
                flash("Kode kelas sudah digunakan.", "error")
                return redirect(url_for("dashboard.staff_courses"))
            course.course_name = course_name
            course.course_code = course_code or None
            db.session.commit()
            flash("Kelas berhasil diperbarui.", "info")
            return redirect(url_for("dashboard.staff_courses"))

        if course_code and Course.query.filter_by(course_code=course_code).first():
            flash("Kode kelas sudah digunakan.", "error")
            return redirect(url_for("dashboard.staff_courses"))
        db.session.add(Course(course_name=course_name, course_code=course_code or None))
        db.session.commit()
        flash("Kelas berhasil ditambahkan.", "info")
        return redirect(url_for("dashboard.staff_courses"))

    q = request.args.get("q", "").strip()
    active_semester = _get_active_semester()
    
    # Tampilkan SEMUA courses tanpa filter semester
    query = Course.query
    if q:
        query = query.filter(
            or_(
                Course.course_name.ilike(f"%{q}%"),
                Course.course_code.ilike(f"%{q}%"),
            )
        )
    courses = query.order_by(Course.id.desc()).limit(50).all()
    return render_template(
        "dashboard/staff_courses.html",
        full_name=session.get("full_name"),
        courses=courses,
        q=q,
        active_semester=active_semester,
    )


@dashboard_bp.route("/staff/lecturers", methods=["GET", "POST"])
@login_required
@role_required("staff")
def staff_lecturers():
    if request.method == "POST":
        action = request.form.get("action", "add")
        lecturer_id = request.form.get("lecturer_id", "").strip()
        lecturer_name = request.form.get("lecturer_name", "").strip()
        nidn = request.form.get("nidn", "").strip()

        if action == "delete":
            if lecturer_id:
                Lecturer.query.filter_by(id=int(lecturer_id)).delete()
                db.session.commit()
                flash("Pengajar berhasil dihapus.", "info")
            return redirect(url_for("dashboard.staff_lecturers"))

        if not lecturer_name:
            flash("Nama pengajar wajib diisi.", "error")
            return redirect(url_for("dashboard.staff_lecturers"))

        if action == "update":
            lecturer = Lecturer.query.get(int(lecturer_id)) if lecturer_id else None
            if not lecturer:
                flash("Pengajar tidak ditemukan.", "error")
                return redirect(url_for("dashboard.staff_lecturers"))
            lecturer.lecturer_name = lecturer_name
            lecturer.nidn = nidn or None
            db.session.commit()
            flash("Pengajar berhasil diperbarui.", "info")
            return redirect(url_for("dashboard.staff_lecturers"))

        db.session.add(Lecturer(lecturer_name=lecturer_name, nidn=nidn or None))
        db.session.commit()
        flash("Pengajar berhasil ditambahkan.", "info")
        return redirect(url_for("dashboard.staff_lecturers"))

    q = request.args.get("q", "").strip()
    active_semester = _get_active_semester()
    
    # Tampilkan SEMUA lecturers tanpa filter semester
    query = Lecturer.query
    if q:
        query = query.filter(
            or_(
                Lecturer.lecturer_name.ilike(f"%{q}%"),
                Lecturer.nidn.ilike(f"%{q}%"),
            )
        )
    lecturers = query.order_by(Lecturer.id.desc()).limit(50).all()
    return render_template(
        "dashboard/staff_lecturers.html",
        full_name=session.get("full_name"),
        lecturers=lecturers,
        q=q,
        active_semester=active_semester,
    )


@dashboard_bp.route("/staff/rooms", methods=["GET", "POST"])
@login_required
@role_required("staff")
def staff_rooms():
    if request.method == "POST":
        action = request.form.get("action", "add")
        room_id = request.form.get("room_id", "").strip()
        room_code = request.form.get("room_code", "").strip()
        room_name = request.form.get("room_name", "").strip()
        building_id = request.form.get("building_id", "").strip()
        floor = request.form.get("floor", "").strip()
        capacity = request.form.get("capacity", "").strip()
        room_type = request.form.get("room_type", "").strip()

        if action == "delete":
            if room_id:
                Room.query.filter_by(id=int(room_id)).delete()
                db.session.commit()
                flash("Ruangan berhasil dihapus.", "info")
            return redirect(url_for("dashboard.staff_rooms"))

        if not room_name:
            flash("Nama ruangan wajib diisi.", "error")
            return redirect(url_for("dashboard.staff_rooms"))

        building_id_value = int(building_id) if building_id else None
        if building_id_value and not Building.query.get(building_id_value):
            flash("ID gedung tidak ditemukan, nilai dikosongkan.", "error")
            building_id_value = None

        if action == "update":
            room = Room.query.get(int(room_id)) if room_id else None
            if not room:
                flash("Ruangan tidak ditemukan.", "error")
                return redirect(url_for("dashboard.staff_rooms"))
            room.room_code = room_code or None
            room.room_name = room_name
            room.building_id = building_id_value
            room.floor = int(floor) if floor else None
            room.capacity = int(capacity) if capacity else None
            room.room_type = room_type or None
            db.session.commit()
            flash("Ruangan berhasil diperbarui.", "info")
            return redirect(url_for("dashboard.staff_rooms"))

        room = Room(
            room_code=room_code or None,
            room_name=room_name,
            building_id=building_id_value,
            floor=int(floor) if floor else None,
            capacity=int(capacity) if capacity else None,
            room_type=room_type or None,
        )
        db.session.add(room)
        db.session.commit()
        flash("Ruangan berhasil ditambahkan.", "info")
        return redirect(url_for("dashboard.staff_rooms"))

    q = request.args.get("q", "").strip()
    active_semester = _get_active_semester()
    
    # Tampilkan SEMUA rooms tanpa filter semester
    query = Room.query
    if q:
        query = query.filter(
            or_(
                Room.room_name.ilike(f"%{q}%"),
                Room.room_code.ilike(f"%{q}%"),
                Room.room_type.ilike(f"%{q}%"),
            )
        )
    rooms = query.order_by(Room.id.desc()).limit(50).all()
    buildings = Building.query.order_by(Building.id.asc()).all()
    return render_template(
        "dashboard/staff_rooms.html",
        full_name=session.get("full_name"),
        rooms=rooms,
        buildings=buildings,
        q=q,
        active_semester=active_semester,
    )


@dashboard_bp.route("/staff/buildings", methods=["GET", "POST"])
@login_required
@role_required("staff")
def staff_buildings():
    if request.method == "POST":
        action = request.form.get("action", "add")
        building_id = request.form.get("building_id", "").strip()
        building_id_input = request.form.get("building_id_input", "").strip()
        building_name = request.form.get("building_name", "").strip()

        if action == "delete":
            if building_id:
                Building.query.filter_by(id=int(building_id)).delete()
                db.session.commit()
                flash("Gedung berhasil dihapus.", "info")
            return redirect(url_for("dashboard.staff_buildings"))

        if not building_name:
            flash("Nama gedung wajib diisi.", "error")
            return redirect(url_for("dashboard.staff_buildings"))

        if action == "update":
            building = Building.query.get(int(building_id)) if building_id else None
            if not building:
                flash("Gedung tidak ditemukan.", "error")
                return redirect(url_for("dashboard.staff_buildings"))
            building.building_name = building_name
            db.session.commit()
            flash("Gedung berhasil diperbarui.", "info")
            return redirect(url_for("dashboard.staff_buildings"))

        building = Building(building_name=building_name)
        if building_id_input:
            building.id = int(building_id_input)
        db.session.add(building)
        try:
            db.session.commit()
            flash("Gedung berhasil ditambahkan.", "info")
        except IntegrityError:
            db.session.rollback()
            flash("ID gedung sudah digunakan.", "error")
        return redirect(url_for("dashboard.staff_buildings"))

    buildings = Building.query.order_by(Building.id.desc()).limit(50).all()
    return render_template(
        "dashboard/staff_buildings.html",
        full_name=session.get("full_name"),
        buildings=buildings,
        active_semester=_get_active_semester(),
    )


@dashboard_bp.route("/staff/bookings", methods=["GET", "POST"])
@login_required
@role_required("staff")
def staff_bookings():
    if request.method == "POST":
        action = request.form.get("action", "")
        booking_id = request.form.get("booking_id", "").strip()
        booking = RoomBooking.query.get(int(booking_id)) if booking_id else None

        if action == "delete" and booking:
            db.session.delete(booking)
            db.session.commit()
            flash("Peminjaman berhasil dihapus.", "info")
            return redirect(url_for("dashboard.staff_bookings"))

        if action == "approve" and booking:
            booking.status = "Disetujui"
            db.session.commit()
            flash("Peminjaman disetujui.", "info")
            return redirect(url_for("dashboard.staff_bookings"))

        if action == "reject" and booking:
            booking.status = "Ditolak"
            db.session.commit()
            flash("Peminjaman ditolak.", "info")
            return redirect(url_for("dashboard.staff_bookings"))

    booking_rows = (
        db.session.query(RoomBooking, Room)
        .join(Room, RoomBooking.room_id == Room.id)
        .order_by(RoomBooking.booking_date.desc(), RoomBooking.start_time.desc(), RoomBooking.id.desc())
        .limit(100)
        .all()
    )
    
    active_semester = _get_active_semester()
    return render_template(
        "dashboard/staff_bookings.html",
        full_name=session.get("full_name"),
        booking_rows=booking_rows,
        active_semester=active_semester,
    )


@dashboard_bp.route("/staff/schedules", methods=["GET", "POST"])
@login_required
@role_required("staff")
def staff_schedules():
    if request.method == "POST":
        action = request.form.get("action", "add")
        schedule_id = request.form.get("schedule_id", "").strip()
        course_id = request.form.get("course_id", "").strip()
        lecturer_id = request.form.get("lecturer_id", "").strip()
        room_id = request.form.get("room_id", "").strip()
        day_name = request.form.get("day_name", "").strip()
        start_time = request.form.get("start_time", "").strip()
        end_time = request.form.get("end_time", "").strip()
        semester_id = request.form.get("semester_id", "").strip()

        if action == "delete":
            if schedule_id:
                ClassSchedule.query.filter_by(id=int(schedule_id)).delete()
                db.session.commit()
                flash("Jadwal berhasil dihapus.", "info")
            return redirect(url_for("dashboard.staff_schedules"))

        if not (course_id and lecturer_id and room_id and day_name and start_time and end_time and semester_id):
            flash("Semua field jadwal wajib diisi.", "error")
            return redirect(url_for("dashboard.staff_schedules"))

        if action == "update":
            schedule = ClassSchedule.query.get(int(schedule_id)) if schedule_id else None
            if not schedule:
                flash("Jadwal tidak ditemukan.", "error")
                return redirect(url_for("dashboard.staff_schedules"))
            schedule.course_id = int(course_id)
            schedule.lecturer_id = int(lecturer_id)
            schedule.room_id = int(room_id)
            schedule.day_name = day_name
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.semester_id = int(semester_id)
            db.session.commit()
            flash("Jadwal berhasil diperbarui.", "info")
            return redirect(url_for("dashboard.staff_schedules"))

        schedule = ClassSchedule(
            course_id=int(course_id),
            lecturer_id=int(lecturer_id),
            room_id=int(room_id),
            day_name=day_name,
            start_time=start_time,
            end_time=end_time,
            semester_id=int(semester_id),
        )
        db.session.add(schedule)
        db.session.commit()
        flash("Jadwal berhasil ditambahkan.", "info")
        return redirect(url_for("dashboard.staff_schedules"))

    q = request.args.get("q", "").strip()
    active_semester = _get_active_semester()
    query = (
        db.session.query(ClassSchedule, Course, Lecturer, Room)
        .join(Course, ClassSchedule.course_id == Course.id)
        .join(Lecturer, ClassSchedule.lecturer_id == Lecturer.id)
        .join(Room, ClassSchedule.room_id == Room.id)
    )
    if active_semester:
        query = query.filter(ClassSchedule.semester_id == active_semester.id)
    else:
        # Jika tidak ada semester yang dipilih, tidak tampilkan jadwal apapun
        query = query.filter(False)
    
    if q:
        query = query.filter(
            or_(
                Course.course_name.ilike(f"%{q}%"),
                Course.course_code.ilike(f"%{q}%"),
                Lecturer.lecturer_name.ilike(f"%{q}%"),
                Room.room_name.ilike(f"%{q}%"),
                ClassSchedule.day_name.ilike(f"%{q}%"),
            )
        )
    schedules = query.order_by(ClassSchedule.day_name.asc(), ClassSchedule.start_time.asc()).limit(50).all()

    courses = Course.query.order_by(Course.course_name.asc()).all()
    lecturers = Lecturer.query.order_by(Lecturer.lecturer_name.asc()).all()
    rooms = Room.query.order_by(Room.room_name.asc()).all()
    semesters = Semester.query.order_by(Semester.id.desc()).all()

    return render_template(
        "dashboard/staff_schedules.html",
        full_name=session.get("full_name"),
        schedules=schedules,
        courses=courses,
        lecturers=lecturers,
        rooms=rooms,
        semesters=semesters,
        q=q,
        active_semester=active_semester,
    )


@dashboard_bp.route("/staff/semesters", methods=["GET", "POST"])
@login_required
@role_required("staff")
def staff_semesters():
    if request.method == "POST":
        action = request.form.get("action", "add")
        semester_id = request.form.get("semester_id", "").strip()
        name = request.form.get("name", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        is_active = request.form.get("is_active") == "on"

        if action == "delete":
            if semester_id:
                Semester.query.filter_by(id=int(semester_id)).delete()
                db.session.commit()
                flash("Semester berhasil dihapus.", "info")
            return redirect(url_for("dashboard.staff_semesters"))

        if not name:
            flash("Nama semester wajib diisi.", "error")
            return redirect(url_for("dashboard.staff_semesters"))

        if action == "update":
            semester = Semester.query.get(int(semester_id)) if semester_id else None
            if not semester:
                flash("Semester tidak ditemukan.", "error")
                return redirect(url_for("dashboard.staff_semesters"))
            if is_active:
                Semester.query.update({Semester.is_active: False})
            semester.name = name
            semester.start_date = start_date or None
            semester.end_date = end_date or None
            semester.is_active = is_active
            db.session.commit()
            flash("Semester berhasil diperbarui.", "info")
            return redirect(url_for("dashboard.staff_semesters"))

        if is_active:
            Semester.query.update({Semester.is_active: False})

        semester = Semester(
            name=name,
            start_date=start_date or None,
            end_date=end_date or None,
            is_active=is_active,
        )
        db.session.add(semester)
        db.session.commit()
        flash("Semester berhasil ditambahkan.", "info")
        return redirect(url_for("dashboard.staff_semesters"))

    q = request.args.get("q", "").strip()
    query = Semester.query
    if q:
        query = query.filter(Semester.name.ilike(f"%{q}%"))
    semesters = query.order_by(Semester.id.desc()).limit(50).all()

    return render_template(
        "dashboard/staff_semesters.html",
        full_name=session.get("full_name"),
        semesters=semesters,
        q=q,
        active_semester=_get_active_semester(),
    )




@dashboard_bp.post("/staff/semester/select")
@login_required
@role_required("staff")
def staff_select_semester():
    semester_id = request.form.get("semester_id", "").strip()
    if semester_id:
        session["active_semester_id"] = int(semester_id)
    else:
        session.pop("active_semester_id", None)
    return redirect(request.referrer or url_for("dashboard.staff_home"))
