import streamlit as st
import base64
from views.p_methodology import render as methodology_render
from views.p_evaluator import render as evaluator_render
from views.p_evaluation_detail import render as evaluation_detail_render
from views.p_summary import render as summary_render
from utils.logo_svg import svg_logo_black, svg_logo_white

st.set_page_config(page_title="AI Use Case Evaluator", layout="wide")

def is_dark_theme():
    theme_base = st.get_option("theme.base")
    if theme_base == "dark":
        return True
    elif theme_base == "light":
        return False
    elif theme_base == "custom":
        try:
            bg_color = st.get_option("theme.backgroundColor")
            return is_dark_background(bg_color)
        except RuntimeError:
            return False  # fallback if not defined
    return False

def is_dark_background(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance < 0.5

def render_svg_logo(width=150):
    svg = svg_logo_white if is_dark_theme() else svg_logo_black
    b64_svg = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    svg_uri = f"data:image/svg+xml;base64,{b64_svg}"
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(svg_uri, width=width)

render_svg_logo()
st.markdown("""""")

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
nav_cols = st.columns(len(VIEWS))
for i, (name, view_fn) in enumerate(VIEWS.items()):
    if nav_cols[i].button(name, use_container_width=True):
        st.query_params.page = name
        st.rerun()

# Render selected view
VIEWS[current_page]()