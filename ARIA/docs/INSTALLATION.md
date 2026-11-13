# Installation

1. Python 3.10+. `python -m venv .venv` and activate it.
2. Website only: `pip install flask python-dotenv numpy`. Full stack: `pip install -r requirements.txt`.
3. `cp .env.example .env`, add `GROQ_API_KEY` (and `GEMINI_API_KEY` for vision fallback).
4. `python scripts/initialize_database.py`
5. `python main.py` then open http://localhost:5000
6. Raspberry Pi: `sudo apt install mpg123 espeak portaudio19-dev`, put YOLO weights at `ai_engine/vision/best.pt`, run `python main.py --pi`.
7. Docker: `docker compose up --build`
