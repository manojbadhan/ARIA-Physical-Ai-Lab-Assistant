import hashlib
import numpy as np

_model = None

def _st():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed(texts):
    """Sentence-transformer embeddings; falls back to hashed bag-of-words if not installed."""
    try:
        return np.asarray(_st().encode(list(texts), normalize_embeddings=True))
    except ImportError:
        out = np.zeros((len(texts), 256), dtype="float32")
        for i, t in enumerate(texts):
            for w in t.lower().split():
                out[i, int(hashlib.md5(w.encode()).hexdigest(), 16) % 256] += 1
        n = np.linalg.norm(out, axis=1, keepdims=True); n[n == 0] = 1
        return out / n
