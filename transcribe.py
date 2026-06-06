import json
import os
import whisper

# Defining whisper model
model = whisper.load_model("base")

# 
def transcribe_audio(audio_file, vid):

    # Make data directory to store files like transcript.json
    os.makedirs("data", exist_ok=True)

    path = f"data/transcript_{vid}.json"

    
    # # Check if transcript.json exists with input url or not
    if os.path.exists(path):
        print("Using cached transcript")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    
    # Calling whisper model to transcribe audio file
    result = model.transcribe(audio_file)

    # Splitting result and storing its data in dictionary for writing json file
    segments = [
        {
            "text": s["text"].strip(),
            "start": s["start"],
            "end": s["end"]
        }
        for s in result["segments"]
    ]

    # Writing json file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=2)

    return segments