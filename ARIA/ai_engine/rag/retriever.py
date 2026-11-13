from ai_engine.rag.chunking import chunk_text
from ai_engine.rag.document_loader import load_documents
from ai_engine.rag.embeddings import embed
from ai_engine.rag.vector_store import VectorStore

class Retriever:
    def __init__(self, folder="storage/documents"):
        self.store = VectorStore()
        chunks = [{"source": d["source"], "text": c} for d in load_documents(folder) for c in chunk_text(d["text"])]
        if chunks: self.store.add(embed([c["text"] for c in chunks]), chunks)

    def context(self, query, k=3, min_score=0.35):
        hits = [m["text"] for s, m in self.store.search(embed([query])[0], k) if s >= min_score]
        return "\n---\n".join(hits)
