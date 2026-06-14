import os
import pickle
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from operator import itemgetter

from utils.prompts import qa_prompt


# Load environment

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")


# Models


# Embedding (stable local model)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Google Gemini LLM (uses env API key)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)


# FAISS VECTOR STORE

def get_vector_store(video_id: str, transcript: str):
    """Cache & reuse FAISS vector store per video."""

    os.makedirs("cache", exist_ok=True)
    cache_path = f"cache/{video_id}_faiss.pkl"

    # Load cache if exists
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            print("Loaded cached FAISS store")
            return pickle.load(f)

    # Split transcript
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    docs = splitter.create_documents([transcript])

    # Create FAISS index
    vector_store = FAISS.from_documents(
        docs,
        embedding=embedding_model
    )

    # Save cache
    with open(cache_path, "wb") as f:
        pickle.dump(vector_store, f)

    print("New FAISS store saved")
    return vector_store



# RAG PIPELINE

def get_answer(transcript: str, question: str, video_id: str = "default") -> str:
    """Generate answer using FAISS + Gemini."""

    vector_store = get_vector_store(video_id, transcript)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # RAG chain
    chain = (
        RunnableParallel({
            "context": itemgetter("question") | retriever | RunnableLambda(format_docs),
            "question": itemgetter("question")
        })
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({"question": question})