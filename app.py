import streamlit as st
import pymupdf, docx, ollama, os

st.set_page_config(page_title="Instant AI Career Portal", layout="wide")

st.title("🚀 Upload Resume & Create Profile Instantly")
st.write("Ahmedabad's Next-Gen Job Matching")

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
        response = ollama.chat(model='llama3.2:1b', messages=[
            {'role': 'user', 'content': f"Extract Name, Email, and 3 Skills as JSON from: {text[:1000]}"}
        ])
        
        # 3. Display Profile Preview
        st.success("Profile Created!")
        st.json(response['message']['content'])
        
        if st.button("Confirm & Save to Database"):
            st.info("Saving to your Railway Postgres database...")
            # SQL logic goes here