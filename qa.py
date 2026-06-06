import os
import google.generativeai as genai

from dotenv import load_dotenv
from retrieval import search



# LOAD ENV

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found"
    )

genai.configure(
    api_key=api_key
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(
    question,
    index_path,
    meta_path
):

    
    # RETRIEVE CHUNKS
    
    results = search(
        question,
        index_path,
        meta_path,
        top_k=10
    )

    if not results:

        return {
            "answer": "No relevant information found.",
            "timestamp": 0,
            "segments": []
        }

    
    # BUILD CONTEXT
    
    context = "\n\n".join(
        chunk["text"]
        for chunk in results
    )

    
    # PROMPT
    
    prompt = f"""
You are a Podcast Question Answering Assistant.

The transcript excerpts below were retrieved because they are relevant to the user's question.

Transcript Excerpts:

{context}

Question:
{question}

Instructions:
- Answer using the transcript excerpts.
- Combine information from multiple excerpts if needed.
- Be concise and accurate.
- Do not repeat the question.
- Do not ask follow-up questions.
- Use only information found in the transcript excerpts.

Answer:
"""

    try:

        response = model.generate_content(
            prompt
        )

        answer = response.text.strip()

    except Exception as e:

        answer = (
            f"Gemini Error: {str(e)}"
        )

    return {
        "answer": answer,
        "timestamp": results[0]["start"],
        "segments": results
    }