import os
import pickle
import faiss
import numpy as np

from embeddings import get_embedding


def build_index(segments, vid):

    os.makedirs("data", exist_ok=True)

    index_path = f"data/vectors_{vid}.faiss"
    meta_path = f"data/meta_{vid}.pkl"

    
    # USE EXISTING FILE
    if os.path.exists(index_path) and os.path.exists(meta_path):
        print("Using cached FAISS index")
        return index_path, meta_path

    vectors = []
    metadata = []

    print(f"Creating embeddings for {len(segments)} segments...")

    for seg in segments:

        text = seg["text"].strip()

        if not text:
            continue

        embedding = get_embedding(text)

        vectors.append(embedding)

        metadata.append(
            {
                "text": seg["text"],
                "start": seg["start"],
                "end": seg["end"]
            }
        )

    if len(vectors) == 0:
        raise ValueError("No valid transcript segments found")

    vectors = np.array(vectors, dtype="float32")

    # normalize for cosine similarity
    faiss.normalize_L2(vectors)

    dimension = vectors.shape[1]

    # cosine similarity index
    index = faiss.IndexFlatIP(dimension)

    index.add(vectors)

    faiss.write_index(index, index_path)

    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

    print(f"FAISS index created with {index.ntotal} vectors")

    return index_path, meta_path

