from app.models.class_schedule import ClassSchedule, class_schedule_lecturers
from app.models.holiday import Holiday
from app.models.lecturer import Lecturer
from app.models.pakta_template import PaktaTemplate
from app.models.reference import Building, Course, Day, TimeSlot
from app.models.room import Room
from app.models.room_booking import RoomBooking
from app.models.user import User
from app.models.semester import Semester

__all__ = [
    "Room",
    "Lecturer",
    "ClassSchedule",
    "Holiday",
    "PaktaTemplate",
    "RoomBooking",
    "Semester",
    "Building",
    "Course",
    "Day",
    "TimeSlot",
    "User",
]
