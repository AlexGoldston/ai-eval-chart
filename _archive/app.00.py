import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title('AI Use Case Weighted Radar Chart')

categories = ["Cost", "Speed", "Culture", "Quality", "Complexity", "Time"]

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Use Case"] + categories)

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
