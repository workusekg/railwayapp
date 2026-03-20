import streamlit as st
import pymupdf, docx, ollama, os
import time

st.set_page_config(page_title="Instant AI Career Portal", layout="wide")


@st.cache_resource(show_spinner="Waiting for Ollama to initialize...")
def wait_for_ollama(retries: int = 5, delay: float = 2.0) -> bool:
    """
    Attempt to reach the Ollama service with exponential backoff.
    Cached by Streamlit so the probe only runs once per app session,
    not on every file upload.

    Returns True when Ollama is ready, False if all retries are exhausted.
    """
    for attempt in range(1, retries + 1):
        try:
            # A lightweight list call is enough to confirm the daemon is up.
            ollama.list()
            return True
        except Exception:
            if attempt < retries:
                wait = delay * (2 ** (attempt - 1))  # 2 s, 4 s, 8 s, 16 s ...
                time.sleep(wait)
    return False


st.title("🚀 Upload Resume & Create Profile Instantly")
st.write("Ahmedabad's Next-Gen Job Matching")

# Probe Ollama once at startup before the user can upload anything.
ollama_ready = wait_for_ollama()
if not ollama_ready:
    st.error(
        "⚠️ Ollama is still starting up. Please wait a moment and refresh the page."
    )
    st.stop()

uploaded_file = st.file_uploader("Drop PDF or Word File", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("AI is reading your resume..."):
        # 1. Extract Text
        text = ""
        if uploaded_file.type == "application/pdf":
            doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
            text = chr(12).join([page.get_text() for page in doc])
        else:
            doc = docx.Document(uploaded_file)
            text = "\n".join([p.text for p in doc.paragraphs])

        # 2. AI Structuring (Llama 3.2)
        try:
            response = ollama.chat(model='llama3.2:1b', messages=[
                {'role': 'user', 'content': f"Extract Name, Email, and 3 Skills as JSON from: {text[:1000]}"}
            ])
        except ConnectionError:
            st.error(
                "⚠️ Could not reach Ollama. It may still be initializing — "
                "please wait a few seconds and re-upload your file."
            )
            st.stop()
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred while contacting Ollama: {e}")
            st.stop()

        # 3. Display Profile Preview
        st.success("Profile Created!")
        st.json(response['message']['content'])

        if st.button("Confirm & Save to Database"):
            st.info("Saving to your Railway Postgres database...")
            # SQL logic goes here
