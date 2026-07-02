"""
Seed script: kosongkan DB (kecuali users & semesters), lalu isi gedung & ruangan.
Jalankan: python seed_rooms.py
"""
from app import create_app
from app.extensions import db
from app.models.reference import Building, Course
from app.models.lecturer import Lecturer
from app.models.room import Room
from app.models.room_booking import RoomBooking
from app.models.class_schedule import ClassSchedule, class_schedule_lecturers
from app.models.pakta_template import PaktaTemplate
from app.models.holiday import Holiday
from sqlalchemy import text

app = create_app()

# ---------------------------------------------------------------------------
# Data gedung & ruangan
# ---------------------------------------------------------------------------
BUILDINGS_AND_ROOMS = [
    {
        "name": "Gedung TML A / FIS V",
        "rooms": [
            {"code": "R.201",        "name": "Lab. Multi Media Sastra Arab",          "type": "Lab",          "floor": 2},
            {"code": "R.202",        "name": "Self Access Centre of Sastra Arab",      "type": "Ruang Kelas",  "floor": 2},
            {"code": "R.211",        "name": "Lensa Budaya (S1 Arkeologi)",            "type": "Ruang Kelas",  "floor": 2},
            {"code": "R.212",        "name": "R.212 (FIB.212)",                        "type": "Ruang Kelas",  "floor": 2},
            {"code": "R.213-R.214",  "name": "R.213-R.214 Ruang Gabungan",            "type": "Ruang Kelas",  "floor": 2},
            {"code": "R.215",        "name": "R.215 (FIB.215)",                        "type": "Ruang Kelas",  "floor": 2},
            {"code": "R.217",        "name": "R.217 (FIB.217)",                        "type": "Ruang Kelas",  "floor": 2},
            {"code": "R.218",        "name": "R.218 (FIB.218)",                        "type": "Ruang Kelas",  "floor": 2},
            {"code": "R.316",        "name": "R.316 (FIB.316)",                        "type": "Ruang Kelas",  "floor": 3},
            {"code": "R.317",        "name": "R.317 (FIB.317)",                        "type": "Ruang Kelas",  "floor": 3},
            {"code": "R.318",        "name": "R.318 (FIB.318)",                        "type": "Ruang Kelas",  "floor": 3},
            {"code": "R.319",        "name": "R.319 (FIB.319)",                        "type": "Ruang Kelas",  "floor": 3},
            {"code": "R.320",        "name": "Lab. Arkeologi (FIB.320)",               "type": "Lab",          "floor": 3},
            {"code": "R.323",        "name": "R.323 (FIB.323)",                        "type": "Ruang Kelas",  "floor": 3},
            {"code": "R.324",        "name": "R.324 (FIB.324)",                        "type": "Ruang Kelas",  "floor": 3},
        ],
    },
    {
        "name": "Gedung TML F",
        "rooms": [
            {"code": "MKU.212", "name": "R.212 (MKU.212)", "type": "Ruang Kelas", "floor": 2},
            {"code": "MKU.213", "name": "R.213 (MKU.213)", "type": "Ruang Kelas", "floor": 2},
            {"code": "MKU.214", "name": "R.214 (MKU.214)", "type": "Ruang Kelas", "floor": 2},
            {"code": "MKU.215", "name": "R.215 (MKU.215)", "type": "Ruang Kelas", "floor": 2},
            {"code": "MKU.223", "name": "R.223 (MKU.223)", "type": "Ruang Kelas", "floor": 2},
            {"code": "MKU.224", "name": "R.224 (MKU.224)", "type": "Ruang Kelas", "floor": 2},
            {"code": "MKU.225", "name": "R.225 (MKU.225)", "type": "Ruang Kelas", "floor": 2},
        ],
    },
    {
        "name": "Gedung TML G",
        "rooms": [
            {"code": "SIL.1", "name": "R.101 (SIL.1)", "type": "Ruang Kelas", "floor": 1},
            {"code": "SIL.2", "name": "R.102 (SIL.2)", "type": "Ruang Kelas", "floor": 1},
            {"code": "SIL.3", "name": "R.103 (SIL.3)", "type": "Ruang Kelas", "floor": 1},
        ],
    },
    {
        "name": "Gedung TML H",
        "rooms": [
            {"code": "Mediatek-F05", "name": "R.201 Mediatek (Sastra Prancis)",              "type": "Lab",         "floor": 2},
            {"code": "AV-F05",       "name": "R.202 AV (Sastra Prancis)",                    "type": "Ruang Kelas", "floor": 2},
            {"code": "R.203",        "name": "R.203",                                         "type": "Ruang Kelas", "floor": 2},
            {"code": "R.204",        "name": "R.204 Mandarin dan Kebudayaan Tiongkok",        "type": "Ruang Kelas", "floor": 2},
        ],
    },
    {
        "name": "Gedung TML HR",
        "rooms": [
            {"code": "Lab-JSI", "name": "R.101 Lab. Sastra Indonesia (JSI)", "type": "Lab",         "floor": 1},
            {"code": "RRJ",     "name": "R.102 RRJ Sastra Indonesia",        "type": "Ruang Kelas", "floor": 1},
        ],
    },
    {
        "name": "Gedung F",
        "rooms": [
            {"code": "MKU.226", "name": "R.226 (MKU.226)", "type": "Ruang Kelas", "floor": 2},
        ],
    },
    {
        "name": "Gedung MKU FIB",
        "rooms": [
            {"code": "R.216 MKU", "name": "R.216 MKU", "type": "Ruang Kelas", "floor": 2},
        ],
    },
    {
        "name": "Pusat Bahasa Mandarin (PBM FIB)",
        "rooms": [
            {"code": "PBM-FIB", "name": "Ruang PBM FIB", "type": "Ruang Kelas", "floor": 1},
        ],
    },
    {
        "name": "Gedung TML (Perpustakaan)",
        "rooms": [
            {"code": "PERPUST-WP", "name": "Warung Prancis", "type": "Ruang Khusus", "floor": 1},
        ],
    },
    {
        "name": "Departemen Sastra Indonesia",
        "rooms": [
            {"code": "R.103-R.104", "name": "R.103 & R.104 (Departemen)", "type": "Ruang Kelas", "floor": 1},
        ],
    },
]


