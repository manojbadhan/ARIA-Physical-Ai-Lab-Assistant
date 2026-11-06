"""ChromaDB store: one record per chunk (text + embedding + metadata)."""
import hashlib
from pathlib import Path

import chromadb
import numpy as np

from config import STORE_DIR

BASE = Path(__file__).resolve().parent.parent
CHROMA_PATH = BASE / STORE_DIR / "chroma"
COLLECTION = "lab_notes"
BATCH = 500
_collection = None


def connect():
    global _collection
    if _collection is None:
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        _collection = client.get_or_create_collection(
            COLLECTION, metadata={"hnsw:space": "cosine"})
    return _collection


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def known_hashes(col):
    metas = col.get(include=["metadatas"])["metadatas"]
    return {m["file"]: m["hash"] for m in metas}


def replace_file(col, name, h, chunks, vectors):
    """Delete the old chunks of this file, then add the new ones."""
    col.delete(where={"file": name})
    equipment = name.split("_")[0] if name.startswith("LAB-OBJ") else ""
    for start in range(0, len(chunks), BATCH):
        part = chunks[start:start + BATCH]
        col.add(
            ids=[f"{name}::{start + i}" for i in range(len(part))],
            embeddings=[np.asarray(v, dtype=np.float32).tolist()
                        for v in vectors[start:start + BATCH]],
            documents=[c["text"] for c in part],
            metadatas=[{"file": name, "hash": h, "page": c["page"],
                        "section": c["section"], "equipment": equipment}
                       for c in part],
        )


def remove_file(col, name):
    col.delete(where={"file": name})


def count(col):
    return col.count()


def load_chunks():
    """All chunks as dicts (BM25 needs the texts). Vectors stay inside Chroma."""
    data = connect().get(include=["documents", "metadatas"])
    return [{"id": i, "file": m["file"], "page": m["page"],
             "section": m["section"], "text": d}
            for i, d, m in zip(data["ids"], data["documents"], data["metadatas"])]


def query(vector, n):
    """Top-n most similar chunks as (id, cosine similarity)."""
    col = connect()
    n = min(n, col.count())
    if n == 0:
        return []
    res = col.query(query_embeddings=[np.asarray(vector, dtype=np.float32).tolist()],
                    n_results=n)
    return [(i, 1.0 - d) for i, d in zip(res["ids"][0], res["distances"][0])]


def similarities(vector, ids):
    """Cosine similarity for specific chunks (ones BM25 found but vector search didn't)."""
    res = connect().get(ids=ids, include=["embeddings"])
    vecs = np.asarray(res["embeddings"], dtype=np.float32)
    sims = vecs @ np.asarray(vector, dtype=np.float32)
    return dict(zip(res["ids"], sims.tolist()))


def notes_summary():
    metas = connect().get(include=["metadatas"])["metadatas"]
    out = {}
    for m in metas:
        f = out.setdefault(m["file"], {"file": m["file"], "pages": 0, "chunks": 0})
        f["pages"] = max(f["pages"], m["page"])
        f["chunks"] += 1
    return sorted(out.values(), key=lambda x: x["file"])