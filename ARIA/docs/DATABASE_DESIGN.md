# Database (SQLite)

- **users**(id, name, email unique, password_hash, role, created_at)
- **equipment**(id, name unique, location, qty, photo, updated_at)
- **conversations**(id, user_id, role, text, created_at)
- **detections**(id, label, photo, kind: usage|detected, created_at)

Schema: `database/init.sql`. Seed data: `database/seeders/seed_equipment.py`.
