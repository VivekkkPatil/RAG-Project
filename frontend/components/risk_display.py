import streamlit as st

def show_risk(score: int):
    color = "green" if score <= 3 else "orange" if score <= 6 else "red"
    st.markdown(f"**Risk Score:** :{color}[{score}/10]")