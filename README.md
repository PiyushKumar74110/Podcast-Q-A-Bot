# YouTube Podcast AI Q&A System

## Overview

YouTube Podcast AI Q&A System is a Retrieval-Augmented Generation (RAG) application that allows users to interact with YouTube videos through natural language questions. The application processes video transcripts, builds semantic search indexes, retrieves relevant content, and generates context-aware answers using Google's Gemini model.

The system combines speech recognition, semantic search, vector databases, and large language models to provide accurate answers along with relevant timestamps and transcript evidence.

---

## Key Features

- Process YouTube videos using a URL
- Download and extract audio automatically
- Generate transcripts using Faster Whisper
- Cache downloaded audio and transcripts
- Create semantic embeddings using Sentence Transformers
- Build FAISS vector indexes for efficient retrieval
- Retrieve the most relevant transcript segments
- Generate grounded answers using Google Gemini
- Display timestamps linked to video content
- Show supporting transcript chunks as evidence
- Interactive Streamlit chat interface

---

## System Workflow

```text
YouTube URL
      │
      ▼
Video ID Extraction
      │
      ▼
Transcript Available?
      │
 ┌────┴────┐
 │         │
Yes       No
 │         │
 ▼         ▼
Load     Download Audio
Transcript     │
               ▼
       Convert to WAV
               │
               ▼
       Faster Whisper
       Transcription
               │
               ▼
       Transcript Segments
               │
               ▼
     Generate Embeddings
               │
               ▼
        Build FAISS Index
               │
               ▼
          User Query
               │
               ▼
      Semantic Retrieval
               │
               ▼
      Relevant Chunks
               │
               ▼
        Gemini LLM
               │
               ▼
    Answer + Timestamp
```

---

## Project Structure

```text
project/
│
├── cache/
│   ├── transcripts
│   └── FAISS cache files
│
├── chunks/
│   └── Temporary audio chunks
│
├── data/
│   ├── transcript files
│   ├── vector indexes
│   └── metadata files
│
├── downloads/
│   └── Downloaded audio files
│
├── utils/
│   ├── prompts.py
│   ├── qa_pipeline.py
│   └── youtube_utils.py
│
├── audio_processor.py
├── downloader.py
├── embeddings.py
├── final_app.py
├── pipeline.py
├── qa.py
├── retrieval.py
├── transcribe.py
├── vector_store.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## Components

### audio_processor.py

Responsible for:

- Downloading YouTube audio using yt-dlp
- Extracting best quality audio
- Converting audio into WAV format using FFmpeg

---

### downloader.py

Responsible for:

- Managing audio downloads
- Generating unique IDs for videos
- Caching previously downloaded audio files

---

### transcribe.py

Responsible for:

- Splitting long audio files into chunks
- Running Faster Whisper transcription
- Generating timestamped transcript segments
- Saving transcript cache

---

### embeddings.py

Responsible for:

- Loading Sentence Transformer model
- Generating semantic embeddings
- Normalizing embeddings for similarity search

Model used:

```text
all-MiniLM-L6-v2
```

---

### vector_store.py

Responsible for:

- Creating FAISS vector indexes
- Storing transcript metadata
- Saving and loading vector indexes

---

### retrieval.py

Responsible for:

- Loading FAISS indexes
- Converting queries into embeddings
- Performing semantic similarity search
- Returning top relevant transcript chunks

---

### qa.py

Responsible for:

- Finding the most relevant timestamp
- Returning timestamp information based on retrieval results

---

### utils/youtube_utils.py

Responsible for:

- Extracting YouTube video IDs
- Fetching transcripts through YouTube Transcript API
- Caching transcript data

---

### utils/prompts.py

Contains the prompt template used by Gemini.

The prompt ensures:

- Answers are grounded in retrieved context
- Hallucinations are minimized
- Unknown answers return a fallback response

---

### utils/qa_pipeline.py

Responsible for:

- Building LangChain retrieval pipeline
- Creating FAISS retriever
- Connecting Gemini with retrieved context
- Generating final answers

---

### final_app.py

Main Streamlit application.

Provides:

- Video processing interface
- Chat interface
- Timestamp display
- Evidence display
- Session state management

---

## Technologies Used

### Backend

- Python

### AI & Machine Learning

- Google Gemini 2.5 Flash
- Sentence Transformers
- Faster Whisper
- LangChain

### Vector Database

- FAISS

### Frontend

- Streamlit

### Audio Processing

- FFmpeg
- yt-dlp

### Data Storage

- JSON
- Pickle

---

## Installation

### Clone Repository

```bash
git clone https://github.com/PiyushKumar74110/Podcast-Q-A-Bot.git

cd Podcast-Q-A-Bot
```

---

### Create Virtual Environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

---

### Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install FFmpeg

### Verify Installation

```bash
ffmpeg -version
```

### Windows

Download from:

https://ffmpeg.org/download.html

Add FFmpeg to PATH.

### Ubuntu

```bash
sudo apt update

sudo apt install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

---

## Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key
```

---

## Running the Application

```bash
streamlit run final_app.py
```

Open:

```text
http://localhost:8501
```

---

## Example Usage

### Step 1

Paste a YouTube URL.

Example:

```text
https://www.youtube.com/watch?v=example
```

### Step 2

Click:

```text
Process Video
```

### Step 3

Wait for:

- Audio download
- Transcript generation
- Vector index creation

### Step 4

Ask questions such as:

```text
What is the main topic of this video?

What does the speaker say about artificial intelligence?

What are the key takeaways?

When is machine learning discussed?
```

### Step 5

Receive:

- AI-generated answer
- Relevant timestamp
- Direct YouTube link
- Supporting transcript evidence

---

## Caching Strategy

The application caches:

### Audio Files

Location:

```text
downloads/
```

Purpose:

- Prevent repeated downloads

---

### Transcripts

Location:

```text
data/
cache/
```

Purpose:

- Prevent repeated transcription

---

### Vector Stores

Location:

```text
data/
cache/
```

Purpose:

- Prevent repeated embedding generation

---

## Performance Optimizations

- Audio chunking for long videos
- Transcript caching
- FAISS indexing
- Embedding normalization
- Cached vector stores
- Efficient semantic retrieval

---

## Current Limitations

- English transcript focus
- CPU-based transcription
- Single-video analysis per session
- Requires internet access for YouTube downloads

---

## Future Improvements

- Multi-video knowledge base
- Speaker diarization
- Multi-language support
- Hybrid retrieval (BM25 + FAISS)
- Reranking models
- Conversation memory
- Cloud deployment
- User authentication
- Real-time transcription

---

## License



---

## Acknowledgements

This project utilizes the following open-source technologies:

- Google Gemini
- LangChain
- FAISS
- Faster Whisper
- Sentence Transformers
- yt-dlp
- Streamlit
- YouTube Transcript API

---