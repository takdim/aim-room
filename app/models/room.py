from app.extensions import db


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(20))
    room_name = db.Column(db.String(100))
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"))
    floor = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    room_type = db.Column(db.String(50))
