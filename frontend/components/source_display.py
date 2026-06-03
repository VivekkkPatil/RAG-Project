import streamlit as st

def show_sources(sources: list):
    with st.expander("📚 Retrieved Sources"):
        for i, s in enumerate(sources):
            st.markdown(f"**Chunk {i+1}:** {s}")