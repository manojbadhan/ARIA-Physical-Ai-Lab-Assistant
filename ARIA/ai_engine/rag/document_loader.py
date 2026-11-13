from pathlib import Path

def load_documents(folder="storage/documents"):
    docs = []
    for p in sorted(Path(folder).glob("**/*")):
        if p.suffix.lower() in (".txt", ".md"):
            docs.append({"source": p.name, "text": p.read_text(errors="ignore")})
    return docs
