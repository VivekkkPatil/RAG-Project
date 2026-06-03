import streamlit as st
import requests

API = "http://127.0.0.1:8000"

def show_voice_input():
    st.subheader("🎙️ Voice Input")
    if st.button("🎤 Speak"):
        with st.spinner("Listening..."):
            res = requests.post(f"{API}/chatbot/voice-input")
            text = res.json().get("transcribed", "")
        st.success(f"You said: **{text}**")
        return text
    return None