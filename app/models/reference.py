from app.extensions import db


class Building(db.Model):
    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(120))


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True)
    course_name = db.Column(db.String(120))


class Day(db.Model):
    __tablename__ = "days"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)


class TimeSlot(db.Model):
    __tablename__ = "time_slots"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    label = db.Column(db.String(50))
