import streamlit as st
import pandas as pd
import plotly.express as px
from utils.score_utils import determine_quadrant, calculate_overall_score

def render():
    # Evaluator Page
    st.title("📊 AI Use Case Evaluator")

    if 'usecases' not in st.session_state:
        st.session_state.usecases = pd.DataFrame(columns=[
            'Use Case', 'Cost', 'Speed', 'Culture', 'Quality', 'Long-term Value',
            'Complexity', 'Time', 'Overall Score', 'Quadrant'
        ])

    with st.sidebar:
        st.header("⚙️ Use Case Configuration")

        usecase_name = st.text_input("Use Case Name")

        st.subheader("Criteria (1=Poor, 100=Excellent)")
        cost = st.slider("Cost (Low Expense)", 1, 100, 5)
        speed = st.slider("Speed (Rapid Implementation)", 1, 100, 5)
        culture = st.slider("Culture (Easy Adoption)", 1, 100, 5)
        quality = st.slider("Quality (Innovation & Impact)", 1, 100, 5)
        long_term = st.slider("Long-term Value (Strategic Impact)", 1, 100, 5)

        st.subheader("Complexity & Time (Higher = More difficult/longer)")
        complexity = st.slider("Complexity (Technical & Operational)", 1, 100, 5)
        time = st.slider("Time (Implementation Effort)", 1, 100, 5)

        if st.button("➕ Add Use Case"):
            if not usecase_name.strip():
                st.warning("Please enter a valid use case name.")
            else:
                overall_score = calculate_overall_score(cost, speed, culture, quality, long_term, complexity, time)
                quadrant = determine_quadrant(complexity, time)

                new_usecase = pd.DataFrame([{
                    'Use Case': usecase_name,
                    'Cost': cost,
                    'Speed': speed,
                    'Culture': culture,
                    'Quality': quality,
                    'Long-term Value': long_term,
                    'Complexity': complexity,
                    'Time': time,
                    'Overall Score': overall_score,
                    'Quadrant': quadrant
                }])

                st.session_state.usecases = pd.concat([st.session_state.usecases, new_usecase], ignore_index=True)
                st.success(f"Added: {usecase_name}")

        if not st.session_state.usecases.empty:
            st.subheader("🗑️ Remove Use Case")
            remove_case = st.selectbox("Select Use Case to Remove", st.session_state.usecases["Use Case"])
            if st.button("❌ Remove Selected"):
                st.session_state.usecases = st.session_state.usecases[st.session_state.usecases["Use Case"] != remove_case]
                st.warning(f"Removed: {remove_case}")

        st.subheader("📥 Import Use Cases from CSV")
        uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

        if uploaded_file is not None:
            try:
                imported_df = pd.read_csv(uploaded_file, usecols=lambda x: x != 'Unnamed: 0')
                required_columns = {'Use Case', 'Cost', 'Speed', 'Culture', 'Quality', 'Long-term Value', 'Complexity', 'Time'}
                if not required_columns.issubset(imported_df.columns):
                    st.error(f"CSV must include the following columns: {', '.join(required_columns)}")
                else:
                    processed_rows = []
                    for _, row in imported_df.iterrows():
                        try:
                            overall_score = calculate_overall_score(
                                row['Cost'], row['Speed'], row['Culture'], row['Quality'],
                                row['Long-term Value'], row['Complexity'], row['Time']
                            )
                            quadrant = determine_quadrant(row['Complexity'], row['Time'])

                            processed_rows.append({
                                'Use Case': row['Use Case'],
                                'Cost': row['Cost'],
                                'Speed': row['Speed'],
                                'Culture': row['Culture'],
                                'Quality': row['Quality'],
                                'Long-term Value': row['Long-term Value'],
                                'Complexity': row['Complexity'],
                                'Time': row['Time'],
                                'Overall Score': overall_score,
                                'Quadrant': quadrant
                            })
                        except Exception as e:
                            st.warning(f"Skipping row due to error: {e}")

                    if processed_rows:
                        new_df = pd.DataFrame(processed_rows)
                        st.session_state.usecases = pd.concat([st.session_state.usecases, new_df], ignore_index=True)
                        st.success(f"Successfully imported {len(processed_rows)} use case(s).")
            except Exception as e:
                st.error(f"Error processing file: {e}")

    st.subheader("📈 Summary Metrics")
    total_usecases = len(st.session_state.usecases)
    avg_score = round(st.session_state.usecases['Overall Score'].mean(), 2)
    avg_complexity = round(st.session_state.usecases['Complexity'].mean(), 2)
    avg_time = round(st.session_state.usecases['Time'].mean(), 2)
    top_quadrant = st.session_state.usecases['Quadrant'].value_counts().idxmax() if total_usecases > 0 else "N/A"

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Use Cases", total_usecases)
    col2.metric("Avg. Score", avg_score)
    col3.metric("Avg. Complexity", avg_complexity)
    col4.metric("Avg. Time", avg_time)
    col5.metric("Most Common Quadrant", top_quadrant)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filter Use Cases")

    quadrant_filter = st.sidebar.multiselect(
        "Select Quadrants to Include",
        options=st.session_state.usecases['Quadrant'].unique().tolist(),
        default=st.session_state.usecases['Quadrant'].unique().tolist()
    )

    min_score, max_score = st.sidebar.slider(
        "Filter by Overall Score",
        min_value=0.0,
        max_value=float(st.session_state.usecases['Overall Score'].max() if not st.session_state.usecases.empty else 1.0),
        value=(0.0, float(st.session_state.usecases['Overall Score'].max() if not st.session_state.usecases.empty else 1.0))
    )

    filtered_df = st.session_state.usecases[
        st.session_state.usecases['Quadrant'].isin(quadrant_filter) &
        st.session_state.usecases['Overall Score'].between(min_score, max_score)
    ]

    st.header("Evaluated Use Cases")

    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)

        # st.subheader("Strategic Positioning of Use Cases")
        color_map = {
            "QUICK WINS": "green",
            "HIGH EFFORT, QUICK WINS": "blue",
            "LONG TERM LOW EFFORT": "orange",
            "STRATEGIC INVESTMENTS": "red"
        }

        fig = px.scatter(
            filtered_df,
            x="Time",
            y="Complexity",
            size=filtered_df["Overall Score"] ** 2,
            color="Quadrant",
            text="Use Case",
            hover_name="Use Case",
            size_max=50,
            color_discrete_map=color_map,
            labels={"Time": "Implementation Time", "Complexity": "Complexity"},
            template="plotly_white",
            title="Strategic Positioning of Use Cases"
        )

        fig.update_traces(textposition='top center', marker=dict(opacity=0.7))
        fig.update_layout(xaxis_range=[0, 110], yaxis_range=[0, 110], height=600)

        fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(dash="dash", width=2, color="gray"))
        fig.add_shape(type="line", x0=0, y0=50, x1=100, y1=50, line=dict(dash="dash", width=2, color="gray"))

        quadrants = {
            'HIGH EFFORT, QUICK WINS': {'x':25,'y':75},
            'STRATEGIC INVESTMENTS': {'x':75,'y':75},
            'QUICK WINS': {'x':25,'y':25},
            'LONG TERM LOW EFFORT': {'x':75,'y':25}
        }
        for q, pos in quadrants.items():
            fig.add_annotation(x=pos['x'], y=pos['y'], text=q, showarrow=False, font=dict(size=16, color='gray'))

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top Use Cases by Score (Faceted by Quadrant)")
        top_cases = (
            filtered_df
            .sort_values(by="Overall Score", ascending=False)
            .groupby("Quadrant", group_keys=False)
            .head(5)
        )

        facet_fig = px.bar(
            top_cases,
            x="Use Case",
            y="Overall Score",
            color="Quadrant",
            facet_col="Quadrant",
            template="plotly_white",
            title="Top Use Cases by Quadrant",
            height=500,
            category_orders={"Use Case": top_cases.sort_values("Overall Score", ascending=False)["Use Case"].tolist()}
        )
        facet_fig.update_layout(showlegend=False)
        facet_fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[1]))
        st.plotly_chart(facet_fig, use_container_width=True)
    else:
        st.info("No use cases match the selected filters.")