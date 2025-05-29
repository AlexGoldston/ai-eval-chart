import streamlit as st
import pandas as pd
from pages import p_evaluator, p_evaluation_detail, p_methodology, p_summary

st.set_page_config(page_title="AI Use Case Evaluator", layout="wide")


# nav
st.markdown("""
    <style>
    div[data-testid="stSidebar"] {display: none;}
    div[data-testid="stHorizontalBlock"] > div {
        display: flex;
        justify-content: space-around;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

pages = {
    "Methodology": p_methodology.render,
    "Evaluator": p_evaluator.render,
    "Evaluation Detail": p_evaluation_detail.render,
    "Summary": p_summary.render
}

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Evaluator" #set default page

selected = st.radio("Navigation", list(pages.keys()), index=list(pages.keys()).index(st.session_state.current_page), horizontal=True)
st.session_state.current_page = selected

# call page render func
pages[selected]()