from sentence_transformers import SentenceTransformer

# Load once at module import
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    return model.encode(text)

def embed_batch(texts: list):
    return model.encode(texts)