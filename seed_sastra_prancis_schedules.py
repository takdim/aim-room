"""
Seed jadwal kelas Prodi Sastra Prancis ke Semester Ganjil 2025/2026.
Jalankan: python seed_sastra_prancis_schedules.py
"""
import datetime as dt
from app import create_app
from app.extensions import db
from app.models.class_schedule import ClassSchedule
from app.models.reference import Course
from app.models.room import Room
from app.models.lecturer import Lecturer
from app.models.semester import Semester

app = create_app()

ROOM_CODE_MAP = {
    "Mediatek-F05": "Mediatek-F05",   # R.201 Mediatek Sastra Prancis
    "AV-F05":       "AV-F05",         # R.202 AV Sastra Prancis
    "PERPUST-WP":   "PERPUST-WP",     # Warung Prancis
}

# Alias dosen
_MASDI   = "Masdiana, S.S., M.Hum."
_IRIANTY = "Dra. Irianty Bandu, M.Pd."
_WAHYU   = "Dr. Wahyuddin, S.S., M.Hum."
_MARDI   = "Dr. Mardi Adi Armin, M.Hum."
_ADE     = "Dr. Ade Yolanda Latjuba, S.S., M.A."
_PRASURI = "Dr. Prasuri Kuswarini, M.A."
_HASBUL  = "Drs. Hasbullah, M.Hum."
_FIEREN  = "Dr. Fierenziana Getruida Junus, S.S., M.Hum."
_HASYIM  = "Prof. Dr. Muhammad Hasyim, M.Si."
_FAISAL  = "Dr. Andi Faisal, S.S., M.Hum."
_ALUNG   = "Alung, S.S., M.A."

