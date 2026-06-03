import streamlit as st
import requests

API = "http://127.0.0.1:8000"

def show_uploader():
    st.subheader("📤 Upload Document")
    file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx", "png", "jpg"])
    if file:
        with st.spinner("Ingesting..."):
            try:
                res = requests.post(
                    f"{API}/document/upload",
                    files={"file": (file.name, file, file.type)},
                    timeout=60
                )
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"✅ Ingested **{data['filename']}** → {data['chunks_ingested']} chunks")
                else:
                    st.error(f"Server error: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Upload failed: {str(e)}")