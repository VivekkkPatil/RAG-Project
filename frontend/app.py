import streamlit as st

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

st.sidebar.title("🤖 RAG Chatbot")
mode = st.sidebar.radio("Select Mode", ["💬 Chatbot", "📄 Document Mode"])

if mode == "💬 Chatbot":
    from frontend.pages.chatbot_mode import show
    show()
else:
    from frontend.pages.document_mode import show
    show()