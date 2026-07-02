"""
Update jadwal yang sudah ada dengan data dosen.
Jalankan: python seed_schedule_lecturers.py
"""
import datetime as dt
from app import create_app
from app.extensions import db
from app.models.class_schedule import ClassSchedule
from app.models.reference import Course
from app.models.lecturer import Lecturer

app = create_app()

# Format: (day, start, course_name, class_name, [lecturer_names])
SCHEDULE_LECTURERS = [
    # ── SENIN 07:30 ──
    ("Senin", "07:30", "Pengantar Perencanaan Pariwisata", "Kelas A", [
        "Dr. Supriadi, S.S., M.A.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
        "Fakhreny Fathu Rahman, S.S., M.Si.",
    ]),
    ("Senin", "07:30", "Metodologi Penelitian", None, [
        "Dr. Supriadi, S.S., M.A.",
        "Dr. Yadi Mulyadi, S.S., M.A.",
        "Dr. Hasanuddin, M.Hum.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
    ]),
    ("Senin", "07:30", "Bahasa Jepang Khusus Pariwisata", "Kelas B", [
        "Meta Sekar Puji Astuti, S.S., M.A., Ph.D.",
        "Muhammad Syachrun Sjam, S.S., M.Hum.",
    ]),
    # ── SENIN 09:10 ──
    ("Senin", "09:10", "Pariwisata Nasional dan Internasional", "Kelas A", [
        "Prof. Dr. Fathu Rahman, M.Hum.",
        "Rezky Ramadhani, S.S., M.Litt.",
    ]),
    ("Senin", "09:10", "Studi Kelayakan Pariwisata Berkelanjutan", None, [
        "Dr. Yadi Mulyadi, S.S., M.A.",
        "Rafika Hayati, S.ST.Par., M.Par.",
        "Fadhillah Duli, S.I.Kom., M.Si.",
    ]),
    ("Senin", "09:10", "Geografi Pariwisata", "Kelas A", [
        "Dr. Ilham Alimuddin, S.T., M.GIS.",
        "Drs. H. Hamris Darwis, M.Si.",
    ]),
    # ── SENIN 10:50 ──
    ("Senin", "10:50", "Teknik Pemandu Wisata", "Kelas A", [
        "Dr. Supriadi, S.S., M.A.",
        "Muhammad Syachrun Sjam, S.S., M.Hum.",
        "Fahran Reza, S.S., M.Hum.",
    ]),
    ("Senin", "10:50", "Pengelolaan Usaha Daya Tarik Wisata", None, [
        "Erwin Mansyur Ugu Saraka, S.S., M.Sc.",
        "Dr. Dirk Rukka Sandarupa, S.S., M.Hum.",
        "Indra Mayanti Noer, S.S., M.Hum.",
    ]),

    # ── SELASA 07:30 ──
    ("Selasa", "07:30", "Pengantar Filsafat", "Kelas A", [
        "Dr. Andi Faisal, S.S., M.Hum.",
        "Fahran Reza, S.S., M.Hum.",
    ]),
    ("Selasa", "07:30", "Pemasaran Pariwisata", "Kelas B", [
        "Dr. Yadi Mulyadi, S.S., M.A.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
        "Indra Mayanti Noer, S.S., M.Hum.",
    ]),
    # ── SELASA 09:10 ──
    ("Selasa", "09:10", "Pariwisata Nasional dan Internasional", "Kelas B", [
        "Erwin Mansyur Ugu Saraka, S.S., M.Sc.",
        "Dr. Dirk Rukka Sandarupa, S.S., M.Hum.",
    ]),
    ("Selasa", "09:10", "Mitigasi Bencana Berbasis Kearifan Lokal", None, [
        "Dr. Ilham Alimuddin, S.T., M.GIS.",
        "Fahran Reza, S.S., M.Hum.",
    ]),
    ("Selasa", "09:10", "Geografi Pariwisata", "Kelas B", [
        "Dr. Ilham Alimuddin, S.T., M.GIS.",
        "Drs. H. Hamris Darwis, M.Si.",
    ]),
    # ── SELASA 10:50 ──
    ("Selasa", "10:50", "Pengantar Ilmu Kepariwisataan", None, [
        "Prof. Dr. Akin Duli, M.A.",
        "Drs. H. Hamris Darwis, M.Si.",
        "Rafika Hayati, S.ST.Par., M.Par.",
    ]),
    ("Selasa", "10:50", "Teknik Pemandu Wisata", "Kelas B", [
        "Dr. Supriadi, S.S., M.A.",
        "Muhammad Syachrun Sjam, S.S., M.Hum.",
        "Fahran Reza, S.S., M.Hum.",
    ]),
    ("Selasa", "10:50", "Pemasaran Pariwisata", "Kelas A", [
        "Dr. Yadi Mulyadi, S.S., M.A.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
        "Indra Mayanti Noer, S.S., M.Hum.",
    ]),

    # ── RABU 07:30 ──
    ("Rabu", "07:30", "Sosiologi Pariwisata", "Kelas A", [
        "Dr. Muhammad Nur, S.S., M.A.",
        "Dr. Hasanuddin, M.Hum.",
    ]),
    ("Rabu", "07:30", "Bahasa Jepang Khusus Pariwisata", "Kelas A", [
        "Meta Sekar Puji Astuti, S.S., M.A., Ph.D.",
        "Indra Mayanti Noer, S.S., M.Hum.",
    ]),
    ("Rabu", "07:30", "Bisnis dan Kewirausahaan Pariwisata", "Kelas B", [
        "Dr. Dirk Rukka Sandarupa, S.S., M.Hum.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
    ]),
    # ── RABU 09:10 ──
    ("Rabu", "09:10", "Pengantar Perencanaan Pariwisata", "Kelas B", [
        "Dr. Yadi Mulyadi, S.S., M.A.",
        "Rafika Hayati, S.ST.Par., M.Par.",
        "Fadhillah Duli, S.I.Kom., M.Si.",
    ]),
    ("Rabu", "09:10", "Pariwisata Perkotaan dan MICE", "Kelas A", [
        "Yusriana, S.S., M.A.",
        "Rafika Hayati, S.ST.Par., M.Par.",
        "Nur Rahmiani Achmad, S.IP., M.M.Par.",
    ]),
    # ── RABU 10:50 ──
    ("Rabu", "10:50", "Pengantar Ilmu Kepariwisataan", None, [
        "Prof. Dr. Akin Duli, M.A.",
        "Drs. H. Hamris Darwis, M.Si.",
        "Rafika Hayati, S.ST.Par., M.Par.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
    ]),
    ("Rabu", "10:50", "Pengelolaan Usaha Akomodasi", None, [
        "Dr. Dirk Rukka Sandarupa, S.S., M.Hum.",
        "Rafika Hayati, S.ST.Par., M.Par.",
        "Fakhreny Fathu Rahman, S.S., M.Si.",
    ]),
    ("Rabu", "10:50", "Pariwisata Pedesaan", "Kelas B", [
        "Prof. Dr. Akin Duli, M.A.",
        "Drs. H. Hamris Darwis, M.Si.",
        "Dr. Dirk Rukka Sandarupa, S.S., M.Hum.",
    ]),

    # ── KAMIS 07:30 ──
    ("Kamis", "07:30", "Metodologi Penelitian", None, [
        "Dr. Supriadi, S.S., M.A.",
        "Dr. Yadi Mulyadi, S.S., M.A.",
        "Dr. Hasanuddin, M.Hum.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
    ]),
    ("Kamis", "07:30", "Bisnis dan Kewirausahaan Pariwisata", "Kelas A", [
        "Dr. Dirk Rukka Sandarupa, S.S., M.Hum.",
        "Fadhillah Duli, S.I.Kom., M.Si.",
    ]),
    ("Kamis", "07:30", "Sistem Informasi Kepariwisataan", "Kelas B", [
        "Dr. Yadi Mulyadi, S.S., M.A.",
        "Fahran Reza, S.S., M.Hum.",
        "Indra Mayanti Noer, S.S., M.Hum.",
    ]),
    # ── KAMIS 09:10 ──
    ("Kamis", "09:10", "Pariwisata Pedesaan", "Kelas A", [
        "Prof. Dr. Akin Duli, M.A.",
        "Drs. H. Hamris Darwis, M.Si.",
        "Dr. Dirk Rukka Sandarupa, S.S., M.Hum.",
    ]),
    ("Kamis", "09:10", "Pengantar Filsafat", "Kelas B", [
        "Dr. Supriadi, S.S., M.A.",
        "Drs. H. Hamris Darwis, M.Si.",
    ]),
    ("Kamis", "09:10", "Pariwisata Berkelanjutan", "Kelas B", [
        "Dr. Supriadi, S.S., M.A.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
        "Fadhillah Duli, S.I.Kom., M.Si.",
    ]),
    # ── KAMIS 10:50 ──
    ("Kamis", "10:50", "Pariwisata Perkotaan dan MICE", "Kelas B", [
        "Yusriana, S.S., M.A.",
        "Rafika Hayati, S.ST.Par., M.Par.",
        "Nur Rahmiani Achmad, S.IP., M.M.Par.",
    ]),
    ("Kamis", "10:50", "Perencanaan Lanskap Pariwisata", None, [
        "Dr. Supriadi, S.S., M.A.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
        "Fahran Reza, S.S., M.Hum.",
    ]),

    # ── JUMAT 07:30 ──
    ("Jumat", "07:30", "Sistem Informasi Kepariwisataan", "Kelas B", [
        "Dr. Yadi Mulyadi, S.S., M.A.",
        "Fahran Reza, S.S., M.Hum.",
        "Indra Mayanti Noer, S.S., M.Hum.",
    ]),
    ("Jumat", "07:30", "Pengelolaan Atraksi Pertunjukan Budaya", None, [
        "Dr. Khadijah Thahir Muda, M.Si.",
        "Indra Mayanti Noer, S.S., M.Hum.",
        "Fadhillah Duli, S.I.Kom., M.Si.",
    ]),
    # ── JUMAT 09:10 ──
    ("Jumat", "09:10", "Sosiologi Pariwisata", "Kelas B", [
        "Dr. Muhammad Nur, S.S., M.A.",
        "Rafika Hayati, S.ST.Par., M.Par.",
    ]),
    ("Jumat", "09:10", "Hospitaliti Pariwisata", "Kelas A", [
        "Erwin Mansyur Ugu Saraka, S.S., M.Sc.",
        "Rafika Hayati, S.ST.Par., M.Par.",
    ]),
    ("Jumat", "09:10", "Tugas Akhir (Skripsi)", None, [
        "Dr. Khadijah Thahir Muda, M.Si.",
        "Erwin Mansyur Ugu Saraka, S.S., M.Sc.",
    ]),
    # ── JUMAT 10:50 ──
    ("Jumat", "10:50", "Pariwisata Berkelanjutan", "Kelas A", [
        "Dr. Supriadi, S.S., M.A.",
        "Fahran Reza, S.S., M.Hum.",
        "Drs. H. Hamris Darwis, M.Si.",
    ]),
    ("Jumat", "10:50", "Pengelolaan Usaha Perjalanan Wisata", None, [
        "Erwin Mansyur Ugu Saraka, S.S., M.Sc.",
        "Dr. Dirk Rukka Sandarupa, S.S., M.Hum.",
        "Muhammad Syachrun Sjam, S.S., M.Hum.",
    ]),
    ("Jumat", "10:50", "Hospitaliti Pariwisata", "Kelas B", [
        "Erwin Mansyur Ugu Saraka, S.S., M.Sc.",
        "Rafika Hayati, S.ST.Par., M.Par.",
    ]),
    ("Jumat", "10:50", "Seminar Proposal", None, [
        "Dr. Supriadi, S.S., M.A.",
        "Aqilah Nurul Khaerani Latif, S.E., M.Par.",
    ]),
]


