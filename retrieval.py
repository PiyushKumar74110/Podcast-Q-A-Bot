import faiss
import pickle
import numpy as np
from embeddings import get_embedding


def search(query, index_path, meta_path, top_k=15):

    try:
        index = faiss.read_index(index_path)
        metadata = pickle.load(open(meta_path, "rb"))
    except Exception as e:
        print("Retrieval Error:", e)
        return []

    qv = np.array([get_embedding(query)], dtype="float32")

    distances, indices = index.search(qv, top_k)

    print("\nQUESTION:", query)
    print("DISTANCES:", distances)

    results = []

    for i in indices[0]:
        if i < len(metadata):
            results.append(metadata[i])

    print("\nTOP RESULTS:")
    for r in results[:3]:
        print(r["text"][:200])

    return results