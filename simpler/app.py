import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Use Case Evaluator", layout="wide")

st.title("📊 AI Use Case Evaluator")

# Session State to Store Use Cases
if 'usecases' not in st.session_state:
    st.session_state.usecases = pd.DataFrame(columns=[
        'Use Case', 'Cost', 'Speed', 'Culture', 'Quality', 'Long-term Value',
        'Complexity', 'Time', 'Overall Score', 'Quadrant'
    ])

# Layout
input_col, output_col = st.columns([1, 2])

# Input Column
with input_col:
    st.header("⚙️ Use Case Configuration")

    usecase_name = st.text_input("Use Case Name")

    st.subheader("Criteria (1=Poor, 10=Excellent)")
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
            overall_score = round((cost + speed + culture + quality + long_term) / (complexity * time), 2)

            # Quadrant determination
            quadrant = ("HIGH EFFORT, QUICK WINS" if complexity >= 50 and time < 50 else
                        "STRATEGIC INVESTMENTS" if complexity >= 50 and time >= 50 else
                        "QUICK WINS" if complexity < 50 and time < 50 else
                        "LONG TERM LOW EFFORT")

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

    # Remove use cases
    if not st.session_state.usecases.empty:
        st.subheader("🗑️ Remove Use Case")
        remove_case = st.selectbox("Select Use Case to Remove", st.session_state.usecases["Use Case"])
        if st.button("❌ Remove Selected"):
            st.session_state.usecases = st.session_state.usecases[st.session_state.usecases["Use Case"] != remove_case]
            st.warning(f"Removed: {remove_case}")

    # CSV Import
    st.subheader("📥 Import Use Cases from CSV")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        try:
            # Ignore the 'Unnamed: 0' index column if present
            imported_df = pd.read_csv(uploaded_file, usecols=lambda x: x != 'Unnamed: 0')

            required_columns = {'Use Case', 'Cost', 'Speed', 'Culture', 'Quality', 'Long-term Value', 'Complexity', 'Time'}
            if not required_columns.issubset(imported_df.columns):
                st.error(f"CSV must include the following columns: {', '.join(required_columns)}")
            else:
                processed_rows = []
                for _, row in imported_df.iterrows():
                    try:
                        overall_score = round(
                            (row['Cost'] + row['Speed'] + row['Culture'] + row['Quality'] + row['Long-term Value']) /
                            (row['Complexity'] * row['Time']), 2
                        )

                        quadrant = (
                            "HIGH EFFORT, QUICK WINS" if row['Complexity'] >= 50 and row['Time'] < 50 else
                            "STRATEGIC INVESTMENTS" if row['Complexity'] >= 50 and row['Time'] >= 50 else
                            "QUICK WINS" if row['Complexity'] < 50 and row['Time'] < 50 else
                            "LONG TERM LOW EFFORT"
                        )

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

# Output Column
with output_col:
    st.header("📌 Evaluated Use Cases")

    if not st.session_state.usecases.empty:
        st.dataframe(st.session_state.usecases, use_container_width=True)

        # Quadrant plot
        st.subheader("Quadrant Matrix (Complexity vs Time)")

        fig = px.scatter(
            st.session_state.usecases,
            x="Time",
            y="Complexity",
            size="Overall Score",
            color="Quadrant",
            text="Use Case",
            size_max=60,
            labels={"Time": "Implementation Time", "Complexity": "Complexity"},
            template="plotly_white",
            title="Use Case Quadrant Matrix"
        )

        fig.update_traces(textposition='top center', marker=dict(opacity=0.7))
        fig.update_layout(xaxis_range=[0, 110], yaxis_range=[0, 110], height=600)

        # Quadrant dividers
        fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(dash="dash", width=2, color="gray"))
        fig.add_shape(type="line", x0=0, y0=50, x1=100, y1=50, line=dict(dash="dash", width=2, color="gray"))

        # Quadrant labels
        quadrants = {
            'HIGH EFFORT, QUICK WINS': {'x':25,'y':75},
            'STRATEGIC INVESTMENTS': {'x':75,'y':75},
            'QUICK WINS': {'x':25,'y':25},
            'LONG TERM LOW EFFORT': {'x':75,'y':25}
        }
        for q, pos in quadrants.items():
            fig.add_annotation(x=pos['x'], y=pos['y'], text=q, showarrow=False, font=dict(size=16, color='gray'))

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add use cases on the left to visualize evaluation.")
