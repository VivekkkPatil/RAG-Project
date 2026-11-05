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
        # Upload
        st.subheader("📤 Upload Document")
        file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx", "png", "jpg"])
        
        if file:
            if st.session_state.get("last_uploaded") != file.name:
                with st.spinner("Ingesting & Analyzing..."):
                    try:
                        # Upload and ingest
                        res = requests.post(
                            f"{API}/document/upload",
                            files={"file": (file.name, file, file.type)},
                            timeout=120
                        )
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state["last_uploaded"] = file.name
                            st.session_state["doc_text"] = data.get("text", "")
                            st.success(f"✅ Ingested **{data['filename']}** → {data['chunks_ingested']} chunks")
                        else:
                            st.error(f"Upload error: {res.text}")
                    except Exception as e:
                        st.error(f"Upload failed: {str(e)}")

            # Auto analysis panel
            if st.session_state.get("last_uploaded") == file.name:
                st.divider()
                tab1, tab2 = st.tabs(["🔍 Evaluate", "🔐 Authenticity"])

                with tab1:
                    if st.button("Analyze Document"):
                        with st.spinner("Analyzing..."):
                            try:
                                res = requests.post(
                                    f"{API}/rag/query",
                                    json={"question": "summarize this document, list key points, risks and action items", "history": [], "mode": "default"},
                                    timeout=120
                                )
                                data = res.json()
                                st.markdown("**Analysis:**")
                                st.write(data["answer"])
                                
                                # Risk score
                                risk_res = requests.post(
                                    f"{API}/eval/evaluate",
                                    json={"text": data["answer"]},
                                    timeout=60
                                )
                                if risk_res.status_code == 200:
                                    rdata = risk_res.json()
                                    show_risk(rdata["risk_score"])
                                    st.markdown("**Domain:** " + rdata["domain"])
                            except Exception as e:
                                st.error(str(e))

                with tab2:
                    if st.button("Check Authenticity"):
                        with st.spinner("Checking..."):
                            try:
                                # Get document content via RAG
                                res = requests.post(
                                    f"{API}/rag/query",
                                    json={"question": "what are all the key facts, dates, numbers and clauses in this document", "history": [], "mode": "default"},
                                    timeout=120
                                )
                                content = res.json().get("answer", "")
                                
                                auth_res = requests.post(
                                    f"{API}/eval/authenticity",
                                    json={"text": content},
                                    timeout=60
                                )
                                adata = auth_res.json()
                                score = adata["score"]
                                color = "green" if score >= 7 else "orange" if score >= 4 else "red"
                                st.markdown(f"**Authenticity Score:** :{color}[{score}/10]")
                                st.markdown(f"**Verdict:** {adata['verdict']}")
                                with st.expander("⚠️ Issues Found"):
                                    st.write(adata["issues"])
                            except Exception as e:
                                st.error(str(e))

    with col2:
        st.subheader("💬 Ask your Document")
        show_chat(endpoint="/rag/query", payload_key="question", show_modes=True)