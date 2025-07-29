"""
File Operations Module
Provides utility functions for creating directories and writing files.
"""

from pathlib import Path

def create_directory_structure(app_path: Path):
    """Creates the necessary directory structure for the Flask application."""
    app_path.mkdir(exist_ok=True) # Ensure base app directory exists

    # Core directories
    (app_path / "templates").mkdir(exist_ok=True)
    (app_path / "static" / "css").mkdir(parents=True, exist_ok=True)
    (app_path / "static" / "js").mkdir(exist_ok=True)
    (app_path / "static" / "uploads").mkdir(exist_ok=True)
    (app_path / "static" / "images").mkdir(exist_ok=True) # Added from paths.py
    (app_path / "logs").mkdir(exist_ok=True)
    (app_path / "routes").mkdir(exist_ok=True)
    (app_path / "utils").mkdir(exist_ok=True)
    (app_path / "data").mkdir(exist_ok=True) # Added from paths.py
    (app_path / "data" / "backups").mkdir(exist_ok=True) # Added from paths.py
    (app_path / "config").mkdir(exist_ok=True) # Added from paths.py

    print(f"Created directory structure in {app_path}")

def write_file(file_path: Path, content: str):
    """Writes content to a specified file, creating parent directories if needed."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Generated: {file_path}")