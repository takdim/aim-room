import datetime as dt
import uuid

from app.extensions import db


def _gen_token():
    return uuid.uuid4().hex


class RoomBooking(db.Model):
    __tablename__ = "room_bookings"

    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Unique token for public status page
    token = db.Column(db.String(32), unique=True, nullable=True, default=_gen_token)

    # Booking type: "regular" (hari kerja biasa) or "event" (event besar/hari libur)
    booking_type = db.Column(db.String(20), nullable=False, default="regular")

    booking_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    submission_date = db.Column(db.Date, default=dt.date.today)

    # Identity data
    borrower_name = db.Column(db.String(120))   # Nama pengguna sistem (bisa diisi via QR)
    name_on_pakta = db.Column(db.String(120))   # Nama sesuai pakta integritas (tampil di daftar)
    phone_number = db.Column(db.String(40))
    borrower_email = db.Column(db.String(120))
    organization = db.Column(db.String(150))
    purpose = db.Column(db.Text)
    notes = db.Column(db.Text)

    # Uploaded files (paths relative to UPLOAD_FOLDER)
    pakta_integritas_path = db.Column(db.String(255))
    surat_permohonan_path = db.Column(db.String(255))

    # Staff checks (manual)
    is_fib_student = db.Column(db.Boolean, default=False)
    is_bem_verified = db.Column(db.Boolean, default=False)
    staff_note = db.Column(db.Text)

    # Approval status:
    # Menunggu Staff → Menunggu Kasubag → Menunggu KTU → Menunggu WD2 → Menunggu Dekan → Disetujui
    # At any point can be Ditolak
    status = db.Column(db.String(30), default="Menunggu Staff")
    rejection_note = db.Column(db.Text)
    rejected_by = db.Column(db.String(50))  # role yang menolak

    room = db.relationship("Room", backref="bookings")
    user = db.relationship("User", backref="bookings")

    @property
    def display_name(self):
        """Name to show in public lists — prefer name from pakta integritas."""
        return self.name_on_pakta or self.borrower_name or "-"
