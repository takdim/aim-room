from app.extensions import db


class RoomBooking(db.Model):
    __tablename__ = "room_bookings"

    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    booking_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    borrower_name = db.Column(db.String(120))
    phone_number = db.Column(db.String(40))
    borrower_email = db.Column(db.String(120))
    organization = db.Column(db.String(150))
    purpose = db.Column(db.Text)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20))

    room = db.relationship("Room", backref="bookings")
    user = db.relationship("User", backref="bookings")
