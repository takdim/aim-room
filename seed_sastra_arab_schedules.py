"""
Seed jadwal kelas Prodi Sastra Arab ke Semester Ganjil 2025/2026.
Jalankan: python seed_sastra_arab_schedules.py
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
    "R.202": "R.202",     # SAC Sastra Arab
    "R.201": "R.201",     # Lab. Multi Media Sastra Arab
    "R.218": "R.218",
    "R.223": "MKU.223",
    "R.213": "MKU.213",
    "R.214": "MKU.214",
    "R.317": "R.317",
}

# Alias dosen yang dipakai berulang
_YUSRING  = "Prof. Dr. Yusring Sanusi B, S.S., M.App.Ling."
_SYAMSUL  = "Dr. Syamsul Bahri Abd. Hamid, L.C., M.A."
_WAHIDAH  = "Dr. Sitti Wahidah Masnani, M.Hum."
_AGUS     = "Dr. Andi Agussalim, M.Hum."
_ZUHRIAH  = "Dr. Zuhriah, S.S., M.Hum."
_HAER     = "Haeruddin, S.S., M.A."
_FITRI    = "Fitriani, S.S., M.Hum."
_RIDWAN   = "Muhammad Ridwan, S.S., M.A."
_FADLAN   = "Fadlan Ahmad, S.S., M.Si."
_SUPR     = "Supratman, S.S., M.A."
_MUJAD    = "Mujadilah Nur, S.S., M.Hum."
_HAERI    = "Haeriyyah, S.Ag., M.Pd.I."

# ---------------------------------------------------------------------------
# Data jadwal: (day, start, end, course_name, class_name, room_key, [lecturers])
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ═══════════════════════════ SENIN ═══════════════════════════
    # 07:30 - 09:00
    ("Senin", "07:30", "09:00", "Ilmu al-Aswat",                               "Kls A",  "R.202",
     [_HAER, _FITRI]),
    ("Senin", "07:30", "09:00", "Semiotika",                                    "Kls A",  "R.218",
     [_WAHIDAH, _AGUS]),
    ("Senin", "07:30", "09:00", "Muhadatsah Li al-Muthawassith",                "Kls B",  "R.223",
     [_RIDWAN, _FADLAN]),
    # 09:10 - 10:40
    ("Senin", "09:10", "10:40", "Ilmu al-Aswat",                               "Kls B",  "R.218",
     [_HAER, _FITRI]),
    ("Senin", "09:10", "10:40", "Morfologi Bahasa Arab Li al-Mubtadiy",         "Kls A",  "R.202",
     [_ZUHRIAH]),
    ("Senin", "09:10", "10:40", "Pembelajaran Bahasa Arab Berbantuan Komputer", "Kls B",  "R.201",
     [_YUSRING, _AGUS]),
    # 10:50 - 12:30
    ("Senin", "10:50", "12:30", "Fiqh Lughah",                                 "Kls B",  "R.218",
     [_ZUHRIAH, _FITRI]),
    ("Senin", "10:50", "12:30", "Program Aplikasi Komputer Bahasa Arab",        "Kls C",  "R.201",
     [_YUSRING, _AGUS]),
    ("Senin", "10:50", "12:30", "Gerakan Politik Negara Arab",                  "Kls B",  "R.223",
     [_SUPR, _FADLAN]),
    ("Senin", "10:50", "12:30", "Al-Fann Al-Araby",                             "Kls A",  "R.202",
     [_HAER, _MUJAD, _FITRI]),
    # 13:00 - 14:30
    ("Senin", "13:00", "14:30", "Pembelajaran Bahasa Arab Berbantuan Komputer", "Kls A",  "R.201",
     [_YUSRING, _AGUS]),
    ("Senin", "13:00", "14:30", "Filsafat dan Pemikiran Islam",                 "Kls B",  "R.218",
     [_SUPR]),
    # 14:40 - 16:00
    ("Senin", "14:40", "16:00", "Istima' Lanjutan",                             "Kls B",  "R.202",
     [_HAER, _FITRI]),
    ("Senin", "14:40", "16:00", "Statistika Bahasa",                            "Kls A",  "R.218",
     [_YUSRING, _AGUS]),

    # ═══════════════════════════ SELASA ═══════════════════════════
    # 07:30 - 09:00
    ("Selasa", "07:30", "09:00", "Tahqiq al-Nushush",                           "Kls B",  "R.223",
     [_WAHIDAH]),
    ("Selasa", "07:30", "09:00", "Sintaksis Bahasa Arab Li al-Muthawassit",     "Kls B",  "R.202",
     [_ZUHRIAH, _AGUS]),
    ("Selasa", "07:30", "09:00", "Istima' Lanjutan",                            "Kls A",  "R.218",
     [_HAER, _FITRI]),
    # 09:10 - 10:40
    ("Selasa", "09:10", "10:40", "Tahqiq al-Nushush",                           "Kls A",  "R.218",
     [_WAHIDAH]),
    ("Selasa", "09:10", "10:40", "Ilmu Rasmi",                                  "Kls B",  "R.202",
     [_RIDWAN, _SUPR]),
    ("Selasa", "09:10", "10:40", "Pembelajaran Bahasa Arab Berbantuan Komputer","Kls C",  "R.201",
     [_YUSRING, _AGUS]),
    # 10:50 - 12:30
    ("Selasa", "10:50", "12:30", "Sintaksis Bahasa Arab Li al-Muthawassit",     "Kls A",  "R.218",
     [_ZUHRIAH, _AGUS]),
    ("Selasa", "10:50", "12:30", "Ilmu Rasmi",                                  "Kls A",  "R.202",
     [_RIDWAN, _SUPR]),
    ("Selasa", "10:50", "12:30", "Pengembangan Diri",                           "Kls B",  "R.223",
     [_HAERI, _FITRI]),
    # 13:00 - 14:30
    ("Selasa", "13:00", "14:30", "Bahasa dan Kebudayaan Persia",                "Kls B",  "R.202",
     [_SUPR]),
    # 14:40 - 16:00
    ("Selasa", "14:40", "16:00", "Muthalaah Lanjutan",                          "Kls A",  "R.202",
     [_SUPR]),

    # ═══════════════════════════ RABU ═══════════════════════════
    # 07:30 - 09:00
    ("Rabu", "07:30", "09:00", "Semantik Bahasa Arab",                          "Kls A",  "R.202",
     [_ZUHRIAH]),
    ("Rabu", "07:30", "09:00", "Program Aplikasi Komputer Bahasa Arab",         "Kls A",  "R.201",
     [_YUSRING, _AGUS]),
    ("Rabu", "07:30", "09:00", "Bahasa Arab Kontemporer",                       "Kls A",  "R.218",
     [_HAER, _FITRI]),
    # 09:10 - 10:40
    ("Rabu", "09:10", "10:40", "Terjemahan Arab Indonesia",                     "Kls B",  "R.218",
     [_YUSRING, _SYAMSUL]),
    ("Rabu", "09:10", "10:40", "Filsafat dan Pemikiran Islam",                  "Kls A",  "R.202",
     [_HAERI]),
    ("Rabu", "09:10", "10:40", "Morfologi Bahasa Arab Li al-Mubtadiy",          "Kls B",  "R.223",
     [_ZUHRIAH]),
    # 10:50 - 12:30
    ("Rabu", "10:50", "12:30", "Telaah Puisi Arab",                             "Kls B",  "R.218",
     [_SYAMSUL, _FADLAN]),
    ("Rabu", "10:50", "12:30", "Program Aplikasi Komputer Bahasa Arab",         "Kls B",  "R.201",
     [_YUSRING, _AGUS]),
    ("Rabu", "10:50", "12:30", "Kajian Al-Qur'an",                              "Kls B",  "R.202",
     ["Dr. H. Ahmad Mujahid, M.Ag.", _HAERI]),
    ("Rabu", "10:50", "12:30", "Seminar Pra Skripsi",                           "Kls A",  "R.223",
     [_WAHIDAH, _ZUHRIAH]),
    # 13:00 - 14:30
    ("Rabu", "13:00", "14:30", "Telaah Naskah",                                 "Kls B",  "R.202",
     [_WAHIDAH, _MUJAD]),
    ("Rabu", "13:00", "14:30", "Telaah Puisi Arab",                             "Kls A",  "R.218",
     [_SYAMSUL, _FADLAN]),
    ("Rabu", "13:00", "14:30", "Program Aplikasi Komputer Bahasa Arab",         "Kls D",  "R.201",
     [_YUSRING, _AGUS]),
    # 14:40 - 16:00
    ("Rabu", "14:40", "16:00", "Kajian Al-Qur'an",                              "Kls A",  "R.218",
     ["Dr. H. Ahmad Mujahid, M.Ag.", _HAERI]),
    ("Rabu", "14:40", "16:00", "Terjemahan Arab Indonesia",                     "Kls A",  "R.202",
     [_YUSRING, _SYAMSUL]),

    # ═══════════════════════════ KAMIS ═══════════════════════════
    # 07:30 - 09:00
    ("Kamis", "07:30", "09:00", "Al-Arabiyyah Li al-Muthawassit",               "Kls B",  "R.218",
     [_YUSRING, _SYAMSUL]),
    ("Kamis", "07:30", "09:00", "Perkembangan Islam Kontemporer",               "Kls A",  "R.202",
     [_WAHIDAH, _AGUS]),
    ("Kamis", "07:30", "09:00", "Muthalaah Lanjutan",                           "Kls B",  "R.213",
     [_SUPR]),
    ("Kamis", "07:30", "09:00", "Tarikh al-Adab",                               "Kls A",  "R.223",
     [_HAER, _MUJAD, _FITRI]),
    # 09:10 - 10:40
    ("Kamis", "09:10", "10:40", "Fiqh Lughah",                                  "Kls A",  "R.202",
     [_ZUHRIAH, _FITRI]),
    ("Kamis", "09:10", "10:40", "Semiotika",                                    "Kls B",  "R.213",
     [_WAHIDAH, _AGUS]),
    # 10:50 - 12:30
    ("Kamis", "10:50", "12:30", "Pengembangan Diri",                            "Kls A",  "R.223",
     [_AGUS, _MUJAD]),
    ("Kamis", "10:50", "12:30", "Al-Arabiyyah Li al-Tamhidiy",                  "Kls A",  "R.218",
     [_YUSRING, _SYAMSUL, _FADLAN]),
    ("Kamis", "10:50", "12:30", "Gerakan Politik Negara Arab",                  "Kls A",  "R.202",
     [_HAERI, _SUPR]),
    ("Kamis", "10:50", "12:30", "Bahasa Arab Kontemporer",                      "Kls B",  "R.213",
     [_HAER, _FITRI]),
    # 13:00 - 14:30
    ("Kamis", "13:00", "14:30", "Al-Arabiyyah Li al-Muthawassit",               "Kls A",  "R.214",
     [_YUSRING, _SYAMSUL, _FADLAN]),
    ("Kamis", "13:00", "14:30", "Al-Fann Al-Araby",                             "Kls B",  "R.202",
     [_HAER, _MUJAD, _FITRI]),
    # 14:40 - 16:00
    ("Kamis", "14:40", "16:00", "Insya Li al-Mubtadiy",                         "Kls A",  "R.202",
     [_RIDWAN, _FADLAN]),
    ("Kamis", "14:40", "16:00", "Perkembangan Islam Kontemporer",               "Kls B",  "R.317",
     ["Meta Sekar Puji Astuti, S.S., M.A., Ph.D.",
      "Ayu Azhariyah, S.E., S.S., Ak., M.A."]),

    # ═══════════════════════════ JUMAT ═══════════════════════════
    # 07:30 - 09:00 (blok pertama)
    ("Jumat", "07:30", "09:00", "Tarikh al-Adab",                               "Kls B",  "R.213",
     [_HAER, _MUJAD, _FITRI]),
    # 08:00 - 09:30 (kelas dalam blok yang sama dengan waktu spesifik)
    ("Jumat", "08:00", "09:30", "Telaah Prosa Arab Li al-Mubtadiy",             "Kls A",  "R.317",
     [_WAHIDAH, _AGUS]),
    ("Jumat", "08:00", "09:30", "Insya Li al-Mubtadiy",                         "Kls B",  "R.202",
     [_RIDWAN, _FADLAN]),
    # 09:40 - 11:15
    ("Jumat", "09:40", "11:15", "Bahasa dan Kebudayaan Persia",                 "Kls A",  "R.202",
     [_SUPR]),
    ("Jumat", "09:40", "11:15", "Statistika Bahasa",                            "Kls B",  "R.213",
     [_YUSRING, _AGUS]),
    # 09:45 - 11:15 (spesifik)
    ("Jumat", "09:45", "11:15", "Telaah Prosa Arab Li al-Mubtadiy",             "Kls B",  "R.218",
     [_WAHIDAH, _ZUHRIAH, _MUJAD]),
    # 13:00 - 14:30
    ("Jumat", "13:00", "14:30", "Semantik Bahasa Arab",                         "Kls B",  "R.218",
     [_ZUHRIAH]),
    ("Jumat", "13:00", "14:30", "Telaah Naskah",                                "Kls A",  "R.202",
     [_WAHIDAH, _MUJAD]),
    # 14:45 - 16:15
    ("Jumat", "14:45", "16:15", "Seminar Pra Skripsi",                          "Kls B",  "R.218",
     [_WAHIDAH, _ZUHRIAH]),
    ("Jumat", "14:45", "16:15", "Muhadatsah Li al-Muthawassith",                "Kls A",  "R.202",
     [_RIDWAN, _FADLAN]),
    # 16:20 - 18:00
    ("Jumat", "16:20", "18:00", "Skripsi/Magang/Praktek Industri (MKPK)",      None,     "R.218",
     [_HAER, _HAERI]),
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
