"""RAG answering: hybrid search (BM25 + vectors) -> top chunks -> grounded LLM answer.

    from rag.retrieve import ask
    ask("How do I use the wash and cure machine?")
    -> {"answer": "...", "sources": [{"file": "...", "page": 7, "section": "..."}], "found": True}
"""
import re

import numpy as np

from config import SIMILARITY_THRESHOLD, TOP_K
from rag import ingest

NOT_IN_NOTES = "This is not in the notes."
CANDIDATES = 20          # how many chunks each search method proposes before fusing
RRF_K = 60               # standard reciprocal-rank-fusion constant
MIN_BM25 = 3.0           # BM25 score that counts as a real keyword match


def tokenize(text):
    return re.findall(r"\w+", text.lower())


class Retriever:
    def __init__(self):
        self.reload()

    def reload(self):
        """Call after ingest so new files are searchable without restarting the server."""
        from rank_bm25 import BM25Okapi
        self.chunks, self.vectors = ingest.load_store()
        self.bm25 = BM25Okapi([tokenize(c["text"]) for c in self.chunks]) if self.chunks else None

    def search(self, query, objects=None, k=TOP_K):
        """Return top-k chunks as dicts with a 0-1 'score' (cosine similarity of the best match)."""
        if not self.chunks:
            return []
        # Camera labels make "how do I use this?" searchable: "this" -> "multimeter"
        text = f"{query} {' '.join(objects)}" if objects else query

        sims = self.vectors @ ingest.embed([text])[0]               # cosine (vectors normalised)
        kw = np.asarray(self.bm25.get_scores(tokenize(text)))

        top_v = np.argsort(-sims)[:CANDIDATES]
        top_k = np.argsort(-kw)[:CANDIDATES]
        fused = {}
        for ranking in (top_v, top_k):                               # reciprocal rank fusion
            for rank, i in enumerate(ranking):
                fused[i] = fused.get(i, 0.0) + 1.0 / (RRF_K + rank + 1)
        best = sorted(fused, key=fused.get, reverse=True)[:k]

        results = []
        for i in best:
            # keep a chunk if EITHER method is confident about it
            if sims[i] >= SIMILARITY_THRESHOLD or kw[i] >= MIN_BM25:
                results.append({**self.chunks[i], "score": round(float(sims[i]), 3),
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
    return {"answer": answer, "sources": sources_of(hits), "found": True}


if __name__ == "__main__":                      # python -m rag.retrieve "your question"
    import json
    import sys
    q = " ".join(sys.argv[1:]) or "What is a wash and cure machine?"
    print(json.dumps(ask(q), indent=2, ensure_ascii=False))
