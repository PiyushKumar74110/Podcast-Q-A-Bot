import os
import json
import ffmpeg
from faster_whisper import WhisperModel


# MODEL (CPU + memory safe)

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


# AUDIO CHUNKING

def chunk_audio(input_path, chunk_seconds=600):
    """
    Split audio into 10-minute chunks to avoid memory overflow
    """
    os.makedirs("chunks", exist_ok=True)

    output_pattern = "chunks/chunk_%03d.wav"

    (
        ffmpeg
        .input(input_path)
        .output(
            output_pattern,
            f="segment",
            segment_time=chunk_seconds,
            ar=16000,
            ac=1
        )
        .overwrite_output()
        .run(quiet=True)
    )

    chunks = sorted([
        os.path.join("chunks", f)
        for f in os.listdir("chunks")
        if f.endswith(".wav")
    ])

    return chunks



# MAIN TRANSCRIPTION FUNCTION

def transcribe_audio(audio_file, vid):

    os.makedirs("data", exist_ok=True)
    path = f"data/transcript_{vid}.json"

    
    # 1. LOAD CACHE IF EXISTS
    
    if os.path.exists(path):
        print("✔ Using cached transcript.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    print("⚡ No cache found. Running transcription pipeline...")

    
    # 2. CHUNK AUDIO
    
    print("Chunking audio...")
    chunks = chunk_audio(audio_file, chunk_seconds=600)

    all_segments = []
    offset = 0

    print(f"Processing {len(chunks)} chunks...")

    
    # 3. TRANSCRIBE EACH CHUNK
    
    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}/{len(chunks)}")

        segments, _ = model.transcribe(
            chunk,
            beam_size=5
        )

        for seg in segments:
            all_segments.append({
                "text": seg.text.strip(),
                "start": float(seg.start + offset),
                "end": float(seg.end + offset)
            })

        offset += 600  # must match chunk_seconds

    
    # 4. SAVE TRANSCRIPT
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_segments, f, indent=2)

    print("✔ Transcription complete")

    return all_segments