from app.extensions import db


class ClassSchedule(db.Model):
    __tablename__ = "class_schedules"

    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    lecturer_id = db.Column(db.Integer, db.ForeignKey("lecturers.id"))

    day_name = db.Column(db.String(20))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"))
