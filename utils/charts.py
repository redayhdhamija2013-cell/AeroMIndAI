import plotly.graph_objects as go

def performance_chart():

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Lift", "Drag", "Efficiency"],
        y=[1.18, 0.028, 42],
        text=["1.18", "0.028", "42"],
        textposition="outside"
    ))

    fig.update_layout(
        title="Aircraft Performance",
        template="plotly_dark",
        height=450
    )

    return fig