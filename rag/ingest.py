import re
from pathlib import Path

import numpy as np

from config import CHUNK_OVERLAP, CHUNK_SIZE, EMBEDDING_MODEL_NAME, NOTES_DIR
from rag import db

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


# ---------- 3. load ----------
def load_store():
    return db.load_all()


# ---------- 4. public API ----------
def ingest_all(force=False):
    """Sync NOTES_DIR into the database. Only new or changed files are re-embedded."""
    files = sorted(p for p in (BASE / NOTES_DIR).rglob("*") if p.suffix.lower() in SUPPORTED)
    if not files:
        raise SystemExit(f"No notes found in {BASE / NOTES_DIR}. Put .pdf/.md files there first.")
    by_name = {p.name: p for p in files}

    con = db.connect()
    known = db.known_hashes(con)

    for name in set(known) - set(by_name):          # file deleted from notes/
        db.remove_file(con, name)
        print(f"[ingest] removed   {name}")

    for name, path in by_name.items():
        h = db.file_hash(path)
        if not force and known.get(name) == h:
            print(f"[ingest] unchanged {name}")
            continue
        chunks = chunk_file(path)
        vectors = embed([c["text"] for c in chunks]) if chunks else []
        db.replace_file(con, name, h, chunks, vectors)
        print(f"[ingest] ingested  {name}: {len(chunks)} chunks")

    total = db.count(con)
    con.close()
    print(f"[ingest] {len(files)} files -> {total} chunks")
    return total


def ingest_file(path):
    """Add (or replace) ONE file. Used by the /ingest endpoint after an upload."""
    path = Path(path)
    new = chunk_file(path)
    vectors = embed([c["text"] for c in new]) if new else []
    con = db.connect()
    db.replace_file(con, path.name, db.file_hash(path), new, vectors)
    total = db.count(con)
    con.close()
    print(f"[ingest] {path.name}: {len(new)} chunks added, {total} total")
    return len(new)


def list_notes():
    """For GET /notes: file name + number of pages/sections + chunk count."""
    return db.notes_summary()


if __name__ == "__main__":                      # python -m rag.ingest [--force]
    import sys
    ingest_all(force="--force" in sys.argv)