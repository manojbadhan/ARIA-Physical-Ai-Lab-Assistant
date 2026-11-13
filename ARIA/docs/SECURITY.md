# Security

- Passwords hashed with Werkzeug (scrypt/pbkdf2). Never stored in plain text.
- Set `SECRET_KEY` and `DEV_OPEN_ACCESS=0` before deploying; faculty endpoints then require a faculty session.
- Uploads limited to 16 MB, filenames sanitised. Keep `.env` out of git.
- Known gap: no CSRF token on form posts and no rate limiting. Add Flask-WTF and Flask-Limiter before public hosting.
- `POST /api/faculty/usage` is open so the robot can post photos; protect it with a shared token in production.
