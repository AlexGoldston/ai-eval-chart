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
