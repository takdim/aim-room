"""
Master seed script — jalankan satu kali untuk setup DB lengkap di VPS.
Urutan: Semester → Rooms/Buildings → Lecturers → Semua Jadwal

Jalankan: python seed_all.py
"""
import subprocess
import sys
import os

# Pastikan working directory adalah root project
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PYTHON = sys.executable

# ── Step 1: Buat semester (jika belum ada) ──────────────────────────────────
print("\n" + "=" * 60)
print("STEP 1: Setup Semester")
print("=" * 60)

from app import create_app
from app.extensions import db
from app.models.semester import Semester

app = create_app()
with app.app_context():
    ganjil = Semester.query.filter(Semester.name.ilike("%Ganjil%2025%")).first()
    if not ganjil:
        ganjil = Semester(name="Semester Ganjil 2025/2026", is_active=True)
        db.session.add(ganjil)
        db.session.commit()
        print(f"  [+] Semester dibuat: {ganjil.name} (ID:{ganjil.id})")
    else:
        if not ganjil.is_active:
            ganjil.is_active = True
            db.session.commit()
        print(f"  [skip] Semester sudah ada: {ganjil.name} (ID:{ganjil.id})")

    genap = Semester.query.filter(Semester.name.ilike("%Genap%2025%")).first()
    if not genap:
        genap = Semester(name="Semester Genap 2025/2026", is_active=False)
        db.session.add(genap)
        db.session.commit()
        print(f"  [+] Semester dibuat: {genap.name} (ID:{genap.id})")
    else:
        print(f"  [skip] Semester sudah ada: {genap.name} (ID:{genap.id})")


# ── Daftar seed scripts dalam urutan yang benar ─────────────────────────────
SCRIPTS = [
    ("Rooms & Buildings",       "seed_rooms.py"),
    ("Lecturers",               "seed_lecturers.py"),
    ("Jadwal Pariwisata",       "seed_schedule_pariwisata.py"),
    ("Jadwal Mandarin (FIB)",   "seed_schedules_mandarin.py"),
    ("Jadwal FIB Lainnya",      "seed_fib_schedules.py"),
    ("Jadwal Sastra Daerah",    "seed_sastra_daerah_schedules.py"),
    ("Jadwal Sastra Arab",      "seed_sastra_arab_schedules.py"),
    ("Jadwal Sastra Prancis",   "seed_sastra_prancis_schedules.py"),
    ("Jadwal Sastra Jepang",    "seed_sastra_jepang_schedules.py"),
    ("Jadwal Sastra Indonesia", "seed_sastra_indonesia_schedules.py"),
    ("Jadwal Sastra Inggris",   "seed_sastra_inggris_schedules.py"),
    ("Jadwal Arkeologi",        "seed_arkeologi_schedules.py"),
    ("Jadwal Ilmu Sejarah",     "seed_ilmu_sejarah_schedules.py"),
]

# ── Jalankan setiap script ───────────────────────────────────────────────────
failed = []
for step, (label, script) in enumerate(SCRIPTS, start=2):
    print(f"\n{'='*60}")
    print(f"STEP {step}: {label}  ({script})")
    print("=" * 60)

    if not os.path.exists(script):
        print(f"  [SKIP] File tidak ditemukan: {script}")
        continue

    result = subprocess.run([PYTHON, script], check=False)
    if result.returncode != 0:
        print(f"\n  [ERROR] {script} gagal (exit code {result.returncode})")
        failed.append(script)
        # Lanjutkan script berikutnya, jangan berhenti total
        continue

# ── Ringkasan ────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
if failed:
    print(f"SELESAI dengan {len(failed)} error:")
    for f in failed:
        print(f"  ✗ {f}")
else:
    print("SELESAI — Semua seed berhasil dijalankan!")
print("=" * 60)
