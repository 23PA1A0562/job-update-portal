"""Low-level file handling and persistence module.

Implements structured file I/O without a database:
- Safe reading and writing of JSON data stores.
- Atomic file write pattern (writes to temporary file first, then replaces) to guarantee data integrity.
- Directory bootstrapping and error resilience.
- CSV export capability for tabular attendance sheets.
"""

import os
import json
import csv
import shutil
from typing import Any, List, Dict, Optional


class FileStorage:
    """Manages file-based persistence for JSON and CSV formats."""

    @staticmethod
    def ensure_directory(dir_path: str) -> None:
        """Create directory if it does not exist."""
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    @classmethod
    def load_json(cls, file_path: str, default: Any = None) -> Any:
        """Read and parse JSON from a file. Returns default if file is missing or empty."""
        if not os.path.exists(file_path):
            return default if default is not None else {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return default if default is not None else {}
                return json.loads(content)
        except (json.JSONDecodeError, OSError) as err:
            # If the file is corrupted, create a timestamped backup before returning default
            backup_path = f"{file_path}.corrupt.bak"
            try:
                shutil.copyfile(file_path, backup_path)
            except OSError:
                pass
            print(f"[Warning] Failed to parse {file_path} ({err}). Created backup at {backup_path}")
            return default if default is not None else {}

    @classmethod
    def save_json(cls, file_path: str, data: Any) -> bool:
        """Atomically persist data to a JSON file.
        
        Writes data to a temporary file in the same directory first, 
        then renames/replaces it atomically to prevent half-written/corrupted files.
        """
        directory = os.path.dirname(file_path)
        if directory:
            cls.ensure_directory(directory)

        temp_file = f"{file_path}.tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())  # Ensure bytes are flushed to physical disk

            # Atomic file replacement
            os.replace(temp_file, file_path)
            return True
        except OSError as err:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except OSError:
                    pass
            print(f"[Error] File persistence failed for {file_path}: {err}")
            return False

    @classmethod
    def export_csv(cls, file_path: str, headers: List[str], rows: List[List[Any]]) -> bool:
        """Write structured tabular records to a CSV file."""
        directory = os.path.dirname(file_path)
        if directory:
            cls.ensure_directory(directory)

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            return True
        except OSError as err:
            print(f"[Error] Failed to export CSV to {file_path}: {err}")
            return False
