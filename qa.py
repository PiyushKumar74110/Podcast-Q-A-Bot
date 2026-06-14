import os
from dotenv import load_dotenv
from retrieval import search


# LOAD ENV (optional if used elsewhere)
load_dotenv()


def generate_timestamp(question, index_path, meta_path):
    """
    Returns the most relevant timestamp using retrieval only (no LLM).
    """

    # -------------------------
    # RETRIEVE CHUNKS
    # -------------------------
    results = search(
        question,
        index_path,
        meta_path,
        top_k=10
    )

    # -------------------------
    # HANDLE EMPTY RESULTS
    # -------------------------
    if not results:
        return {
            "timestamp": 0,
            "segments": []
        }

    # -------------------------
    # PICK BEST MATCH (TOP-1)
    # -------------------------
    best_chunk = results[0]

    # safety check
    timestamp = best_chunk.get("start", 0)

    return {
        "timestamp": timestamp,
        "segments": results
    }