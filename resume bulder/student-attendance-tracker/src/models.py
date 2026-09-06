"""Data models representing Students and Attendance records."""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime


class AttendanceStatus(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    LATE = "Late"

    @classmethod
    def from_code(cls, code: str) -> "AttendanceStatus":
        code_upper = code.strip().upper()
        if code_upper in ("P", "PRESENT"):
            return cls.PRESENT
        elif code_upper in ("A", "ABSENT"):
            return cls.ABSENT
        elif code_upper in ("L", "LATE"):
            return cls.LATE
        raise ValueError(f"Invalid attendance status code: '{code}'. Use P (Present), A (Absent), or L (Late).")


class Student:
    """Represents an enrolled student in the tracker."""

    def __init__(self, student_id: str, name: str, batch: str, email: str = ""):
        self.student_id = student_id.strip().upper()
        self.name = name.strip()
        self.batch = batch.strip().upper()
        self.email = email.strip().lower()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "batch": self.batch,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            batch=data.get("batch", "GENERAL"),
            email=data.get("email", "")
        )

    def __repr__(self) -> str:
        return f"<Student {self.student_id} - {self.name} ({self.batch})>"
