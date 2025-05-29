import streamlit as st
import plotly.express as px
from utils.score_utils import determine_quadrant, calculate_overall_score
from utils.plot_utils import create_radar_chart, create_gauge

def render():
    # Presentation Mode Page
    st.title("Executive Summary View")
    st.markdown("""
    This page presents a simplified view of the most important insights for an executive audience:
    - Focus is on clarity, prioritization, and strategic alignment
    - Technical metrics are abstracted in favor of value categories
    """)

    if 'usecases' in st.session_state and not st.session_state.usecases.empty:
        st.subheader("Strategic Quadrant Overview")
        quadrant_counts = st.session_state.usecases['Quadrant'].value_counts().reset_index()
        quadrant_counts.columns = ['Quadrant', 'Count']
        pie_chart = px.pie(quadrant_counts, names='Quadrant', values='Count', title='Use Case Distribution by Quadrant')
        st.plotly_chart(pie_chart, use_container_width=True)

        st.subheader("Top Strategic Opportunities")
        top_strategic = st.session_state.usecases[st.session_state.usecases['Quadrant'] == 'STRATEGIC INVESTMENTS']
        top_5 = top_strategic.sort_values(by='Overall Score', ascending=False).head(5)
        st.table(top_5[['Use Case', 'Overall Score', 'Complexity', 'Time']])

        fig = px.scatter(
            st.session_state.usecases,
            x="Time",
            y="Complexity",
            size=st.session_state.usecases["Overall Score"] ** 2,
            color="Quadrant",
            hover_name="Use Case",
            color_discrete_map={
                "QUICK WINS": "green",
                "HIGH EFFORT, QUICK WINS": "blue",
                "LONG TERM LOW EFFORT": "orange",
                "STRATEGIC INVESTMENTS": "red"
            },
            template="plotly_white",
            title="Strategic Positioning of Use Cases"
        )
        fig.update_traces(marker=dict(opacity=0.75))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No use cases available to display. Please add or import data in the Evaluator page.")