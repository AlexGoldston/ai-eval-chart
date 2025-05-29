import streamlit as st
from views.p_methodology import render as methodology_render
from views.p_evaluator import render as evaluator_render
from views.p_evaluation_detail import render as evaluation_detail_render
from views.p_summary import render as summary_render

st.set_page_config(page_title="AI Use Case Evaluator", layout="wide")

# Views mapping
VIEWS = {
    "Methodology": methodology_render,
    "Evaluator": evaluator_render,
    "Evaluation Detail": evaluation_detail_render,
    "Summary": summary_render,
}

# Determine active page from query param
params = st.query_params
current_page = params.get("page", "Evaluator")
st.session_state["current_page"] = current_page

# Navigation bar (using native buttons)
st.divider()
st.columns(1)[0].markdown("### Navigation")

nav_cols = st.columns(len(VIEWS))
for i, (name, view_fn) in enumerate(VIEWS.items()):
    if nav_cols[i].button(name, use_container_width=True):
        st.query_params.page = name
        st.rerun()

# Render selected view
VIEWS[current_page]()