"""Flask Web Server for Student Attendance Tracker Localhost Dashboard.

Bridges the structured file I/O backend to an interactive, modern web browser interface.
Run with:
    python app.py
"""

import os
from flask import Flask, render_template, request, jsonify, send_file

from src.attendance_manager import AttendanceManager
from sample_data import load_sample_dataset

app = Flask(__name__, template_folder="templates")

# Initialize manager pointing to persistent data directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
manager = AttendanceManager(DATA_DIR)


@app.route("/")
def index():
    """Render the dashboard HTML interface."""
    return render_template("index.html")


@app.route("/api/students", methods=["GET"])
def get_students():
    """Fetch all students along with their calculated attendance metrics."""
    summary = manager.get_class_summary()
    total_dates = len(manager.get_all_dates())
    defaulters = manager.get_defaulters(threshold=75.0)

    stats = {
        "total_students": len(summary),
        "total_sessions": total_dates,
        "defaulter_count": len(defaulters),
        "eligible_count": len(summary) - len(defaulters)
    }

    return jsonify({
        "students": summary,
        "stats": stats
    })


@app.route("/api/students", methods=["POST"])
def add_student():
    """Add a new student to the file persistence store."""
    payload = request.get_json() or {}
    student_id = payload.get("student_id", "").strip()
    name = payload.get("name", "").strip()
    batch = payload.get("batch", "CSE-A").strip()
    email = payload.get("email", "").strip()

    if not student_id or not name:
        return jsonify({"error": "Student ID and Name are required"}), 400

    success, msg = manager.add_student(student_id, name, batch, email)
    if success:
        return jsonify({"message": msg}), 201
    return jsonify({"error": msg}), 400


@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    """Delete a student and remove their attendance logs."""
    success, msg = manager.delete_student(student_id)
    if success:
        return jsonify({"message": msg}), 200
    return jsonify({"error": msg}), 404


@app.route("/api/attendance/<date_str>", methods=["GET"])
def get_attendance(date_str):
    """Retrieve attendance records for a specific date."""
    records = manager.get_attendance_for_date(date_str)
    return jsonify({
        "date": date_str,
        "records": records or {}
    })


@app.route("/api/attendance", methods=["POST"])
def save_attendance():
    """Save/update attendance records for a specific date."""
    payload = request.get_json() or {}
    date_str = payload.get("date", "").strip()
    records = payload.get("records", {})

    if not date_str or not records:
        return jsonify({"error": "Date and attendance records are required"}), 400

    success, msg = manager.record_date_attendance(date_str, records)
    if success:
        return jsonify({"message": msg}), 200
    return jsonify({"error": msg}), 500


@app.route("/api/demo", methods=["POST"])
def load_demo():
    """Populate sample demo dataset."""
    load_sample_dataset(manager)
    return jsonify({"message": "Sample demo records generated successfully"}), 200


@app.route("/api/export", methods=["GET"])
def export_csv():
    """Generate and download latest attendance summary CSV."""
    success, file_path = manager.export_summary_to_csv()
    if success and os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            download_name="attendance_summary.csv",
            mimetype="text/csv"
        )
    return jsonify({"error": "Failed to generate CSV export"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Student Attendance Tracker Localhost Server on http://localhost:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
