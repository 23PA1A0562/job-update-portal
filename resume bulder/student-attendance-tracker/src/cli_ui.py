"""Terminal UI rendering, formatting, and interactive input handling.

Features:
- ANSI color formatting for clear visual cues (Green=Present, Red=Absent/Defaulter, Yellow=Late/Warning).
- Formatted tabular data rendering with automatic column padding.
- Input validation helpers to prevent runtime errors on invalid user input.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional


class Colors:
    """ANSI terminal color codes."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


class CLIInterface:
    """Terminal interface utilities for formatted output and user interactions."""

    @staticmethod
    def print_banner() -> None:
        """Displays the application header."""
        banner = f"""{Colors.CYAN}{Colors.BOLD}
===================================================================
      🎓 STUDENT ATTENDANCE TRACKER - BACKEND CLI SYSTEM 🎓
         [File I/O CRUD Persistence · No Database Engine]
==================================================================={Colors.RESET}"""
        print(banner)

    @staticmethod
    def print_success(msg: str) -> None:
        print(f"{Colors.GREEN}{Colors.BOLD}[✓ SUCCESS]{Colors.RESET} {msg}")

    @staticmethod
    def print_error(msg: str) -> None:
        print(f"{Colors.RED}{Colors.BOLD}[✗ ERROR]{Colors.RESET} {msg}")

    @staticmethod
    def print_warning(msg: str) -> None:
        print(f"{Colors.YELLOW}{Colors.BOLD}[! WARNING]{Colors.RESET} {msg}")

    @staticmethod
    def print_info(msg: str) -> None:
        print(f"{Colors.BLUE}[ℹ INFO]{Colors.RESET} {msg}")

    @staticmethod
    def print_menu() -> None:
        """Prints the primary interaction menu."""
        menu = f"""
{Colors.BOLD}----------- MAIN MENU -----------{Colors.RESET}
  {Colors.CYAN}1.{Colors.RESET} 📝 Mark Daily Attendance (Batch Session)
  {Colors.CYAN}2.{Colors.RESET} 📊 View Attendance Register & Percentages
  {Colors.CYAN}3.{Colors.RESET} ⚠️  Identify Low Attendance Defaulters (< 75%)
  {Colors.CYAN}4.{Colors.RESET} 👥 Student Management (Add / Update / Delete / List)
  {Colors.CYAN}5.{Colors.RESET} 🔍 Search Attendance by Date or Roll No
  {Colors.CYAN}6.{Colors.RESET} 📁 Export Attendance Report to CSV
  {Colors.CYAN}7.{Colors.RESET} ⚡ Populate Sample Demo Data
  {Colors.CYAN}8.{Colors.RESET} 🚪 Exit System
---------------------------------"""
        print(menu)

    @staticmethod
    def prompt_input(prompt: str, default: Optional[str] = None, required: bool = True) -> str:
        """Prompt user with optional default value and non-empty enforcement."""
        prompt_text = f"{Colors.BOLD}{prompt}{Colors.RESET}"
        if default is not None:
            prompt_text += f" [{default}]"
        prompt_text += ": "

        while True:
            val = input(prompt_text).strip()
            if not val and default is not None:
                return default
            if not val and required:
                print(f"{Colors.RED}This field is required. Please enter a value.{Colors.RESET}")
                continue
            return val

    @staticmethod
    def prompt_date(prompt: str = "Enter Date (YYYY-MM-DD)") -> str:
        """Prompts for a date, defaulting to today."""
        today_str = datetime.now().strftime("%Y-%m-%d")
        while True:
            val = input(f"{Colors.BOLD}{prompt}{Colors.RESET} [{today_str}]: ").strip()
            if not val:
                return today_str
            try:
                datetime.strptime(val, "%Y-%m-%d")
                return val
            except ValueError:
                print(f"{Colors.RED}Invalid date format '{val}'. Must be YYYY-MM-DD (e.g. 2026-09-06).{Colors.RESET}")

    @staticmethod
    def render_table(headers: List[str], rows: List[List[Any]]) -> None:
        """Prints formatted tabular data with dynamic column sizing."""
        if not rows:
            print(f"{Colors.YELLOW}(No records found){Colors.RESET}")
            return

        # Calculate max column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for idx, cell in enumerate(row):
                # Strip ANSI codes when calculating width
                clean_cell = str(cell)
                for color_code in [Colors.HEADER, Colors.BLUE, Colors.CYAN, Colors.GREEN,
                                   Colors.YELLOW, Colors.RED, Colors.BOLD, Colors.UNDERLINE, Colors.RESET]:
                    clean_cell = clean_cell.replace(color_code, "")
                if len(clean_cell) > col_widths[idx]:
                    col_widths[idx] = len(clean_cell)

        # Build horizontal separator
        sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

        # Print header
        print(sep)
        header_line = "| " + " | ".join(f"{Colors.BOLD}{h.ljust(col_widths[i])}{Colors.RESET}" for i, h in enumerate(headers)) + " |"
        print(header_line)
        print(sep)

        # Print rows
        for row in rows:
            formatted_cells = []
            for i, cell in enumerate(row):
                cell_str = str(cell)
                # Compute visual length
                clean_cell = cell_str
                for code in [Colors.HEADER, Colors.BLUE, Colors.CYAN, Colors.GREEN,
                             Colors.YELLOW, Colors.RED, Colors.BOLD, Colors.UNDERLINE, Colors.RESET]:
                    clean_cell = clean_cell.replace(code, "")
                padding = col_widths[i] - len(clean_cell)
                formatted_cells.append(cell_str + (" " * padding))
            print("| " + " | ".join(formatted_cells) + " |")

        print(sep)
