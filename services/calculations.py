import plotly.graph_objects as go
def performance_chart(cl,cd,ld):

    fig=go.Figure()

    fig.add_trace(go.Bar(
        x=["Lift","Drag","L/D"],
        y=[cl,cd,ld],
        text=[cl,cd,ld],
        textposition="outside"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=450,
        title="Performance Analysis"
    )

    return fig


def calculate_lift(speed,cl):

    rho=1.225
    area=1

    v=speed/3.6

    return 0.5*rho*(v**2)*area*cl
