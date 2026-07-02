"""
Seed jadwal kelas FIB Mandarin ke Semester Ganjil 2025/2026.
Jalankan: python seed_fib_schedules.py
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
    "PBM FIB":    "PBM-FIB",
    "R.203":      "R.203",
    "R.204":      "R.204",
    "R.217":      "R.217",
}

# ---------------------------------------------------------------------------
# Data jadwal
# format: (day, start, end, course_name, class_name, room_key, [lecturer_names])
# lecturer_names harus PERSIS sama dengan nama di DB
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ────────────── SENIN ──────────────
    # 07:30 - 09:00
    ("Senin", "07:30", "09:00", "Bahasa Mandarin Komprehensif Dasar 1",       "Kls 2025 A",        "PBM FIB",
     ["Wa Ode Sitti Hardianti Halidun, S.S., M.A.", "Shen Su Jia"]),
    ("Senin", "07:30", "09:00", "Budaya Dalam Karya Sastra Tiongkok",          "Kls 2023",          "R.203",
     ["Fakhriawan Fathu Rahman, S.S., M.Litt.", "Prof. Wan Wen Bin"]),
    ("Senin", "07:30", "09:00", "Pengantar Ilmu Sastra",                       "Kls 2025 C",        "R.204",
     ["Rezky Ramadhani, S.S., M.Litt.", "Ilham, S.S., M.Hum."]),
    # 09:10 - 10:40
    ("Senin", "09:10", "10:40", "Kritik Sastra",                               "Kls 2023 A",        "R.203",
     ["Khairil Anwar, S.S., M.A.", "Prof. Wan Wen Bin"]),
    ("Senin", "09:10", "10:40", "Bahasa Mandarin Komprehensif Dasar 1",        "Kls 2025 B",        "PBM FIB",
     ["Wa Ode Sitti Hardianti Halidun, S.S., M.A.", "Shen Su Jia"]),
    ("Senin", "09:10", "10:40", "Fonetik Fonologi Bahasa Mandarin Modern",     "Kls 2025 A",        "R.204",
     ["Leni Cahyati, S.S., M.CIE.", "Andi Filsah Muslimat, S.S., M.Hum."]),
    # 10:50 - 12:20
    ("Senin", "10:50", "12:20", "Masyarakat dan Kebudayaan Tiongkok di Dunia", "Kls 2024 A",        "PBM FIB",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Wa Ode Sitti Hardianti Halidun, S.S., M.A."]),
    ("Senin", "10:50", "12:20", "Fonetik Fonologi Bahasa Mandarin Modern",     "Kls 2025 B",        "R.203",
     ["Leni Cahyati, S.S., M.CIE.", "Andi Filsah Muslimat, S.S., M.Hum."]),
    ("Senin", "10:50", "12:20", "Kritik Sastra",                               "Kls 2023 B",        "R.204",
     ["Khairil Anwar, S.S., M.A.", "Prof. Wan Wen Bin"]),
    # 12:50 - 14:20
    ("Senin", "12:50", "14:20", "Kewirausahaan",                               "Kls 2024 B",        "R.203",
     ["Khairil Anwar, S.S., M.A.", "Fajar Sidiq Limola, S.S., M.Hum."]),
    ("Senin", "12:50", "14:20", "Fonetik Fonologi Bahasa Mandarin Modern",     "Kls 2025 C",        "R.204",
     ["Dr. Ikhwan Sumantri, M.Hum.", "Asmuliyati Nahnu, S.S., M.CIE."]),
    ("Senin", "12:50", "14:20", "Strategi HSK & HSKK",                        "Kls 2023 A",        "PBM FIB",
     ["Leni Cahyati, S.S., M.CIE."]),
    # 14:30 - 16:00
    ("Senin", "14:30", "16:00", "Bahasa Mandarin Komprehensif Dasar 1",        "Kls 2025 C",        "R.203",
     ["Asmuliyati Nahnu, S.S., M.CIE."]),
    ("Senin", "14:30", "16:00", "Kewirausahaan",                               "Kls 2024 A",        "R.204",
     ["Khairil Anwar, S.S., M.A.", "Fajar Sidiq Limola, S.S., M.Hum."]),
    ("Senin", "14:30", "16:00", "Strategi HSK & HSKK",                        "Kls 2023 B",        "PBM FIB",
     ["Leni Cahyati, S.S., M.CIE."]),

    # ────────────── SELASA ──────────────
    # 07:30 - 09:00
    ("Selasa", "07:30", "09:00", "Bacaan Pilihan Kesusastraan Modern",          "Kls 2024 B",        "R.203",
     ["Khairil Anwar, S.S., M.A.", "Prof. Wan Wen Bin", "Prof. Wu Xiao Ling"]),
    ("Selasa", "07:30", "09:00", "Penulisan Akademik",                          "Kls 2023 B",        "R.204",
     ["Prof. Dr. Munira Hasjim, S.S., M.Hum."]),
    ("Selasa", "07:30", "09:00", "Sintaksis Bahasa Mandarin Modern",            "Kls 2024 A",        "PBM FIB",
     ["Wa Ode Sitti Hardianti Halidun, S.S., M.A.", "Shen Su Jia", "Prof. Wu Xiao Ling"]),
    # 09:10 - 10:40
    ("Selasa", "09:10", "10:40", "Bacaan Pilihan Kesusastraan Modern",          "Kls 2024 A",        "R.203",
     ["Fakhriawan Fathu Rahman, S.S., M.Litt.", "Prof. Wan Wen Bin"]),
    ("Selasa", "09:10", "10:40", "Filsafat China",                              "Kls 2024 B",        "R.204",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Ilham, S.S., M.Hum.", "Prof. Wu Xiao Ling"]),
    ("Selasa", "09:10", "10:40", "Penulisan Akademik",                          "Kls 2023 A",        "PBM FIB",
     ["Dra. Ria Rosdiana Jubhari, M.A., Ph.D."]),
    # 10:50 - 12:20
    ("Selasa", "10:50", "12:20", "Metode Penelitian Kebudayaan",                "Kls 2023",          "R.203",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Dr. Andi Faisal, S.S., M.Hum."]),
    ("Selasa", "10:50", "12:20", "Menyimak & Bercakap Bahasa Mandarin Dasar 1","Kls 2025 A",        "PBM FIB",
     ["Rizqi Awalia Ilma, S.S., M.TCSOL.", "Chen Dandan"]),
    ("Selasa", "10:50", "12:20", "Filsafat China",                              "Kls 2024 A",        "R.204",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Ilham, S.S., M.Hum.", "Prof. Wu Xiao Ling"]),
    # 12:50 - 14:20
    ("Selasa", "12:50", "14:20", "Metode Pembelajaran Bahasa Mandarin",         "Kls 2023",          "PBM FIB",
     ["Leni Cahyati, S.S., M.CIE.", "Nirdayanti M., S.S., M.CIE."]),
    ("Selasa", "12:50", "14:20", "Membaca & Menulis Karakter Mandarin 1",       "Kls 2025 A",        "R.204",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Khafifa Fuji Lestari, S.Pd., M.Ed."]),
    ("Selasa", "12:50", "14:20", "Menyimak & Bercakap Bahasa Mandarin Dasar 1","Kls 2025 C",        "R.203",
     ["Asmuliyati Nahnu, S.S., M.CIE."]),
    # 14:30 - 16:00
    ("Selasa", "14:30", "16:00", "Menyimak & Bercakap Bahasa Mandarin Dasar 1","Kls 2025 B",        "R.204",
     ["Rizqi Awalia Ilma, S.S., M.TCSOL.", "Chen Dandan"]),
    ("Selasa", "14:30", "16:00", "Membaca & Menulis Karakter Mandarin 1",       "Kls 2025 C",        "R.203",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Asmuliyati Nahnu, S.S., M.CIE."]),
    ("Selasa", "14:30", "16:00", "Menulis Bahasa Mandarin Lanjutan",            "Kls 2023 B",        "PBM FIB",
     ["Wa Ode Sitti Hardianti Halidun, S.S., M.A.", "Khafifa Fuji Lestari, S.Pd., M.Ed."]),

    # ────────────── RABU ──────────────
    # 07:30 - 09:00
    ("Rabu", "07:30", "09:00", "Metode Penelitian Sastra",                      "Kls 2023",          "R.204",
     ["Fakhriawan Fathu Rahman, S.S., M.Litt.", "Dr. Inriati Lewa, M.Hum."]),
    ("Rabu", "07:30", "09:00", "Pengantar Ilmu Sastra",                         "Kls 2025 B",        "PBM FIB",
     ["Rezky Ramadhani, S.S., M.Litt.", "Ilham, S.S., M.Hum."]),
    ("Rabu", "07:30", "09:00", "Metode Penelitian Linguistik",                  "Kls 2023",          "R.203",
     ["Andi Filsah Muslimat, S.S., M.Hum.", "Prof. Dr. Munira Hasjim, S.S., M.Hum."]),
    # 09:10 - 10:40
    ("Rabu", "09:10", "10:40", "Menulis Bahasa Mandarin Menengah 1",            "Kls 2024 A",        "R.203",
     ["Rizqi Awalia Ilma, S.S., M.TCSOL.", "Yunita Tetta Dendo, S.S., M.CIE."]),
    ("Rabu", "09:10", "10:40", "Geografi dan Kebudayaan Tiongkok",              "Kls 2024 B",        "R.204",
     ["Leni Cahyati, S.S., M.CIE.", "Erwin Mansyur Ugu Saraka, S.S., M.Sc."]),
    ("Rabu", "09:10", "10:40", "Menulis Bahasa Mandarin Lanjutan",              "Kls 2023 A",        "PBM FIB",
     ["Erwin Mansyur Ugu Saraka, S.S., M.Sc.", "Wa Ode Sitti Hardianti Halidun, S.S., M.A.",
      "Khafifa Fuji Lestari, S.Pd., M.Ed."]),
    # 10:50 - 12:20
    ("Rabu", "10:50", "12:20", "Menulis Bahasa Mandarin Menengah 1",            "Kls 2024 B",        "R.203",
     ["Rizqi Awalia Ilma, S.S., M.TCSOL.", "Yunita Tetta Dendo, S.S., M.CIE."]),
    ("Rabu", "10:50", "12:20", "Geografi dan Kebudayaan Tiongkok",              "Kls 2024 B",        "R.204",
     ["Leni Cahyati, S.S., M.CIE.", "Erwin Mansyur Ugu Saraka, S.S., M.Sc."]),
    # 12:50 - 14:20
    ("Rabu", "12:50", "14:20", "Bahasa Mandarin Komprehensif Dasar 1",          "Kls 2024 B",        "R.203",
     ["Khafifa Fuji Lestari, S.Pd., M.Ed.", "Yunita Tetta Dendo, S.S., M.CIE."]),
    ("Rabu", "12:50", "14:20", "Analisis Wacana",                               "Kls 2023 A",        "R.204",
     ["Andi Filsah Muslimat, S.S., M.Hum.", "Khairil Anwar, S.S., M.A."]),
    ("Rabu", "12:50", "14:20", "Membaca Bahasa Mandarin Menengah 1",            "Kls 2024 A",        "PBM FIB",
     ["Leni Cahyati, S.S., M.CIE.", "Rizqi Awalia Ilma, S.S., M.TCSOL."]),
    # 14:30 - 16:00
    ("Rabu", "14:30", "16:00", "Bahasa Mandarin Komprehensif Dasar 1",          "Kls 2024 A",        "R.203",
     ["Khairil Anwar, S.S., M.A.", "Fajar Sidiq Limola, S.S., M.Hum."]),
    ("Rabu", "14:30", "16:00", "Analisis Wacana",                               "Kls 2023 B",        "R.204",
     ["Andi Filsah Muslimat, S.S., M.Hum.", "Khairil Anwar, S.S., M.A."]),
    ("Rabu", "14:30", "16:00", "Membaca Bahasa Mandarin Menengah 1",            "Kls 2024 B",        "PBM FIB",
     ["Leni Cahyati, S.S., M.CIE.", "Rizqi Awalia Ilma, S.S., M.TCSOL."]),

    # ────────────── KAMIS ──────────────
    # 07:30 - 09:00
    ("Kamis", "07:30", "09:00", "Rancangan Pembelajaran Bahasa Mandarin",       "Kls 2024 B",        "R.203",
     ["Andi Filsah Muslimat, S.S., M.Hum.", "Zhu Tong Xin"]),
    ("Kamis", "07:30", "09:00", "Pengantar Ilmu Sastra",                        "Kls 2025 A",        "R.204",
     ["Rezky Ramadhani, S.S., M.Litt.", "Ilham, S.S., M.Hum."]),
    ("Kamis", "07:30", "09:00", "Membaca Bahasa Mandarin Lanjutan",             "Kls 2023 B",        "PBM FIB",
     ["Fakhriawan Fathu Rahman, S.S., M.Litt.", "Yunita Tetta Dendo, S.S., M.CIE."]),
    # 09:10 - 10:40
    ("Kamis", "09:10", "10:40", "Komputerisasi Hanzi",                          "Kls 2024 A",        "R.203",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Wa Ode Sitti Hardianti Halidun, S.S., M.A."]),
    ("Kamis", "09:10", "10:40", "Membaca Bahasa Mandarin Lanjutan",             "Kls 2023 A",        "PBM FIB",
     ["Fakhriawan Fathu Rahman, S.S., M.Litt.", "Yunita Tetta Dendo, S.S., M.CIE."]),
    # 10:50 - 12:10
    ("Kamis", "10:50", "12:10", "Membaca & Menulis Karakter Mandarin 1",        "Kls 2025 B",        "R.203",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Khafifa Fuji Lestari, S.Pd., M.Ed."]),
    ("Kamis", "10:50", "12:10", "Pengantar Linguistik Umum",                    "Kls 2025 C",        "R.204",
     ["Dr. Ikhwan Sumantri, M.Hum."]),
    ("Kamis", "10:50", "12:10", "Bahasa Mandarin Komprehensif Dasar 1",         "Kls Qu Wei Hanyu",  "PBM FIB",
     ["Zhu Tong Xin", "Dian Sari Unga Waru, S.S., M.TCSOL.", "Chen Dandan"]),
    # 12:50 - 14:20
    ("Kamis", "12:50", "14:20", "Rancangan Pembelajaran Bahasa Mandarin",       "Kls 2024 A",        "R.204",
     ["Andi Filsah Muslimat, S.S., M.Hum.", "Zhu Tong Xin"]),
    ("Kamis", "12:50", "14:20", "Komputerisasi Hanzi",                          "Kls 2024 B",        "R.203",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Wa Ode Sitti Hardianti Halidun, S.S., M.A."]),
    ("Kamis", "12:50", "14:20", "Menyimak & Bercakap Bahasa Mandarin Lanjutan","Kls 2023 B",        "PBM FIB",
     ["Rizqi Awalia Ilma, S.S., M.TCSOL.", "Chen Dandan"]),
    # 14:30 - 16:00
    ("Kamis", "14:30", "16:00", "Masyarakat dan Kebudayaan Indonesia",          "Kls 2025 B",        "R.217",
     ["Andi Tenri Bali Baso, S.S., M.Hum.", "Khairil Anwar, S.S., M.A."]),
    ("Kamis", "14:30", "16:00", "Masyarakat dan Kebudayaan Tiongkok di Dunia",  "Kls 2024 B",        "R.203",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Wa Ode Sitti Hardianti Halidun, S.S., M.A."]),
    ("Kamis", "15:15", "17:30", "Menyimak & Bercakap Bahasa Mandarin Lanjutan","Kls 2023 A",        "PBM FIB",
     ["Rizqi Awalia Ilma, S.S., M.TCSOL.", "Chen Dandan"]),

    # ────────────── JUMAT ──────────────
    # 07:30 - 09:00
    ("Jumat", "07:30", "09:00", "Sintaksis Bahasa Mandarin Modern",             "Kls 2024 B",        "PBM FIB",
     ["Wa Ode Sitti Hardianti Halidun, S.S., M.A.", "Shen Su Jia"]),
    ("Jumat", "07:30", "09:00", "Komunikasi Lintas Budaya",                     "Kls 2023",          "R.203",
     ["Dian Sari Unga Waru, S.S., M.TCSOL.", "Dr. Karmila Mokoginta, S.S., M.Hum."]),
    ("Jumat", "07:30", "09:00", "Pengantar Linguistik Umum",                    "Kls 2025 A",        "R.204",
     ["Andi Filsah Muslimat, S.S., M.Hum.", "Dr. Ery Iswary, M.Hum."]),
    # 09:10 - 10:40
    ("Jumat", "09:10", "10:40", "Pengantar Linguistik Umum",                    "Kls 2025 B",        "R.204",
     ["Andi Filsah Muslimat, S.S., M.Hum.", "Dr. Ery Iswary, M.Hum."]),
    ("Jumat", "09:10", "10:40", "Bahasa Mandarin Komprehensif Lanjutan",        "Kls 2023 A",        "PBM FIB",
     ["Zhu Tong Xin", "Khafifa Fuji Lestari, S.Pd., M.Ed.", "Leni Cahyati, S.S., M.CIE."]),
    ("Jumat", "09:10", "10:40", "Seminar Pra Skripsi",                          None,                "R.203",
     ["Dian Sari Unga Waru, S.S., M.TCSOL."]),
    # 13:00 - 14:30
    ("Jumat", "13:00", "14:30", "Masyarakat dan Kebudayaan Indonesia",          "Kls 2025 B",        "R.204",
     ["Andi Tenri Bali Baso, S.S., M.Hum.", "Khairil Anwar, S.S., M.A."]),
    ("Jumat", "13:00", "14:30", "Menyimak & Bercakap Bahasa Mandarin Menengah 1","Kls 2024 A",      "R.203",
     ["Rizqi Awalia Ilma, S.S., M.TCSOL.", "Nirdayanti M., S.S., M.CIE."]),
    ("Jumat", "13:00", "14:30", "Bahasa Mandarin Komprehensif Lanjutan",        "Kls 2023 B",        "PBM FIB",
     ["Zhu Tong Xin", "Khafifa Fuji Lestari, S.Pd., M.Ed.", "Leni Cahyati, S.S., M.CIE."]),
    # 15:40 - 17:10
    ("Jumat", "15:40", "17:10", "Masyarakat dan Kebudayaan Indonesia",          "Kls 2025 A",        "R.204",
     ["Andi Tenri Bali Baso, S.S., M.Hum.", "Khairil Anwar, S.S., M.A."]),
    ("Jumat", "15:40", "17:10", "Menyimak & Bercakap Bahasa Mandarin Menengah 1","Kls 2024 B",      "R.203",
     ["Rizqi Awalia Ilma, S.S., M.TCSOL.", "Nirdayanti M., S.S., M.CIE."]),

    # ────────────── SABTU ──────────────
    ("Sabtu", "09:00", "11:00", "Skripsi",                                      None,                "R.204",
     ["Dian Sari Unga Waru, S.S., M.TCSOL."]),
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
        # Cari room
        room_code = ROOM_CODE_MAP.get(room_key, room_key)
        room = room_cache.get(room_code)
        if not room:
            missing_rooms.add(f"{room_key!r} (code={room_code!r})")
            continue

        # Cari / buat course
        if course_name not in course_cache:
            course = Course.query.filter(Course.course_name.ilike(course_name)).first()
            if not course:
                course = Course(course_name=course_name)
                db.session.add(course)
                db.session.flush()
                print(f"  [NEW] Mata kuliah baru: {course_name!r}")
            course_cache[course_name] = course
        course = course_cache[course_name]

        # Buat jadwal
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

        # Assign dosen
        lecturers = [get_or_create_lecturer(n, lecturer_cache) for n in lec_names]
        sched.lecturers = lecturers
        added += 1

    db.session.commit()

    print(f"\n{'='*50}")
    print(f"Selesai: {added} jadwal berhasil ditambahkan.")
    if missing_rooms:
        print(f"WARNING - Room tidak ditemukan: {missing_rooms}")
