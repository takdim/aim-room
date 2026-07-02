from app.extensions import db

# Many-to-many: satu jadwal bisa punya banyak dosen
class_schedule_lecturers = db.Table(
    "class_schedule_lecturers",
    db.Column("schedule_id", db.Integer, db.ForeignKey("class_schedules.id"), primary_key=True),
    db.Column("lecturer_id", db.Integer, db.ForeignKey("lecturers.id"), primary_key=True),
)


class ClassSchedule(db.Model):
    __tablename__ = "class_schedules"

    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    class_name = db.Column(db.String(150))  # e.g. "Pengantar Perencanaan Pariwisata (A)"

    day_name = db.Column(db.String(20))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"))

    lecturers = db.relationship(
        "Lecturer",
        secondary=class_schedule_lecturers,
        lazy="selectin",
    )
