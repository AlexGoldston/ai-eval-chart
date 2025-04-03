import streamlit as st
import sys
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title('AI Use Case Weighted Radar Chart')

DEMO_MODE = "-demo" in sys.argv
categories = ["Cost", "Speed", "Culture", "Quality", "Complexity", "Time"]

#init session state data
if 'data' not in st.session_state:
    if DEMO_MODE:
        preloaded_data = [
            ["Proposal and RFP Research Agent", 5, 5, 4, 5, 3, 3],
            ["Code/Regulation Assistant", 4, 5, 4, 5, 2, 2],
            ["HR Process & Policy Assistant", 4, 4, 5, 4, 2, 3],
            ["AI Construction Management Assistant", 5, 4, 4, 5, 3, 4],
            ["Semantic-Index Search", 4, 4, 5, 5, 2, 2],
            ["Graph Powered Visual Search", 4, 3, 4, 4, 4, 3],
            ["Workplan Generator", 4, 4, 4, 4, 3, 3],
            ["Market Trends Agent", 4, 3, 4, 5, 3, 4],
            ["Bid/RFP Assistant", 4, 3, 4, 4, 3, 3],
            ["Private Image Generation Platform", 3, 3, 3, 4, 4, 3],
            ["Drawing Analysis Agent", 3, 2, 3, 4, 4, 4],
            ["BIM QA/QC Agent", 3, 2, 3, 5, 5, 4],
            ["Image Analysis Pipeline", 3, 3, 3, 4, 5, 4],
            ["Generative Space Layout Assistant", 3, 2, 3, 5, 5, 5],
            ["BIM Material Optimization Insights", 3, 3, 4, 5, 4, 4],
            ["BIM Room Typology Classifier", 3, 3, 3, 4, 4, 3],
            ["Graph-Based BIM Relationship Analysis", 2, 3, 3, 4, 5, 5],
            ["BIM Spatial Efficiency Benchmarking", 2, 3, 3, 4, 4, 3],
            ["BIM Cross-Model Clustering", 2, 2, 3, 4, 5, 5],
            ["BIM Feature Extractor & Comparator", 2, 2, 3, 4, 5, 5],
            ["BIM Space Program Analyzer", 2, 2, 2, 4, 5, 5],
            ["Masterplanning System", 1, 2, 2, 5, 5, 5],
            ["BIM Copilot Chatbot", 2, 2, 2, 4, 5, 5],
            ["Project Benchmarking", 2, 3, 3, 4, 4, 4]
        ]
        st.session_state.data = pd.DataFrame(preloaded_data, columns=["Use Case"] + categories)
    else:
        st.session_state.data = pd.DataFrame(columns=["Use Case"] + categories)

# Sidebar - Add & Remove Use Case
with st.sidebar:
    st.header("➕ Add New Use Case")
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

    st.header("❌ Remove Use Case")
    remove_case = st.selectbox("Select Use Case to Remove", [""] + st.session_state.data["Use Case"].tolist())
    if st.button("Remove Use Case") and remove_case:
        st.session_state.data = st.session_state.data[st.session_state.data["Use Case"] != remove_case].reset_index(drop=True)

# Toggle for dataframe scrollability
expand_df = st.checkbox("🖥️ Expand DataFrame to full view", value=False)

st.subheader("📋 Evaluated Use Cases")

if expand_df:
    st.data_editor(
        st.session_state.data,
        use_container_width=True,
        height=(len(st.session_state.data) + 1) * 35  # Adjust row height (~35px per row)
    )
else:
    st.dataframe(
        st.session_state.data,
        use_container_width=True,
        height=300
    )


# Combined radar plot
fig_combined = go.Figure()
for idx, row in st.session_state.data.iterrows():
    values = row[categories].tolist() + [row[categories].tolist()[0]]
    fig_combined.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=row["Use Case"]
    ))

fig_combined.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, st.session_state.data[categories].max().max() + 1])),
    height=700,
    showlegend=True
)

st.subheader("📊 Combined Radar Plot")
st.plotly_chart(fig_combined, use_container_width=True)

# Individual radar charts grid
st.subheader("🔎 Individual Use Case Radar Plots")
num_cols = 3
cols = st.columns(num_cols)

for idx, row in st.session_state.data.iterrows():
    col = cols[idx % num_cols]
    with col:
        fig_individual = go.Figure(go.Scatterpolar(
            r=row[categories].tolist() + [row[categories].tolist()[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=row["Use Case"]
        ))

        fig_individual.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, st.session_state.data[categories].max().max() + 1])),
            title=row["Use Case"],
            margin=dict(l=30, r=30, b=30, t=50),
            height=400
        )

        st.plotly_chart(fig_individual, use_container_width=True)
