import datetime as dt

from app.extensions import db


class Holiday(db.Model):
    """Manual holiday entries. Sundays are auto-detected in code."""

    __tablename__ = "holidays"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False)

    @staticmethod
    def is_holiday(date: dt.date) -> bool:
        """Return True if the given date is Sunday or a registered holiday."""
        if date.weekday() == 6:  # Sunday
            return True
        return db.session.query(
            Holiday.query.filter_by(date=date).exists()
        ).scalar()
