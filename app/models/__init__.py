from app.models.class_schedule import ClassSchedule
from app.models.lecturer import Lecturer
from app.models.reference import Building, Course, Day, TimeSlot
from app.models.room import Room
from app.models.room_booking import RoomBooking
from app.models.user import User
from app.models.semester import Semester

__all__ = [
    "Room",
    "Lecturer",
    "ClassSchedule",
    "RoomBooking",
    "Semester",
    "Building",
    "Course",
    "Day",
    "TimeSlot",
    "User",
]
