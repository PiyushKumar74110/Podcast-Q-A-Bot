import yt_dlp
import os
import subprocess
import soundfile as sf
import numpy as np

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)



# Check if ffmpeg exists or not
print(subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout[:150])



# FFmpeg used internally
# Download you tube video
# Convert to wav format
def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    wav_path = filename.replace(".webm", ".wav").replace(".m4a", ".wav")
    return wav_path
