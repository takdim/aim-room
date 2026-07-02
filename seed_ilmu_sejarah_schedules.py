"""
Seed jadwal Prodi Ilmu Sejarah - Semester Ganjil 2025/2026
Total: 64 jadwal
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import datetime as dt
from app import create_app
from app.extensions import db
from app.models.class_schedule import ClassSchedule
from app.models.lecturer import Lecturer
from app.models.room import Room
from app.models.semester import Semester
from app.models.reference import Course

app = create_app()

ROOM_CODE_MAP = {
    "MKU.225": "MKU.225",
    "R.324":   "R.324",
    "R.212":   "R.212",
    "R.211":   "R.211",
}

# Canonical lecturer names (verified in DB)
_ILHAM    = "Dr. Ilham, S.S., M.Hum."
_RASYID   = "Drs. Abd. Rasyid R., M.Ag."
_AMRULLAH = "Amrullah Amir, S.S., M.A., Ph.D."
_FAJAR    = "Fajar Sidiq Limola, S.S., M.Hum."
_NASIHIN  = "Nasihin, S.S., M.A."
_SURIADI  = "Dr. Suriadi Mappangara, M.Hum."
_IDA      = "Dr. Ida Liana Tanjung, M.Hum."
_DIAS     = "Drs. Dias Pradadmara, M.A."
_NAHDIA   = "Dr. Nahdia Nur, M.Hum."
_MUSLIMIN = "Dr. Muslimin A. R. Effendy, M.A."
_BAHAR    = "Dr. Muhammad Bahar Akase Teng, LCP, M.Hum."
_ERNI     = "Dr. Erni Erawati, M.Si."
_YUSRIANA = "Yusriana, S.S., M.A."
_ROSMAWATI= "Dr. Rosmawati, S.S., M.Si."
_RISKA    = "Riska Faradilla Nazar, S.S., M.Hum."
_TIM      = "Tim Dosen Sejarah"

# (day, start, end, course_name, class_name, room_key, [lecturers])
SCHEDULES = [
    # ===== SENIN =====
    ("Senin",  "07:30", "09:10", "Sejarah Kawasan Timur Indonesia",             "A", "MKU.225", [_ILHAM, _RASYID]),
    ("Senin",  "07:30", "09:10", "Sejarah Kesehatan",                           "A", "R.324",   [_AMRULLAH, _FAJAR]),
    ("Senin",  "07:30", "09:10", "Bahasa Belanda Sumber",                       "A", "R.212",   [_NASIHIN, _SURIADI]),
    ("Senin",  "09:20", "11:00", "Pengantar Ilmu Sejarah",                      "A", "MKU.225", [_IDA, _DIAS]),
    ("Senin",  "09:20", "11:00", "Bahasa Belanda Sumber",                       "B", "R.212",   [_AMRULLAH, _NASIHIN]),
    ("Senin",  "09:20", "11:00", "Sejarah Eropa",                               "A", "R.324",   [_DIAS, _RASYID]),
    ("Senin",  "11:00", "12:50", "Sufisme dan Islam Modern Indonesia",           "A", "R.324",   [_NASIHIN, _BAHAR]),
    ("Senin",  "11:00", "12:50", "Pengantar Ilmu Sejarah",                      "B", "MKU.225", [_IDA, _DIAS]),
    ("Senin",  "11:00", "12:50", "Sejarah Kawasan Timur Indonesia",             "B", "R.212",   [_NAHDIA, _RASYID]),
    ("Senin",  "13:00", "14:40", "Teori Perubahan Sosial",                      "A", "R.212",   [_DIAS, _FAJAR]),
    ("Senin",  "13:00", "14:40", "Sejarah Kesehatan",                           "B", "R.324",   [_AMRULLAH, _FAJAR]),
    ("Senin",  "14:30", "16:00", "Sejarah Pariwisata di Indonesia",             "A", "R.324",   [_IDA]),
    ("Senin",  "14:30", "16:00", "Teori Perubahan Sosial",                      "B", "R.212",   [_NASIHIN, _BAHAR]),

    # ===== SELASA =====
    ("Selasa", "07:30", "09:10", "Pengantar Ilmu Sosial dan Humaniora",         "A", "MKU.225", [_NASIHIN, _BAHAR]),
    ("Selasa", "07:30", "09:10", "Pengantar Sejarah Dunia",                     "A", "R.212",   [_DIAS, _NAHDIA]),
    ("Selasa", "07:30", "09:10", "Kewirausahaan Warisan Budaya",                "A", "R.211",   [_ERNI, _YUSRIANA]),
    ("Selasa", "07:30", "09:10", "Sejarah Migrasi dan Diaspora di Indonesia",   "A", "R.324",   [_AMRULLAH, _FAJAR]),
    ("Selasa", "09:20", "11:00", "Sejarah Indonesia Modern (1900-1950)",        "A", "R.324",   [_DIAS, _RASYID]),
    ("Selasa", "09:20", "11:00", "Pengantar Sejarah Indonesia",                 "B", "R.212",   [_AMRULLAH, _MUSLIMIN]),
    ("Selasa", "11:00", "12:50", "Pengantar Sejarah Dunia",                     "B", "R.212",   [_DIAS, _NAHDIA]),
    ("Selasa", "11:00", "12:50", "Pengantar Ilmu Sosial dan Humaniora",         "B", "R.324",   [_NASIHIN, _BAHAR]),
    ("Selasa", "11:00", "12:50", "Kajian Museum dan Kuratorial",                "A", "MKU.225", [_MUSLIMIN, _FAJAR]),
    ("Selasa", "13:00", "14:40", "Sejarah Migrasi dan Diaspora di Indonesia",   "B", "R.324",   [_AMRULLAH, _FAJAR]),
    ("Selasa", "13:00", "14:40", "Sufisme dan Islam Modern Indonesia",           "B", "R.212",   [_NASIHIN, _BAHAR]),
    ("Selasa", "14:30", "16:10", "Sejarah Indonesia Modern (1900-1950)",        "B", "R.324",   [_DIAS, _NASIHIN]),
    ("Selasa", "14:30", "16:10", "Sejarah Pariwisata di Indonesia",             "B", "R.212",   [_IDA, _ILHAM]),

    # ===== RABU =====
    ("Rabu",   "07:30", "09:10", "Sejarah Indonesia Kuno s/d 1600",             "A", "MKU.225", [_NAHDIA, _NASIHIN]),
    ("Rabu",   "07:30", "09:10", "Geografi Sejarah",                            "A", "R.212",   [_DIAS, _FAJAR]),
    ("Rabu",   "07:30", "09:10", "Film dan Dokumentasi Sejarah",                "A", "R.324",   [_AMRULLAH, _FAJAR]),
    ("Rabu",   "09:20", "11:00", "Sejarah Indonesia Kuno s/d 1600",             "B", "R.211",   [_ROSMAWATI, _RISKA]),
    ("Rabu",   "09:20", "11:00", "Historiografi Umum",                          "B", "R.212",   [_FAJAR, _MUSLIMIN]),
    ("Rabu",   "09:20", "11:00", "Sejarah Penguasaan dan Pengamanan Laut",      "A", "R.324",   [_DIAS, _RASYID]),
    ("Rabu",   "11:00", "12:50", "Geografi Sejarah",                            "B", "R.212",   [_DIAS, _NASIHIN]),
    ("Rabu",   "11:00", "12:50", "Bahasa Belanda",                              "B", "R.324",   [_AMRULLAH, _SURIADI]),
    ("Rabu",   "11:00", "12:50", "Sejarah Sosial",                              "A", "MKU.225", [_AMRULLAH, _FAJAR]),
    ("Rabu",   "13:00", "14:40", "Historiografi Umum",                          "A", "R.212",   [_SURIADI, _MUSLIMIN]),
    ("Rabu",   "13:00", "14:40", "Sejarah Sosial",                              "B", "R.324",   [_AMRULLAH, _FAJAR]),
    ("Rabu",   "14:30", "16:10", "Ruang Kota Dalam Modernitas Kolonial & Pascakolonial", "A", "R.212", [_ILHAM, _IDA]),
    ("Rabu",   "14:30", "16:10", "Sejarah Penguasaan dan Pengamanan Laut",      "B", "R.211",   [_DIAS, _RASYID]),

    # ===== KAMIS =====
    ("Kamis",  "07:30", "09:10", "Sejarah Peradaban Islam",                     "A", "R.212",   [_RASYID, _NASIHIN]),
    ("Kamis",  "07:30", "09:10", "Teori dan Metodologi Sejarah",                "A", "MKU.225", [_ILHAM, _IDA]),
    ("Kamis",  "07:30", "09:10", "Sejarah Asia dan Samudera Hindia",            "A", "R.324",   [_DIAS, _MUSLIMIN]),
    ("Kamis",  "09:20", "11:00", "Teori dan Metodologi Sejarah",                "B", "MKU.225", [_IDA, _SURIADI]),
    ("Kamis",  "09:20", "11:00", "Sejarah Peradaban Islam",                     "B", "R.212",   [_RASYID, _BAHAR]),
    ("Kamis",  "09:20", "11:00", "Seminar Pra Skripsi",                         "B", "R.324",   [_TIM]),
    ("Kamis",  "11:00", "12:50", "Bahasa Belanda",                              "A", "MKU.225", [_NASIHIN, _SURIADI]),
    ("Kamis",  "11:00", "12:50", "Sejarah Sulawesi Selatan Modern Awal (1700-1900)", "A", "R.212", [_AMRULLAH, _SURIADI]),
    ("Kamis",  "11:00", "12:50", "Sejarah Eropa",                               "B", "R.324",   [_DIAS, _RASYID]),
    ("Kamis",  "13:00", "14:40", "Kajian Museum dan Kuratorial",                "B", "R.324",   [_MUSLIMIN, _FAJAR]),
    ("Kamis",  "13:00", "14:40", "Sejarah Daerah Perbatasan & Pulau Terpencil", "A", "R.212",   [_RASYID, _SURIADI]),
    ("Kamis",  "14:30", "16:10", "Sejarah Sulawesi Selatan Modern Awal (1700-1900)", "B", "R.212", [_AMRULLAH, _FAJAR]),
    ("Kamis",  "14:30", "16:10", "Sejarah Maritim",                             "B", "R.324",   [_IDA, _MUSLIMIN]),

    # ===== JUMAT =====
    ("Jumat",  "07:30", "09:10", "Pengantar Sejarah Publik",                    "A", "MKU.225", [_ILHAM, _MUSLIMIN]),
    ("Jumat",  "07:30", "09:10", "Sejarah Politik",                             "B", "R.212",   [_FAJAR, _SURIADI]),
    ("Jumat",  "07:30", "09:10", "Sungai dan Perkembangan Peradaban Nusantara", "A", "R.324",   [_DIAS, _MUSLIMIN]),
    ("Jumat",  "07:30", "16:00", "SKRIPSI",                                     "",  "R.324",   [_ILHAM]),
    ("Jumat",  "09:20", "11:00", "Sejarah Maritim",                             "A", "R.212",   [_IDA, _RASYID]),
    ("Jumat",  "09:20", "11:00", "Film dan Dokumentasi Sejarah",                "B", "R.324",   [_AMRULLAH, _FAJAR]),
    ("Jumat",  "09:20", "11:00", "Pengantar Sejarah Publik",                    "B", "MKU.225", [_ILHAM, _DIAS]),
    ("Jumat",  "13:00", "14:40", "Sejarah Politik",                             "A", "R.212",   [_NASIHIN, _NAHDIA]),
    ("Jumat",  "13:00", "14:40", "Sungai dan Perkembangan Peradaban Nusantara", "B", "R.324",   [_DIAS, _IDA]),
    ("Jumat",  "14:30", "16:10", "Sejarah Daerah Perbatasan & Pulau Terpencil", "B", "R.212",   [_RASYID, _SURIADI]),
    ("Jumat",  "14:30", "16:10", "Sejarah Asia dan Samudera Hindia",            "B", "R.324",   [_DIAS, _MUSLIMIN]),
    ("Jumat",  "15:30", "16:10", "Seminar Pra Skripsi",                         "A", "R.324",   [_DIAS, _NASIHIN]),
]


def get_or_create_lecturer(name, cache):
    if name in cache:
        return cache[name]
    lec = Lecturer.query.filter_by(lecturer_name=name).first()
    if not lec:
        lec = Lecturer(lecturer_name=name)
        db.session.add(lec)
        db.session.flush()
        print(f"  [NEW] Dosen baru: '{name}'")
    cache[name] = lec
    return lec


with app.app_context():
    semester = Semester.query.filter(Semester.name.ilike("%Ganjil%")).first()
    if not semester:
        print("ERROR: Semester Ganjil tidak ditemukan!")
        sys.exit(1)
    print(f"Semester : {semester.name} (ID:{semester.id})\n")

    room_cache = {r.room_code: r for r in Room.query.all()}
    lecturer_cache = {}
    course_cache = {}
    added = 0
    missing_rooms = set()

    for day, start, end, course_name, class_name, room_key, lecturer_names in SCHEDULES:
        db_code = ROOM_CODE_MAP.get(room_key)
        if not db_code:
            print(f"  [SKIP] Room key tidak ada di map: '{room_key}'")
            missing_rooms.add(room_key)
            continue

        room = room_cache.get(db_code)
        if not room:
            print(f"  [SKIP] Ruang tidak ditemukan di DB: '{db_code}'")
            missing_rooms.add(db_code)
            continue

        # Get or create course
        course_key = course_name
        if course_key not in course_cache:
            course = Course.query.filter_by(course_name=course_name).first()
            if not course:
                course = Course(course_name=course_name)
                db.session.add(course)
                db.session.flush()
                print(f"  [NEW] Mata kuliah baru: '{course_name}'")
            course_cache[course_key] = course
        course_ref = course_cache[course_key]

        start_time = dt.time(*map(int, start.split(":")))
        end_time   = dt.time(*map(int, end.split(":")))

        schedule = ClassSchedule(
            semester_id=semester.id,
            room_id=room.id,
            course_id=course_ref.id,
            class_name=class_name,
            day_name=day,
            start_time=start_time,
            end_time=end_time,
        )
        db.session.add(schedule)
        db.session.flush()

        for lec_name in lecturer_names:
            lec = get_or_create_lecturer(lec_name, lecturer_cache)
            schedule.lecturers.append(lec)

        added += 1

    db.session.commit()

    total = ClassSchedule.query.count()
    print(f"\n{'='*55}")
    print(f"Selesai: {added} jadwal Ilmu Sejarah berhasil ditambahkan.")
    if missing_rooms:
        print(f"Ruang tidak ditemukan: {missing_rooms}")
    print(f"Total jadwal di DB: {total}")
