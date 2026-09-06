"""Core business logic for the Student Attendance Tracker.

Handles Student CRUD operations, transactional date-wise attendance registers,
statistical aggregation (attendance percentage, shortage/defaulter detection),
and CSV export triggers using file handling.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from .models import Student, AttendanceStatus
from .storage import FileStorage


class AttendanceManager:
    """Manages student records and attendance operations persisted in structured files."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.students_file = os.path.join(data_dir, "students.json")
        self.attendance_file = os.path.join(data_dir, "attendance.json")
        self.exports_dir = os.path.join(data_dir, "exports")

        FileStorage.ensure_directory(self.data_dir)
        FileStorage.ensure_directory(self.exports_dir)

        # In-memory cached representations synced with files
        self._students: Dict[str, Student] = {}
        self._attendance: Dict[str, Dict[str, str]] = {}  # { "YYYY-MM-DD": { "STUDENT_ID": "Present" } }
        self._load_data()

    def _load_data(self) -> None:
        """Load data from JSON files into memory."""
        raw_students = FileStorage.load_json(self.students_file, default={})
        self._students = {
            s_id: Student.from_dict(data)
            for s_id, data in raw_students.items()
        }

        self._attendance = FileStorage.load_json(self.attendance_file, default={})

    def _save_students(self) -> bool:
        """Persist current students state to students.json."""
        data = {s_id: s.to_dict() for s_id, s in self._students.items()}
        return FileStorage.save_json(self.students_file, data)

    def _save_attendance(self) -> bool:
        """Persist current attendance registers to attendance.json."""
        return FileStorage.save_json(self.attendance_file, self._attendance)

    # -------------------------------------------------------------------------
    # Student CRUD Operations
    # -------------------------------------------------------------------------

    def add_student(self, student_id: str, name: str, batch: str = "A", email: str = "") -> Tuple[bool, str]:
        """Create a new student record."""
        clean_id = student_id.strip().upper()
        clean_name = name.strip()

        if not clean_id or not clean_name:
            return False, "Student ID and Name cannot be empty."

        if clean_id in self._students:
            return False, f"Student with ID '{clean_id}' already exists."

        student = Student(student_id=clean_id, name=clean_name, batch=batch, email=email)
        self._students[clean_id] = student

        if self._save_students():
            return True, f"Student '{clean_name}' ({clean_id}) added successfully."
        return False, "Failed to persist student record to disk."

    def get_student(self, student_id: str) -> Optional[Student]:
        """Read a single student by ID."""
        return self._students.get(student_id.strip().upper())

    def get_all_students(self) -> List[Student]:
        """Read all enrolled students sorted by ID."""
        return sorted(self._students.values(), key=lambda s: s.student_id)

    def update_student(self, student_id: str, name: Optional[str] = None, batch: Optional[str] = None, email: Optional[str] = None) -> Tuple[bool, str]:
        """Update an existing student's details."""
        clean_id = student_id.strip().upper()
        if clean_id not in self._students:
            return False, f"Student '{clean_id}' not found."

        student = self._students[clean_id]
        if name and name.strip():
            student.name = name.strip()
        if batch and batch.strip():
            student.batch = batch.strip().upper()
        if email is not None:
            student.email = email.strip().lower()

        if self._save_students():
            return True, f"Student '{clean_id}' updated successfully."
        return False, "Failed to persist updated student record to disk."

    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        """Delete a student and clean up their attendance records."""
        clean_id = student_id.strip().upper()
        if clean_id not in self._students:
            return False, f"Student '{clean_id}' not found."

        student_name = self._students[clean_id].name
        del self._students[clean_id]
        self._save_students()

        # Cascade delete attendance records for this student
        records_removed = 0
        for date_key, date_records in self._attendance.items():
            if clean_id in date_records:
                del date_records[clean_id]
                records_removed += 1

        self._save_attendance()
        return True, f"Student '{student_name}' ({clean_id}) and {records_removed} attendance logs deleted."

    # -------------------------------------------------------------------------
    # Attendance Tracking Operations
    # -------------------------------------------------------------------------

    def record_date_attendance(self, date_str: str, records: Dict[str, str]) -> Tuple[bool, str]:
        """Mark or update attendance for a specific date (YYYY-MM-DD)."""
        # Validate date format
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False, f"Invalid date format '{date_str}'. Required format: YYYY-MM-DD."

        if date_str not in self._attendance:
            self._attendance[date_str] = {}

        for s_id, status_val in records.items():
            clean_id = s_id.strip().upper()
            if clean_id in self._students:
                self._attendance[date_str][clean_id] = status_val

        if self._save_attendance():
            return True, f"Attendance saved successfully for {date_str} ({len(records)} students recorded)."
        return False, "Failed to persist attendance register to disk."

    def get_attendance_for_date(self, date_str: str) -> Optional[Dict[str, str]]:
        """Return the attendance register for a specific date."""
        return self._attendance.get(date_str)

    def get_all_dates(self) -> List[str]:
        """Return list of all dates with recorded attendance, sorted chronologically."""
        return sorted(self._attendance.keys())

    # -------------------------------------------------------------------------
    # Analytics & Percentage Calculations
    # -------------------------------------------------------------------------

    def calculate_student_stats(self, student_id: str) -> Dict[str, Any]:
        """Calculate total sessions, present, absent, late counts, and attendance percentage."""
        clean_id = student_id.strip().upper()
        student = self.get_student(clean_id)

        present = 0
        absent = 0
        late = 0
        total_sessions = 0

        for date_str, records in self._attendance.items():
            if clean_id in records:
                total_sessions += 1
                status = records[clean_id]
                if status == AttendanceStatus.PRESENT.value:
                    present += 1
                elif status == AttendanceStatus.ABSENT.value:
                    absent += 1
                elif status == AttendanceStatus.LATE.value:
                    late += 1

        # Percentage calculation logic:
        # Full credit for Present, half credit (0.5) for Late
        effective_present = present + (0.5 * late)
        percentage = round((effective_present / total_sessions * 100), 2) if total_sessions > 0 else 0.0

        return {
            "student_id": clean_id,
            "name": student.name if student else "Unknown",
            "batch": student.batch if student else "N/A",
            "total_sessions": total_sessions,
            "present_count": present,
            "absent_count": absent,
            "late_count": late,
            "effective_present": effective_present,
            "percentage": percentage,
            "is_defaulter": percentage < 75.0 if total_sessions > 0 else False
        }

    def get_class_summary(self) -> List[Dict[str, Any]]:
        """Generate statistical summary for all enrolled students."""
        summary = []
        for student in self.get_all_students():
            summary.append(self.calculate_student_stats(student.student_id))
        return summary

    def get_defaulters(self, threshold: float = 75.0) -> List[Dict[str, Any]]:
        """Filter students whose attendance percentage is below the given threshold (default: 75%)."""
        summary = self.get_class_summary()
        # Only consider students where at least 1 session has occurred
        return [
            s for s in summary
            if s["total_sessions"] > 0 and s["percentage"] < threshold
        ]

    # -------------------------------------------------------------------------
    # CSV Reporting & File Exports
    # -------------------------------------------------------------------------

    def export_summary_to_csv(self, file_path: Optional[str] = None) -> Tuple[bool, str]:
        """Export overall student attendance summary to a CSV file."""
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(self.exports_dir, f"attendance_summary_{timestamp}.csv")

        headers = [
            "Student ID", "Full Name", "Batch",
            "Total Sessions", "Present", "Absent", "Late",
            "Attendance %", "Defaulter (<75%)"
        ]

        summary = self.get_class_summary()
        rows = []
        for s in summary:
            rows.append([
                s["student_id"],
                s["name"],
                s["batch"],
                s["total_sessions"],
                s["present_count"],
                s["absent_count"],
                s["late_count"],
                f"{s['percentage']}%",
                "YES" if s["is_defaulter"] else "NO"
            ])

        success = FileStorage.export_csv(file_path, headers, rows)
        if success:
            return True, file_path
        return False, "Failed to write CSV summary report."

    def export_date_attendance_to_csv(self, date_str: str, file_path: Optional[str] = None) -> Tuple[bool, str]:
        """Export a single day's attendance register to CSV."""
        records = self.get_attendance_for_date(date_str)
        if records is None:
            return False, f"No attendance data recorded for date {date_str}."

        if not file_path:
            file_path = os.path.join(self.exports_dir, f"attendance_{date_str}.csv")

        headers = ["Roll No / ID", "Name", "Batch", "Status", "Date"]
        rows = []
        for student in self.get_all_students():
            status = records.get(student.student_id, "Not Marked")
            rows.append([
                student.student_id,
                student.name,
                student.batch,
                status,
                date_str
            ])

        success = FileStorage.export_csv(file_path, headers, rows)
        if success:
            return True, file_path
        return False, f"Failed to write CSV report for date {date_str}."
