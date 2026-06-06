import streamlit as st

from pipeline import pipeline
from qa import generate_answer



# FORMATTING TIMESTAMP

def format_timestamp(seconds):

    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:02d}"
    )



# PAGE CONFIG

st.set_page_config(
    page_title="Podcast Q&A Bot",
    layout="centered"
)

st.title("🎙️ Podcast Q&A Bot")
st.write(
    "Paste a YouTube podcast URL and ask questions about the podcast."
)



# SESSION STATE

if "ready" not in st.session_state:
    st.session_state.ready = False

if "index_path" not in st.session_state:
    st.session_state.index_path = None

if "meta_path" not in st.session_state:
    st.session_state.meta_path = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "current_url" not in st.session_state:
    st.session_state.current_url = None



# URL INPUT

url = st.text_input(
    "Enter YouTube URL"
)



# PROCESS PODCAST

if st.button("Process Podcast"):

    if not url:
        st.error(
            "Please enter a YouTube URL"
        )
        st.stop()

    try:

        with st.status(
            "Processing podcast...",
            expanded=True
        ) as status:

            data = pipeline(url)

            status.update(
                label="Podcast processed successfully",
                state="complete"
            )

        st.session_state.ready = True

        st.session_state.index_path = (
            data["index_path"]
        )

        st.session_state.meta_path = (
            data["meta_path"]
        )

        st.session_state.video_id = (
            data["video_id"]
        )

        st.session_state.current_url = url

        st.success(
            "🎉 Podcast is ready for Q&A!"
        )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )



# Q & A

if st.session_state.ready:

    st.divider()

    st.subheader(
        "Ask Questions"
    )

    question = st.text_input(
        "Type your question"
    )

    if st.button("Get Answer"):

        if not question:

            st.warning(
                "Please enter a question"
            )

            st.stop()

        try:

            with st.spinner(
                "Searching podcast and generating answer..."
            ):

                response = generate_answer(
                    question,
                    st.session_state.index_path,
                    st.session_state.meta_path
                )

            
            # ANSWER
            
            st.subheader(
                "Answer"
            )

            st.write(
                response["answer"]
            )

            
            # CONFIDENCE SCORE
            
            if response["segments"]:

                confidence = (
                    response["segments"][0]
                    .get("score", 0)
                )

                st.metric(
                    "Confidence Score",
                    f"{confidence:.4f}"
                )

            
            # TIMESTAMP
            
            timestamp = int(
                response["timestamp"]
            )

            formatted_time = (
                format_timestamp(
                    timestamp
                )
            )

            st.metric(
                "Timestamp",
                formatted_time
            )

            
            # YOUTUBE JUMP LINK
            
            jump_link = (
                f"{st.session_state.current_url}"
                f"&t={timestamp}s"
            )

            st.markdown(
                f"[▶ Jump to Moment]({jump_link})"
            )

            
            # VERIFICATION INFO
            
            st.info(
                "Answer generated from retrieved transcript chunks."
            )

            
            # EVIDENCE CHUNKS
            
            with st.expander(
                "View Supporting Transcript Chunks"
            ):

                for i, chunk in enumerate(
                    response["segments"]
                ):

                    st.markdown(
                        f"### Chunk {i + 1}"
                    )

                    st.write(
                        f"Similarity Score: "
                        f"{chunk.get('score', 0):.4f}"
                    )

                    start_time = (
                        format_timestamp(
                            chunk["start"]
                        )
                    )

                    end_time = (
                        format_timestamp(
                            chunk["end"]
                        )
                    )

                    st.write(
                        f"⏱ {start_time} "
                        f"→ {end_time}"
                    )

                    st.write(
                        chunk["text"]
                    )

                    st.divider()

        except Exception as e:

            st.error(
                f"Failed to generate answer: {str(e)}"
            )