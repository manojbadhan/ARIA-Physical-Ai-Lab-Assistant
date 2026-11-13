# API

| Method | Path | Body | Returns |
|---|---|---|---|
| POST | /api/auth/signup | name, email, password, role | user, redirects for forms |
| POST | /api/auth/login | email, password | user |
| POST | /api/chat | {message} | {reply, intent, photo?} |
| GET | /api/inventory | | {items[]} |
| GET | /api/inventory/stats | | tools, missing, questions, uses, recent |
| POST | /api/vision/identify | multipart image | {label, photo} |
| POST | /api/voice/stt | multipart audio | {text} |
| POST | /api/voice/tts | {text} | audio/mpeg |
| POST | /api/faculty/tools | multipart photo, name, almirah, rack, box | {ok, name, location} |
| GET | /api/faculty/usage | | {items[]} |
| POST | /api/faculty/usage | multipart photo, tool | {ok} (robot) |
