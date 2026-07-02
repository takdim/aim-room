"""
Seed jadwal kelas Prodi Sastra Jepang ke Semester Ganjil 2025/2026.
Jalankan: python seed_sastra_jepang_schedules.py
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
    "R.316":     "R.316",
    "R.317":     "R.317",
    "R.319":     "R.319",
    "R.212 MKU": "MKU.212",   # R.212 (MKU.212) — beda dari R.212 FIB
    "R.212 FIB": "R.212",     # R.212 (FIB.212)
    "R.216 MKU": "R.216 MKU",
    "R.214":     "MKU.214",
}

# Alias dosen
_NURFITRI  = "Nurfitri, S.S., M.Hum."
_TAQDIR    = "Taqdir, S.Pd., M.Hum."
_IMELDA    = "Dr. Imelda, S.S., M.Pd."
_HADI      = "Hadi Hidayat, S.S., M.Hum."
_HARUNA    = "Haruna Fukuda"
_META      = "Meta Sekar Puji Astuti, S.S., M.A., Ph.D."
_AYU       = "Ayu Azhariyah, S.E., S.S., Ak., M.A."
_NURSIDAH  = "Dr. Nursidah, S.Pd., M.Pd."
_KHAIRIL   = "Khairil Anwar, S.S., M.A."
_KASMAWATI = "Kasmawati, S.S., M.Hum."
_FITHYANI  = "Fithyani Anwar, S.S., M.A., Ph.D."

# ---------------------------------------------------------------------------
# Data jadwal: (day, start, end, course_name, class_name, room_key, [lecturers])
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ═══════════════════════════ SENIN ═══════════════════════════
    # 07:30 - 09:00
    ("Senin", "07:30", "09:00", "Bahasa Jepang Terpadu I",             "Kls A",  "R.316",     [_NURFITRI]),
    ("Senin", "07:30", "09:00", "Bunpou 1",                            "Kls B",  "R.317",     [_TAQDIR]),
    ("Senin", "07:30", "09:00", "Hyouki 1",                            "Kls C",  "R.212 MKU", [_IMELDA]),
    ("Senin", "07:30", "09:00", "Kewirausahaan",                       "Kls B",  "R.216 MKU", [_HADI]),
    ("Senin", "07:30", "09:00", "Bahasa Jepang Terpadu III",           "Kls A",  "R.214",     [_HARUNA]),
    # 09:10 - 10:40
    ("Senin", "09:10", "10:40", "Bahasa Jepang Terpadu I",             "Kls B",  "R.316",     [_NURFITRI]),
    ("Senin", "09:10", "10:40", "Bunpou 1",                            "Kls A",  "R.317",     [_TAQDIR]),
    ("Senin", "09:10", "10:40", "Hyouki 1",                            "Kls D",  "R.212 MKU", [_IMELDA]),
    ("Senin", "09:10", "10:40", "Kewirausahaan",                       "Kls C",  "R.216 MKU", [_HADI]),
    ("Senin", "09:10", "10:40", "Bahasa Jepang Terpadu III",           "Kls B",  "R.214",     [_HARUNA]),
    # 10:50 - 12:30
    ("Senin", "10:50", "12:30", "Bahasa Jepang Terpadu I",             "Kls C",  "R.316",     [_NURFITRI]),
    ("Senin", "10:50", "12:30", "Bunpou 1",                            "Kls D",  "R.317",     [_TAQDIR]),
    ("Senin", "10:50", "12:30", "Hyouki 1",                            "Kls A",  "R.212 MKU", [_IMELDA]),
    ("Senin", "10:50", "12:30", "Kewirausahaan",                       "Kls A",  "R.216 MKU", [_HADI]),
    ("Senin", "10:50", "12:30", "Bahasa Jepang Terpadu III",           "Kls C",  "R.214",     [_HARUNA]),
    # 13:00 - 14:30
    ("Senin", "13:00", "14:30", "Bunpou 3",                            "Kls D",  "R.316",     [_IMELDA]),
    ("Senin", "13:00", "14:30", "Sejarah Seni Indonesia-Jepang",       "Kls A",  "R.317",     [_META]),
    # 14:40 - 16:00
    ("Senin", "14:40", "16:00", "Bunpou 3",                            "Kls C",  "R.316",     [_IMELDA]),
    ("Senin", "14:40", "16:00", "Sejarah Seni Indonesia-Jepang",       "Kls B",  "R.317",     [_META]),

    # ═══════════════════════════ SELASA ═══════════════════════════
    # 07:30 - 09:00
    ("Selasa", "07:30", "09:00", "Hyouki 1",                           "Kls B",  "R.316",     [_IMELDA]),
    ("Selasa", "07:30", "09:00", "Bahasa Jepang Terpadu I",            "Kls D",  "R.317",     [_NURFITRI]),
    ("Selasa", "07:30", "09:00", "Metode Penelitian (Sastra)",          None,     "R.319",     [_KHAIRIL]),
    ("Selasa", "07:30", "09:00", "Bunpou 1",                           "Kls C",  "R.212 MKU", [_TAQDIR]),
    ("Selasa", "07:30", "09:00", "Korespondensi Bahasa Jepang",         "Kls B",  "R.216 MKU", [_HARUNA]),
    ("Selasa", "07:30", "09:00", "Bahasa dan Budaya Jepang",            "Kls A",  "R.214",     [_NURSIDAH]),
    # 09:10 - 10:40
    ("Selasa", "09:10", "10:40", "Japanalogi",                          "Kls A",  "R.316",     [_AYU]),
    ("Selasa", "09:10", "10:40", "Pengantar Kesusastraan Jepang",       "Kls C",  "R.317",     [_KHAIRIL]),
    ("Selasa", "09:10", "10:40", "Bunpou 3",                           "Kls A",  "R.212 MKU", [_IMELDA]),
    ("Selasa", "09:10", "10:40", "Bahasa dan Budaya Jepang",            "Kls B",  "R.216 MKU", [_NURSIDAH]),
    ("Selasa", "09:10", "10:40", "Semiotika",                           "Kls A",  "R.214",     [_TAQDIR]),
    # 10:50 - 12:30
    ("Selasa", "10:50", "12:30", "Japanalogi",                          "Kls B",  "R.316",     [_AYU]),
    ("Selasa", "10:50", "12:30", "Pengantar Kesusastraan Jepang",       "Kls A",  "R.317",     [_KHAIRIL]),
    ("Selasa", "10:50", "12:30", "Semiotika",                           "Kls B",  "R.212 MKU", [_TAQDIR]),
    ("Selasa", "10:50", "12:30", "Korespondensi Bahasa Jepang",         "Kls A",  "R.216 MKU", [_HARUNA]),
    ("Selasa", "10:50", "12:30", "Metode Pengajaran Bahasa Jepang",     None,     "R.214",     [_NURSIDAH]),
    # 13:00 - 14:30
    ("Selasa", "13:00", "14:30", "Japanalogi",                          "Kls C",  "R.316",     [_AYU]),
    ("Selasa", "13:00", "14:30", "Pengantar Kesusastraan Jepang",       "Kls B",  "R.317",     [_KHAIRIL]),
    # 14:40 - 16:00
    ("Selasa", "14:40", "16:00", "Metode Penelitian (Sejarah Budaya)",  None,     "R.319",     [_META]),
    ("Selasa", "14:40", "16:00", "Analisis Wacana 1",                   None,     "R.316",     [_HADI]),
    ("Selasa", "14:40", "16:00", "Bahasa Jepang Bisnis",                None,     "R.212 FIB", [_KASMAWATI, _AYU]),

    # ═══════════════════════════ RABU ═══════════════════════════
    # 07:30 - 09:00
    ("Rabu", "07:30", "09:00", "Bahasa Jepang Terpadu I",              "Kls A",  "R.316",     [_NURSIDAH]),
    ("Rabu", "07:30", "09:00", "Bunpou 1",                             "Kls B",  "R.317",     [_TAQDIR]),
    ("Rabu", "07:30", "09:00", "Bahasa Jepang Terpadu III",            "Kls B",  "R.212 MKU", [_AYU]),
    ("Rabu", "07:30", "09:00", "Pengantar Linguistik Jepang",          "Kls A",  "R.216 MKU", [_KASMAWATI, _NURFITRI]),
    ("Rabu", "07:30", "09:00", "Kritik Sastra Jepang",                 None,     "R.214",     [_KHAIRIL]),
    # 09:10 - 10:40
    ("Rabu", "09:10", "10:40", "Bahasa Jepang Terpadu I",              "Kls B",  "R.316",     [_NURSIDAH]),
    ("Rabu", "09:10", "10:40", "Bunpou 1",                             "Kls A",  "R.317",     [_TAQDIR]),
    ("Rabu", "09:10", "10:40", "Bahasa Jepang Terpadu III",            "Kls C",  "R.216 MKU", [_AYU]),
    ("Rabu", "09:10", "10:40", "Pengantar Linguistik Jepang",          "Kls B",  "R.212 MKU", [_KASMAWATI, _NURFITRI]),
    ("Rabu", "09:10", "10:40", "Kajian Industri Jepang",               "Kls A",  "R.214",     [_META]),
    # 10:50 - 12:30
    ("Rabu", "10:50", "12:30", "Bahasa Jepang Terpadu III",            "Kls A",  "R.216 MKU", [_AYU]),
    ("Rabu", "10:50", "12:30", "Bahasa Jepang Terpadu I",              "Kls C",  "R.316",     [_NURSIDAH]),
    ("Rabu", "10:50", "12:30", "Bunpou 1",                             "Kls D",  "R.317",     [_TAQDIR]),
    ("Rabu", "10:50", "12:30", "Pengantar Linguistik Jepang",          "Kls C",  "R.212 MKU", [_KASMAWATI, _NURFITRI]),
    ("Rabu", "10:50", "12:30", "Kajian Industri Jepang",               "Kls B",  "R.214",     [_META]),
    # 13:00 - 14:30
    ("Rabu", "13:00", "14:30", "Bahasa Jepang Terpadu I",              "Kls D",  "R.316",     [_NURSIDAH]),
    ("Rabu", "13:00", "14:30", "Bunpou 1",                             "Kls C",  "R.317",     [_TAQDIR]),
    # 14:40 - 16:00
    ("Rabu", "14:40", "16:00", "Korespondensi Bahasa Jepang",          "Kls C",  "R.316",     [_HARUNA]),
    ("Rabu", "14:40", "16:00", "Terjemahan Jepang-Indonesia",          None,     "R.317",     [_KASMAWATI]),

    # ═══════════════════════════ KAMIS ═══════════════════════════
    # 07:30 - 09:00
    ("Kamis", "07:30", "09:00", "Bunpou 3",                            "Kls B",  "R.214",     [_IMELDA]),
    ("Kamis", "07:30", "09:00", "Sastra Anak Jepang",                  "Kls C",  "R.316",     [_FITHYANI]),
    ("Kamis", "07:30", "09:00", "Korespondensi Bahasa Jepang",         "Kls B",  "R.317",     [_HARUNA]),
    ("Kamis", "07:30", "09:00", "Sejarah Jepang",                      "Kls A",  "R.212 FIB", [_META]),
    ("Kamis", "07:30", "09:00", "Sastra Bandingan Indonesia-Jepang",   "Kls B",  "R.216 MKU", [_KHAIRIL]),
    # 09:10 - 10:40
    ("Kamis", "09:10", "10:40", "Bunpou 3",                            "Kls A",  "R.214",     [_IMELDA]),
    ("Kamis", "09:10", "10:40", "Sastra Anak Jepang",                  "Kls B",  "R.316",     [_FITHYANI]),
    ("Kamis", "09:10", "10:40", "Komposisi Bahasa Jepang",             "Kls A",  "R.317",     [_HARUNA]),
    ("Kamis", "09:10", "10:40", "Sejarah Jepang",                      "Kls C",  "R.212 FIB", [_META]),
    ("Kamis", "09:10", "10:40", "Sastra Bandingan Indonesia-Jepang",   "Kls A",  "R.216 MKU", [_KHAIRIL]),
    # 10:50 - 12:30
    ("Kamis", "10:50", "12:30", "Bunpou 3",                            "Kls C",  "R.214",     [_IMELDA]),
    ("Kamis", "10:50", "12:30", "Sastra Anak Jepang",                  "Kls A",  "R.316",     [_FITHYANI]),
    ("Kamis", "10:50", "12:30", "Sejarah Jepang",                      "Kls B",  "R.317",     [_META]),
    ("Kamis", "10:50", "12:30", "Wacana Kejepangan dan Media",         "Kls A",  "R.212 MKU", [_HADI]),
    ("Kamis", "10:50", "12:30", "Telaah Drama Jepang",                 None,     "R.216 MKU", [_KHAIRIL]),
    # 13:00 - 14:30
    ("Kamis", "13:00", "14:30", "Seminar Praskripsi (Linguistik)",     None,     "R.316",     [_NURSIDAH]),
    ("Kamis", "13:00", "14:30", "Wacana Kejepangan dan Media",         "Kls B",  "R.317",     [_HADI]),
    ("Kamis", "13:00", "14:30", "Seminar Praskripsi (Kesusastraan)",   None,     "R.319",     [_FITHYANI]),
    # 14:40 - 16:00
    ("Kamis", "14:40", "16:00", "Bahasa Jepang Pariwisata",            None,     "R.316",     [_KASMAWATI]),
    ("Kamis", "14:40", "16:00", "Seminar Praskripsi (Sejarah Budaya)", None,     "R.317",     [_META, _AYU]),

    # ═══════════════════════════ JUMAT ═══════════════════════════
    # 07:30 - 09:00
    ("Jumat", "07:30", "09:00", "Bahasa Jepang Terpadu III",           "Kls A",  "R.316",     [_HARUNA]),
    ("Jumat", "07:30", "09:00", "Sastra Populer Jepang",               "Kls A",  "R.317",     [_FITHYANI]),
    ("Jumat", "07:30", "09:00", "Pranata Masyarakat Jepang",           "Kls C",  "R.212 MKU", [_META, _AYU]),
    ("Jumat", "07:30", "09:00", "Pengantar Linguistik Jepang",         "Kls B",  "R.216 MKU", [_NURFITRI, _KASMAWATI]),
    ("Jumat", "07:30", "09:00", "Sosiolinguistik",                     None,     "R.214",     [_KASMAWATI]),
    # 09:10 - 10:40
    ("Jumat", "09:10", "10:40", "Bahasa Jepang Terpadu III",           "Kls A",  "R.316",     [_HARUNA]),
    ("Jumat", "09:10", "10:40", "Pengantar Linguistik Jepang",         "Kls C",  "R.216 MKU", [_NURFITRI, _KASMAWATI]),
    ("Jumat", "09:10", "10:40", "Sastra Populer Jepang",               "Kls A",  "R.317",     [_FITHYANI]),
    ("Jumat", "09:10", "10:40", "Pranata Masyarakat Jepang",           "Kls A",  "R.212 MKU", [_META, _AYU]),
    ("Jumat", "09:10", "10:40", "Metode Penelitian (Linguistik)",      None,     "R.214",     [_TAQDIR, _KASMAWATI]),
    # 13:00 - 14:30
    ("Jumat", "13:00", "14:30", "Bahasa Jepang Terpadu III",           "Kls A",  "R.316",     [_HARUNA]),
    ("Jumat", "13:00", "14:30", "Pengantar Linguistik Jepang",         "Kls A",  "R.317",     [_NURFITRI, _KASMAWATI]),
    # 14:40 - 16:00
    ("Jumat", "14:40", "16:00", "Pranata Masyarakat Jepang",           "Kls B",  "R.316",     [_META, _AYU]),
    ("Jumat", "14:40", "16:00", "Semantik Bahasa Jepang",              None,     "R.317",     [_NURFITRI]),
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
