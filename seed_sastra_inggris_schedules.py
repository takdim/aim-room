"""
Seed jadwal kelas Prodi Sastra Inggris ke Semester Ganjil 2025/2026.
Jalankan: python seed_sastra_inggris_schedules.py

Catatan entri yang dilewati (tidak ada info ruang di jadwal asli):
- RABU  09:10-10:40 : Pengantar Linguistik Terapan Kls A–F (6 kelas paralel)
- RABU  10:50-12:20 : Menyimak & Berbicara Kls A–F (sesi pertemuan kedua)
- KAMIS 09:10-10:40 : Menulis Esai Argumentatif Kls A–C (sesi pertemuan kedua)
- KAMIS 14:30-16:00 : Penerjemahan & Penjurubahasaan Kls A–C (sesi pertemuan kedua)
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
    "R.215":       "R.215",        # FIB.215
    "SIL.1":       "SIL.1",        # R.101 Gedung TML G
    "SIL.2":       "SIL.2",        # R.102 Gedung TML G
    "SIL.3":       "SIL.3",        # R.103 Gedung TML G
    "R.213-R.214": "R.213-R.214",  # Ruang Gabungan
    "MKU.213":     "MKU.213",      # R.213 (MKU)
}

# ---------------------------------------------------------------------------
# Alias dosen – nama persis dari DB
# ---------------------------------------------------------------------------
_HASYIM        = "Drs. Husain Hasyim, M.Hum."
_FATHU         = "Prof. Dr. Fathu Rahman, M.Hum."
_AINUN         = "Ainun Fatimah, S.S., M.Hum."
_RIDHA         = "Muh. Ridha Anugrah, S.S., M.Hum."
_BURHAN_KADIR  = "Burhan Kadir, S.S., M.A."
_MHASYIM       = "Prof. Dr. Muhammad Hasyim, M.Si."
_WAHYUDDIN     = "Dr. Wahyuddin, S.S., M.Hum."
_NASMILAH      = "Prof. Dr. Nasmilah, M.Hum."
_PRATIWI       = "Dr. Pratiwi Bahar, S.S., M.Hum."
_REZKY         = "Rezky Ramadhani, S.S., M.Litt."
_KARMILA       = "Dr. Karmila Mokoginta, S.S., M.Hum."
_WARDATUL      = "Andi Wardatul Wahidah Lufini, S.Pd., M.A."
_SAHRAENY      = "Dr. Sitti Sahraeny, S.S., M.Hum."
_DIAN          = "Dian Rahmawati Arief, S.S., M.Hum."
_INAYAH        = "Andi Inayah Soraya, S.S., M.Hum."
_HIDAYAT       = "Hidayatullah Yunus, S.S., M.TESOL."
_MARLENY       = "Dra. Marleny Rajuni, M.Ed."
_KHAERUDDIN    = "Khaeruddin, M.Hum., Ph.D."
_NADIRA        = "Dra. Nadira Mahaseng, M.Ed."
_MULYANI       = "Dr. Mulyani, S.Pd., M.Pd."
_KAMSINAH      = "Prof. Dr. Kamsinah, M.Hum."
_SIMON         = "Drs. Simon Sitoto, M.A."
_RIA           = "Dra. Ria Rosdiana Jubhari, M.A., Ph.D."
_AMIR          = "Prof. Dr. M. Amir P., M.Hum."
_AYUB          = "Dr. Ayub Khan, M.Si."
_NOER          = "Prof. Dr. Noer Jihad Saleh, M.Hum."
_ABIDIN        = "Dr. Abidin Pammu, M.A."
_HAKIM         = "Prof. Dr. Abdul Hakim, M.Hum."
_ABBAS         = "Dr. Abbas, S.S., M.Hum."
_BURHAN_ARAFAH = "Prof. Drs. Burhanuddin Arafah, M.Hum., Ph.D."
_HERAWATY      = "Prof. Dr. Herawaty, M.Hum., Ph.D."
_HARLINAH      = "Prof. Dr. Harlinah Sahib, M.Hum."
_SUKMAWATY     = "Dr. Sukmawaty, M.Hum."

# ---------------------------------------------------------------------------
# Data jadwal: (hari, start, end, course_name, class_name, room_key, [dosen])
# ---------------------------------------------------------------------------
SCHEDULES = [
    # ═══════════════════════════ SENIN ═══════════════════════════
    # 07:30 – 09:00
    ("Senin", "07:30", "09:00", "Morfologi Bahasa Inggris",                  None,       "R.215",       [_HASYIM]),
    ("Senin", "07:30", "09:00", "Kewirausahaan",                             "Kls A",    "SIL.1",       [_FATHU, _AINUN]),
    ("Senin", "07:30", "09:00", "Kewirausahaan",                             "Kls B",    "SIL.2",       [_RIDHA]),
    ("Senin", "07:30", "09:00", "Kewirausahaan",                             "Kls C",    "R.213-R.214", [_BURHAN_KADIR]),
    ("Senin", "07:30", "09:00", "Kewirausahaan",                             "Kls D",    "SIL.3",       [_MHASYIM, _WAHYUDDIN]),
    # 09:10 – 10:40
    ("Senin", "09:10", "10:40", "Teori Berpikir Kritis",                     "Kls A",    "SIL.3",       [_NASMILAH, _PRATIWI]),
    ("Senin", "09:10", "10:40", "Teori Berpikir Kritis",                     "Kls B",    "SIL.1",       [_REZKY]),
    ("Senin", "09:10", "10:40", "Teori Berpikir Kritis",                     "Kls C",    "SIL.2",       [_KARMILA]),
    ("Senin", "09:10", "10:40", "Teori Berpikir Kritis",                     "Kls D",    "R.215",       [_RIDHA, _WARDATUL]),
    ("Senin", "09:10", "10:40", "Teori Berpikir Kritis",                     "Kls E",    "MKU.213",     [_SAHRAENY, _DIAN]),
    ("Senin", "09:10", "10:40", "Teori Berpikir Kritis",                     "Kls F",    "R.213-R.214", [_INAYAH]),
    # 10:50 – 12:20
    ("Senin", "10:50", "12:20", "Menyimak dan Berbicara B. Inggris",         "Kls A",    "R.213-R.214", [_HIDAYAT, _AINUN]),
    ("Senin", "10:50", "12:20", "Menyimak dan Berbicara B. Inggris",         "Kls B",    "SIL.1",       [_REZKY, _MARLENY]),
    ("Senin", "10:50", "12:20", "Menyimak dan Berbicara B. Inggris",         "Kls C",    "SIL.2",       [_KHAERUDDIN, _RIDHA]),
    ("Senin", "10:50", "12:20", "Menyimak dan Berbicara B. Inggris",         "Kls D",    "SIL.3",       [_DIAN, _NADIRA]),
    ("Senin", "10:50", "12:20", "Menyimak dan Berbicara B. Inggris",         "Kls E",    "R.215",       [_INAYAH, _MULYANI]),
    ("Senin", "10:50", "12:20", "Menyimak dan Berbicara B. Inggris",         "Kls F",    "MKU.213",     [_WARDATUL, _PRATIWI]),
    # 12:50 – 14:20
    ("Senin", "12:50", "14:20", "Struktur B. Inggris Lanjutan",              "Kls A",    "SIL.1",       [_HASYIM, _WARDATUL]),
    ("Senin", "12:50", "14:20", "Struktur B. Inggris Lanjutan",              "Kls B",    "SIL.2",       [_KAMSINAH]),
    ("Senin", "12:50", "14:20", "Struktur B. Inggris Lanjutan",              "Kls C",    "SIL.3",       [_SIMON]),
    ("Senin", "12:50", "14:20", "Teknologi Dalam Pembelajaran B. Inggris",   None,       "R.213-R.214", [_RIA, _HIDAYAT]),
    ("Senin", "12:50", "14:20", "Telaah Prosa Inggris",                      None,       "SIL.1",       [_AMIR, _INAYAH]),
    # 14:30 – 16:00
    ("Senin", "14:30", "16:00", "Komunikasi Lintas Budaya",                  "Kls A",    "SIL.1",       [_AYUB]),
    ("Senin", "14:30", "16:00", "Komunikasi Lintas Budaya",                  "Kls B",    "SIL.2",       [_NOER]),
    ("Senin", "14:30", "16:00", "Komunikasi Lintas Budaya",                  "Kls C",    "SIL.3",       [_KARMILA]),
    ("Senin", "14:30", "16:00", "Antropolinguistik",                         None,       "R.213-R.214", [_HARLINAH, _SIMON]),
    ("Senin", "14:30", "16:00", "Metodologi Penelitian Pengajaran Bahasa",   None,       "R.215",       [_ABIDIN, _MULYANI]),

    # ═══════════════════════════ SELASA ══════════════════════════
    # 07:30 – 09:00  – Pengantar Ilmu Sastra Kls A–F paralel
    ("Selasa", "07:30", "09:00", "Pengantar Ilmu Sastra",                    "Kls A",    "R.213-R.214", [_ABBAS]),
    ("Selasa", "07:30", "09:00", "Pengantar Ilmu Sastra",                    "Kls B",    "SIL.1",       [_BURHAN_ARAFAH]),
    ("Selasa", "07:30", "09:00", "Pengantar Ilmu Sastra",                    "Kls C",    "SIL.2",       [_AMIR]),
    ("Selasa", "07:30", "09:00", "Pengantar Ilmu Sastra",                    "Kls D",    "SIL.3",       [_HERAWATY]),
    ("Selasa", "07:30", "09:00", "Pengantar Ilmu Sastra",                    "Kls E",    "MKU.213",     [_REZKY]),
    ("Selasa", "07:30", "09:00", "Pengantar Ilmu Sastra",                    "Kls F",    "R.215",       [_INAYAH]),
    # 09:10 – 10:40
    ("Selasa", "09:10", "10:40", "Tata Bahasa Sistemik Fungsional",          "Kls A",    "R.213-R.214", [_HAKIM, _RIDHA]),
    ("Selasa", "09:10", "10:40", "Tata Bahasa Sistemik Fungsional",          "Kls B",    "R.215",       [_SIMON, _WARDATUL]),
    ("Selasa", "09:10", "10:40", "Menulis Esai Argumentatif",                "Kls A",    "SIL.1",       [_RIA]),
    ("Selasa", "09:10", "10:40", "Menulis Esai Argumentatif",                "Kls B",    "SIL.2",       [_KARMILA, _DIAN]),
    ("Selasa", "09:10", "10:40", "Menulis Esai Argumentatif",                "Kls C",    "SIL.3",       [_NASMILAH, _MULYANI]),
    # 10:50 – 12:20  – Pengantar Linguistik Umum Kls A–F paralel
    ("Selasa", "10:50", "12:20", "Pengantar Linguistik Umum",                "Kls A",    "R.215",       [_KAMSINAH]),
    ("Selasa", "10:50", "12:20", "Pengantar Linguistik Umum",                "Kls B",    "SIL.1",       [_HAKIM]),
    ("Selasa", "10:50", "12:20", "Pengantar Linguistik Umum",                "Kls C",    "SIL.2",       [_NOER, _WARDATUL]),
    ("Selasa", "10:50", "12:20", "Pengantar Linguistik Umum",                "Kls D",    "SIL.3",       [_HARLINAH]),
    ("Selasa", "10:50", "12:20", "Pengantar Linguistik Umum",                "Kls E",    "R.213-R.214", [_AYUB]),
    ("Selasa", "10:50", "12:20", "Pengantar Linguistik Umum",                "Kls F",    "MKU.213",     [_MULYANI, _DIAN]),
    # 12:50 – 14:20
    ("Selasa", "12:50", "14:20", "Sosiologi Sastra",                         None,       "R.215",       [_ABBAS]),
    ("Selasa", "12:50", "14:20", "Penerjemahan & Penjurubahasaan",           "Kls A",    "SIL.1",       [_NOER, _RIDHA]),
    ("Selasa", "12:50", "14:20", "Penerjemahan & Penjurubahasaan",           "Kls B",    "SIL.2",       [_HERAWATY, _KHAERUDDIN]),
    ("Selasa", "12:50", "14:20", "Penerjemahan & Penjurubahasaan",           "Kls C",    "SIL.3",       [_ABIDIN, _HASYIM]),
    ("Selasa", "12:50", "14:20", "Metode Penelitian Linguistik",             None,       "R.213-R.214", [_HAKIM, _PRATIWI]),
    # 14:30 – 16:00
    ("Selasa", "14:30", "16:00", "Budaya dalam Pengajaran Bahasa Inggris",   None,       "SIL.3",       [_NASMILAH]),
    ("Selasa", "14:30", "16:00", "Metodologi Penelitian Kesusastraan",       None,       "R.215",       [_HERAWATY, _ABBAS]),
    ("Selasa", "14:30", "16:00", "Fonetik dan Fonologi Bahasa Inggris",      None,       "SIL.1",       [_HAKIM, _HARLINAH]),
    ("Selasa", "14:30", "16:00", "Metodologi Penelitian Pengajaran Bahasa",  None,       "R.213-R.214", [_ABIDIN, _MULYANI]),

    # ═══════════════════════════ RABU ════════════════════════════
    # 07:30 – 09:00  – Semiologi & Literasi Digital paralel
    ("Rabu", "07:30", "09:00", "Semiologi",                                  "Kls A",    "SIL.2",       [_AMIR]),
    ("Rabu", "07:30", "09:00", "Semiologi",                                  "Kls B",    "SIL.3",       [_AYUB]),
    ("Rabu", "07:30", "09:00", "Semiologi",                                  "Kls C",    "SIL.1",       [_SIMON]),
    ("Rabu", "07:30", "09:00", "Literasi Digital",                           "Kls A",    "R.213-R.214", [_WARDATUL, _RIDHA]),
    ("Rabu", "07:30", "09:00", "Literasi Digital",                           "Kls B",    "R.215",       [_REZKY]),
    ("Rabu", "07:30", "09:00", "Literasi Digital",                           "Kls C",    "MKU.213",     [_HIDAYAT]),
    # 09:10-14:30  – Pengantar Linguistik Terapan Kls A–F: DILEWATI (tidak ada info ruang)
    # 10:50-12:20  – Menyimak & Berbicara sesi 2: DILEWATI (tidak ada info ruang)
    # 12:50 – 14:20
    ("Rabu", "12:50", "14:20", "Telaah Prosa Inggris",                       None,       "R.215",       [_AMIR, _INAYAH]),
    ("Rabu", "12:50", "14:20", "Antropolinguistik",                          None,       "R.213-R.214", [_HARLINAH, _SIMON]),
    ("Rabu", "12:50", "14:20", "Korespondensi B. Inggris",                   "Kls A",    "SIL.1",       [_HIDAYAT]),
    ("Rabu", "12:50", "14:20", "Korespondensi B. Inggris",                   "Kls B",    "SIL.2",       [_ABIDIN]),
    ("Rabu", "12:50", "14:20", "Korespondensi B. Inggris",                   "Kls C",    "SIL.3",       [_DIAN, _KHAERUDDIN]),
    # 14:30 – 16:00
    ("Rabu", "14:30", "16:00", "Teori Sastra",                               None,       "R.213-R.214", [_BURHAN_ARAFAH]),
    ("Rabu", "14:30", "16:00", "Metodologi Pengajaran Bahasa Inggris",       None,       "SIL.2",       [_ABIDIN, _SAHRAENY]),
    ("Rabu", "14:30", "16:00", "Sosiolinguistik",                            None,       "SIL.1",       [_HAKIM, _HASYIM]),
    ("Rabu", "14:30", "16:00", "Sastra Anak",                                None,       "R.215",       [_REZKY]),
    ("Rabu", "14:30", "16:00", "Praktikum Pengajaran",                       None,       "SIL.3",       [_NASMILAH]),

    # ═══════════════════════════ KAMIS ═══════════════════════════
    # 07:30 – 09:00
    ("Kamis", "07:30", "09:00", "Budaya dalam Kesusastraan Inggris",         None,       "R.213-R.214", [_ABBAS]),
    ("Kamis", "07:30", "09:00", "Analisis Wacana",                           "Kls A",    "SIL.1",       [_KARMILA]),
    ("Kamis", "07:30", "09:00", "Analisis Wacana",                           "Kls B",    "SIL.2",       [_AYUB]),
    ("Kamis", "07:30", "09:00", "Analisis Wacana",                           "Kls C",    "SIL.3",       [_FATHU]),
    # 09:10 – 10:40  – Menulis Esai sesi 2: DILEWATI (tidak ada info ruang)
    ("Kamis", "09:10", "10:40", "Metodologi Penelitian Kesusastraan",        None,       "R.215",       [_HERAWATY, _ABBAS]),
    ("Kamis", "09:10", "10:40", "Evaluasi Bahan Ajar",                       None,       "MKU.213",     [_ABIDIN, _SAHRAENY]),
    ("Kamis", "09:10", "10:40", "Pragmatik Bahasa Inggris",                  None,       "R.213-R.214", [_SUKMAWATY, _PRATIWI]),
    # 10:50 – 12:20
    ("Kamis", "10:50", "12:20", "Isu Aktual dalam Kesusastraan",             None,       "SIL.1",       [_AMIR, _REZKY]),
    ("Kamis", "10:50", "12:20", "Teknologi Dalam Pembelajaran B. Inggris",   None,       "SIL.3",       [_RIA, _HIDAYAT]),
    ("Kamis", "10:50", "12:20", "Sosiolinguistik",                           None,       "SIL.2",       [_HAKIM, _HASYIM]),
    ("Kamis", "10:50", "12:20", "Penulisan Kreatif",                         None,       "R.215",       [_INAYAH]),
    # 12:50 – 14:20
    ("Kamis", "12:50", "14:20", "Isu Aktual dalam Pengajaran B. Inggris",    None,       "R.215",       [_SAHRAENY]),
    ("Kamis", "12:50", "14:20", "Fonetik dan Fonologi Bahasa Inggris",       None,       "R.213-R.214", [_HAKIM, _HARLINAH]),
    ("Kamis", "12:50", "14:20", "Public Speaking",                           "Kls A",    "SIL.1",       [_AINUN]),
    ("Kamis", "12:50", "14:20", "Public Speaking",                           "Kls B",    "SIL.2",       [_INAYAH]),
    ("Kamis", "12:50", "14:20", "Public Speaking",                           "Kls C",    "SIL.3",       [_REZKY]),
    # 14:30 – 16:00  – Penerjemahan sesi 2: DILEWATI (tidak ada info ruang)
    ("Kamis", "14:30", "16:00", "Metode Penelitian Linguistik",              None,       "R.213-R.214", [_HAKIM, _PRATIWI]),
    ("Kamis", "14:30", "16:00", "Pengajaran Bahasa Inggris melalui Karya Sastra", None,  "R.215",       [_SAHRAENY]),

    # ═══════════════════════════ JUMAT ═══════════════════════════
    # 08:00 – 09:30  – Mata Kuliah Bahasa Asing Pilihan (tanpa dosen spesifik)
    ("Jumat", "08:00", "09:30", "Bahasa Korea",                              None,       "R.213-R.214", []),
    ("Jumat", "08:00", "09:30", "Bahasa Jepang",                             None,       "R.215",       []),
    ("Jumat", "08:00", "09:30", "Bahasa Arab",                               None,       "SIL.1",       []),
    ("Jumat", "08:00", "09:30", "Bahasa Mandarin",                           None,       "SIL.2",       []),
    ("Jumat", "08:00", "09:30", "Bahasa Perancis",                           None,       "SIL.3",       []),
    # 09:10 – 10:50  – Kewirausahaan lanjutan
    ("Jumat", "09:10", "10:50", "Kewirausahaan",                             "Kls E",    "R.213-R.214", [_BURHAN_KADIR]),
    ("Jumat", "09:10", "10:50", "Kewirausahaan",                             "Kls F",    "SIL.3",       [_AINUN]),
    ("Jumat", "09:10", "10:50", "Kewirausahaan",                             "Kls G",    "R.215",       [_MHASYIM, _WAHYUDDIN]),
    # Siang / Sore
    ("Jumat", "10:40", "14:30", "SKRIPSI",                                   None,       "SIL.1",       [_NASMILAH, _SAHRAENY]),
    ("Jumat", "11:15", "13:05", "Kewirausahaan",                             "Kls H",    "R.213-R.214", [_BURHAN_KADIR]),
    ("Jumat", "13:00", "14:30", "Kewirausahaan",                             "Kls I",    "SIL.2",       [_FATHU, _AINUN]),
    ("Jumat", "13:00", "14:30", "Kewirausahaan",                             "Kls J",    "SIL.3",       [_RIDHA]),
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
    print(f"Selesai: {added} jadwal Sastra Inggris berhasil ditambahkan.")
    if missing_rooms:
        print(f"WARNING – Ruang tidak ditemukan: {missing_rooms}")
    print(f"Total jadwal di DB: {ClassSchedule.query.count()}")
