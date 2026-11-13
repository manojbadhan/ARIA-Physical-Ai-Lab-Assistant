from backend.extensions import db

def add(user_id, role, text):
    db().execute("INSERT INTO conversations(user_id,role,text) VALUES(?,?,?)", (user_id, role, text)); db().commit()

def history(user_id, limit=10):
    rows = db().execute("SELECT role,text FROM conversations WHERE user_id IS ? ORDER BY id DESC LIMIT ?", (user_id, limit)).fetchall()
    return [{"role": r["role"], "content": r["text"]} for r in reversed(rows)]
