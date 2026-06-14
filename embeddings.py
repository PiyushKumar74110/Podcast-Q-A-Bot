from sentence_transformers import SentenceTransformer

# Defining model for embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Creating embeddings for content retrieval
def get_embedding(text):
    # Calling model to create embeddings
    return model.encode(text, normalize_embeddings=True).tolist()
