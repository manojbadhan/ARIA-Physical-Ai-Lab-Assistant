# Architecture

```
Browser (frontend/)  --->  Flask API (backend/)  --->  SQLite (storage/aria.db)
                                 |
                                 v
                        ai_engine/orchestration/agent.py
              intent_router -> where_is | vision | greeting | general
                                                        |
                                    topic_filter -> RAG (optional) -> Groq / Gemini
Raspberry Pi (hardware/raspberry_pi/main.py): mic -> VAD -> Whisper -> wake word -> agent -> TTS -> speaker
                                              camera -> YOLO (best.pt) -> tracker -> usage photo -> /api/faculty/usage
```

Layers: `api` (HTTP) -> `services` (logic) -> `repositories` (SQL). The agent has no Flask dependency, so the Pi runs it directly.
