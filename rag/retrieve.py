"""RAG answering: hybrid search (BM25 + vectors) -> top chunks -> grounded LLM answer.

    from rag.retrieve import ask
    ask("How do I use the wash and cure machine?")
    -> {"answer": "...", "sources": [{"file": "...", "page": 7, "section": "..."}], "found": True}
"""
import re

import numpy as np

from config import SIMILARITY_THRESHOLD, TOP_K
from rag import db, ingest

NOT_IN_NOTES = "This is not in the notes."
CANDIDATES = 20          # how many chunks each search method proposes before fusing
RRF_K = 60               # standard reciprocal-rank-fusion constant
MIN_BM25 = 3.0           # BM25 score that counts as a real keyword match

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "it", "its", "this", "that",
    "what", "which", "who", "how", "why", "when", "where", "do", "does", "did",
    "of", "to", "in", "on", "for", "with", "and", "or", "can", "i", "you", "me", "my",
}


def tokenize(text):
    return [w for w in re.findall(r"\w+", text.lower()) if w not in STOPWORDS]


class Retriever:
    def __init__(self):
        self.reload()

    def reload(self):
        """Call after ingest so new files are searchable without restarting the server."""
        from rank_bm25 import BM25Okapi
        self.chunks = ingest.load_store()
        self.pos = {c["id"]: i for i, c in enumerate(self.chunks)}
        self.bm25 = BM25Okapi([tokenize(c["text"]) for c in self.chunks]) if self.chunks else None

    def search(self, query, objects=None, k=TOP_K):
        """Return top-k chunks as dicts with a 0-1 'score' (cosine similarity)."""
        if not self.chunks:
            return []
        # Camera labels make "how do I use this?" searchable: "this" -> "multimeter"
        text = f"{query} {' '.join(objects)}" if objects else query

        qvec = ingest.embed([text])[0]
        vec_hits = db.query(qvec, CANDIDATES)                  # Chroma vector search
        sims = dict(vec_hits)
        top_v = [self.pos[i] for i, _ in vec_hits if i in self.pos]

        kw = np.asarray(self.bm25.get_scores(tokenize(text)))
        top_k = np.argsort(-kw)[:CANDIDATES]

        fused = {}
        for ranking in (top_v, top_k):                         # reciprocal rank fusion
            for rank, i in enumerate(ranking):
                fused[i] = fused.get(i, 0.0) + 1.0 / (RRF_K + rank + 1)
        best = sorted(fused, key=fused.get, reverse=True)[:k]

        # chunks found only by BM25 have no vector score yet, so fetch it
        missing = [self.chunks[i]["id"] for i in best if self.chunks[i]["id"] not in sims]
        if missing:
            sims.update(db.similarities(qvec, missing))

        results = []
        for i in best:
            s = sims[self.chunks[i]["id"]]
            # keep a chunk if EITHER method is confident about it
            if s >= SIMILARITY_THRESHOLD or kw[i] >= MIN_BM25:
                results.append({**self.chunks[i], "score": round(float(s), 3),
                                "keyword": round(float(kw[i]), 2)})
        return results


_retriever = None


def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def build_context(hits):
    return "\n\n".join(f"[{h['file']}, {'section' if h['section'] else 'page'} "
                       f"{h['section'] or h['page']}]\n{h['text']}" for h in hits)


def sources_of(hits):
    seen, out = set(), []
    for h in hits:
        key = (h["file"], h["page"])
        if key not in seen:
            seen.add(key)
            out.append({"file": h["file"], "page": h["page"], "section": h["section"],
                        "score": h["score"]})
    return out


def for_speech(text):
    """Clean an answer so text-to-speech reads it naturally."""
    text = re.sub(r"\[[^\]]*\.(md|pdf|txt)[^\]]*\]", "", text)   # [file.md, section 3]
    text = re.sub(r"[*_`#>]+", "", text)                           # markdown symbols
    text = re.sub(r"^\s*[-•]\s+", "", text, flags=re.M)            # bullet markers
    return re.sub(r"\s+", " ", text).strip()


def ask(query, objects=None, history=None, llm=None):
    """Full RAG answer. Does NOT call the LLM when nothing relevant is found."""
    hits = get_retriever().search(query, objects)
    if not hits:
        return {"answer": NOT_IN_NOTES, "sources": [], "found": False}
    if llm is None:
        from llm.model import LabAssistantLLM
        llm = LabAssistantLLM()
    from llm.prompts import RAG_SYSTEM_PROMPT
    answer = llm.generate_response(user_message=query, system_prompt=RAG_SYSTEM_PROMPT,
                                   conversation_history=history,
                                   retrieved_context=build_context(hits))
    return {"answer": answer, "speech": for_speech(answer),
            "sources": sources_of(hits), "found": True}

def ensure_store():
    """Build or update the database from notes/ (only new or changed files are embedded).
    This makes a fresh machine, such as the Pi, work without a manual ingest."""
    try:
        ingest.ingest_all()
    except SystemExit as error:                 # ingest_all exits when notes/ is missing or empty
        print(f"[rag] NO NOTES FOUND: {error}")
    except Exception as error:
        print(f"[rag] ingest failed: {type(error).__name__}: {error}")


def warm_up():
    ensure_store()
    retriever = get_retriever()
    retriever.reload()
    print(f"[rag] ready: {len(retriever.chunks)} chunks loaded")
    retriever.search("warm up")                 # loads the embedding model


if __name__ == "__main__":                      # python -m rag.retrieve "your question"
    import json
    import sys
    q = " ".join(sys.argv[1:]) or "What is a wash and cure machine?"
    print(json.dumps(ask(q), indent=2, ensure_ascii=False))