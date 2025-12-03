import sqlite3
from pathlib import Path

# This tells Python where to create the database file
DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to the SQLite database file."""
    return sqlite3.connect(str(db_path))
