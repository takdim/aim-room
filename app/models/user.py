from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash

# Roles: admin, staff, kasubag, ktu, wd2, dekan
ROLES = ("admin", "staff", "kasubag", "ktu", "wd2", "dekan")
APPROVAL_ROLES = ("kasubag", "ktu", "wd2", "dekan")

# Map role → which booking status they handle
ROLE_STATUS_MAP = {
    "staff": "Menunggu Staff",
    "kasubag": "Menunggu Kasubag",
    "ktu": "Menunggu KTU",
    "wd2": "Menunggu WD2",
    "dekan": "Menunggu Dekan",
}

# Next status after approval at each level
NEXT_STATUS_MAP = {
    "staff": "Menunggu Kasubag",
    "kasubag": "Menunggu KTU",
    "ktu": "Menunggu WD2",
    "wd2": "Menunggu Dekan",
    "dekan": "Disetujui",
}


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="staff")

    __table_args__ = (
        db.CheckConstraint(
            "role IN ('admin', 'staff', 'kasubag', 'ktu', 'wd2', 'dekan')",
            name="ck_users_role",
        ),
    )

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)
