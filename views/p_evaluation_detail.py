import streamlit as st
import pandas as pd
from utils.plot_utils import create_half_radar_chart

def render():
    st.markdown('<h3 style="color:#1C19B5; font-weight:600;">Individual Evaluation View</h3>', unsafe_allow_html=True)

    st.divider()
    if 'usecases' not in st.session_state or st.session_state.usecases.empty:
        st.warning("No use cases found - please add them first on the evaluator page")
        st.stop()

    df = st.session_state.usecases.reset_index(drop=True)
    idx = st.session_state.get('selected_eval_index', 0)
    idx = min(max(0, idx), len(df) - 1)

    selected_name = st.selectbox("Select Use Case", df["Use Case"], index=int(idx))
    idx = df[df["Use Case"] == selected_name].index[0]
    st.session_state['selected_eval_index'] = int(idx)

    selected_row = df.iloc[idx]
    st.divider()

    # Layout with 1/5 and 4/5 ratio
    chart_col1, chart_col2 = st.columns([1, 4])

    with chart_col1:
        st.markdown("### Metrics")
        for metric in ['Cost', 'Speed', 'Culture', 'Quality', 'Long-term Value']:
            val = int(selected_row[metric])
            st.markdown(f"**{metric}** ({val})")
            st.progress(val)

    with chart_col2:
        st.markdown("### Evaluation Overview - Radar Plot")
        metrics = {
            "Cost": selected_row["Cost"],
            "Speed": selected_row["Speed"],
            "Culture": selected_row["Culture"],
            "Quality": selected_row["Quality"],
            "Long-term Value": selected_row["Long-term Value"]
        }
        radar_fig = create_half_radar_chart(metrics)
        st.plotly_chart(radar_fig, use_container_width=True)