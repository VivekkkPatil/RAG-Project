import streamlit as st
import requests

API = "http://127.0.0.1:8000"

voice_text = st.session_state.pop("voice_input", None)
st.write(f"DEBUG voice_text: {voice_text}")  # temporary debug
user_input = st.chat_input("Ask something...")

def show_chat(endpoint: str = "/rag/query", payload_key: str = "question", show_modes: bool = False):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    mode = "default"
    if show_modes:
        mode = st.selectbox("Explanation Mode", [
            "default", "simple", "key_points", "worry_about", "action_items", "eli5"
        ], format_func=lambda x: {
            "default": "💬 Default",
            "simple": "🗣️ Explain Simply",
            "key_points": "📌 Key Points Only",
            "worry_about": "⚠️ What Should I Worry About",
            "action_items": "✅ What Do I Need To Do",
            "eli5": "👶 Explain Like I'm 5"
        }[x])

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    voice_text = st.session_state.pop("voice_input", None)
    user_input = st.chat_input("Ask something...")

    if voice_text and not user_input:
        user_input = voice_text

    if user_input:
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
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    payload = {payload_key: user_input, "history": history, "mode": mode}
                    res = requests.post(f"{API}{endpoint}", json=payload, timeout=60)
                    data = res.json()
                    answer = data.get("answer") or data.get("response") or "No response"
                except Exception as e:
                    answer = f"Error: {str(e)}"
                    data = {}
                st.write(answer)
                if "sources" in data:
                    with st.expander("📚 Sources"):
                        for s in data["sources"]:
                            st.caption(s)

        st.session_state.messages.append({"role": "assistant", "content": answer})