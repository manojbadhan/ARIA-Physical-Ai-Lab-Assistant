"""Pre-download the sentence-transformer used by the topic filter and RAG."""
from sentence_transformers import SentenceTransformer
SentenceTransformer("all-MiniLM-L6-v2")
print("Model cached. Put your YOLO weights at ai_engine/vision/best.pt")
