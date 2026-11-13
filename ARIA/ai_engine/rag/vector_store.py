import json
from pathlib import Path
import numpy as np

class VectorStore:
    def __init__(self, folder="storage/embeddings"):
        self.dir = Path(folder); self.vecs = None; self.meta = []

    def add(self, vectors, meta):
        v = np.asarray(vectors)
        self.vecs = v if self.vecs is None else np.vstack([self.vecs, v]); self.meta += meta

    def search(self, qvec, k=3):
        if self.vecs is None or not len(self.meta): return []
        scores = self.vecs @ np.asarray(qvec).reshape(-1)
        return [(float(scores[i]), self.meta[i]) for i in np.argsort(-scores)[:k]]

    def save(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        np.save(self.dir / "vecs.npy", self.vecs); (self.dir / "meta.json").write_text(json.dumps(self.meta))

    def load(self):
        if (self.dir / "vecs.npy").exists():
            self.vecs = np.load(self.dir / "vecs.npy"); self.meta = json.loads((self.dir / "meta.json").read_text())
        return self
