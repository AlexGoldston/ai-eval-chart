import streamlit as st

def render():
    # Methodology Page
    st.title("📘 Evaluation Methodology")
    st.markdown("""
    ### Overview
    This app evaluates AI use cases based on both **strategic impact** and **effort required**.

    **Impact Criteria** (weighted):
    - **Long-term Value** – 50%
    - **Quality / Innovation** – 20%
    - **Cost Savings**, **Speed**, **Cultural Fit** – 10% each

    **Effort Penalty**:
    - Based on average of **Complexity** and **Implementation Time**
    - Higher effort **moderately reduces** score

    ### Calculation

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

    ### Quadrants (for visualization)

    | Quadrant | Description |
    |----------|-------------|
    | **QUICK WINS** | Low complexity, short time |
    | **STRATEGIC INVESTMENTS** | High effort, long-term value |
    | **HIGH EFFORT, QUICK WINS** | Fast, high-value, complex ideas |
    | **LONG TERM LOW EFFORT** | Low complexity but slow to realize |
        """)
