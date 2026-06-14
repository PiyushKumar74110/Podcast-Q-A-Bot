import streamlit as st
from utils.youtube_utils import extract_video_id, fetch_transcript
from utils.qa_pipeline import get_answer
from pipeline import pipeline
from retrieval import search


# PAGE CONFIG
st.set_page_config(
    page_title="Podcast Q&A Bot",
    page_icon="🎥",
    layout="wide"
)

st.title("Podcast Q&A Bot")


# SESSION STATE
if "chat" not in st.session_state:
    st.session_state.chat = []

if "video_ready" not in st.session_state:
    st.session_state.video_ready = False

if "video_data" not in st.session_state:
    st.session_state.video_data = None

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None


# HELPERS
def format_time(seconds):
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def youtube_link(video_id, start):
    return f"https://www.youtube.com/watch?v={video_id}&t={int(start)}s"


def get_best_result(results):
    return results[0] if results else None


# STRONG NOT FOUND DETECTOR
def is_not_in_video(answer: str):
    signals = [
        "i don't know",
        "i do not know",
        "not in this video",
        "not mentioned",
        "not discussed",
        "no information",
        "cannot find",
        "based on this video i don't know"
    ]
    return any(s in answer.lower() for s in signals)


# SIDEBAR - VIDEO SETUP
with st.sidebar:
    st.header("Video Setup")

    youtube_url = st.text_input("Enter YouTube URL")

    if st.button("Process Video"):
        if youtube_url:
            video_id = extract_video_id(youtube_url)

            if video_id:
                with st.spinner("Processing video..."):
                    transcript = fetch_transcript(video_id)
                    data = pipeline(youtube_url)

                st.session_state.video_ready = True
                st.session_state.video_data = data
                st.session_state.transcript = transcript
                st.session_state.video_id = video_id

                st.success("Video Ready")
            else:
                st.error("Invalid URL")

    st.divider()

    if st.session_state.video_ready:
        st.success("Video Loaded")
        st.code(st.session_state.video_id)
    else:
        st.warning("No Video Loaded")


# CHAT UI
st.subheader("Chat")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # EXPANDER (ONLY TOP 3–4 CHUNKS)
        if msg["role"] == "assistant" and "evidence" in msg:

            with st.expander("Relevant Transcript Chunks"):

                top_chunks = msg["evidence"][:4]

                for i, chunk in enumerate(top_chunks):

                    st.markdown(f"**Chunk {i + 1}**")

                    start = format_time(chunk.get("start", 0))
                    end = format_time(chunk.get("end", chunk.get("start", 0)))

                    st.write(f"⏱ {start} → {end}")

                    st.write(chunk.get("text", ""))

                    st.divider()


# INPUT
question = st.chat_input("Ask something about the video...")


# MAIN PROCESSING
if question:

    if not st.session_state.video_ready:
        st.warning("Please process a video first")
        st.stop()

    video_data = st.session_state.video_data
    transcript = st.session_state.transcript
    video_id = st.session_state.video_id

    # store user msg
    st.session_state.chat.append({"role": "user", "content": question})

    # FAISS retrieval
    results = search(
        question,
        video_data["index_path"],
        video_data["meta_path"]
    ) or []

    best = get_best_result(results)

    # GEMINI ANSWER
    with st.spinner("Thinking..."):
        answer = get_answer(transcript, question, video_id)

    # NOT FOUND LOGIC
    not_found = is_not_in_video(answer)

    if not_found or best is None:
        response = f"{answer}\n\n⏱ Timestamp: N/A"
    else:
        time_str = format_time(best["start"])
        link = youtube_link(video_id, best["start"])

        response = f"""{answer}

⏱ Timestamp: {time_str}
▶ {link}
"""

    # STORE ASSISTANT MSG + EVIDENCE
    st.session_state.chat.append({
        "role": "assistant",
        "content": response,
        "evidence": results   # full results stored, UI shows only top 4
    })

    st.rerun()