# ---------------------------------------------------------------------------
# Data jadwal: (day, start, end, course_name, class_name, room_key, [lecturers])
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ═══════════════════════════ SENIN ═══════════════════════════
    # 07:30 - 10:00
    ("Senin", "07:30", "10:00", "Compréhension orale 1",                "Kls A",  "Mediatek-F05", [_MASDI, _IRIANTY]),
    ("Senin", "07:30", "10:00", "Compréhension orale 3",                "Kls A",  "PERPUST-WP",   [_WAHYU, _MARDI]),
    ("Senin", "07:30", "10:00", "Telaah Sastra Prancis & Frankofon",   None,     "AV-F05",       [_ADE, _PRASURI, _HASBUL]),
    # 10:10 - 12:40
    ("Senin", "10:10", "12:40", "Compréhension orale 1",                "Kls B",  "Mediatek-F05", [_FIEREN, _IRIANTY]),
    ("Senin", "10:10", "12:40", "Compréhension orale 3",                "Kls B",  "PERPUST-WP",   [_HASBUL, _IRIANTY]),
    ("Senin", "10:10", "12:40", "Kajian Linguistik Interdisipliner",    None,     "AV-F05",       [_ADE, _PRASURI, _FIEREN]),
    # 13:00 - 14:40
    ("Senin", "13:00", "14:40", "Kewirausahaan",                        None,     "AV-F05",       [_HASYIM, _MARDI]),
    ("Senin", "13:00", "14:40", "Metodologi Penelitian",                None,     "Mediatek-F05", [_ADE, _PRASURI]),
    ("Senin", "13:00", "14:40", "Magang/Praktek Kerja",                 None,     "PERPUST-WP",   [_MASDI]),
    # 14:50 - 16:30
    ("Senin", "14:50", "16:30", "Komunikasi Digital",                   None,     "Mediatek-F05", [_MASDI]),
    ("Senin", "14:50", "16:30", "Strategi Negosiasi",                   None,     "PERPUST-WP",   [_WAHYU]),
    ("Senin", "14:50", "16:30", "Magang/Praktek Kerja",                 None,     "AV-F05",       [_MASDI]),

    # ═══════════════════════════ SELASA ═══════════════════════════
    # 07:30 - 09:10
    ("Selasa", "07:30", "09:10", "Expression orale 1",                  "Kls A",  "Mediatek-F05", [_MASDI, _ALUNG]),
    ("Selasa", "07:30", "09:10", "Expression orale 3",                  "Kls A",  "AV-F05",       [_WAHYU, _FAISAL]),
    ("Selasa", "07:30", "09:10", "Pengembangan Masyarakat",             None,     "PERPUST-WP",   [_PRASURI]),
    # 09:20 - 11:00
    ("Selasa", "09:20", "11:00", "Semantik Pragmatik",                  None,     "Mediatek-F05", [_ADE, _HASYIM]),
    ("Selasa", "09:20", "11:00", "Pengantar Linguistik",                None,     "AV-F05",       [_ADE, _PRASURI]),
    ("Selasa", "09:20", "11:00", "Etika Profesi",                       None,     "PERPUST-WP",   [_FAISAL]),
    # 11:10 - 12:50
    ("Selasa", "11:10", "12:50", "Expression orale 1",                  "Kls B",  "Mediatek-F05", [_FIEREN]),
    ("Selasa", "11:10", "12:50", "Expression orale 3",                  "Kls B",  "AV-F05",       [_HASBUL]),
    ("Selasa", "11:10", "12:50", "Bahasa Jerman",                       None,     "Mediatek-F05", [_PRASURI]),
    # 13:00 - 14:40
    ("Selasa", "13:00", "14:40", "Kajian Budaya dan Media Prancis",     None,     "Mediatek-F05", [_FAISAL, _HASYIM]),
    ("Selasa", "13:00", "14:40", "Pengantar Filsafat Prancis",          None,     "AV-F05",       [_MARDI]),
    ("Selasa", "13:00", "14:40", "Empati Sosial",                       None,     "PERPUST-WP",   [_PRASURI]),
    # 14:50 - 16:30
    ("Selasa", "14:50", "16:30", "Magang/Praktek Kerja",                None,     "Mediatek-F05", [_MASDI]),
    ("Selasa", "14:50", "16:30", "Komunikasi dan Kerjasama",            None,     "AV-F05",       [_FIEREN]),
    ("Selasa", "14:50", "16:30", "Kewirausahaan Rintisan",              None,     "PERPUST-WP",   [_WAHYU]),

    # ═══════════════════════════ RABU ═══════════════════════════
    # 07:30 - 09:00
    ("Rabu", "07:30", "09:00", "Compréhension écrite 1",               "Kls A",  "Mediatek-F05", [_MASDI, _IRIANTY]),
    ("Rabu", "07:30", "09:00", "Compréhension écrite 3",               "Kls A",  "AV-F05",       [_WAHYU, _MARDI, _HASYIM]),
    ("Rabu", "07:30", "09:00", "Magang/Praktek Kerja",                  None,     "PERPUST-WP",   [_MASDI]),
    # 10:10 - 12:40
    ("Rabu", "10:10", "12:40", "Compréhension écrite 1",               "Kls B",  "Mediatek-F05", [_FIEREN, _IRIANTY]),
    ("Rabu", "10:10", "12:40", "Compréhension écrite 3",               "Kls B",  "AV-F05",       [_HASBUL, _IRIANTY]),
    ("Rabu", "10:10", "12:40", "Kepemimpinan Inovatif",                 None,     "PERPUST-WP",   [_ADE]),
    # 13:00 - 14:40
    ("Rabu", "13:00", "14:40", "Expression orale 1",                   "Kls A",  "Mediatek-F05", [_MASDI, _ALUNG]),
    ("Rabu", "13:00", "14:40", "Expression orale 3",                   "Kls A",  "AV-F05",       [_WAHYU, _FAISAL]),
    ("Rabu", "13:00", "14:40", "Literasi dan Presentasi Ilmiah",        None,     "PERPUST-WP",   [_HASBUL]),
    # 14:50 - 16:30
    ("Rabu", "14:50", "16:30", "Expression orale 1",                   "Kls B",  "Mediatek-F05", [_FIEREN]),
    ("Rabu", "14:50", "16:30", "Expression orale 3",                   "Kls B",  "AV-F05",       [_HASBUL]),
    ("Rabu", "14:50", "16:30", "Studi/Proyek Independen",               None,     "PERPUST-WP",   [_MASDI]),

    # ═══════════════════════════ KAMIS ═══════════════════════════
    # 07:30 - 09:10
    ("Kamis", "07:30", "09:10", "Expression écrite 1",                  "Kls A",  "Mediatek-F05", [_MASDI, _ALUNG]),
    ("Kamis", "07:30", "09:10", "Expression écrite 3",                  "Kls A",  "AV-F05",       [_WAHYU, _FAISAL]),
    ("Kamis", "07:30", "09:10", "Keberagaman Budaya",                   None,     "PERPUST-WP",   [_FAISAL]),
    # 09:20 - 11:00
    ("Kamis", "09:20", "11:00", "Expression écrite 1",                  "Kls B",  "Mediatek-F05", [_FIEREN]),
    ("Kamis", "09:20", "11:00", "Expression écrite 3",                  "Kls B",  "AV-F05",       [_HASBUL, _ALUNG]),
    ("Kamis", "09:20", "11:00", "Pengembangan Talenta",                 None,     "PERPUST-WP",   [_FIEREN]),
    # 11:10 - 12:50
    ("Kamis", "11:10", "12:50", "Apresiasi Sastra Prancis & Frankofon", None,     "Mediatek-F05", [_ADE, _PRASURI]),
    ("Kamis", "11:10", "12:50", "Pengantar Ilmu Budaya",                None,     "AV-F05",       [_FAISAL, _ALUNG]),
    ("Kamis", "11:10", "12:50", "Berpikir Kritis dan Kreatif",          None,     "PERPUST-WP",   [_FIEREN]),
    # 13:00 - 15:50 / 14:40
    ("Kamis", "13:00", "15:50", "Wacana dan Semiologi",                 None,     "Mediatek-F05", [_ADE, _HASYIM]),
    ("Kamis", "13:00", "14:40", "Pengantar Ilmu Sastra",                None,     "AV-F05",       [_ADE, _PRASURI]),
    ("Kamis", "13:00", "14:40", "Kewirausahaan Rintisan",               None,     "PERPUST-WP",   [_WAHYU]),
    # 14:50 - 16:30
    ("Kamis", "14:50", "16:30", "Manajemen Kegiatan",                   None,     "Mediatek-F05", [_ADE]),
    ("Kamis", "14:50", "16:30", "Studi/Proyek Independen",              None,     "AV-F05",       [_MASDI]),

    # ═══════════════════════════ JUMAT ═══════════════════════════
    # 07:30 - 09:10
    ("Jumat", "07:30", "09:10", "Expression écrite 1",                  "Kls A",  "Mediatek-F05", [_MASDI]),
    ("Jumat", "07:30", "09:10", "Expression écrite 3",                  "Kls A",  "AV-F05",       [_WAHYU, _FAISAL]),
    ("Jumat", "07:30", "09:10", "Pemecahan Masalah",                    None,     "PERPUST-WP",   [_FIEREN]),
    # 09:20 - 11:00
    ("Jumat", "09:20", "11:00", "Expression écrite 1",                  "Kls B",  "Mediatek-F05", [_FIEREN]),
    ("Jumat", "09:20", "11:00", "Expression écrite 3",                  "Kls B",  "AV-F05",       [_HASBUL, _ALUNG]),
    ("Jumat", "09:20", "11:00", "Pengambilan Keputusan",                None,     "PERPUST-WP",   [_ADE]),
    # 13:10 - 14:40
    ("Jumat", "13:10", "14:40", "Seminar Proposal",                     None,     "Mediatek-F05", [_PRASURI, _MASDI]),
    ("Jumat", "13:10", "14:40", "Skripsi",                              None,     "AV-F05",       [_PRASURI, _MASDI]),
    ("Jumat", "13:10", "14:40", "Pembelajaran Aktif",                   None,     "PERPUST-WP",   [_FIEREN]),
    # 14:50 - 16:30
    ("Jumat", "14:50", "16:30", "Kreativitas Solutif",                  None,     "Mediatek-F05", [_ADE]),
    ("Jumat", "14:50", "16:30", "Pengembangan Talenta",                 None,     "AV-F05",       [_FAISAL]),
    ("Jumat", "14:50", "16:30", "Magang/Praktek Kerja",                 None,     "PERPUST-WP",   [_MASDI]),
]


