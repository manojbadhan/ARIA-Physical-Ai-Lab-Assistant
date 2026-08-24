import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
GROQ_MODEL = "openai/gpt-oss-120b"  
STT_MODEL = "whisper-large-v3-turbo"

# RAG 
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  
NOTES_DIR = "notes/"
CHUNK_SIZE = 400          # characters per chunk
CHUNK_OVERLAP = 50
TOP_K = 3                 # how many chunks to retrieve per question
SIMILARITY_THRESHOLD = 0.35  # below this, treat as "no relevant notes found"

# Store paths 
STORE_DIR = "rag/store/"
CHUNKS_PATH = STORE_DIR + "chunks.pkl"
EMBEDDINGS_PATH = STORE_DIR + "embeddings.npy"