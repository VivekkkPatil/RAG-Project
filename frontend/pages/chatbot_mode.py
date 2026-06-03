import streamlit as st
from frontend.components.chat_window import show_chat
import requests

API = "http://127.0.0.1:8000"

def show():
    st.title("💬 General Chatbot")
    st.caption("Chat directly with the LLM — no documents needed.")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🎤 Speak"):
            with st.spinner("Listening..."):
                try:
                    res = requests.post(f"{API}/chatbot/voice-input", timeout=15)
                    text = res.json().get("transcribed", "")
                    st.success(f"You said: **{text}**")
                    st.session_state["voice_input"] = text
                except Exception as e:
                    st.error(f"Voice error: {str(e)}")

    show_chat(endpoint="/chatbot/chat", payload_key="message")