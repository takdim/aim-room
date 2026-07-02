"""
Seed jadwal kelas ke Semester Ganjil 2025/2026.
Jalankan: python seed_schedules.py
"""
import datetime as dt
from app import create_app
from app.extensions import db
from app.models.class_schedule import ClassSchedule
from app.models.reference import Course
from app.models.room import Room
from app.models.semester import Semester

app = create_app()

# ---------------------------------------------------------------------------
# Data jadwal
# format: (day, start, end, course_name, class_name, room_code)
# room_code sesuai yang ada di DB (MKU.xxx / kode lain)
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ── SENIN ──
    ("Senin", "07:30", "09:00", "Pengantar Perencanaan Pariwisata",      "Kelas A", "MKU.226"),
    ("Senin", "07:30", "09:00", "Metodologi Penelitian",                  None,      "MKU.225"),
    ("Senin", "07:30", "09:00", "Bahasa Jepang Khusus Pariwisata",        "Kelas B", "MKU.224"),
    ("Senin", "09:10", "10:40", "Pariwisata Nasional dan Internasional",  "Kelas A", "MKU.225"),
    ("Senin", "09:10", "10:40", "Studi Kelayakan Pariwisata Berkelanjutan", None,    "MKU.226"),
    ("Senin", "09:10", "10:40", "Geografi Pariwisata",                    "Kelas A", "MKU.223"),
    ("Senin", "10:50", "12:00", "Teknik Pemandu Wisata",                  "Kelas A", "MKU.224"),
    ("Senin", "10:50", "12:00", "Pengelolaan Usaha Daya Tarik Wisata",    None,      "MKU.225"),

    # ── SELASA ──
    ("Selasa", "07:30", "09:00", "Pengantar Filsafat",                    "Kelas A", "MKU.224"),
    ("Selasa", "07:30", "09:00", "Pemasaran Pariwisata",                  "Kelas B", "MKU.225"),
    ("Selasa", "09:10", "10:40", "Pariwisata Nasional dan Internasional", "Kelas B", "MKU.225"),
    ("Selasa", "09:10", "10:40", "Mitigasi Bencana Berbasis Kearifan Lokal", None,   "MKU.224"),
    ("Selasa", "09:10", "10:40", "Geografi Pariwisata",                   "Kelas B", "MKU.226"),
    ("Selasa", "10:50", "12:00", "Pengantar Ilmu Kepariwisataan",         None,      "MKU.226"),
    ("Selasa", "10:50", "12:00", "Teknik Pemandu Wisata",                 "Kelas B", "MKU.226"),
    ("Selasa", "10:50", "12:00", "Pemasaran Pariwisata",                  "Kelas A", "MKU.224"),

    # ── RABU ──
    ("Rabu", "07:30", "09:00", "Sosiologi Pariwisata",                    "Kelas A", "MKU.225"),
    ("Rabu", "07:30", "09:00", "Bahasa Jepang Khusus Pariwisata",         "Kelas A", "MKU.226"),
    ("Rabu", "07:30", "09:00", "Bisnis dan Kewirausahaan Pariwisata",     "Kelas B", "MKU.224"),
    ("Rabu", "09:10", "10:40", "Pengantar Perencanaan Pariwisata",        "Kelas B", "MKU.224"),
    ("Rabu", "09:10", "10:40", "Pariwisata Perkotaan dan MICE",           "Kelas A", "MKU.225"),
    ("Rabu", "10:50", "12:00", "Pengantar Ilmu Kepariwisataan",           None,      "MKU.226"),
    ("Rabu", "10:50", "12:00", "Pengelolaan Usaha Akomodasi",             None,      "MKU.224"),
    ("Rabu", "10:50", "12:00", "Pariwisata Pedesaan",                     "Kelas B", "MKU.225"),

    # ── KAMIS ──
    ("Kamis", "07:30", "09:00", "Metodologi Penelitian",                  None,      "MKU.225"),
    ("Kamis", "07:30", "09:00", "Bisnis dan Kewirausahaan Pariwisata",    "Kelas A", "MKU.226"),
    ("Kamis", "07:30", "09:00", "Sistem Informasi Kepariwisataan",        "Kelas B", "MKU.224"),
    ("Kamis", "09:10", "10:40", "Pariwisata Pedesaan",                    "Kelas A", "MKU.226"),
    ("Kamis", "09:10", "10:40", "Pengantar Filsafat",                     "Kelas B", "MKU.224"),
    ("Kamis", "09:10", "10:40", "Pariwisata Berkelanjutan",               "Kelas B", "MKU.225"),
    ("Kamis", "10:50", "12:00", "Pariwisata Perkotaan dan MICE",          "Kelas B", "MKU.213"),
    ("Kamis", "10:50", "12:00", "Perencanaan Lanskap Pariwisata",         None,      "MKU.224"),

    # ── JUMAT ──
    ("Jumat", "07:30", "09:00", "Sistem Informasi Kepariwisataan",        "Kelas B", "MKU.224"),
    ("Jumat", "07:30", "09:00", "Pengelolaan Atraksi Pertunjukan Budaya", None,      "MKU.225"),
    ("Jumat", "09:10", "10:40", "Sosiologi Pariwisata",                   "Kelas B", "MKU.224"),
    ("Jumat", "09:10", "10:40", "Hospitaliti Pariwisata",                 "Kelas A", "MKU.226"),
    ("Jumat", "09:10", "10:50", "Tugas Akhir (Skripsi)",                  None,      "MKU.213"),
    ("Jumat", "10:50", "12:00", "Pariwisata Berkelanjutan",               "Kelas A", "MKU.225"),
    ("Jumat", "10:50", "12:00", "Pengelolaan Usaha Perjalanan Wisata",    None,      "MKU.226"),
    ("Jumat", "10:50", "12:00", "Hospitaliti Pariwisata",                 "Kelas B", "MKU.224"),
    ("Jumat", "10:50", "12:00", "Seminar Proposal",                       None,      "MKU.226"),
]


with app.app_context():
    # Cari semester Ganjil
    semester = Semester.query.filter(Semester.name.ilike("%Ganjil%")).first()
    if not semester:
        print("ERROR: Semester Ganjil tidak ditemukan!")
        exit(1)
    print(f"Menggunakan semester: {semester.name} (ID:{semester.id})")

    # Cache course & room agar tidak query berulang
    course_cache = {}
    room_cache   = {r.room_code: r for r in Room.query.all()}

    missing_rooms = set()
    added = 0

    for day, start, end, course_name, class_name, room_code in SCHEDULES:
        # Cari / buat course
        if course_name not in course_cache:
            course = Course.query.filter(Course.course_name.ilike(course_name)).first()
            if not course:
                course = Course(course_name=course_name)
                db.session.add(course)
                db.session.flush()
            course_cache[course_name] = course
        course = course_cache[course_name]

        # Cari room
        room = room_cache.get(room_code)
        if not room:
            missing_rooms.add(room_code)
            continue

        sched = ClassSchedule(
            course_id   = course.id,
            class_name  = class_name,
            room_id     = room.id,
            day_name    = day,
            start_time  = dt.time(*map(int, start.split(":"))),
            end_time    = dt.time(*map(int, end.split(":"))),
            semester_id = semester.id,
        )
        sched.lecturers = []
        db.session.add(sched)
        added += 1

    db.session.commit()

    print(f"\nSelesai: {added} jadwal berhasil dimasukkan.")
    print(f"Mata kuliah baru dibuat: {len(course_cache)}")
    if missing_rooms:
        print(f"WARNING - Room code tidak ditemukan: {missing_rooms}")
