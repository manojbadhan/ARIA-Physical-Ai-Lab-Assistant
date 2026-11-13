import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from database.connection import init_db
from database.seeders.seed_equipment import seed

if __name__ == "__main__":
    init_db(); seed(); print("Database ready: storage/aria.db")
