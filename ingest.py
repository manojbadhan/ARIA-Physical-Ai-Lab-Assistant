"""RAG indexing: read notes (.pdf / .md / .txt) -> chunk -> embed -> save.

Run once from the project root:      python -m rag.ingest
Add one new file without a restart:  from rag.ingest import ingest_file; ingest_file("notes/new.pdf")

Every chunk keeps {file, page, section, text}. The UI needs file + page for source chips.
For .md files "page" is the section number and "section" is the heading text.
"""
import pickle
import re
from pathlib import Path

import numpy as np

from config import (CHUNK_OVERLAP, CHUNK_SIZE, CHUNKS_PATH, EMBEDDING_MODEL_NAME,
                    EMBEDDINGS_PATH, NOTES_DIR, STORE_DIR)

BASE = Path(__file__).resolve().parent.parent
SUPPORTED = {".pdf", ".md", ".txt"}
_model = None


def get_model():
    """Load the embedding model once and reuse it."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def embed(texts):
    """Normalised vectors, so cosine similarity = dot product."""
    return get_model().encode(texts, normalize_embeddings=True,
                              show_progress_bar=False).astype("float32")


# ---------- 1. read ----------
def read_pdf(path):
    import fitz  # PyMuPDF
    pages = []
    with fitz.open(path) as doc:
        for number, page in enumerate(doc, start=1):
            pages.append({"page": number, "section": "", "text": page.get_text()})
    return pages


def read_markdown(path):
    """One section per '#'/'##'/'###' heading, so a chunk never mixes two topics."""
    text = Path(path).read_text(encoding="utf-8")
    title = next((m.group(1) for m in re.finditer(r"^#\s+(.+)$", text, re.M)), Path(path).stem)
    parts = re.split(r"^(#{1,3}\s+.+)$", text, flags=re.M)  # [pre, h1, body, h2, body, ...]
    sections, heading = [], title
    if parts[0].strip():
        sections.append((heading, parts[0]))
    for i in range(1, len(parts), 2):
        heading = parts[i].lstrip("# ").strip()
        sections.append((heading, parts[i + 1]))
    return [{"page": n, "section": h, "text": f"{title} - {h}\n{body}"}
            for n, (h, body) in enumerate(sections, start=1) if body.strip()]


def read_file(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return read_pdf(path)
    if ext == ".md":
        return read_markdown(path)
    return [{"page": 1, "section": "", "text": Path(path).read_text(encoding="utf-8")}]


# ---------- 2. clean + chunk ----------
def clean(text):
    text = re.sub(r"-\n(\w)", r"\1", text)      # re-join words hyphenated at line end
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def split_words(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Sliding window over words (about 1 word = 1.3 tokens, so 400 words is a bit over the 300-500 target)."""
    words = text.split()
    if len(words) <= size:
        return [text] if words else []
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, len(words), step)
            if len(words[i:i + size]) > overlap]


def chunk_file(path):
    name = Path(path).name
    chunks = []
    for unit in read_file(path):
        for piece in split_words(clean(unit["text"])):
            if len(piece.split()) >= 8:         # drop page numbers, empty headers
                chunks.append({"file": name, "page": unit["page"],
                               "section": unit["section"], "text": piece})
    return chunks


# ---------- 3. save / load ----------
def save_store(chunks, vectors):
    (BASE / STORE_DIR).mkdir(parents=True, exist_ok=True)
    with open(BASE / CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    np.save(BASE / EMBEDDINGS_PATH, vectors)


def load_store():
    cp, ep = BASE / CHUNKS_PATH, BASE / EMBEDDINGS_PATH
    if not (cp.exists() and ep.exists()):
        return [], np.zeros((0, 384), dtype="float32")
    with open(cp, "rb") as f:
        return pickle.load(f), np.load(ep)


# ---------- 4. public API ----------
def ingest_all():
    """Rebuild the whole index from NOTES_DIR."""
    files = sorted(p for p in (BASE / NOTES_DIR).rglob("*") if p.suffix.lower() in SUPPORTED)
    chunks = [c for p in files for c in chunk_file(p)]
    if not chunks:
        raise SystemExit(f"No notes found in {BASE / NOTES_DIR}. Put .pdf/.md files there first.")
    save_store(chunks, embed([c["text"] for c in chunks]))
    print(f"[ingest] {len(files)} files -> {len(chunks)} chunks")
    return len(chunks)


def ingest_file(path):
    """Add (or replace) ONE file. Used by the /ingest endpoint after an upload."""
    path = Path(path)
    new = chunk_file(path)
    chunks, vectors = load_store()
    keep = [i for i, c in enumerate(chunks) if c["file"] != path.name]   # replace old version
    chunks = [chunks[i] for i in keep]
    vectors = vectors[keep] if keep else np.zeros((0, 384), dtype="float32")
    if new:
        chunks += new
        vectors = np.vstack([vectors, embed([c["text"] for c in new])])
    save_store(chunks, vectors)
    print(f"[ingest] {path.name}: {len(new)} chunks added, {len(chunks)} total")
    return len(new)


def list_notes():
    """For GET /notes: file name + number of pages/sections + chunk count."""
    chunks, _ = load_store()
    info = {}
    for c in chunks:
        d = info.setdefault(c["file"], {"file": c["file"], "pages": 0, "chunks": 0})
        d["pages"] = max(d["pages"], c["page"])
        d["chunks"] += 1
    return list(info.values())


if __name__ == "__main__":
    ingest_all()
