# Creating pipeline for smooth workflow

from downloader import process_youtube
from transcribe import transcribe_audio
from vector_store import build_index
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    query = urlparse(url)

    if query.hostname == "youtu.be":
        return query.path[1:]

    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            return parse_qs(query.query)["v"][0]

    return None


def pipeline(url):
    print("Downloading audio...")
    audio_path, vid = process_youtube(url)
    real_vid = extract_video_id(url)
    print("Audio ready")

    print("Transcribing audio...")
    segments = transcribe_audio(audio_path, vid)
    print(f"Transcript ready ({len(segments)} segments)")

    print("Building / Loading FAISS index...")
    index_path, meta_path = build_index(segments, vid)
    print("Index successfully created")

    return {
        "audio_path": audio_path,
        "video_id": real_vid,
        "segments": segments,
        "index_path": index_path,
        "meta_path": meta_path
    }
