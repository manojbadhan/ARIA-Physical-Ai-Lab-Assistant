from database.connection import get_db

ITEMS = [("Multimeter", "Rack 2, Box 3", 4), ("ESP32 DevKit", "Almirah A, Box 1", 9),
         ("Soldering iron", "Rack 1, Box 2", 2), ("Raspberry Pi 5", "Almirah B, Box 4", 3),
         ("Jumper wires", "Rack 3, Box 1", 20), ("Breadboard", "Rack 3, Box 2", 12)]

def seed(path=None):
    db = get_db(path)
    for name, loc, qty in ITEMS:
        db.execute("INSERT OR IGNORE INTO equipment(name,location,qty) VALUES(?,?,?)", (name, loc, qty))
    db.commit(); db.close()

if __name__ == "__main__":
    seed()
