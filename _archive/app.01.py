import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title('AI Use Case Weighted Radar Chart')

categories = ["Cost", "Speed", "Culture", "Quality", "Complexity", "Time"]

initial_data = [
    ["Proposal and RFP Research, Writing, and Response Agent", 5, 5, 4, 5, 3, 3],
    ["Code/Regulation Assistant", 4, 5, 4, 5, 2, 2],
    ["HR Process & Policy Assistant", 4, 4, 5, 4, 2, 3],
    ["AI Construction Management Assistant (RFIs, Submittals, Minutes)", 5, 4, 4, 5, 3, 4],
    ["Semantic-Index Search", 4, 4, 5, 5, 2, 2],
    ["Graph Powered Visual Search", 4, 3, 4, 4, 4, 3],
    ["Workplan Generator", 4, 4, 4, 4, 3, 3],
    ["Market Trends and Competitive Analysis Agent", 4, 3, 4, 5, 3, 4],
    ["Bid/RFP Assistant", 4, 3, 4, 4, 3, 3],
    ["Private Image Generation Platform", 3, 3, 3, 4, 4, 3],
    ["Drawing Analysis Agent (CAD/BIM QA)", 3, 2, 3, 4, 4, 4],
    ["BIM QA/QC Agent (Review Automation Agent)", 3, 2, 3, 5, 5, 4],
    ["Image Analysis and Feature Detection Pipeline", 3, 3, 3, 4, 5, 4],
    ["Generative Space Layout Assistant", 3, 2, 3, 5, 5, 5],
    ["BIM Material Use Optimization & Sustainability Insights", 3, 3, 4, 5, 4, 4],
    ["BIM Model Room Typology Classifier", 3, 3, 3, 4, 4, 3],
    ["Graph-Based BIM Relationship Analysis", 2, 3, 3, 4, 5, 5],
    ["BIM Spatial Efficiency & Circulation Ratio Benchmarking", 2, 3, 3, 4, 4, 3],
    ["BIM Cross-Model Design Element Clustering & Visualization", 2, 2, 3, 4, 5, 5],
    ["BIM Model Feature Extractor + Project Comparator", 2, 2, 3, 4, 5, 5],
    ["BIM AI-Generated Space Program vs. Actual Model Analyzer", 2, 2, 2, 4, 5, 5],
    ["Masterplanning System (Generative Zoning & Flow Analysis)", 1, 2, 2, 5, 5, 5],
    ["\"BIM Copilot\" Chatbot for Model Queries", 2, 2, 2, 4, 5, 5],
    ["Project Benchmarking (Analytical benchmarks)", 2, 3, 3, 4, 4, 4]
]

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(initial_data, columns=["Use Case"] + categories)

with st.sidebar:
    st.header("Add New Use Case")
    use_case_name = st.text_input("Use Case Name")

    scores = [
        st.slider(f"{cat} Score", 1, 5, 3, key=f"score_{cat}") for cat in categories
    ]

    weights = [
        st.slider(f"{cat} Weight", 0.1, 2.0, 1.0, 0.1, key=f"weight_{cat}") for cat in categories
    ]

    if st.button("Add Use Case"):
        weighted_scores = np.array(scores) * np.array(weights)
        new_row = pd.DataFrame([[use_case_name] + list(weighted_scores)], columns=["Use Case"] + categories)
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

    st.header("Remove Use Case")
    remove_case = st.selectbox("Select Use Case to Remove", [""] + st.session_state.data["Use Case"].tolist())
    if st.button("Remove Use Case") and remove_case:
        st.session_state.data = st.session_state.data[st.session_state.data["Use Case"] != remove_case].reset_index(drop=True)

st.subheader("Entered Use Cases")
st.dataframe(st.session_state.data, use_container_width=True)

fig = go.Figure()

for idx, row in st.session_state.data.iterrows():
    values = row[categories].tolist()
    values += values[:1]  # close the loop
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=row["Use Case"]
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, st.session_state.data[categories].max().max() + 1])),
    showlegend=True,
    height=700
)

st.plotly_chart(fig, use_container_width=True)
