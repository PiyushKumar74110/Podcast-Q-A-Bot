# Creating pipeline for smooth workflow

from downloader import process_youtube
from transcribe import transcribe_audio
from vector_store import build_index


def pipeline(url):
    print("Downloading audio...")
    audio_path, vid = process_youtube(url)
    print("Audio ready")

    print("Transcribing audio...")
    segments = transcribe_audio(audio_path, vid)
    print(f"Transcript ready ({len(segments)} segments)")

    print("Building / Loading FAISS index...")
    index_path, meta_path = build_index(segments, vid)
    print("Index successfully created")

    return {
        "audio_path": audio_path,
        "video_id": vid,
        "segments": segments,
        "index_path": index_path,
        "meta_path": meta_path
    }
