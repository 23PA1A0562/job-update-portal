"""Unit test suite for Student Attendance Tracker.

Validates:
- File persistence and atomic I/O operations without an external database.
- Student CRUD operations (Create, Read, Update, Delete).
- Date-wise attendance recording.
- Statistical percentage calculations and defaulter detection (< 75%).
- CSV report generation.
"""

import os
import shutil
import tempfile
import unittest
from datetime import datetime

from src.models import Student, AttendanceStatus
from src.storage import FileStorage
from src.attendance_manager import AttendanceManager


class TestStudentAttendanceTracker(unittest.TestCase):

    def setUp(self):
        # Create an isolated temporary directory for test file I/O
        self.test_dir = tempfile.mkdtemp()
        self.manager = AttendanceManager(self.test_dir)

    def tearDown(self):
        # Clean up temporary test files
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_student_crud_lifecycle(self):
        """Test full Create, Read, Update, Delete lifecycle for students."""
        # 1. Create
        success, msg = self.manager.add_student("23PA1A0501", "Aarav Sharma", "CSE-A", "aarav@test.edu")
        self.assertTrue(success)
        self.assertIn("added successfully", msg)

        # Duplicate check
        dup_success, dup_msg = self.manager.add_student("23PA1A0501", "Duplicate Student", "CSE-A")
        self.assertFalse(dup_success)

        # 2. Read
        student = self.manager.get_student("23PA1A0501")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Aarav Sharma")
        self.assertEqual(student.batch, "CSE-A")

        # 3. Update
        up_success, _ = self.manager.update_student("23PA1A0501", name="Aarav K. Sharma", batch="CSE-B")
        self.assertTrue(up_success)
        updated_student = self.manager.get_student("23PA1A0501")
        self.assertEqual(updated_student.name, "Aarav K. Sharma")
        self.assertEqual(updated_student.batch, "CSE-B")

        # 4. Delete
        del_success, _ = self.manager.delete_student("23PA1A0501")
        self.assertTrue(del_success)
        self.assertIsNone(self.manager.get_student("23PA1A0501"))

    def test_file_persistence_reloading(self):
        """Test that data written to disk persists when creating a new manager instance."""
        self.manager.add_student("23PA1A0502", "Bhavya Reddy", "CSE-A")
        self.manager.record_date_attendance("2026-09-01", {"23PA1A0502": "Present"})

        # Spin up a fresh manager pointing to the same directory
        reloaded_manager = AttendanceManager(self.test_dir)
        student = reloaded_manager.get_student("23PA1A0502")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Bhavya Reddy")

        attendance = reloaded_manager.get_attendance_for_date("2026-09-01")
        self.assertEqual(attendance.get("23PA1A0502"), "Present")

    def test_attendance_percentage_and_defaulters(self):
        """Test accuracy of percentage calculation and defaulter filtering."""
        self.manager.add_student("S1", "High Attendance", "Batch-1")
        self.manager.add_student("S2", "Low Attendance", "Batch-1")

        # Record 4 sessions:
        # S1 attended 4/4 (100%)
        # S2 attended 1/4 (25%)
        dates = ["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04"]
        for d in dates:
            self.manager.record_date_attendance(d, {"S1": "Present", "S2": "Absent"})

        # Record S2 as present on 1 day
        self.manager.record_date_attendance("2026-09-01", {"S1": "Present", "S2": "Present"})

        stats_s1 = self.manager.calculate_student_stats("S1")
        stats_s2 = self.manager.calculate_student_stats("S2")

        self.assertEqual(stats_s1["percentage"], 100.0)
        self.assertFalse(stats_s1["is_defaulter"])

        self.assertEqual(stats_s2["percentage"], 25.0)
        self.assertTrue(stats_s2["is_defaulter"])

        defaulters = self.manager.get_defaulters(threshold=75.0)
        self.assertEqual(len(defaulters), 1)
        self.assertEqual(defaulters[0]["student_id"], "S2")

    def test_csv_export(self):
        """Test CSV file generation for cumulative summaries."""
        self.manager.add_student("S10", "Export Test", "Batch-A")
        self.manager.record_date_attendance("2026-09-01", {"S10": "Present"})

        export_path = os.path.join(self.test_dir, "test_summary.csv")
        success, path = self.manager.export_summary_to_csv(export_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(path))

        # Check content
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Student ID", content)
            self.assertIn("Export Test", content)
            self.assertIn("S10", content)


if __name__ == "__main__":
    unittest.main()
