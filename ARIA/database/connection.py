import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "storage" / "aria.db"

def get_db(path=None):
    conn = sqlite3.connect(str(path or DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db(path=None):
    conn = get_db(path)
    conn.executescript((ROOT / "database" / "init.sql").read_text())
    conn.commit()
    conn.close()
