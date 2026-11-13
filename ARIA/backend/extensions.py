from flask import g
from database.connection import get_db, init_db

def db():
    if "db" not in g:
        g.db = get_db()
    return g.db

def close_db(_exc=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()

def init_extensions(app):
    init_db()
    app.teardown_appcontext(close_db)
