"""SQLite store: one row per chunk, the embedding vector saved as float32 bytes."""
import hashlib
import sqlite3
from pathlib import Path

import numpy as np

from config import STORE_DIR

BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / STORE_DIR / "lab.db"
DIM = 384          # all-MiniLM-style size, same as your old np.zeros((0, 384))


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")     # makes ON DELETE CASCADE work
    con.executescript("""
        CREATE TABLE IF NOT EXISTS files (
            name TEXT PRIMARY KEY,
            hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS chunks (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            file    TEXT NOT NULL REFERENCES files(name) ON DELETE CASCADE,
            page    INTEGER NOT NULL,
            section TEXT NOT NULL,
            text    TEXT NOT NULL,
            vector  BLOB NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_chunks_file ON chunks(file);
    """)
    return con


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def known_hashes(con):
    return dict(con.execute("SELECT name, hash FROM files"))


def replace_file(con, name, h, chunks, vectors):
    """Swap in the new version of one file (old rows deleted) in a single transaction."""
    with con:
        con.execute("DELETE FROM files WHERE name = ?", (name,))   # cascades to its chunks
        con.execute("INSERT INTO files (name, hash) VALUES (?, ?)", (name, h))
        con.executemany(
            "INSERT INTO chunks (file, page, section, text, vector) VALUES (?, ?, ?, ?, ?)",
            [(name, c["page"], c["section"], c["text"],
              np.asarray(v, dtype=np.float32).tobytes())
             for c, v in zip(chunks, vectors)],
        )


def remove_file(con, name):
    with con:
        con.execute("DELETE FROM files WHERE name = ?", (name,))


def count(con):
    return con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]


def load_all():
    """Same shape the old pickle/npy gave: (list of chunk dicts, float32 matrix)."""
    con = connect()
    rows = con.execute(
        "SELECT file, page, section, text, vector FROM chunks ORDER BY id").fetchall()
    con.close()
    if not rows:
        return [], np.zeros((0, DIM), dtype="float32")
    chunks = [{"file": f, "page": p, "section": s, "text": t} for f, p, s, t, _ in rows]
    vectors = np.vstack([np.frombuffer(v, dtype=np.float32) for *_, v in rows])
    return chunks, vectors


def notes_summary():
    con = connect()
    rows = con.execute(
        "SELECT file, MAX(page), COUNT(*) FROM chunks GROUP BY file ORDER BY file").fetchall()
    con.close()
    return [{"file": f, "pages": p, "chunks": n} for f, p, n in rows]