def find_lecturer(name: str):
    """Cari dosen dengan exact match, lalu fallback ke partial match 3 kata pertama."""
    name = name.strip().replace('\u0131', 'i')  # normalize Turkish i
    lect = Lecturer.query.filter(Lecturer.lecturer_name.ilike(name)).first()
    if lect:
        return lect
    # Fallback: cari 3 kata pertama
    words = name.split()[:3]
    partial = ' '.join(words)
    lect = Lecturer.query.filter(Lecturer.lecturer_name.ilike(f'{partial}%')).first()
    return lect


with app.app_context():
    updated = 0
    not_found_schedules = []
    not_found_lecturers = set()

    for day, start, course_name, class_name, lecturer_names in SCHEDULE_LECTURERS:
        start_time = dt.time(*map(int, start.split(':')))

        # Cari jadwal
        q = (
            db.session.query(ClassSchedule)
            .join(Course, ClassSchedule.course_id == Course.id)
            .filter(
                ClassSchedule.day_name == day,
                ClassSchedule.start_time == start_time,
                Course.course_name.ilike(course_name),
            )
        )
        if class_name:
            q = q.filter(ClassSchedule.class_name == class_name)
        else:
            q = q.filter(ClassSchedule.class_name.is_(None))

        sched = q.first()
        if not sched:
            not_found_schedules.append(f"{day} {start} – {course_name} ({class_name})")
            continue

        # Cari dosen
        lecturers = []
        for lname in lecturer_names:
            lect = find_lecturer(lname)
            if lect:
                lecturers.append(lect)
            else:
                not_found_lecturers.add(lname)

        sched.lecturers = lecturers
        updated += 1

    db.session.commit()

    print(f"Selesai: {updated} jadwal diperbarui.")
    if not_found_schedules:
        print(f"\nJadwal tidak ditemukan ({len(not_found_schedules)}):")
        for s in not_found_schedules:
            print(f"  - {s}")
    if not_found_lecturers:
        print(f"\nDosen tidak ditemukan ({len(not_found_lecturers)}):")
        for l in sorted(not_found_lecturers):
            print(f"  - {l}")
