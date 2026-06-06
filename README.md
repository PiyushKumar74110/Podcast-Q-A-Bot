# Podcast Q&A Bot

## Project Overview

This project is an AI-powered Podcast Question Answering system that allows users to ask questions about any YouTube podcast.

Instead of manually listening to long podcast episodes, users can simply provide a YouTube podcast URL, process the podcast, and ask questions in natural language. The system retrieves the most relevant parts of the transcript and generates answers using a Large Language Model (Google Gemini).

The project follows the Retrieval-Augmented Generation (RAG) approach, where answers are generated from the podcast transcript rather than relying solely on the language model's knowledge.

---

## Problem Statement

Podcasts often contain valuable information, but finding specific information inside a 1–3 hour episode is time-consuming.

The goal of this project is to make podcast content searchable and interactive by allowing users to ask questions directly about the episode.

---

## Features

* Download audio from YouTube podcasts
* Automatic speech-to-text transcription using Whisper
* Semantic search using vector embeddings
* FAISS vector database for fast retrieval
* AI-generated answers using Google Gemini
* Timestamp navigation to relevant podcast moments
* Supporting transcript evidence for answer verification
* Confidence score display

---

## Technologies Used

### Frontend

* Streamlit

### Audio Processing

* yt-dlp
* FFmpeg

### Speech Recognition

* OpenAI Whisper

### Embedding Model

* all-MiniLM-L6-v2 (Sentence Transformers)

### Vector Database

* FAISS

### LLM

* Google Gemini 2.5 Flash

### Backend

* Python

---

## Project Workflow

### Step 1: Podcast Processing

The user enters a YouTube podcast URL.

The application downloads the audio from YouTube using yt-dlp.

---

### Step 2: Transcription

The downloaded audio is converted into text using Whisper.

The transcript is divided into smaller chunks along with their timestamps.

---

### Step 3: Embedding Generation

Each transcript chunk is converted into a vector embedding using the Sentence Transformer model.

These embeddings capture the semantic meaning of the text.

---

### Step 4: Vector Storage

All embeddings are stored in a FAISS index.

This allows efficient similarity search when users ask questions.

---

### Step 5: Question Answering

When a user asks a question:

1. The question is converted into an embedding.
2. FAISS retrieves the most relevant transcript chunks.
3. Retrieved chunks are passed to Gemini.
4. Gemini generates an answer using only the retrieved transcript content.

---

### Step 6: Answer Verification

The application displays:

* Generated answer
* Confidence score
* Timestamp
* Supporting transcript chunks

This helps users verify where the answer came from.

---

## Folder Structure

```text
youtube-podcast-qa/

├── app.py
├── pipeline.py
├── downloader.py
├── transcribe.py
├── embeddings.py
├── vector_store.py
├── retrieval.py
├── qa.py
├── data/
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd youtube-podcast-qa
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Project

```bash
streamlit run app.py
```

Open the local Streamlit URL in your browser.

---

## Challenges Faced

During development, the main challenges were:

* Improving retrieval quality from podcast transcripts
* Handling long podcast episodes efficiently
* Reducing irrelevant transcript chunks
* Ensuring Gemini answers were based only on retrieved content
* Managing transcription and indexing time for large podcasts

---

## Future Improvements

Some possible improvements include:

* Multi-podcast search
* Hybrid retrieval (keyword + semantic search)
* Chat history and conversation memory
* Podcast summarization
* Speaker identification
* Better evaluation metrics

---

## Learning Outcomes

Through this project, I gained practical experience with:

* Retrieval-Augmented Generation (RAG)
* Vector databases (FAISS)
* Embedding models
* Whisper transcription
* Prompt engineering
* Google Gemini API
* Streamlit application development

---

## Author

Developed as part of a Generative AI internship project focused on building real-world RAG applications.
