"""
Seed jadwal kelas Prodi Sastra Indonesia ke Semester Ganjil 2025/2026.
Jalankan: python seed_sastra_indonesia_schedules.py
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
# Ruang – key di SCHEDULES → room_code di DB
# R.103 dan R.104 digunakan terpisah (beda dari combined R.103-R.104).
# Script akan membuat R.103 dan R.104 jika belum ada di DB.
# ---------------------------------------------------------------------------
ROOM_CODE_MAP = {
    "Lab-JSI":  "Lab-JSI",    # R.101 Lab. Sastra Indonesia
    "RRJ":      "RRJ",         # R.102 RRJ Sastra Indonesia
    "R.103":    "R.103",       # R.103 Departemen (dibuat jika belum ada)
    "R.104":    "R.104",       # R.104 Departemen (dibuat jika belum ada)
    "MKU.215":  "MKU.215",    # R.215 MKU
    "R.319":    "R.319",       # R.319 FIB
}

# ---------------------------------------------------------------------------
# Alias dosen – gunakan nama persis dari DB
# ---------------------------------------------------------------------------
_MUNIRA      = "Prof. Dr. Munira Hasjim, S.S., M.Hum."
_ASRIANI     = "Prof. Dr. Asriani Abbas, M.Hum."
_INRIATI     = "Dr. Inriati Lewa, M.Hum."
_SYAHWAN     = "Syahwan Alfianto Amir, S.S., M.Hum."
_NURSA       = "Dra. St. Nursa'adah, S.S., M.Hum."
_TAKKO       = "Prof. Dr. A. B. Takko, M.Hum."
_MUSLIMAT    = "Dr. Muslimat, M.Hum."
_LUKMAN      = "Prof. Dr. Lukman, M.S."
_NURIMAN     = "Muhammad Nur Iman, S.S., M.Hum."
_DARWIS      = "Prof. Dr. Muhammad Darwis, M.Hum."
_KAHARUDD    = "Dr. Kaharuddin, M.Hum."
_RISMAY      = "Rismayanti, S.S., M.Hum."
_DAHLAN      = "Dr. Drs. H. M. Dahlan Abubakar, M.Hum."
_NURHAYATI   = "Prof. Dr. Nurhayati, M.Hum."
_TAMMASSE    = "Dr. Tammasse, M.Hum."
_AYUB        = "Dr. Ayub Khan, M.Si."
_IKHWAN      = "Dr. Ikhwan Sumantri, M.Hum."
_HARYENI     = "Dr. Haryeni, M.Hum."
_YUSUF       = "Drs. Yusuf, S.U."
_FAISAL      = "Faisal Oddang, S.S., M.Hum."
_MEIRLING    = "A. Meirling, S.S., M.Hum."
_ILHAM       = "Ilham, S.S., M.Hum."
_INDARWATI   = "Dr. Hj. Indarwati, S.S., M.Hum."

# Tim dosen (dibuat baru jika belum ada)
_TIM_MORFOLOGI   = "Tim Dosen Morfologi"
_TIM_SASTRA      = "Tim Dosen Sastra"
_TIM_STALISTIKA  = "Tim Dosen Stalistika"
_TIM_DRAMA       = "Tim Dosen Drama"
_TIM_LINGUISTIK  = "Tim Dosen Linguistik"

# ---------------------------------------------------------------------------
# Data jadwal: (hari, start, end, course_name, class_name, room_key, [dosen])
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ═══════════════════════════ SENIN ═══════════════════════════
    # 07:30 – 09:00
    ("Senin", "07:30", "09:00", "Pengantar Linguistik Umum",           "Kls C",       "Lab-JSI",  [_MUNIRA, _ASRIANI]),
    ("Senin", "07:30", "09:00", "Feminisme",                           "Kls B",       "RRJ",      [_INRIATI, _SYAHWAN]),
    ("Senin", "07:30", "09:00", "Metode Penelitian Sastra",            None,          "R.319",    [_INRIATI, _NURSA, _SYAHWAN]),
    ("Senin", "07:30", "09:00", "Dasar-Dasar Filsafat",                "Kls D",       "R.103",    [_TAKKO, _NURSA]),
    ("Senin", "07:30", "09:00", "Feminisme",                           "Kls C",       "MKU.215",  [_MUSLIMAT]),
    # 09:10 – 10:40
    ("Senin", "09:10", "10:40", "Feminisme",                           "Kls D",       "R.103",    [_MUSLIMAT]),
    ("Senin", "09:10", "10:40", "Pengantar Linguistik Umum",           "Kls A",       "RRJ",      [_LUKMAN, _NURIMAN]),
    ("Senin", "09:10", "10:40", "Morfologi",                           "Kls B",       "Lab-JSI",  [_DARWIS, _ASRIANI, _KAHARUDD, _RISMAY, _NURIMAN]),
    ("Senin", "09:10", "10:40", "Stalistika",                          "Kls A",       "R.319",    [_DARWIS, _NURSA, _NURHAYATI, _RISMAY, _DAHLAN]),
    ("Senin", "09:10", "10:40", "Morfologi",                           "Kls C",       "MKU.215",  [_DARWIS, _ASRIANI, _KAHARUDD, _RISMAY, _NURIMAN]),
    # 10:50 – 12:20
    ("Senin", "10:50", "12:20", "Masyarakat dan Kebudayaan Indonesia", "Kls A",       "Lab-JSI",  [_TAKKO, _INDARWATI]),
    ("Senin", "10:50", "12:20", "Telaah Puisi Indonesia",              "Kls A",       "RRJ",      [_INRIATI, _YUSUF, _SYAHWAN]),
    ("Senin", "10:50", "12:20", "Telaah Drama Indonesia",              "Kls B",       "R.319",    [_YUSUF, _ILHAM]),
    ("Senin", "10:50", "12:20", "Masyarakat dan Kebudayaan Indonesia", "Kls D",       "MKU.215",  [_TAKKO, _FAISAL]),
    ("Senin", "10:50", "12:20", "Telaah Puisi Indonesia",              "Kls C",       "R.103",    [_HARYENI, _FAISAL]),
    # 13:00 – 14:29
    ("Senin", "13:00", "14:29", "Pengantar Linguistik Umum",           "Kls B",       "R.319",    [_LUKMAN, _MUNIRA]),
    ("Senin", "13:00", "14:29", "Semiotika",                           "Kls B",       "Lab-JSI",  [_TAKKO, _NURSA]),
    ("Senin", "13:00", "14:29", "Morfologi",                           "Kls A",       "R.104",    [_TIM_MORFOLOGI]),
    ("Senin", "13:00", "14:29", "Semiotika",                           "Kls C",       "RRJ",      [_MUSLIMAT, _MEIRLING]),
    ("Senin", "13:00", "14:29", "Antropolinguistik",                   "Kls A",       "R.103",    [_TAKKO, _INDARWATI]),
    # 14:30 – 16:00
    ("Senin", "14:30", "16:00", "Masyarakat dan Kebudayaan Indonesia", "Kls C",       "Lab-JSI",  [_LUKMAN, _MEIRLING]),
    ("Senin", "14:30", "16:00", "Antropologi Budaya",                  "Kls A",       "R.319",    [_TAKKO, _MUSLIMAT]),
    ("Senin", "14:30", "16:00", "Semiotika",                           "Kls D",       "R.104",    [_MUSLIMAT, _MEIRLING]),
    ("Senin", "14:30", "16:00", "Pengantar Linguistik Umum",           "Kls D",       "RRJ",      [_ASRIANI, _NURIMAN]),
    ("Senin", "14:30", "16:00", "Seminar Linguistik",                  "Kls B",       "R.103",    [_LUKMAN, _TAMMASSE]),

    # ═══════════════════════════ SELASA ═══════════════════════════
    # 07:30 – 09:00
    ("Selasa", "07:30", "09:00", "Dasar-Dasar Filsafat",               "Kls B",       "R.319",    [_TAMMASSE, _AYUB]),
    ("Selasa", "07:30", "09:00", "Dasar-Dasar Filsafat",               "Kls A",       "Lab-JSI",  [_RISMAY, _AYUB]),
    ("Selasa", "07:30", "09:00", "B. Indonesia Untuk Penulisan Karya Ilmiah", "Kls A", "MKU.215", [_DARWIS, _NURIMAN]),
    ("Selasa", "07:30", "09:00", "Kritik Sastra Indonesia",            "Kls A",       "RRJ",      [_HARYENI, _YUSUF, _FAISAL]),
    ("Selasa", "07:30", "09:00", "B. Indonesia Untuk Penulisan Karya Ilmiah", "Kls D", "R.103",   [_ASRIANI, _IKHWAN]),
    # 09:10 – 10:40
    ("Selasa", "09:10", "10:40", "Dasar-Dasar Filsafat",               "Kls C",       "R.103",    [_TAKKO, _NURSA]),
    ("Selasa", "09:10", "10:40", "Sejarah Pengkajian Bahasa Indonesia", "Kls B",      "Lab-JSI",  [_NURHAYATI, _MEIRLING]),
    ("Selasa", "09:10", "10:40", "Fonologi",                           "Kls A",       "R.319",    [_NURHAYATI, _IKHWAN]),
    ("Selasa", "09:10", "10:40", "Kritik Sastra Indonesia",            "Kls B",       "RRJ",      [_INRIATI, _NURSA, _SYAHWAN]),
    # 10:50 – 12:20
    ("Selasa", "10:50", "12:20", "Fonologi",                           "Kls B",       "R.319",    [_NURHAYATI, _IKHWAN]),
    ("Selasa", "10:50", "12:20", "Analisis Wacana Bahasa Indonesia",   "Kls B",       "RRJ",      [_LUKMAN, _MUNIRA]),
    ("Selasa", "10:50", "12:20", "Antropologi Budaya",                 "Kls C",       "R.103",    [_TAKKO, _NURSA]),
    ("Selasa", "10:50", "12:20", "Telaah Drama Indonesia",             "Kls D",       "Lab-JSI",  [_MUSLIMAT, _FAISAL]),
    # 13:00 – 14:30
    ("Selasa", "13:00", "14:30", "Seminar Linguistik",                 "Kls A",       "RRJ",      [_DARWIS, _ASRIANI]),
    ("Selasa", "13:00", "14:30", "Fonologi",                           "Kls C",       "R.319",    [_KAHARUDD, _RISMAY]),
    ("Selasa", "13:00", "14:30", "Masyarakat dan Kebudayaan Indonesia", "Kls B",      "Lab-JSI",  [_MUNIRA, _RISMAY]),
    ("Selasa", "13:00", "14:30", "Pengantar Ilmu Sastra",              "Kls D",       "R.103",    [_INRIATI, _SYAHWAN]),
    # 14:30 – 16:00
    ("Selasa", "14:30", "16:00", "Telaah Puisi Indonesia",             "Kls B",       "RRJ",      [_INRIATI, _YUSUF, _SYAHWAN]),
    ("Selasa", "14:30", "16:00", "Fonologi",                           "Kls D",       "Lab-JSI",  [_KAHARUDD, _RISMAY]),
    ("Selasa", "14:30", "16:00", "Morfologi",                          "Kls D",       "R.104",    [_TIM_MORFOLOGI]),

    # ═══════════════════════════ RABU ════════════════════════════
    # 07:30 – 09:00
    ("Rabu", "07:30", "09:00", "Feminisme",                            "Kls A",       "R.103",    [_INRIATI, _SYAHWAN]),
    ("Rabu", "07:30", "09:00", "Sastra Religius",                      "Kls C",       "R.319",    [_TAKKO, _NURSA]),
    ("Rabu", "07:30", "09:00", "Leksikografi Bahasa Indonesia",        "Kls B",       "MKU.215",  [_IKHWAN, _MEIRLING]),
    # 09:10 – 10:40
    ("Rabu", "09:10", "10:40", "Posmodernisme",                        "Kls A",       "R.319",    [_TAKKO, _NURSA]),
    ("Rabu", "09:10", "10:40", "Tugas Akhir (Skripsi)",                None,          "Lab-JSI",  [_MUNIRA]),
    # 10:50 – 12:20
    ("Rabu", "10:50", "12:20", "Telaah Drama Indonesia",               "Kls B",       "R.103",    [_YUSUF, _ILHAM]),
    ("Rabu", "10:50", "12:20", "Telaah Puisi Indonesia",               "Kls C",       "Lab-JSI",  [_HARYENI, _FAISAL]),
    ("Rabu", "10:50", "12:20", "Posmodernisme",                        "Kls B",       "R.319",    [_TAKKO, _INDARWATI]),
    ("Rabu", "10:50", "12:20", "Leksikografi Bahasa Indonesia",        "Kls A",       "RRJ",      [_LUKMAN, _INDARWATI]),
    ("Rabu", "10:50", "12:20", "Seminar Praskripsi Sastra",            None,          "MKU.215",  [_TIM_SASTRA]),
    # 13:00 – 14:30
    ("Rabu", "13:00", "14:30", "Pragmatik Bahasa Indonesia",           "Kls B",       "R.104",    [_MUNIRA]),
    ("Rabu", "13:00", "14:30", "Telaah Puisi Indonesia",               "Kls D",       "RRJ",      [_MUSLIMAT]),
    ("Rabu", "13:00", "14:30", "Telaah Drama Indonesia",               "Kls A",       "R.319",    [_INRIATI, _NURSA, _SYAHWAN]),
    # 14:30 – 16:00
    ("Rabu", "14:30", "16:00", "Sejarah Pengkajian Bahasa Indonesia",  "Kls D",       "R.103",    [_MUNIRA]),
    ("Rabu", "14:30", "16:00", "Pragmatik Bahasa Indonesia",           "Kls A",       "R.104",    [_LUKMAN, _MEIRLING]),
    ("Rabu", "14:30", "16:00", "Seminar Praskripsi Kebahasaan",        None,          "R.319",    [_TIM_LINGUISTIK]),

    # ═══════════════════════════ KAMIS ═══════════════════════════
    # 07:30 – 09:00
    ("Kamis", "07:30", "09:00", "Kritik Sastra Indonesia",             "Kls A",       "MKU.215",  [_HARYENI, _YUSUF, _FAISAL]),
    ("Kamis", "07:30", "09:00", "Sastra Religius",                     "Kls D",       "R.319",    [_MUSLIMAT, _YUSUF]),
    ("Kamis", "07:30", "09:00", "Semiotika",                           "Kls A",       "Lab-JSI",  [_TAKKO, _NURSA]),
    ("Kamis", "07:30", "09:00", "Sastra Religius",                     "Kls B",       "RRJ",      [_HARYENI, _FAISAL]),
    # 09:10 – 10:40
    ("Kamis", "09:10", "10:40", "Kritik Sastra Indonesia",             "Kls B",       "R.103",    [_INRIATI, _SYAHWAN, _NURSA]),
    ("Kamis", "09:10", "10:40", "Seminar Sastra",                      "Wajib-PS",    "MKU.215",  [_TIM_SASTRA]),
    ("Kamis", "09:10", "10:40", "Retorika",                            "Kls A",       "Lab-JSI",  [_TAKKO, _NURSA]),
    ("Kamis", "09:10", "10:40", "Metode Penelitian Kebudayaan",        "Kls A",       "R.319",    [_TAKKO, _INDARWATI]),
    ("Kamis", "09:10", "10:40", "Retorika",                            "Kls B",       "RRJ",      [_NURHAYATI, _MUSLIMAT]),
    # 10:40/10:50 – 12:20
    ("Kamis", "10:40", "12:20", "Pengantar Ilmu Sastra",               "Kls B",       "R.319",    [_MUSLIMAT, _YUSUF]),   # mulai 10:40
    ("Kamis", "10:50", "12:20", "Retorika",                            "Kls C",       "RRJ",      [_DARWIS, _TAMMASSE]),
    ("Kamis", "10:50", "12:20", "Retorika",                            "Kls D",       "MKU.215",  [_TAKKO, _RISMAY]),
    ("Kamis", "10:50", "12:20", "Antropologi Budaya",                  "Kls D",       "Lab-JSI",  [_TAKKO, _NURSA]),
    ("Kamis", "10:50", "12:20", "Antropolinguistik",                   "Kls B",       "R.103",    [_MUNIRA, _MEIRLING]),
    # 13:00 – 14:29
    ("Kamis", "13:00", "14:29", "Metode Penelitian Linguistik",        "Kls A",       "R.319",    [_LUKMAN, _MUNIRA]),
    ("Kamis", "13:00", "14:29", "Pengantar Ilmu Sastra",               "Kls C",       "RRJ",      [_NURSA]),
    ("Kamis", "13:00", "14:29", "Telaah Drama Indonesia",              "Kls C",       "Lab-JSI",  [_YUSUF, _ILHAM]),
    # 14:30 – 16:00
    ("Kamis", "14:30", "16:00", "Metode Penelitian Kebudayaan",        "Kls B",       "R.104",    [_MUNIRA, _MEIRLING]),
    ("Kamis", "14:30", "16:00", "Sastra Religius",                     "Kls A",       "R.103",    [_INRIATI, _SYAHWAN]),
    ("Kamis", "14:30", "16:00", "Stalistika",                          "Kls B",       "RRJ",      [_TIM_STALISTIKA]),
    ("Kamis", "14:30", "16:00", "Stalistika",                          "Kls C",       "R.319",    [_TIM_STALISTIKA]),

    # ═══════════════════════════ JUMAT ═══════════════════════════
    # 07:30 – 09:00
    ("Jumat", "07:30", "09:00", "Morfologi",                           "Kls A",       "R.319",    [_TIM_MORFOLOGI]),
    ("Jumat", "07:30", "09:00", "Morfologi",                           "Kls D",       "R.103",    [_TIM_MORFOLOGI]),
    ("Jumat", "07:30", "09:00", "Pengantar Ilmu Sastra",               "Kls A",       "MKU.215",  [_HARYENI, _FAISAL]),
    ("Jumat", "07:30", "09:00", "Antropologi Budaya",                  "Kls B",       "Lab-JSI",  [_TAKKO, _MUSLIMAT]),
    ("Jumat", "07:30", "09:00", "B. Indonesia Untuk Penulisan Karya Ilmiah", "Kls C", "RRJ",      [_ASRIANI, _IKHWAN]),
    # 09:10 – 10:40/10:50
    ("Jumat", "09:10", "10:40", "Sejarah Pengkajian Bahasa Indonesia", "Kls A",       "R.103",    [_ASRIANI, _INDARWATI]),
    ("Jumat", "09:10", "10:40", "B. Indonesia Untuk Penulisan Karya Ilmiah", "Kls B", "RRJ",      [_NURHAYATI, _MUNIRA]),
    ("Jumat", "09:10", "10:40", "Stalistika",                          "Kls D",       "MKU.215",  [_TIM_STALISTIKA]),
    ("Jumat", "09:10", "10:50", "Telaah Drama Indonesia",              "Kls A",       "Lab-JSI",  [_INRIATI, _NURSA, _SYAHWAN]),  # hingga 10:50
    # 10:40/10:50 – 12:20
    ("Jumat", "10:50", "12:20", "Analisis Wacana Bahasa Indonesia",    "Kls A",       "R.103",    [_IKHWAN, _DAHLAN]),
    ("Jumat", "10:40", "12:20", "Seminar Sastra",                      "Wajib-PS",    "R.319",    [_TIM_SASTRA]),  # mulai 10:40
    # 13:00 – 14:30
    ("Jumat", "13:00", "14:30", "Telaah Drama Indonesia",              "Kls C / Kls D", "RRJ",    [_TIM_DRAMA]),
    ("Jumat", "13:00", "14:30", "Metode Penelitian Kebudayaan",        "Kls B",       "R.103",    [_MUNIRA, _MEIRLING]),
    ("Jumat", "13:00", "14:30", "Sejarah Pengkajian Bahasa Indonesia", "Kls C",       "R.104",    [_TAMMASSE, _NURIMAN]),
    ("Jumat", "13:00", "14:30", "Leksikografi Bahasa Indonesia",       "Kls A",       "R.319",    [_INDARWATI, _FAISAL]),
    # 14:30 – 16:00
    ("Jumat", "14:30", "16:00", "Metode Penelitian Linguistik",        "Kls B",       "RRJ",      [_NURHAYATI, _IKHWAN]),
    ("Jumat", "14:30", "16:00", "Leksikografi Bahasa Indonesia",       "Kls B",       "R.104",    [_IKHWAN, _MEIRLING]),
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


def ensure_room(code, name, building_name, room_cache):
    """Buat ruang baru jika belum ada di DB. Cari building by name."""
    if code in room_cache:
        return room_cache[code]
    from app.models.reference import Building
    building = Building.query.filter(Building.building_name.ilike(f"%{building_name}%")).first()
    building_id = building.id if building else None
    room = Room(room_code=code, room_name=name, building_id=building_id)
    db.session.add(room)
    db.session.flush()
    room_cache[code] = room
    print(f"  [NEW] Ruang baru dibuat: {code!r} – {name}")
    return room


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

    # Pastikan R.103 dan R.104 tersedia sebagai ruang terpisah
    # Building 12 = Departemen Sastra Indonesia
    ensure_room("R.103", "R.103 Departemen Sastra Indonesia", "Sastra Indonesia", room_cache)
    ensure_room("R.104", "R.104 Departemen Sastra Indonesia", "Sastra Indonesia", room_cache)

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
    print(f"Selesai: {added} jadwal Sastra Indonesia berhasil ditambahkan.")
    if missing_rooms:
        print(f"WARNING – Ruang tidak ditemukan: {missing_rooms}")
    print(f"Total jadwal di DB: {ClassSchedule.query.count()}")