with app.app_context():
    print("=== Membersihkan database... ===")

    # Hapus junction table dulu (tidak punya model ORM)
    db.session.execute(text("DELETE FROM class_schedule_lecturers"))
    db.session.flush()

    # Hapus tabel-tabel (urutan sesuai FK)
    RoomBooking.query.delete()
    ClassSchedule.query.delete()
    Room.query.delete()
    Building.query.delete()
    Course.query.delete()
    Lecturer.query.delete()
    PaktaTemplate.query.delete()
    Holiday.query.delete()

    db.session.commit()
    print("Database berhasil dikosongkan (users & semesters tetap ada).")

    print("\n=== Mengisi data gedung & ruangan... ===")
    total_rooms = 0
    for bdata in BUILDINGS_AND_ROOMS:
        building = Building(building_name=bdata["name"])
        db.session.add(building)
        db.session.flush()  # dapatkan building.id

        for rdata in bdata["rooms"]:
            room = Room(
                room_code=rdata["code"],
                room_name=rdata["name"],
                building_id=building.id,
                floor=rdata.get("floor"),
                room_type=rdata.get("type", "Ruang Kelas"),
            )
            db.session.add(room)
            total_rooms += 1

        print(f"  ✓ {bdata['name']} ({len(bdata['rooms'])} ruangan)")

    db.session.commit()
    print(f"\nSelesai: {len(BUILDINGS_AND_ROOMS)} gedung, {total_rooms} ruangan berhasil dimasukkan.")
