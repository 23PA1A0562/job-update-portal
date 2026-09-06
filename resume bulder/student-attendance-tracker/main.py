"""Main entry point for the Student Attendance Tracker CLI Application.

Run this script to start the interactive terminal session:
    python main.py
"""

import os
import sys
from datetime import datetime

from src.attendance_manager import AttendanceManager
from src.models import AttendanceStatus
from src.cli_ui import CLIInterface, Colors
from sample_data import load_sample_dataset


class AttendanceCLIApp:
    """Orchestrates CLI workflows and user interactions."""

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        self.manager = AttendanceManager(data_dir)

    def run(self) -> None:
        """Main application lifecycle loop."""
        CLIInterface.print_banner()

        while True:
            try:
                CLIInterface.print_menu()
                choice = input(f"\n{Colors.BOLD}Select an option (1-8): {Colors.RESET}").strip()

                if choice == "1":
                    self.handle_mark_attendance()
                elif choice == "2":
                    self.handle_view_attendance_summary()
                elif choice == "3":
                    self.handle_view_defaulters()
                elif choice == "4":
                    self.handle_student_management()
                elif choice == "5":
                    self.handle_search_records()
                elif choice == "6":
                    self.handle_export_csv()
                elif choice == "7":
                    self.handle_populate_demo()
                elif choice == "8":
                    print(f"\n{Colors.GREEN}Thank you for using Student Attendance Tracker. Goodbye! 👋{Colors.RESET}\n")
                    sys.exit(0)
                else:
                    CLIInterface.print_error("Invalid option selected. Please choose a number between 1 and 8.")
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{Colors.YELLOW}Session interrupted by user. Exiting safely.{Colors.RESET}")
                sys.exit(0)
            except Exception as ex:
                CLIInterface.print_error(f"An unexpected error occurred: {ex}")

    # -------------------------------------------------------------------------
    # Option 1: Mark Attendance
    # -------------------------------------------------------------------------
    def handle_mark_attendance(self) -> None:
        students = self.manager.get_all_students()
        if not students:
            CLIInterface.print_warning("No students registered yet! Please add students first via Option 4.")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}--- Mark Daily Attendance Session ---{Colors.RESET}")
        date_str = CLIInterface.prompt_date("Enter Attendance Date (YYYY-MM-DD)")

        existing = self.manager.get_attendance_for_date(date_str)
        if existing:
            CLIInterface.print_warning(f"Attendance for {date_str} is ALREADY recorded ({len(existing)} records).")
            overwrite = CLIInterface.prompt_input("Do you want to review/update this date's records? (y/n)", default="y")
            if overwrite.lower() not in ("y", "yes"):
                print("Operation cancelled.")
                return

        print(f"\n{Colors.BLUE}Marking attendance for {len(students)} students on {date_str}.{Colors.RESET}")
        print("Legend: [P] = Present (1.0), [A] = Absent (0.0), [L] = Late (0.5 credit)\n")

        records = {}
        for idx, s in enumerate(students, start=1):
            current_status = existing.get(s.student_id, "Present") if existing else "Present"
            prompt_default = "P" if current_status == "Present" else ("A" if current_status == "Absent" else "L")

            while True:
                user_val = input(f"[{idx}/{len(students)}] {s.student_id} - {s.name} ({s.batch}) [{prompt_default}]: ").strip()
                if not user_val:
                    user_val = prompt_default
                try:
                    status_enum = AttendanceStatus.from_code(user_val)
                    records[s.student_id] = status_enum.value
                    break
                except ValueError as err:
                    print(f"{Colors.RED}{err}{Colors.RESET}")

        success, msg = self.manager.record_date_attendance(date_str, records)
        if success:
            CLIInterface.print_success(msg)
        else:
            CLIInterface.print_error(msg)

    # -------------------------------------------------------------------------
    # Option 2: View Register & Percentages
    # -------------------------------------------------------------------------
    def handle_view_attendance_summary(self) -> None:
        summary = self.manager.get_class_summary()
        if not summary:
            CLIInterface.print_warning("No student records available.")
            return

        total_dates = len(self.manager.get_all_dates())
        print(f"\n{Colors.CYAN}{Colors.BOLD}--- Class Attendance Register & Analytics Summary ---{Colors.RESET}")
        print(f"Total Academic Sessions Recorded: {Colors.BOLD}{total_dates}{Colors.RESET}\n")

        headers = ["Roll No", "Student Name", "Batch", "Sessions", "Present", "Absent", "Late", "Attendance %", "Status"]
        rows = []

        for item in summary:
            pct = item["percentage"]
            if item["total_sessions"] == 0:
                pct_display = "N/A"
                status_display = f"{Colors.YELLOW}No Sessions{Colors.RESET}"
            elif pct >= 75.0:
                pct_display = f"{Colors.GREEN}{pct:.1f}%{Colors.RESET}"
                status_display = f"{Colors.GREEN}ELIGIBLE{Colors.RESET}"
            else:
                pct_display = f"{Colors.RED}{pct:.1f}%{Colors.RESET}"
                status_display = f"{Colors.RED}SHORTAGE (<75%){Colors.RESET}"

            rows.append([
                item["student_id"],
                item["name"],
                item["batch"],
                item["total_sessions"],
                item["present_count"],
                item["absent_count"],
                item["late_count"],
                pct_display,
                status_display
            ])

        CLIInterface.render_table(headers, rows)

    # -------------------------------------------------------------------------
    # Option 3: Identify Defaulters
    # -------------------------------------------------------------------------
    def handle_view_defaulters(self) -> None:
        defaulters = self.manager.get_defaulters(threshold=75.0)
        print(f"\n{Colors.RED}{Colors.BOLD}--- Low Attendance Defaulter Report (< 75.0%) ---{Colors.RESET}")

        if not defaulters:
            CLIInterface.print_success("Great news! All enrolled students have maintained 75% or higher attendance.")
            return

        CLIInterface.print_warning(f"Found {len(defaulters)} student(s) with attendance below mandatory 75% threshold:")
        headers = ["Roll No", "Student Name", "Batch", "Total Classes", "Attended", "Attendance %", "Required for 75%"]
        rows = []

        for d in defaulters:
            # Calculate how many consecutive classes they need to attend to reach 75%
            # (present + x) / (total + x) >= 0.75  =>  x >= (0.75*total - present) / 0.25
            total = d["total_sessions"]
            effective = d["effective_present"]
            needed = max(0, int(((0.75 * total) - effective) / 0.25) + 1)

            rows.append([
                d["student_id"],
                d["name"],
                d["batch"],
                total,
                f"{effective:g}",
                f"{Colors.RED}{d['percentage']:.1f}%{Colors.RESET}",
                f"{Colors.YELLOW}+{needed} more classes{Colors.RESET}"
            ])

        CLIInterface.render_table(headers, rows)

    # -------------------------------------------------------------------------
    # Option 4: Student Management (CRUD)
    # -------------------------------------------------------------------------
    def handle_student_management(self) -> None:
        while True:
            print(f"\n{Colors.BOLD}--- Student Management Sub-Menu ---{Colors.RESET}")
            print(f"  {Colors.CYAN}1.{Colors.RESET} List All Students")
            print(f"  {Colors.CYAN}2.{Colors.RESET} Add New Student (Create)")
            print(f"  {Colors.CYAN}3.{Colors.RESET} Update Student Details (Update)")
            print(f"  {Colors.CYAN}4.{Colors.RESET} Delete Student Record (Delete)")
            print(f"  {Colors.CYAN}5.{Colors.RESET} Return to Main Menu")

            sub_choice = input(f"\n{Colors.BOLD}Select operation (1-5): {Colors.RESET}").strip()

            if sub_choice == "1":
                students = self.manager.get_all_students()
                headers = ["Roll No / ID", "Full Name", "Batch", "Email"]
                rows = [[s.student_id, s.name, s.batch, s.email or "N/A"] for s in students]
                print(f"\nTotal Students: {len(students)}")
                CLIInterface.render_table(headers, rows)

            elif sub_choice == "2":
                print(f"\n{Colors.CYAN}Add New Student:{Colors.RESET}")
                s_id = CLIInterface.prompt_input("Enter Student ID / Roll No (e.g. 23PA1A0507)")
                name = CLIInterface.prompt_input("Enter Student Full Name")
                batch = CLIInterface.prompt_input("Enter Batch / Section", default="CSE-A")
                email = CLIInterface.prompt_input("Enter Email Address (Optional)", default="", required=False)

                success, msg = self.manager.add_student(s_id, name, batch, email)
                if success:
                    CLIInterface.print_success(msg)
                else:
                    CLIInterface.print_error(msg)

            elif sub_choice == "3":
                s_id = CLIInterface.prompt_input("Enter Student ID to update")
                student = self.manager.get_student(s_id)
                if not student:
                    CLIInterface.print_error(f"Student with ID '{s_id.upper()}' does not exist.")
                    continue

                print(f"Editing {student.name} ({student.student_id}). Press Enter to keep current value.")
                new_name = CLIInterface.prompt_input("New Name", default=student.name)
                new_batch = CLIInterface.prompt_input("New Batch", default=student.batch)
                new_email = CLIInterface.prompt_input("New Email", default=student.email, required=False)

                success, msg = self.manager.update_student(s_id, new_name, new_batch, new_email)
                if success:
                    CLIInterface.print_success(msg)
                else:
                    CLIInterface.print_error(msg)

            elif sub_choice == "4":
                s_id = CLIInterface.prompt_input("Enter Student ID to delete")
                student = self.manager.get_student(s_id)
                if not student:
                    CLIInterface.print_error(f"Student with ID '{s_id.upper()}' does not exist.")
                    continue

                confirm = CLIInterface.prompt_input(f"Are you sure you want to permanently delete {student.name} and their records? (yes/no)", default="no")
                if confirm.lower() in ("y", "yes"):
                    success, msg = self.manager.delete_student(s_id)
                    if success:
                        CLIInterface.print_success(msg)
                    else:
                        CLIInterface.print_error(msg)
                else:
                    print("Deletion aborted.")

            elif sub_choice == "5":
                break
            else:
                CLIInterface.print_error("Invalid sub-menu choice.")

    # -------------------------------------------------------------------------
    # Option 5: Search Records
    # -------------------------------------------------------------------------
    def handle_search_records(self) -> None:
        print(f"\n{Colors.BOLD}--- Search Attendance Records ---{Colors.RESET}")
        print("  1. Search by Specific Date")
        print("  2. Search by Student Roll No")

        sub_choice = input(f"\n{Colors.BOLD}Choose search type (1-2): {Colors.RESET}").strip()

        if sub_choice == "1":
            date_str = CLIInterface.prompt_date("Enter Date to View (YYYY-MM-DD)")
            records = self.manager.get_attendance_for_date(date_str)
            if not records:
                CLIInterface.print_warning(f"No attendance record found for {date_str}.")
                return

            headers = ["Roll No", "Student Name", "Batch", "Attendance Status"]
            rows = []
            for s in self.manager.get_all_students():
                st = records.get(s.student_id, "Not Marked")
                color = Colors.GREEN if st == "Present" else (Colors.RED if st == "Absent" else Colors.YELLOW)
                rows.append([s.student_id, s.name, s.batch, f"{color}{st}{Colors.RESET}"])

            print(f"\nAttendance Register for: {Colors.BOLD}{date_str}{Colors.RESET}")
            CLIInterface.render_table(headers, rows)

        elif sub_choice == "2":
            s_id = CLIInterface.prompt_input("Enter Student ID / Roll No").upper()
            student = self.manager.get_student(s_id)
            if not student:
                CLIInterface.print_error(f"Student '{s_id}' not found.")
                return

            stats = self.manager.calculate_student_stats(s_id)
            print(f"\n{Colors.BOLD}Student Profile:{Colors.RESET} {student.name} ({student.student_id}) | Batch: {student.batch}")
            print(f"Attendance: {stats['percentage']}% ({stats['present_count']} Present, {stats['late_count']} Late, {stats['absent_count']} Absent out of {stats['total_sessions']} sessions)\n")

            headers = ["Date", "Status"]
            rows = []
            for date_key in self.manager.get_all_dates():
                day_records = self.manager.get_attendance_for_date(date_key) or {}
                if s_id in day_records:
                    st = day_records[s_id]
                    color = Colors.GREEN if st == "Present" else (Colors.RED if st == "Absent" else Colors.YELLOW)
                    rows.append([date_key, f"{color}{st}{Colors.RESET}"])

            CLIInterface.render_table(headers, rows)

    # -------------------------------------------------------------------------
    # Option 6: Export CSV
    # -------------------------------------------------------------------------
    def handle_export_csv(self) -> None:
        print(f"\n{Colors.CYAN}{Colors.BOLD}--- Export Attendance to CSV ---{Colors.RESET}")
        print("  1. Export Cumulative Class Summary (All Students + Percentages)")
        print("  2. Export Specific Date Attendance Register")

        sub_choice = input(f"\n{Colors.BOLD}Choose export type (1-2): {Colors.RESET}").strip()

        if sub_choice == "1":
            success, path_or_err = self.manager.export_summary_to_csv()
            if success:
                CLIInterface.print_success(f"Report exported successfully!\nFile: {path_or_err}")
            else:
                CLIInterface.print_error(path_or_err)

        elif sub_choice == "2":
            date_str = CLIInterface.prompt_date("Enter date to export (YYYY-MM-DD)")
            success, path_or_err = self.manager.export_date_attendance_to_csv(date_str)
            if success:
                CLIInterface.print_success(f"Daily report for {date_str} exported successfully!\nFile: {path_or_err}")
            else:
                CLIInterface.print_error(path_or_err)

    # -------------------------------------------------------------------------
    # Option 7: Demo Data
    # -------------------------------------------------------------------------
    def handle_populate_demo(self) -> None:
        confirm = CLIInterface.prompt_input("Populate demo engineering student records and 5 days of history? (y/n)", default="y")
        if confirm.lower() in ("y", "yes"):
            load_sample_dataset(self.manager)
            CLIInterface.print_success("Demo data loaded successfully! Choose Option 2 to view the register.")


if __name__ == "__main__":
    app = AttendanceCLIApp()
    app.run()
