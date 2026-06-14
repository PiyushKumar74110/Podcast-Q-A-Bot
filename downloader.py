# FOR Downloading audio file and Save into downloads directory

import os
import hashlib
from audio_processor import download_youtube_audio

DOWNLOAD_DIR = "downloads"


def get_id(url):
    return hashlib.md5(url.encode()).hexdigest()


def process_youtube(url):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    vid = get_id(url)
    audio_path = os.path.join(DOWNLOAD_DIR, f"audio_{vid}.wav")

    # Check if audio file exists with input url or not
    if os.path.exists(audio_path):
        print("Using cached audio")
        return audio_path, vid

    
    # DOWNLOAD
    downloaded = download_youtube_audio(url)

    os.rename(downloaded, audio_path)

    print("Downloaded:", audio_path)

    return audio_path, vid