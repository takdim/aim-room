from app.extensions import db


class Lecturer(db.Model):
    __tablename__ = "lecturers"

    id = db.Column(db.Integer, primary_key=True)
    lecturer_name = db.Column(db.String(100))
    nidn = db.Column(db.String(50))
