"""
Seed jadwal kelas Prodi Arkeologi ke Semester Ganjil 2025/2026.
Jalankan: python seed_arkeologi_schedules.py
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

# ---------------------------------------------------------------------------
# Room keys → room_code di DB
# ---------------------------------------------------------------------------
ROOM_CODE_MAP = {
    "R.211":       "R.211",        # Lensa Budaya (Arkeologi)
    "R.320":       "R.320",        # Lab. Arkeologi
    "MKU.213":     "MKU.213",      # R.213 MKU
    "MKU.223":     "MKU.223",      # R.223 MKU
    "MKU.215":     "MKU.215",      # R.215 MKU
    "R.215":       "R.215",        # R.215 FIB
    "R.213-R.214": "R.213-R.214",  # Ruang Gabungan
}

# ---------------------------------------------------------------------------
# Alias dosen – nama persis dari DB
# ---------------------------------------------------------------------------
_ERNI       = "Dr. Erni Erawati, M.Si."
_YUSRIANA   = "Yusriana, S.S., M.A."
_SUPRIADI   = "Dr. Supriadi, S.S., M.A."
_FAHRAN     = "Fahran Reza, S.S., M.Hum."
_MNUR       = "Dr. Muhammad Nur, S.S., M.A."
_HASANUDDIN = "Dr. Hasanuddin, M.Hum."
_ERWIN      = "Erwin Mansyur Ugu Saraka, S.S., M.Sc."
_BAHRUL     = "A. Bahrul Hidayah, S.T., M.T."
_AKIN       = "Prof. Dr. Akin Duli, M.A."
_KHADIJAH   = "Dr. Khadijah Thahir Muda, M.Si."
_SURYATMAN  = "Suryatman, S.S., M.Hum."
_LAODE      = "Drs. Laode Muhammad Aksa, M.Hum."
_RISKA      = "Riska Faradilla Nazar, S.S., M.Hum."
_ROSMAWATI  = "Dr. Rosmawati, S.S., M.Si."
_SAIFUL     = "A. Muh. Saiful, S.S., M.A."
_YADI       = "Dr. Yadi Mulyadi, S.S., M.A."
_BAHAR      = "Dr. Muhammad Bahar Akase Teng, LCP, M.Hum."
_MUHLIS     = "Prof. Dr. Muhlis Hadrawi, S.S., M.Hum."

# ---------------------------------------------------------------------------
# Data jadwal: (hari, start, end, course_name, class_name, room_key, [dosen])
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ═══════════════════════════ SENIN ═══════════════════════════
    # 07:30 – 09:00
    ("Senin", "07:30", "09:00", "Kewirausahaan Warisan Budaya",               "Kelas B", "MKU.213",     [_ERNI, _YUSRIANA]),
    ("Senin", "07:30", "09:00", "Arkeologi dan Pariwisata",                   "Kelas A", "R.211",       [_SUPRIADI, _FAHRAN]),
    # 09:10 – 10:40
    ("Senin", "09:10", "10:40", "Etnoarkeologi",                              "Kelas A", "R.211",       [_MNUR, _HASANUDDIN]),
    ("Senin", "09:10", "10:40", "Geoarkeologi",                               "Kelas A", "R.320",       [_ERWIN, _FAHRAN, _BAHRUL]),
    ("Senin", "09:10", "10:40", "Sejarah dan Kebudayaan Indonesia",            "Kelas A", "MKU.223",     [_AKIN, _ERNI]),
    # 10:50 – 12:30
    ("Senin", "10:50", "12:30", "Kajian Pelestarian Cagar Budaya",            "Kelas A", "R.211",       [_SUPRIADI, _YADI, _LAODE]),
    # 13:00 – 14:30
    ("Senin", "13:00", "14:30", "Teknoarkeologi",                             "Kelas A", "R.320",       [_KHADIJAH, _ERWIN, _SURYATMAN]),
    # 14:30 – 16:00
    ("Senin", "14:30", "16:00", "Arkeologi Konflik",                          "P",       "R.211",       [_SUPRIADI, _FAHRAN]),

    # ═══════════════════════════ SELASA ══════════════════════════
    # 07:30 – 09:00
    ("Selasa", "07:30", "09:00", "Tata Pamer Museum",                         "Kelas A", "MKU.215",     [_YUSRIANA, _RISKA]),
    ("Selasa", "07:30", "09:00", "Arkeologi Kolonial",                        "Kelas B", "MKU.223",     [_ERNI, _SURYATMAN]),
    ("Selasa", "07:30", "09:00", "Kewirausahaan Warisan Budaya",               "Kelas A", "R.211",       [_ERNI, _YUSRIANA]),
    ("Selasa", "07:30", "09:00", "Analisis Data Arkeologi",                   "Kelas A", "R.320",       [_MNUR, _SAIFUL, _SURYATMAN]),
    # 09:10 – 10:40
    ("Selasa", "09:10", "10:40", "Geoarkeologi",                              "Kelas B", "MKU.213",     [_ERWIN, _FAHRAN, _BAHRUL]),
    ("Selasa", "09:10", "10:40", "Kajian Pelestarian Cagar Budaya",           "Kelas B", "MKU.223",     [_SUPRIADI, _YADI, _LAODE]),
    ("Selasa", "09:10", "10:40", "Arkeologi Islam",                           "Kelas A", "R.211",       [_ROSMAWATI, _RISKA]),
    # 10:50 – 12:20
    ("Selasa", "10:50", "12:20", "Teknoarkeologi",                            "Kelas B", "MKU.215",     [_KHADIJAH, _ERWIN, _SURYATMAN]),
    ("Selasa", "10:50", "12:20", "Dasar-Dasar Filsafat Ilmu Sosial & Ilmu Budaya", "Kelas A", "R.211", [_AKIN, _BAHAR]),
    # 13:00 – 14:30
    ("Selasa", "13:00", "14:30", "Sejarah Budaya Sulawesi",                   "Kelas A", "R.211",       [_ROSMAWATI, _MNUR]),
    ("Selasa", "13:00", "14:30", "Prasejarah Sulawesi",                       "Kelas A", "R.320",       [_AKIN, _MNUR]),
    # 14:30 – 16:00
    ("Selasa", "14:30", "16:00", "Keramologi",                                "Kelas A", "R.211",       [_KHADIJAH, _YUSRIANA]),
    ("Selasa", "14:30", "16:00", "Pengelolaan Sumber Daya Arkeologi",         "Kelas A", "R.320",       [_KHADIJAH, _SUPRIADI, _YUSRIANA, _RISKA, _LAODE]),

    # ═══════════════════════════ RABU ════════════════════════════
    # 07:30 – 09:00
    ("Rabu", "07:30", "09:00", "Media Sosial dan Arkeologi",                  "Kelas A", "MKU.223",     [_YADI, _SAIFUL]),
    ("Rabu", "07:30", "09:00", "Paleografi dan Filologi Sulawesi",            "P",       "R.211",       [_ERNI, _MUHLIS, _BAHAR]),
    # 09:05 – 10:40
    ("Rabu", "09:05", "10:40", "Dasar-Dasar Filsafat Ilmu Sosial & Ilmu Budaya", "Kelas B", "R.211",  [_AKIN, _BAHAR]),
    # 10:50 – 12:30
    ("Rabu", "10:50", "12:30", "Arkeologi Islam",                             "Kelas B", "R.211",       [_ROSMAWATI, _RISKA]),
    # 13:00 – 14:30
    ("Rabu", "13:00", "14:30", "Sejarah Budaya Sulawesi",                     "Kelas B", "R.211",       [_ROSMAWATI, _MNUR]),
    ("Rabu", "13:00", "14:30", "Prasejarah Sulawesi",                         "Kelas B", "R.320",       [_AKIN, _MNUR, _HASANUDDIN, _SURYATMAN]),
    # 14:30 – 16:00
    ("Rabu", "14:30", "16:00", "Etnoarkeologi",                               "Kelas B", "R.211",       [_MNUR]),

    # ═══════════════════════════ KAMIS ═══════════════════════════
    # 07:30 – 09:00
    ("Kamis", "07:30", "09:00", "Arkeologi dan Pariwisata",                   "Kelas B", "R.213-R.214", [_SUPRIADI, _FAHRAN]),
    ("Kamis", "07:30", "09:00", "Sejarah dan Kebudayaan Indonesia",            "Kelas B", "R.215",       [_AKIN, _ERNI]),
    ("Kamis", "07:30", "09:00", "Ekskavasi Arkeologis",                       "Kelas A", "R.320",       [_MNUR, _HASANUDDIN, _SAIFUL, _SURYATMAN]),
    # 09:10 – 10:40
    ("Kamis", "09:10", "10:40", "Tata Pamer Museum",                          "Kelas B", "R.211",       [_YUSRIANA, _RISKA]),
    # 10:50 – 12:20
    ("Kamis", "10:50", "12:20", "Keramologi",                                 "Kelas B", "MKU.213",     [_KHADIJAH, _YUSRIANA]),
    ("Kamis", "10:50", "12:20", "Media Sosial dan Arkeologi",                 "Kelas B", "R.211",       [_YADI, _SAIFUL]),
    ("Kamis", "10:50", "12:20", "Pengantar Arkeologi",                        "Kelas A", "R.213-R.214", [_ROSMAWATI, _ERWIN]),
    # 13:00 – 14:30
    ("Kamis", "13:00", "14:30", "Aspek Hukum dalam Arkeologi",                "Kelas B", "R.211",       [_YADI, _SAIFUL, _LAODE]),
    # 14:30 – 16:00
    ("Kamis", "14:30", "16:00", "Analisis Data Arkeologi",                    "Kelas B", "R.320",       [_MNUR, _SAIFUL, _SURYATMAN]),
    ("Kamis", "14:30", "16:00", "Pengelolaan Sumber Daya Arkeologi",          "Kelas B", "R.211",       [_KHADIJAH, _SUPRIADI, _YUSRIANA, _RISKA, _LAODE]),

    # ═══════════════════════════ JUMAT ═══════════════════════════
    # 07:30 – 09:00
    ("Jumat", "07:30", "09:00", "Arkeologi Maritim",                          "Kelas A", "R.211",       [_SUPRIADI, _YUSRIANA, _RISKA, _LAODE]),
    ("Jumat", "07:30", "09:00", "Arkeologi Maritim",                          "Kelas B", "R.320",       [_SUPRIADI, _YUSRIANA, _RISKA, _LAODE]),
    ("Jumat", "07:30", "09:00", "Etika Profesi Arkeologi",                    "Kelas A", "R.213-R.214", [_SUPRIADI, _RISKA]),
    # 09:00 – 16:00  (SKRIPSI seharian)
    ("Jumat", "09:00", "16:00", "SKRIPSI",                                    None,      "R.211",       [_ROSMAWATI]),
    # 09:05 – 10:40
    ("Jumat", "09:05", "10:40", "Bioarkeologi",                               "Kelas A", "R.211",       [_KHADIJAH, _ERWIN]),
    ("Jumat", "09:05", "10:40", "Ekskavasi Arkeologis",                       "Kelas B", "MKU.223",     [_MNUR, _HASANUDDIN, _SAIFUL, _SURYATMAN]),
    ("Jumat", "09:05", "10:40", "Arkeometri",                                 "P",       "MKU.223",     [_KHADIJAH]),
    # 10:40 – 12:20
    ("Jumat", "10:40", "12:20", "Arkeologi Kolonial",                         "Kelas A", "R.211",       [_ERNI, _SURYATMAN]),
    ("Jumat", "10:50", "12:20", "Aspek Hukum dalam Arkeologi",                "Kelas A", "R.213-R.214", [_YADI, _SAIFUL, _LAODE]),   # mulai 10:50
    # 13:00 – 14:30
    ("Jumat", "13:00", "14:30", "Pengantar Arkeologi",                        "Kelas B", "R.213-R.214", [_ROSMAWATI, _ERWIN]),
    ("Jumat", "13:30", "15:00", "Bioarkeologi",                               "Kelas B", "R.211",       [_KHADIJAH, _ERWIN]),        # mulai 13:30
    # 14:40 – 16:15
    ("Jumat", "14:40", "16:15", "Arkeologi Arsitektur",                       "P",       "R.213-R.214", [_ERNI, _SAIFUL]),
    ("Jumat", "14:40", "16:15", "Etika Profesi Arkeologi",                    "Kelas B", "R.211",       [_YADI, _RISKA]),
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
        print(f"  [NEW] Dosen baru: {name!r}")
    cache[name] = lec
    return lec


with app.app_context():
    semester = Semester.query.filter(Semester.name.ilike("%Ganjil%")).first()
    if not semester:
        print("ERROR: Semester Ganjil tidak ditemukan!")
        exit(1)
    print(f"Semester : {semester.name} (ID:{semester.id})\n")

    room_cache     = {r.room_code: r for r in Room.query.all()}
    course_cache   = {}
    lecturer_cache = {}
    added          = 0
    missing_rooms  = set()

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

    print(f"\n{'='*55}")
    print(f"Selesai: {added} jadwal Arkeologi berhasil ditambahkan.")
    if missing_rooms:
        print(f"WARNING – Ruang tidak ditemukan: {missing_rooms}")
    print(f"Total jadwal di DB: {ClassSchedule.query.count()}")
