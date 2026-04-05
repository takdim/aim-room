# aim-room

Static dummy HTML untuk GitHub Pages:

- Beranda: `/aim-room/`
- Ruangan:
  - `/aim-room/aula-mattulada/`
  - `/aim-room/ruangan-mangemba/`
  - `/aim-room/ruang-senat/`
  - `/aim-room/lounge-fib/`
- Kelas:
  - `/aim-room/kelas-1/`
  - `/aim-room/kelas-2/`
  - `/aim-room/kelas-3/`

Contoh isi QR:

`https://takdim.github.io/aim-room/kelas-1/`

## Flask + Database

1. Install dependencies:
   `pip install -r requirements.txt`
2. Copy env:
   `cp .env.example .env`
3. Buat migration folder:
   `flask db init`
4. Generate migration pertama:
   `flask db migrate -m "initial tables"`
5. Apply ke database `rooms`:
   `flask db upgrade`