def get_or_create_lecturer(name, cache):
    if name in cache:
        return cache[name]
    lec = Lecturer.query.filter_by(lecturer_name=name).first()
    if not lec:
        lec = Lecturer.query.filter(Lecturer.lecturer_name.ilike(name)).first()
    if not lec:
        lec = Lecturer(lecturer_name=name)
        db.session.add(lec)
        db.session.flush()
        print(f"  [NEW] Dosen baru dibuat: {name!r}")
    cache[name] = lec
    return lec


with app.app_context():
    semester = Semester.query.filter(Semester.name.ilike("%Ganjil%")).first()
    if not semester:
        print("ERROR: Semester Ganjil tidak ditemukan!")
        exit(1)
    print(f"Semester: {semester.name} (ID:{semester.id})\n")

    room_cache     = {r.room_code: r for r in Room.query.all()}
    course_cache   = {}
    lecturer_cache = {}
    missing_rooms  = set()
    added = 0

    for day, start, end, course_name, class_name, room_key, lec_names in SCHEDULES:
        room_code = ROOM_CODE_MAP.get(room_key, room_key)
        room = room_cache.get(room_code)
        if not room:
            missing_rooms.add(f"{room_key!r} (code={room_code!r})")
            continue

        if course_name not in course_cache:
            course = Course.query.filter(Course.course_name.ilike(course_name)).first()
            if not course:
                course = Course(course_name=course_name)
                db.session.add(course)
                db.session.flush()
                print(f"  [NEW] Mata kuliah baru: {course_name!r}")
            course_cache[course_name] = course
        course = course_cache[course_name]

        sched = ClassSchedule(
            course_id   = course.id,
            class_name  = class_name,
            room_id     = room.id,
            day_name    = day,
            start_time  = dt.time(*map(int, start.split(":"))),
            end_time    = dt.time(*map(int, end.split(":"))),
            semester_id = semester.id,
        )
        db.session.add(sched)
        db.session.flush()

        sched.lecturers = [get_or_create_lecturer(n, lecturer_cache) for n in lec_names]
        added += 1

    db.session.commit()

    print(f"\n{'='*50}")
    print(f"Selesai: {added} jadwal berhasil ditambahkan.")
    if missing_rooms:
        print(f"WARNING - Room tidak ditemukan: {missing_rooms}")
