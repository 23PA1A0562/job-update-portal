"""Utility script to populate sample student data and past attendance sessions.

Provides immediate demo-ready data with realistic engineering student profiles
and varied attendance levels (exemplary, borderline, and defaulter status).
"""

import os
from datetime import datetime, timedelta
from src.attendance_manager import AttendanceManager
from src.models import AttendanceStatus


def load_sample_dataset(manager: AttendanceManager) -> None:
    """Populates 6 sample students and 5 historical attendance sessions."""
    students = [
        ("23PA1A0501", "Aarav Sharma", "CSE-A", "aarav.sharma@example.edu"),
        ("23PA1A0502", "Bhavya Reddy", "CSE-A", "bhavya.reddy@example.edu"),
        ("23PA1A0503", "Chirag Verma", "CSE-B", "chirag.verma@example.edu"),
        ("23PA1A0504", "Divya Patel", "CSE-B", "divya.patel@example.edu"),
        ("23PA1A0505", "Eshwar Rao", "CSE-A", "eshwar.rao@example.edu"),
        ("23PA1A0506", "Farhan Khan", "CSE-B", "farhan.khan@example.edu"),
    ]

    for s_id, name, batch, email in students:
        if not manager.get_student(s_id):
            manager.add_student(s_id, name, batch, email)

    # 5 consecutive past working days
    base_date = datetime.now() - timedelta(days=6)
    history = [
        # Day 1
        {
            "23PA1A0501": AttendanceStatus.PRESENT.value,
            "23PA1A0502": AttendanceStatus.PRESENT.value,
            "23PA1A0503": AttendanceStatus.ABSENT.value,
            "23PA1A0504": AttendanceStatus.PRESENT.value,
            "23PA1A0505": AttendanceStatus.LATE.value,
            "23PA1A0506": AttendanceStatus.ABSENT.value,
        },
        # Day 2
        {
            "23PA1A0501": AttendanceStatus.PRESENT.value,
            "23PA1A0502": AttendanceStatus.PRESENT.value,
            "23PA1A0503": AttendanceStatus.ABSENT.value,
            "23PA1A0504": AttendanceStatus.PRESENT.value,
            "23PA1A0505": AttendanceStatus.PRESENT.value,
            "23PA1A0506": AttendanceStatus.ABSENT.value,
        },
        # Day 3
        {
            "23PA1A0501": AttendanceStatus.PRESENT.value,
            "23PA1A0502": AttendanceStatus.LATE.value,
            "23PA1A0503": AttendanceStatus.ABSENT.value,
            "23PA1A0504": AttendanceStatus.PRESENT.value,
            "23PA1A0505": AttendanceStatus.PRESENT.value,
            "23PA1A0506": AttendanceStatus.ABSENT.value,
        },
        # Day 4
        {
            "23PA1A0501": AttendanceStatus.PRESENT.value,
            "23PA1A0502": AttendanceStatus.PRESENT.value,
            "23PA1A0503": AttendanceStatus.PRESENT.value,
            "23PA1A0504": AttendanceStatus.LATE.value,
            "23PA1A0505": AttendanceStatus.ABSENT.value,
            "23PA1A0506": AttendanceStatus.PRESENT.value,
        },
        # Day 5
        {
            "23PA1A0501": AttendanceStatus.PRESENT.value,
            "23PA1A0502": AttendanceStatus.PRESENT.value,
            "23PA1A0503": AttendanceStatus.ABSENT.value,
            "23PA1A0504": AttendanceStatus.PRESENT.value,
            "23PA1A0505": AttendanceStatus.PRESENT.value,
            "23PA1A0506": AttendanceStatus.ABSENT.value,
        },
    ]

    for i, day_records in enumerate(history):
        target_date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        manager.record_date_attendance(target_date, day_records)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data")
    mgr = AttendanceManager(data_path)
    load_sample_dataset(mgr)
    print("Sample data populated successfully.")
