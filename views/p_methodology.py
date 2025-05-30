import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render():
    # Methodology Page
    st.divider()
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<h3 style="color:#1C19B5; font-weight:600;">Evaluation Methodology</h3>', unsafe_allow_html=True)
        st.markdown("""
        This app is designed to allow us to evaluate use cases based on both **strategic impact** and **effort required**.

        **Impact Criteria** (weighted):
        - **Long-term Value** – 50%
        - **Quality / Innovation** – 20%
        - **Cost Savings**, **Speed**, **Cultural Fit** – 10% each

        **Effort Penalty**:
        - Based on average of **Complexity** and **Implementation Time**
        - Higher effort **moderately reduces** score

        """)
    
    with col2:
        st.markdown('<h3 style="color:#1C19B5; font-weight:600;">Calculation</h3>', unsafe_allow_html=True)
        st.markdown("""
        #### Impact Score (0–100):
        ```text
        Impact Score = (0.1 × Cost + 0.1 × Speed + 0.1 × Culture + 0.2 × Quality + 0.5 × Long-term Value)
        ```

        #### Effort Modifier:
        ```text
        Effort = (Complexity + Time) / 2
        Modifier = 1 - (Effort / 200)
        ```

        #### Final Score:
        ```text
        Overall Score = Impact Score × (1 + Modifier)
        ```
        """)

    st.divider()
    col3,col4 = st.columns(2)
    with col3:
        st.markdown('<h3 style="color:#1C19B5; font-weight:600;">Strategic Quadrants</h3>', unsafe_allow_html=True)
        st.markdown("""

    | Quadrant | Description |
    |----------|-------------|
    | **QUICK WINS** | Low complexity, short time |
    | **STRATEGIC INVESTMENTS** | High effort, long-term value |
    | **HIGH EFFORT, QUICK WINS** | Fast, high-value, complex ideas |
    | **LONG TERM LOW EFFORT** | Low complexity but slow to realize |

    Each quadrant represents a strategic lens through which to assess use cases:

    - **Quick Wins** are ideal pilot candidates: low complexity, fast to implement, and often boost momentum for broader adoption.
    - **Strategic Investments** offer high long-term value but require careful planning, stakeholder alignment, and sustained execution.
    - **High Effort, Quick Wins** tend to be innovative but technically challenging; consider them when short-term impact justifies the complexity.
    - **Long Term Low Effort** use cases are slow burners — they may lack immediate impact but can deliver steady value with minimal overhead.

    We use this framework to **sequence implementation**, decide where to experiment, and identify which ideas need further refinement or rescoping.
    """)
    with col4:
        dummy_data = pd.DataFrame({
            "Use Case": [f"Example {i}" for i in range(1, 9)],
            "Time":     [15, 36, 74, 92, 32, 63, 18, 88],     # Shifted from center
            "Complexity": [22, 44, 38, 42, 72, 66, 82, 88],   # Ditto for vertical
        })

        def get_quadrant(time, complexity):
            if time <= 50 and complexity <= 50:
                return "QUICK WINS"
            elif time > 50 and complexity <= 50:
                return "LONG TERM LOW EFFORT"
            elif time <= 50 and complexity > 50:
                return "HIGH EFFORT, QUICK WINS"
            else:
                return "STRATEGIC INVESTMENTS"

        dummy_data["Quadrant"] = dummy_data.apply(lambda row: get_quadrant(row["Time"], row["Complexity"]), axis=1)

        color_map = {
            "QUICK WINS": "#8A8DA4",
            "HIGH EFFORT, QUICK WINS": "#91A598",
            "LONG TERM LOW EFFORT": "#A49393",
            "STRATEGIC INVESTMENTS": "#1C19B5",
        }

        fig = px.scatter(
            dummy_data,
            x="Time",
            y="Complexity",
            color="Quadrant",
            text="Use Case",
            color_discrete_map=color_map,
            template="plotly_white",
            size_max=30,
            labels={"Time": "Implementation Time", "Complexity": "Complexity"},
        )

        fig.update_traces(textposition='top center', marker=dict(size=14, opacity=0.8))

        # Dashed quadrant dividers
        fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(dash="dash", color="gray"))
        fig.add_shape(type="line", x0=0, y0=50, x1=100, y1=50, line=dict(dash="dash", color="gray"))

        # Labels for each quadrant
        annotations = {
            "QUICK WINS": (25, 25),
            "LONG TERM LOW EFFORT": (75, 25),
            "HIGH EFFORT, QUICK WINS": (25, 75),
            "STRATEGIC INVESTMENTS": (75, 75),
        }
        for name, (x, y) in annotations.items():
            fig.add_annotation(
                x=x, y=y, text=name,
                showarrow=False,
                font=dict(size=14, color="gray")
            )

        fig.update_layout(
            height=500,
            xaxis_range=[0, 110],
            yaxis_range=[0, 110],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.05,
                xanchor="center",
                x=0.5
            ),
            legend_title_text=None,
        )

        st.plotly_chart(fig, use_container_width=True)