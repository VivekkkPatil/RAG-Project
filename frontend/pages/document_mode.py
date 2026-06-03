import streamlit as st
from frontend.components.uploader import show_uploader
from frontend.components.chat_window import show_chat
from frontend.components.risk_display import show_risk
import requests

API = "http://127.0.0.1:8000"

def show():
    st.title("📄 Document Mode")
    col1, col2 = st.columns([1, 2])

    with col1:
        show_uploader()
        st.divider()
        st.subheader("🔍 Evaluate Document")
        text = st.text_area("Paste text to evaluate")
        if st.button("Evaluate") and text:
            with st.spinner("Evaluating..."):
                res = requests.post(f"{API}/eval/evaluate", json={"text": text})
                data = res.json()
            st.markdown("**Summary:**")
            st.write(data["summary"])
            show_risk(data["risk_score"])
            st.markdown("**Domain:** " + data["domain"])
            with st.expander("📋 Actions"):
                st.write(data["actions"])
            with st.expander("❓ FAQs"):
                st.write(data["faqs"])

    with col2:
        st.subheader("💬 Ask your Document")
        show_chat(endpoint="/rag/query", payload_key="question", show_modes=True)