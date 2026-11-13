"""Tech/lab-only filter. Embedding similarity to topic anchors; keyword fallback if the model is missing."""
TOPICS = ["Raspberry Pi", "ESP32", "Arduino", "sensors", "motors and servos", "ROS and robotics", "computer vision",
          "YOLO object detection", "machine learning", "deep learning", "large language models", "Python programming",
          "C++ programming", "electronics circuits", "multimeter and lab tools", "soldering", "networking",
          "operating systems", "databases", "cloud computing", "3D printing", "microcontrollers", "embedded systems",
          "algorithms", "cybersecurity"]
ALLOW, NEAR = 0.38, 0.25
_emb = None

def _keyword_check(q):
    ql = q.lower()
    for t in TOPICS:
        if any(w in ql for w in t.lower().split() if len(w) > 3): return "allow", t
    return "reject", None

def check(query):
    global _emb
    try:
        from ai_engine.rag.embeddings import _st
        import numpy as np
        m = _st()
        if _emb is None: _emb = m.encode(TOPICS, normalize_embeddings=True)
        sims = _emb @ m.encode(query, normalize_embeddings=True)
        i = int(np.argmax(sims)); s = float(sims[i])
        return ("allow" if s >= ALLOW else "suggest" if s >= NEAR else "reject"), (TOPICS[i] if s >= NEAR else None)
    except ImportError:
        return _keyword_check(query)
