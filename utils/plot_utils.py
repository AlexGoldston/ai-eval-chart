import plotly.graph_objects as go

def create_radar_chart(row):
    categories = ['Cost', 'Speed', 'Culture', 'Quality', 'Long-term Value']
    values = [row[c] for c in categories]
    return go.Figure(data=[
        go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself')
    ])

def create_gauge(title,value):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [0,100]}}
    ))

def create_half_radar_chart(metrics: dict):
    categories = list(metrics.keys())
    values = list(metrics.values())

    # Close the loop
    categories += [categories[0]]
    values += [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Evaluation',
        line_color='royalblue'
    ))

    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                direction='clockwise',
                rotation=270,  # start at top center
                showline=False,
                tickfont=dict(size=12)
            ),
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showline=False,
                ticks=''
            )
        ),
        showlegend=False,
        margin=dict(t=30, b=30, l=30, r=30),
        height=400
    )

    return fig