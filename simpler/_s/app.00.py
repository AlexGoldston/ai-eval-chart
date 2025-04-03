import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Use Case Evaluator", layout="wide")

st.title("📊 AI Use Case Quick Evaluator")

# Initialize use case storage
if 'usecases' not in st.session_state:
    st.session_state.usecases = pd.DataFrame(columns=[
        'Use Case', 'Cost', 'Speed', 'Culture', 'Quality',
        'Complexity', 'Time', 'Weighted Score', 'Quadrant'
    ])

# Split the main layout into two columns
input_col, output_col = st.columns([1, 2])

with input_col:
    st.header("🔧 Configure Use Case")

    usecase_name = st.text_input("Use Case Name")

    st.subheader("Evaluation Scores (1-5)")
    cost = st.slider("Cost (Financial Impact)", 1, 5, 3)
    speed = st.slider("Speed (Time-to-value)", 1, 5, 3)
    culture = st.slider("Culture (Fit & Adoption)", 1, 5, 3)
    quality = st.slider("Quality (Innovation & Impact)", 1, 5, 3)

    st.subheader("Complexity & Time")
    complexity = st.slider("Complexity (Technical & Operational)", 1, 5, 3)
    time = st.slider("Time (Implementation Effort)", 1, 5, 3)

    # Buttons to add use case
    if st.button("➕ Add Use Case"):
        if usecase_name.strip() == "":
            st.warning("Please provide a name for the use case.")
        else:
            weight = complexity * time
            weighted_score = (cost + speed + culture + quality) * weight

            if complexity >= 3 and time < 3:
                quadrant = 'COST (High Complexity, Short Time)'
            elif complexity >= 3 and time >= 3:
                quadrant = 'SPEED (High Complexity, Long Time)'
            elif complexity < 3 and time < 3:
                quadrant = 'CULTURE (Low Complexity, Short Time)'
            else:
                quadrant = 'QUALITY (Low Complexity, Long Time)'

            new_row = pd.DataFrame([{
                'Use Case': usecase_name,
                'Cost': cost,
                'Speed': speed,
                'Culture': culture,
                'Quality': quality,
                'Complexity': complexity,
                'Time': time,
                'Weighted Score': weighted_score,
                'Quadrant': quadrant
            }])

            st.session_state.usecases = pd.concat([st.session_state.usecases, new_row], ignore_index=True)
            st.success(f"Added: {usecase_name}")

    # Selection to remove use cases
    if not st.session_state.usecases.empty:
        st.subheader("🗑️ Remove Use Case")
        remove_case = st.selectbox("Select Use Case to Remove", st.session_state.usecases["Use Case"].tolist())

        if st.button("❌ Remove Selected"):
            st.session_state.usecases = st.session_state.usecases[st.session_state.usecases["Use Case"] != remove_case]
            st.warning(f"Removed: {remove_case}")

with output_col:
    st.header("📌 Evaluated Use Cases")

    # Display DataFrame
    if not st.session_state.usecases.empty:
        st.dataframe(st.session_state.usecases, use_container_width=True)

        # Plot Quadrant Matrix
        st.subheader("Quadrant Matrix")

        fig = px.scatter(
            st.session_state.usecases,
            x="Time",
            y="Complexity",
            text="Use Case",
            color="Quadrant",
            size="Weighted Score",
            size_max=50,
            template="plotly_white",
            labels={
                "Time": "Implementation Time (Effort)",
                "Complexity": "Technical/Operational Complexity"
            },
            title="AI Use Case Quadrant Matrix"
        )

        fig.update_traces(textposition='top center')
        fig.update_layout(
            xaxis=dict(title='Time (Effort Needed)', range=[0, 6], dtick=1),
            yaxis=dict(title='Complexity', range=[0, 6], dtick=1),
            height=600
        )

        # Quadrant lines
        fig.add_shape(type="line", x0=3, y0=0, x1=3, y1=6, line=dict(dash="dash", width=2, color="gray"))
        fig.add_shape(type="line", x0=0, y0=3, x1=6, y1=3, line=dict(dash="dash", width=2, color="gray"))

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No use cases added yet. Start by adding a use case from the left panel.")

