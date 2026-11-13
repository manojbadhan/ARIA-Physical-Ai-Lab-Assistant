import sys, pathlib, pytest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

@pytest.fixture
def client(tmp_path, monkeypatch):
    import database.connection as c
    monkeypatch.setattr(c, "DB_PATH", tmp_path / "t.db")
    c.init_db()
    from database.seeders.seed_equipment import seed
    seed()
    from backend.app import create_app
    app = create_app(); app.config["TESTING"] = True
    return app.test_client()
