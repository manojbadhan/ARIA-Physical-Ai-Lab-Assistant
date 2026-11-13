from backend.extensions import db

def create(name, email, pw_hash, role):
    c = db().execute("INSERT INTO users(name,email,password_hash,role) VALUES(?,?,?,?)", (name, email, pw_hash, role))
    db().commit(); return c.lastrowid

def by_email(email):
    return db().execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
