import streamlit as st
import requests

API = "http://127.0.0.1:8000"

def show():
    st.title("💬 General Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_input" not in st.session_state:
        st.session_state.pending_input = None

    if st.button("🎤 Speak"):
        with st.spinner("Listening..."):
            try:
                res = requests.post(f"{API}/chatbot/voice-input", timeout=15)
                text = res.json().get("transcribed", "")
                if text and text != "Could not understand audio":
                    st.session_state.pending_input = text
                else:
                    st.warning("Could not understand.")
            except Exception as e:
                st.error(str(e))

    if st.session_state.pending_input:
        user_input = st.session_state.pending_input
        st.session_state.pending_input = None
        _send(user_input)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask something...")
    if user_input:
        _send(user_input)

def _send(user_input: str):
    history = []
    msgs = st.session_state.messages
    i = 0
    while i < len(msgs) - 1:
        if msgs[i]["role"] == "user" and msgs[i+1]["role"] == "assistant":
            history.append({
                "question": msgs[i]["content"],
                "answer": msgs[i+1]["content"]
            })
            i += 2
        else:
            i += 1

    st.session_state.messages.append({"role": "user", "content": user_input})

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    with st.chat_message("assistant"):
        answer_placeholder = st.empty()
        full_answer = ""
        try:
            with requests.post(
                f"{API}/chatbot/chat/stream",
                json={"message": user_input, "history": history},
                stream=True,
                timeout=120
            ) as res:
                for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        full_answer += chunk
                        answer_placeholder.write(full_answer + "▌")
                answer_placeholder.write(full_answer)
        except Exception as e:
            full_answer = f"Error: {str(e)}"
            answer_placeholder.write(full_answer)

    st.session_state.messages.append({"role": "assistant", "content": full_answer})