"""Remembers where each tool was last placed. Used by the 'where is X' intent."""
from database.connection import get_db

def remember(name, location, photo=None):
    db = get_db()
    db.execute("""INSERT INTO equipment(name,location,photo) VALUES(?,?,?)
        ON CONFLICT(name) DO UPDATE SET location=excluded.location, photo=COALESCE(excluded.photo,photo), updated_at=CURRENT_TIMESTAMP""",
        (name, location, photo))
    db.commit(); db.close()

def find(name):
    db = get_db()
    row = db.execute("SELECT name,location,photo FROM equipment WHERE lower(name) LIKE ? LIMIT 1", (f"%{name.lower().strip()}%",)).fetchone()
    if not row:  # fuzzy fallback: Whisper often mishears tool names
        import difflib
        names = [r["name"] for r in db.execute("SELECT name FROM equipment")]
        m = difflib.get_close_matches(name.title(), names, n=1, cutoff=0.6)
        if m: row = db.execute("SELECT name,location,photo FROM equipment WHERE name=?", (m[0],)).fetchone()
    db.close()
    return dict(row) if row else None
