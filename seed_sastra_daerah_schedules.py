"""
Seed jadwal kelas Prodi Sastra Daerah ke Semester Ganjil 2025/2026.
Jalankan: python seed_sastra_daerah_schedules.py
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
# Pemetaan nama ruangan ke room_code di DB
# ---------------------------------------------------------------------------
ROOM_CODE_MAP = {
    "R.323": "R.323",
    "R.217": "R.217",
    "R.224": "MKU.224",   # Gedung TML F
    "R.223": "MKU.223",   # Gedung TML F
    "R.203": "R.203",
    "R.318": "R.318",
    "R.218": "R.218",
}

# Dosen Sabtu (dipakai berulang)
_G  = "Prof. Dr. Gusnawaty, M.Hum."
_P  = "Pammuda, S.S., M.Si."

# ---------------------------------------------------------------------------
# Data jadwal
# format: (day, start, end, course_name, class_name, room_key, [lecturer_names])
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ═══════════════════════════ SENIN ═══════════════════════════
    # 07:30 - 09:00
    ("Senin", "07:30", "09:00", "Pengayaan Kurikulum Bahasa Daerah",           "Kls 5B",  "R.323",
     [_G, "Andi Tenri Bali Baso, S.S., M.Hum."]),
    ("Senin", "07:30", "09:00", "Dasar-dasar Filsafat Ilmu Sosial Budaya",     "Kls 1A",  "R.217",
     ["Dr. Muhammad Bahar Akase Teng, LCP, M.Hum.", "Burhan Kadir, S.S., M.A."]),
    ("Senin", "07:30", "09:00", "Antropolinguistik",                           "Kls 3",   "R.224",
     ["Dr. Ery Iswary, M.Hum.", "Hunaeni, S.S., M.Si."]),
    # 09:10 - 10:40
    ("Senin", "09:10", "10:40", "Tekstologi",                                  "Kls 5B",  "R.323",
     ["Prof. Dr. Nurhayati Rahman, M.S.", "Basiah, S.S., M.A."]),
    ("Senin", "09:10", "10:40", "Morfologi Bahasa Bugis-Makassar",             "Kls 3",   "R.217",
     ["Dr. M. Dalyan Tahir, M.Hum.", "Dr. Sumarlin Rengko H. R., S.S., M.Hum."]),
    ("Senin", "09:10", "10:40", "Kemahiran Menyimak dan Berbicara Bahasa Bugis","Kls 1A",  "R.224",
     ["Dr. Dafirah, M.Hum.", "Hunaeni, S.S., M.Si."]),
    # 10:50 - 12:20
    ("Senin", "10:50", "12:20", "Metodologi Pengajaran Bahasa dan Sastra",     "Kls 5B",  "R.224",
     ["Hunaeni, S.S., M.Si.", "Mutahharah Nemin Kaharuddin, S.S., M.Hum."]),
    ("Senin", "10:50", "12:20", "Komunikasi Lintas Budaya",                    "Kls 3",   "R.323",
     ["Prof. Dr. Muhlis Hadrawi, S.S., M.Hum.", _P]),
    ("Senin", "10:50", "12:20", "Semiotika",                                   "Kls 5A",  "R.217",
     ["Dr. Dafirah, M.Hum.", "Burhan Kadir, S.S., M.A."]),
    # 13:00 - 14:30
    ("Senin", "13:00", "14:30", "Kemahiran Menyimak dan Berbicara Bahasa Bugis","Kls 1B",  "R.203",
     [_G, "Andi Tenri Bali Baso, S.S., M.Hum."]),
    ("Senin", "13:00", "14:30", "Tekstologi",                                  "Kls 5A",  "R.217",
     ["Prof. Dr. Muhlis Hadrawi, S.S., M.Hum.", "Basiah, S.S., M.A."]),
    # 14:40 - 16:10
    ("Senin", "14:40", "16:10", "Dasar-dasar Filsafat Ilmu Sosial Budaya",     "Kls 1B",  "R.217",
     [_P, "Burhan Kadir, S.S., M.A."]),
    ("Senin", "14:40", "16:10", "Pengayaan Kurikulum Bahasa Daerah",           "Kls 5A",  "R.323",
     [_P, "Andi Tenri Bali Baso, S.S., M.Hum."]),
    ("Senin", "14:40", "16:10", "Magang/Praktek Kerja",                        None,      "R.223",
     [_G, _P]),

    # ═══════════════════════════ SELASA ═══════════════════════════
    # 07:30 - 09:00
    ("Selasa", "07:30", "09:00", "Leksikografi",                               "Kls 5B",  "R.323",
     [_G, "Mutahharah Nemin Kaharuddin, S.S., M.Hum."]),
    ("Selasa", "07:30", "09:00", "Pengantar Ilmu Sastra",                      "Kls 1A",  "R.217",
     ["Prof. Dr. Andi Muhammad Akhmar, S.S., M.Hum.", "Hunaeni, S.S., M.Si.",
      "Nur Syam, S.S., M.Hum."]),
    ("Selasa", "07:30", "09:00", "Kajian Puisi Bugis Makassar",                "Kls 3",   "R.224",
     ["Hunaeni, S.S., M.Si.", "Dr. Sumarlin Rengko H. R., S.S., M.Hum."]),
    # 09:10 - 10:40
    ("Selasa", "09:10", "10:40", "Metodologi Pengajaran Bahasa dan Sastra",    "Kls 5A",  "R.217",
     ["Hunaeni, S.S., M.Si.", "Mutahharah Nemin Kaharuddin, S.S., M.Hum."]),
    ("Selasa", "09:10", "10:40", "Seminar Proposal",                           None,      "R.224",
     [_G, "Prof. Dr. Andi Muhammad Akhmar, S.S., M.Hum.",
      "Prof. Dr. Muhlis Hadrawi, S.S., M.Hum.", "Dr. Ery Iswary, M.Hum."]),
    ("Selasa", "09:10", "10:40", "Pengantar Filologi",                         "Kls 1A",  "R.323",
     ["Prof. Dr. Nurhayati Rahman, M.S.", "Basiah, S.S., M.A."]),
    # 10:50 - 12:20
    ("Selasa", "10:50", "12:20", "Pengantar Filologi",                         "Kls 1B",  "R.323",
     ["Prof. Dr. Nurhayati Rahman, M.S.", "Basiah, S.S., M.A."]),
    ("Selasa", "10:50", "12:20", "Analisis Wacana Bahasa Bugis-Makassar",      "Kls 5B",  "R.224",
     ["Dr. M. Dalyan Tahir, M.Hum.", "Dr. Ery Iswary, M.Hum."]),
    ("Selasa", "10:50", "12:20", "Kajian Budaya",                              "Kls 5A",  "R.217",
     ["Prof. Dr. Andi Muhammad Akhmar, S.S., M.Hum.", _P]),
    # 13:00 - 14:30
    ("Selasa", "13:00", "14:30", "Hukum Adat Bugis-Makassar",                  "Kls 5A",  "R.323",
     ["Prof. Dr. Muhlis Hadrawi, S.S., M.Hum.", "Dr. M. Dalyan Tahir, M.Hum."]),
    ("Selasa", "13:00", "14:30", "Sosiolinguistik",                            "Kls 3",   "R.217",
     [_P, "Mutahharah Nemin Kaharuddin, S.S., M.Hum."]),
    # 14:40 - 16:10
    ("Selasa", "14:40", "16:10", "Semiotika",                                  "Kls 5B",  "R.217",
     ["Dr. Dafirah, M.Hum.", "Burhan Kadir, S.S., M.A."]),
    ("Selasa", "14:40", "16:10", "Literasi dan Presentasi Ilmiah",             None,      "R.323",
     [_G, _P]),
    ("Selasa", "14:40", "16:10", "Magang/Praktek Kerja",                       None,      "R.223",
     [_G, _P]),

    # ═══════════════════════════ RABU ═══════════════════════════
    # 07:30 - 09:00
    ("Rabu", "07:30", "09:00", "Leksikografi",                                 "Kls 5B",  "R.217",
     [_G, "Mutahharah Nemin Kaharuddin, S.S., M.Hum."]),
    ("Rabu", "07:30", "09:00", "Kemahiran Menyimak dan Berbicara Bahasa Makassar","Kls 1A","R.323",
     ["Dr. Ery Iswary, M.Hum.", "Dr. Sumarlin Rengko H. R., S.S., M.Hum.",
      "Nur Syam, S.S., M.Hum."]),
    ("Rabu", "07:30", "09:00", "Kebudayaan Maritim Bugis-Makassar",            "Kls 3",   "R.224",
     ["Prof. Dr. Nurhayati Rahman, M.S.", "Basiah, S.S., M.A."]),
    # 09:10 - 10:40
    ("Rabu", "09:10", "10:40", "Sosiologi Sastra",                             "Kls 5A",  "R.217",
     ["Prof. Dr. Andi Muhammad Akhmar, S.S., M.Hum.", "Dr. Dafirah, M.Hum."]),
    ("Rabu", "09:10", "10:40", "Pengantar La Galigo",                          "Kls 1A",  "R.323",
     ["Prof. Dr. Nurhayati Rahman, M.S.", "Basiah, S.S., M.A."]),
    # 10:50 - 12:30
    ("Rabu", "10:50", "12:30", "Pengantar La Galigo",                          "Kls 1B",  "R.323",
     ["Prof. Dr. Nurhayati Rahman, M.S.", "Basiah, S.S., M.A."]),
    ("Rabu", "10:50", "12:30", "Pariwisata Budaya",                            "Kls 5A",  "R.217",
     ["Dr. Ery Iswary, M.Hum.", "Hunaeni, S.S., M.Si."]),
    ("Rabu", "10:50", "12:30", "Magang/Praktek Kerja",                         None,      "R.223",
     [_G, _P]),
    # 13:00 - 14:30
    ("Rabu", "13:00", "14:30", "Kajian Budaya",                                "Kls 5B",  "R.323",
     ["Prof. Dr. Andi Muhammad Akhmar, S.S., M.Hum.", _P]),
    ("Rabu", "13:00", "14:30", "Kemahiran Menyimak dan Berbicara Bahasa Makassar","Kls 1B","R.217",
     ["Dr. Ery Iswary, M.Hum.", "Dr. Sumarlin Rengko H. R., S.S., M.Hum.",
      "Nur Syam, S.S., M.Hum."]),
    # 14:40 - 16:10
    ("Rabu", "14:40", "16:10", "Etika Bisnis",                                 "Kls 5B",  "R.217",
     ["Dr. M. Dalyan Tahir, M.Hum.", "Burhan Kadir, S.S., M.A."]),
    ("Rabu", "14:40", "16:10", "Terjemahan Lontara Bugis-Makassar",            "Kls 3",   "R.323",
     ["Prof. Dr. Muhlis Hadrawi, S.S., M.Hum.", "Dr. Sumarlin Rengko H. R., S.S., M.Hum."]),

    # ═══════════════════════════ KAMIS ═══════════════════════════
    # 07:30 - 09:00
    ("Kamis", "07:30", "09:00", "Analisis Wacana Bahasa Bugis-Makassar",       "Kls 5A",  "R.217",
     ["Dr. Ery Iswary, M.Hum.", "Dr. M. Dalyan Tahir, M.Hum."]),
    # 09:10 - 10:40
    ("Kamis", "09:10", "10:40", "Preservasi dan Digitalisasi Naskah Bugis-Makassar","Kls 3","R.217",
     ["Prof. Dr. Muhlis Hadrawi, S.S., M.Hum.", "Dr. Sumarlin Rengko H. R., S.S., M.Hum.",
      "Nur Syam, S.S., M.Hum."]),
    ("Kamis", "09:10", "10:40", "Etika Bisnis",                                "Kls 5B",  "R.323",
     ["Dr. M. Dalyan Tahir, M.Hum.", "Burhan Kadir, S.S., M.A."]),
    ("Kamis", "09:10", "10:40", "Pengantar Linguistik Umum",                   "Kls 1B",  "R.224",
     [_G, "Andi Tenri Bali Baso, S.S., M.Hum."]),
    # 10:50 - 12:20
    ("Kamis", "10:50", "12:20", "Tradisi Lisan Bugis-Makassar",                "Kls 3",   "R.224",
     ["Dr. Dafirah, M.Hum.", "Dr. Ery Iswary, M.Hum."]),
    ("Kamis", "10:50", "12:20", "Pengantar Linguistik Umum",                   "Kls 1A",  "R.217",
     [_G, "Andi Tenri Bali Baso, S.S., M.Hum."]),
    ("Kamis", "10:50", "12:20", "Hukum Adat Bugis-Makassar",                   "Kls 5B",  "R.323",
     ["Prof. Dr. Nurhayati Rahman, M.S.", "Basiah, S.S., M.A."]),
    # 13:00 - 14:30
    ("Kamis", "13:00", "14:30", "Penyusunan Materi Pembelajaran Bahasa Daerah","Kls 3",   "R.323",
     [_G, "Mutahharah Nemin Kaharuddin, S.S., M.Hum."]),
    ("Kamis", "13:00", "14:30", "Linguistik Bandingan Nusantara",              "Kls 5A",  "R.217",
     [_P, "Andi Tenri Bali Baso, S.S., M.Hum."]),
    ("Kamis", "13:00", "14:30", "Proyek Independen",                           None,      "R.223",
     [_G, _P]),
    # 14:40 - 16:10
    ("Kamis", "14:40", "16:10", "Pengantar Ilmu Sastra",                       "Kls 1B",  "R.217",
     ["Prof. Dr. Andi Muhammad Akhmar, S.S., M.Hum.", "Hunaeni, S.S., M.Si.",
      "Nur Syam, S.S., M.Hum."]),
    ("Kamis", "14:40", "16:10", "Pariwisata Budaya",                           "Kls 5B",  "R.323",
     ["Dr. Dafirah, M.Hum.", "Burhan Kadir, S.S., M.A."]),

    # ═══════════════════════════ JUMAT ═══════════════════════════
    # 07:30 - 09:00
    ("Jumat", "07:30", "09:00", "Pengembangan dan Penguatan Kewirausahaan",    None,      "R.323",
     [_G, _P]),
    ("Jumat", "07:30", "09:00", "Praktek Dunia Usaha/Dunia Industri",          None,      "R.224",
     [_G, _P]),
    # 09:10 - 10:40
    ("Jumat", "09:10", "10:40", "Sastra Bandingan Nusantara",                  "Kls 3",   "R.217",
     ["Dr. Dafirah, M.Hum.", "Burhan Kadir, S.S., M.A."]),
    ("Jumat", "09:10", "10:40", "Linguistik Bandingan Nusantara",              "Kls 5B",  "R.323",
     [_P, "Andi Tenri Bali Baso, S.S., M.Hum."]),
    ("Jumat", "09:10", "10:40", "Kelas Pengembangan Karakter/Komunikasi",      None,      "R.223",
     [_G, _P]),
    # 13:30 - 15:00
    ("Jumat", "13:30", "15:00", "Sosiologi Sastra",                            "Kls 5B",  "R.323",
     ["Prof. Dr. Andi Muhammad Akhmar, S.S., M.Hum.", "Dr. Dafirah, M.Hum.",
      "Nur Syam, S.S., M.Hum."]),
    ("Jumat", "13:30", "15:00", "Sintaksis Bahasa Bugis-Makassar",             "Kls 3",   "R.217",
     ["Dr. M. Dalyan Tahir, M.Hum.", "Dr. Sumarlin Rengko H. R., S.S., M.Hum."]),
    # 15:00 - 16:30
    ("Jumat", "15:00", "16:30", "Ujian Skripsi",                               None,      "R.217",
     [_G]),
    ("Jumat", "15:00", "16:30", "Riset Mandiri",                               None,      "R.323",
     [_G, _P]),
    ("Jumat", "15:00", "16:30", "Mata Kuliah Kewirausahaan/BMI/Karakter",      None,      "R.224",
     [_G, _P]),

    # ═══════════════════════════ SABTU ═══════════════════════════
    # 07:30 - 09:00
    ("Sabtu", "07:30", "09:00", "Komunikasi dan Kerjasama",                    None,      "R.323",  [_G, _P]),
    ("Sabtu", "07:30", "09:00", "Manajemen Kegiatan",                          None,      "R.318",  [_G, _P]),
    ("Sabtu", "07:30", "09:00", "Strategi Negosiasi",                          None,      "R.217",  [_G, _P]),
    ("Sabtu", "07:30", "09:00", "Komunikasi Digital",                          None,      "R.223",  [_G, _P]),
    ("Sabtu", "07:30", "09:00", "Pembelajaran Aktif",                          None,      "R.224",  [_G, _P]),
    # 09:10 - 10:40
    ("Sabtu", "09:10", "10:40", "Empati Sosial",                               None,      "R.217",  [_G, _P]),
    ("Sabtu", "09:10", "10:40", "Keberagaman Budaya",                          None,      "R.224",  [_G, _P]),
    ("Sabtu", "09:10", "10:40", "Pengembangan Masyarakat",                     None,      "R.323",  [_G, _P]),
    # 10:50 - 12:20
    ("Sabtu", "10:50", "12:20", "Kewirausahaan Rintisan",                      None,      "R.217",  [_G, _P]),
    ("Sabtu", "10:50", "12:20", "Kepemimpinan Inovatif",                       None,      "R.318",  [_G, _P]),
    ("Sabtu", "10:50", "12:20", "Pengambilan Keputusan",                       None,      "R.224",  [_G, _P]),
    # 13:00 - 14:30
    ("Sabtu", "13:00", "14:30", "Pemecahan Masalah",                           None,      "R.217",  [_G, _P]),
    ("Sabtu", "13:00", "14:30", "Etika Profesi",                               None,      "R.318",  [_G, _P]),
    ("Sabtu", "13:00", "14:30", "Berpikir Kritis dan Kreatif",                 None,      "R.323",  [_G, _P]),
    ("Sabtu", "13:00", "14:30", "Kreativitas Solutif",                         None,      "R.318",  [_G, _P]),
    # 14:40 - 16:10
    ("Sabtu", "14:40", "16:10", "Inovasi dan Pemikiran Desain",                None,      "R.318",  [_G, _P]),
    ("Sabtu", "14:40", "16:10", "Pengembangan Talenta",                        None,      "R.223",  [_G, _P]),
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
