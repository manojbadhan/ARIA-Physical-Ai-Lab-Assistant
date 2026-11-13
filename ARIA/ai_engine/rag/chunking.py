def chunk_text(text, size=500, overlap=80):
    words, out, step = text.split(), [], max(1, size - overlap)
    for i in range(0, len(words), step):
        piece = " ".join(words[i:i + size])
        if piece: out.append(piece)
    return out
