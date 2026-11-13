# ARIA - Physical AI Lab Assistant

Voice + vision lab assistant. Students ask tech questions or "where is the multimeter?"; faculty register tools by photo and location.

## Run
```
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install flask python-dotenv                        # minimum for the website
python scripts/initialize_database.py
python main.py                                         # http://localhost:5000
```
Full AI stack: `pip install -r requirements.txt`, copy `.env.example` to `.env`, add `GROQ_API_KEY` / `GEMINI_API_KEY`.
On the robot: `python main.py --pi`.

Optional libraries (sentence-transformers, ultralytics, cv2, edge-tts, webrtcvad) are imported lazily; the site runs without them and falls back to simple behaviour.

## Layout
`frontend/` pages and assets, `backend/` Flask API, `ai_engine/` LLM, RAG, vision, speech, routing, `hardware/` Pi + microcontrollers, `database/` schema and seeds, `docs/` documentation.
