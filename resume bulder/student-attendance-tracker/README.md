# 🎓 Student Attendance Tracker (Python Backend CLI)

> **Academic Project**  
> **Tech Stack:** Python 3.x (Standard Library: `json`, `csv`, `os`, `datetime`, `unittest`)  
> **Persistence Engine:** Structured File I/O (CRUD without an external database)

---

## 📌 Project Overview

**Student Attendance Tracker** is a robust backend Command-Line Interface (CLI) application developed to manage institutional student attendance records without relying on external database management systems (like MySQL, PostgreSQL, or MongoDB). 

The project emphasizes core **software engineering fundamentals**, **logic building**, and **resilient data persistence** through structured file I/O operations (JSON & CSV), atomic file writes, error-tolerant user interactions, and statistical analytics.

---

## 🚀 Key Features

1. **Student Management (Master Record CRUD)**
   - **Create**: Add new students with unique Roll Numbers/IDs, full names, batch designations, and emails.
   - **Read**: View enrolled students, search records by Roll Number or Name.
   - **Update**: Modify student details while preserving historical records.
   - **Delete**: Remove student profiles with cascading cleanup of associated attendance logs.

2. **Daily Attendance Marking (Batch Session Register)**
   - Mark attendance for any calendar date (defaults to today `YYYY-MM-DD`).
   - Supports intuitive status codes: `[P]resent` (1.0 credit), `[A]bsent` (0.0 credit), and `[L]ate` (0.5 credit).
   - Duplicate entry prevention with interactive prompt to review/update existing logs.

3. **Analytics & Logic Building**
   - **Attendance Percentage**: Calculated dynamically per student:
     $$\text{Attendance \%} = \left( \frac{\text{Present} + 0.5 \times \text{Late}}{\text{Total Sessions}} \right) \times 100$$
   - **Defaulter Detection (< 75%)**: Automatically filters and highlights students below the mandatory 75% threshold, calculating the exact number of consecutive classes required to restore eligibility.

4. **Structured File Handling & Data Persistence**
   - **Zero External Dependencies**: Built entirely using Python standard libraries.
   - **Atomic File Writes**: Writes data to a temporary file (`.tmp`) before replacing the target via `os.replace`, preventing corrupted files during sudden application termination or power failure.
   - **Automatic Directory Bootstrapping**: Ensures required data folders (`data/`, `data/exports/`) exist at runtime.
   - **Corrupted File Recovery**: Creates an automated timestamped backup copy (`.corrupt.bak`) if unparsable data is detected.

5. **Reporting & Data Export**
   - Export cumulative class summary sheets to standard CSV format.
   - Export single-day attendance registers to CSV for reporting to faculty/administration.

---

## 📂 Project Architecture

```
student-attendance-tracker/
│
├── data/                               # Persistent file storage
│   ├── students.json                   # Master student profiles (JSON)
│   ├── attendance.json                 # Date-wise attendance registers (JSON)
│   └── exports/                        # Generated CSV attendance reports
│
├── src/
│   ├── __init__.py
│   ├── models.py                       # Data classes: Student, AttendanceStatus Enum
│   ├── storage.py                      # Resilient File I/O (Atomic writes, JSON/CSV handling)
│   ├── attendance_manager.py           # Core business logic (CRUD, percentages, defaulter alerts)
│   └── cli_ui.py                       # ANSI terminal UI, formatted tables, input validation
│
├── tests/
│   ├── __init__.py
│   └── test_tracker.py                 # Automated unit test suite (CRUD, calculations, I/O)
│
├── main.py                             # Interactive CLI entry point
├── sample_data.py                      # Demo generator with realistic student records
└── README.md                           # Documentation & Interview Guide
```

---

## 🛠️ Installation & Setup

1. **Clone or Navigate to the Project Directory:**
   ```bash
   cd student-attendance-tracker
   ```

2. **Verify Python Installation:**
   Requires Python 3.8+ (no third-party packages or virtual environment required):
   ```bash
   python --version
   ```

---

## 💻 How to Run

### 1. Launch the Interactive CLI
```bash
python main.py
```

### 2. Populate Sample Demo Records (Optional)
To quickly load 6 sample students and 5 days of attendance history for demonstration:
```bash
python sample_data.py
```
*(Or select Option 7 inside the running CLI menu).*

### 3. Run Automated Unit Tests
Verify all CRUD operations, file read/write resilience, and calculations:
```bash
python -m unittest discover -s tests
```

---

## 🖥️ CLI Menu Preview

```text
===================================================================
      🎓 STUDENT ATTENDANCE TRACKER - BACKEND CLI SYSTEM 🎓
         [File I/O CRUD Persistence · No Database Engine]
===================================================================

----------- MAIN MENU -----------
  1. 📝 Mark Daily Attendance (Batch Session)
  2. 📊 View Attendance Register & Percentages
  3. ⚠️  Identify Low Attendance Defaulters (< 75%)
  4. 👥 Student Management (Add / Update / Delete / List)
  5. 🔍 Search Attendance by Date or Roll No
  6. 📁 Export Attendance Report to CSV
  7. ⚡ Populate Sample Demo Data
  8. 🚪 Exit System
---------------------------------
```

---

## 🎯 Resume & Technical Interview Guide

When discussing this project with recruiters and interviewers, use these talking points:

### 1. Why file handling instead of a database?
> *"In this academic project, I chose to implement persistent storage purely through Python's file I/O operations rather than using an ORM or external database. This allowed me to demonstrate low-level systems logic: handling serialization/deserialization, managing file concurrency, handling edge cases like corrupted JSON files, and implementing the atomic write pattern."*

### 2. How did you ensure data integrity during file writes?
> *"In simple file write operations using `open(..., 'w')`, if the application crashes mid-write, the file is left truncated or corrupted. To prevent this, I implemented an **atomic write pattern** in `FileStorage`: the application writes to a temporary file (`.tmp`), invokes `os.fsync` to flush the buffer to physical disk, and then performs an atomic `os.replace` operation to replace the primary data file."*

### 3. How are attendance percentages calculated?
> *"The system treats `Present` as 1.0 session credit, `Late` as 0.5 session credit, and `Absent` as 0.0 credit. When calculating the defaulter threshold (< 75%), the system also projects how many consecutive upcoming classes a student must attend to cross the 75% mark, which provides actionable feedback rather than just a raw statistic."*

### 4. What is the time complexity of record lookups?
> *"In-memory data structures map Student IDs as dictionary hash keys ($O(1)$ lookup time), ensuring that reading a student or updating their attendance status executes in constant time before syncing to disk."*
