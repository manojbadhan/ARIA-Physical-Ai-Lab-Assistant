from backend.extensions import db

def all_items():
    rows = db().execute("SELECT name,location,qty,photo,updated_at FROM equipment ORDER BY name").fetchall()
    return [{"name": r["name"], "location": r["location"], "qty": r["qty"], "photo": r["photo"], "updated": (r["updated_at"] or "")[:10]} for r in rows]

def upsert(name, location, photo=None):
    db().execute("""INSERT INTO equipment(name,location,photo) VALUES(?,?,?)
        ON CONFLICT(name) DO UPDATE SET location=excluded.location, photo=COALESCE(excluded.photo,photo), updated_at=CURRENT_TIMESTAMP""",
        (name, location, photo))
    db().commit()

def find(name):
    return db().execute("SELECT * FROM equipment WHERE lower(name) LIKE ? LIMIT 1", (f"%{name.lower()}%",)).fetchone()

def add_detection(label, photo, kind="usage"):
    db().execute("INSERT INTO detections(label,photo,kind) VALUES(?,?,?)", (label, photo, kind)); db().commit()

def detections(kind="usage", limit=12):
    return db().execute("SELECT label,photo,created_at FROM detections WHERE kind=? ORDER BY id DESC LIMIT ?", (kind, limit)).fetchall()

def counts():
    d = db()
    q = lambda s: d.execute(s).fetchone()[0]
    return {"tools": q("SELECT COUNT(*) FROM equipment"), "missing": q("SELECT COUNT(*) FROM equipment WHERE qty=0"),
            "questions": q("SELECT COUNT(*) FROM conversations WHERE role='user' AND date(created_at)=date('now')"),
            "uses": q("SELECT COUNT(*) FROM detections WHERE kind='usage'")}
