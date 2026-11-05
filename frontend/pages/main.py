
import streamlit as st
import requests

API = "http://127.0.0.1:8000"


def show():

    # SIDEBAR
    with st.sidebar:

        st.title("🧠 DocuSimple")
        st.caption("Your AI Document Assistant")
        st.divider()

        st.subheader("📤 Upload Document")

        file = st.file_uploader(
            "Upload PDF or DOCX",
            type=["pdf", "docx", "png", "jpg"]
        )

        if file:
            if st.session_state.get("last_uploaded") != file.name:

                with st.spinner("Ingesting document..."):

                    try:
                        res = requests.post(
                            f"{API}/document/upload",
                            files={
                                "file": (
                                    file.name,
                                    file,
                                    file.type
                                )
                            },
                            timeout=120
                        )

                        if res.status_code == 200:

                            data = res.json()

                            st.session_state["last_uploaded"] = file.name
                            st.session_state["doc_mode"] = True
                            st.session_state["messages"] = []

                            st.success(
                                f"✅ {data['filename']} → "
                                f"{data['chunks_ingested']} chunks"
                            )

                        else:
                            st.error(f"Upload error: {res.text}")

                    except Exception as e:
                        st.error(f"Upload failed: {str(e)}")

        st.divider()

        # DOCUMENT OPTIONS
        if st.session_state.get("doc_mode"):

            st.subheader("⚙️ Options")

            mode = st.selectbox(
                "Explanation Mode",
                [
                    "default",
                    "simple",
                    "key_points",
                    "worry_about",
                    "action_items",
                    "eli5"
                ],
                format_func=lambda x: {
                    "default": "💬 Default",
                    "simple": "🗣️ Explain Simply",
                    "key_points": "📌 Key Points Only",
                    "worry_about": "⚠️ What Should I Worry About",
                    "action_items": "✅ What Do I Need To Do",
                    "eli5": "👶 Explain Like I'm 5"
                }[x]
            )

            st.session_state["mode"] = mode

            st.divider()

            # ANALYZE DOCUMENT
            if st.button("🔍 Analyze Document"):

                with st.spinner("Analyzing document..."):

                    try:
                        res = requests.post(
                            f"{API}/rag/query",
                            json={
                                "question": (
                                    "Summarize this document "
                                    "and list key points and risks."
                                ),
                                "history": [],
                                "mode": "default"
                            },
                            timeout=120
                        )

                        res.raise_for_status()

                        st.session_state["analysis"] = (
                            res.json().get("answer", "")
                        )

                    except Exception as e:
                        st.error(str(e))

            # CLEAR DOCUMENT
            if st.button("🗑️ Clear Document"):

                try:
                    requests.post(
                        f"{API}/document/clear",
                        timeout=10
                    )
                except Exception as e:
                    st.error(str(e))

                st.session_state["doc_mode"] = False
                st.session_state["last_uploaded"] = None
                st.session_state["messages"] = []
                st.session_state["analysis"] = ""

                st.rerun()

        st.divider()

        # VOICE INPUT
        if st.button("🎤 Speak"):

            with st.spinner("Listening... speak now!"):

                try:
                    res = requests.post(
                        f"{API}/chatbot/voice-input",
                        timeout=20
                    )

                    text = res.json().get("transcribed", "")

                    if text and text not in [
                        "Could notunderstand audio",
                        "Timeout - no speech detected"
                    ]:
                        st.session_state["pending_input"] = text
                        st.success(f"Got: {text}")

                    else:
                        st.warning("Could not understand. Try again.")

                except Exception as e:
                    st.error(str(e))

    # MAIN AREA
    if st.session_state.get("doc_mode"):

        st.title(
            f"📄 {st.session_state.get('last_uploaded', 'Document')}"
        )

    else:
        st.title("💬 DocuSimple Assistant")
        st.caption("Upload a document or just start chatting!")

    # DOCUMENT ANALYSIS
    if st.session_state.get("analysis"):

        with st.expander("📊 Document Analysis", expanded=True):
            st.write(st.session_state["analysis"])

    # AUTHENTICITY RESULTS
    authenticity = st.session_state.get("authenticity")

    if authenticity:

        with st.expander("🔍 Authenticity Results", expanded=True):

            if isinstance(authenticity, dict):

                if "score" in authenticity:
                    st.write(f"Score: {authenticity['score']}/10")

                if "verdict" in authenticity:
                    st.write(f"Verdict: {authenticity['verdict']}")

                if "issues" in authenticity:
                    st.write(authenticity["issues"])

            else:
                st.write(authenticity)

    # INITIALIZE CHAT HISTORY
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # DISPLAY PREVIOUS MESSAGES ONLY ONCE
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # HANDLE VOICE INPUT
    if st.session_state.get("pending_input"):

        voice_input = st.session_state.pop("pending_input")
        _send(voice_input)

    # NORMAL CHAT INPUT
    user_input = st.chat_input(
        "Ask anything or about your document..."
    )

    if user_input:
        _send(user_input)


def _send(user_input: str):

    # PREPARE CONVERSATION HISTORY
    history = []

    msgs = st.session_state.messages

    i = 0

    while i < len(msgs) - 1:

        if (
            msgs[i]["role"] == "user"
            and msgs[i + 1]["role"] == "assistant"
        ):

            history.append({
                "question": msgs[i]["content"],
                "answer": msgs[i + 1]["content"]
            })

            i += 2

        else:
            i += 1

    # SAVE AND DISPLAY CURRENT QUESTION ONCE
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # SELECT BACKEND ENDPOINT
    if st.session_state.get("doc_mode"):

        endpoint = f"{API}/rag/query"

        payload = {
            "question": user_input,
            "history": history,
            "mode": st.session_state.get("mode", "default")
        }

    else:

        endpoint = f"{API}/chatbot/chat/stream"

        payload = {
            "message": user_input,
            "history": history
        }

    # GENERATE ANSWER
    full_answer = ""

    with st.chat_message("assistant"):

        placeholder = st.empty()

        try:

            if st.session_state.get("doc_mode"):

                res = requests.post(
                    endpoint,
                    json=payload,
                    timeout=120
                )

                res.raise_for_status()

                data = res.json()

                full_answer = (
                    data.get("answer")
                    or data.get("response")
                    or "No response received."
                )

                placeholder.write(full_answer)

            else:

                with requests.post(
                    endpoint,
                    json=payload,
                    stream=True,
                    timeout=120
                ) as res:

                    res.raise_for_status()

                    for chunk in res.iter_content(
                        chunk_size=None,
                        decode_unicode=True
                    ):

                        if chunk:

                            full_answer += chunk

                            placeholder.write(
                                full_answer + "▌"
                            )

                    placeholder.write(full_answer)

        except Exception as e:

            full_answer = f"Error: {str(e)}"
            placeholder.write(full_answer)

    # SAVE ANSWER ONCE
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_answer
    })
