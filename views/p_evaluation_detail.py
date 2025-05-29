import streamlit as st
import pandas as pd
from utils.plot_utils import create_radar_chart, create_gauge


def render():
    st.title(
        "Detailed Evaluation View"
    )

    if 'usecases' not in st.session_state or st.session_state.usecases.empty:
        st.warning("No use cases found - please add them first on the evaluator page")
        st.stop()

    df = st.session_state.usecases.reset_index(drop=True)
    idx = st.session_state.get('selected_eval_index', 0)

    col1,col2,col3 = st.columns([1,4,1])
    with col1:
        if st.button("<<"):
            idx = max(0,idx-1)
    with col3:
        if st.button(">>"):
            idx = min(len(df)-1, idx+1)
    with col2:
        selected_name = st.selectbox("Select Use Case", df["Use Case"], index=idx)
        idx = df[df["Use Case"] == selected_name].index[0]
        st.session_state['selected_eval_index'] = idx

    selected_row = df.iloc[idx]

    # layout
    left,right = st.columns([1,2])

    with left:
        for metric in ['Cost', 'Speed', 'Culture', 'Quality', 'Long-term Value']:
            st.plotly_chart(create_gauge(metric, selected_row[metric]), use_container_width=True)

    with right:
        st.subheader("Evaluation Overview - Radar Plot")
        radar_fig = create_radar_chart(selected_row)
        st.plotly_chart(radar_fig, use_container_width=True)
