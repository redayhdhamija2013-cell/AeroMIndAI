from services.calculations import calculate_lift, performance_chart
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import time
import math

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AeroMind AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================
def load_css():
    css_file = Path(__file__).parent / "styles" / "style.css"

    with open(css_file, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ==========================================================
# AIRFOIL DATABASE
# ==========================================================

AIRFOILS = {

("Drone","Surveillance"):
{
"name":"NACA 4412",
"cl":1.18,
"cd":0.028,
"ld":42,
"stall":42,
"description":"Excellent lift and stability."
},

("Drone","Delivery"):
{
"name":"S1223",
"cl":1.45,
"cd":0.040,
"ld":36,
"stall":35,
"description":"High lift airfoil."
},

("Passenger Aircraft","Commercial"):
{
"name":"NASA SC(2)-0612",
"cl":0.92,
"cd":0.021,
"ld":44,
"stall":63,
"description":"Efficient supercritical airfoil."
},

("Cargo Aircraft","Delivery"):
{
"name":"Clark Y",
"cl":1.10,
"cd":0.032,
"ld":35,
"stall":50,
"description":"Reliable cargo airfoil."
},

("Glider","Long Endurance"):
{
"name":"MH32",
"cl":0.95,
"cd":0.020,
"ld":48,
"stall":38,
"description":"Excellent glide performance."
},

("Fighter Jet","Racing"):
{
"name":"NACA 64A204",
"cl":0.88,
"cd":0.018,
"ld":50,
"stall":65,
"description":"Low drag high-speed airfoil."
}

}

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def recommend_airfoil(aircraft, mission):

    return AIRFOILS.get(
        (aircraft, mission),
        {
            "name":"NACA 2412",
            "cl":1.0,
            "cd":0.030,
            "ld":34,
            "stall":48,
            "description":"General purpose airfoil."
        }
    )


def draw_airfoil():

    x=np.linspace(0,1,200)

    t=0.12

    yt=5*t*(
        0.2969*np.sqrt(x)
        -0.1260*x
        -0.3516*x**2
        +0.2843*x**3
        -0.1015*x**4
    )

    fig,ax=plt.subplots(figsize=(8,3))

    ax.plot(x,yt,linewidth=2)
    ax.plot(x,-yt,linewidth=2)

    ax.fill_between(x,yt,-yt,alpha=0.3)

    ax.axis("off")
    ax.set_aspect("equal")

    return fig




# ==========================================================
# SESSION STATE
# ==========================================================

if "airfoil" not in st.session_state:
    st.session_state.airfoil=None

if "aircraft" not in st.session_state:
    st.session_state.aircraft=None

if "mission" not in st.session_state:
    st.session_state.mission=None

if "speed" not in st.session_state:
    st.session_state.speed=0


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("✈ AeroMind AI")

page=st.sidebar.radio(

"Navigation",

[
"🏠 Dashboard",
"🛩 Aircraft Designer",
"📊 Analysis",
"🪶 Airfoil Explorer",
"🤖 AI Engineer",
"📄 Reports"
]

)

st.sidebar.markdown("---")

st.sidebar.success("System Status : Online")

st.sidebar.metric("AI Confidence","98%")

st.sidebar.metric("Database","6 Airfoils")

st.sidebar.metric("Version","3.0")

# ==========================================================
# DASHBOARD
# ==========================================================

if page=="🏠 Dashboard":

    st.title("✈ AeroMind AI")

    st.subheader("AI Powered Aerodynamic Design Platform")

    st.divider()

    c1,c2,c3,c4=st.columns(4)

    c1.metric("Airfoils","6")
    c2.metric("Aircraft","5")
    c3.metric("Design Accuracy","98%")
    c4.metric("Status","Online")

    st.divider()

    left,right=st.columns([2,1])

    with left:

        st.markdown("""
### Welcome to AeroMind AI

AeroMind AI is an intelligent aircraft design assistant
that helps students and engineers select the best airfoil
based on aircraft type and mission profile.

Features

- Aircraft Design
- AI Airfoil Recommendation
- Aerodynamic Analysis
- Interactive Charts
- Engineering Reports
- AI Assistant

""")

    with right:

        fig=go.Figure(go.Indicator(
            mode="gauge+number",
            value=98,
            title={"text":"AI Confidence"},
            gauge={
                "axis":{"range":[0,100]}
            }
        ))

        st.plotly_chart(fig,use_container_width=True)

    st.divider()

    st.subheader("Available Airfoils")

    table=pd.DataFrame(AIRFOILS).T

    st.dataframe(table,use_container_width=True)
    # ==========================================================
# AIRCRAFT DESIGNER
# ==========================================================

elif page == "🛩 Aircraft Designer":

    st.title("🛩 Aircraft Designer")

    st.write("Fill in the aircraft specifications below.")

    left, right = st.columns([2, 1])

    with left:

        aircraft = st.selectbox(
            "Aircraft Type",
            [
                "Drone",
                "Passenger Aircraft",
                "Cargo Aircraft",
                "Glider",
                "Fighter Jet"
            ]
        )

        mission = st.selectbox(
            "Mission",
            [
                "Surveillance",
                "Delivery",
                "Commercial",
                "Long Endurance",
                "Racing"
            ]
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.1,
            value=10.0,
            step=0.5
        )

        speed = st.number_input(
            "Cruise Speed (km/h)",
            min_value=10,
            value=80,
            step=5
        )

        altitude = st.number_input(
            "Altitude (m)",
            min_value=0,
            value=500
        )

        wingspan = st.number_input(
            "Wing Span (m)",
            min_value=0.1,
            value=2.0
        )

        generate = st.button(
            "🚀 Generate AI Design",
            use_container_width=True
        )

    with right:

        st.subheader("Current Configuration")

        st.info(f"""
Aircraft : **{aircraft}**

Mission : **{mission}**

Weight : **{weight} kg**

Cruise Speed : **{speed} km/h**

Altitude : **{altitude} m**

Wing Span : **{wingspan} m**
""")

    # ------------------------------------------------------

    if generate:

        status = st.empty()
        progress = st.progress(0)

        status.write("🔍 Reading aircraft specifications...")
        progress.progress(15)
        time.sleep(0.5)

        status.write("🧠 AI selecting best airfoil...")
        progress.progress(40)
        time.sleep(0.6)

        status.write("📊 Running aerodynamic calculations...")
        progress.progress(65)
        time.sleep(0.6)

        status.write("⚙ Optimizing performance...")
        progress.progress(90)
        time.sleep(0.5)

        status.write("✅ Finalizing design...")
        progress.progress(100)
        time.sleep(0.5)

        status.empty()
        progress.empty()

        airfoil = recommend_airfoil(aircraft, mission)

        st.session_state.airfoil = airfoil
        st.session_state.aircraft = aircraft
        st.session_state.mission = mission
        st.session_state.speed = speed

        st.success("✅ AI Design Generated Successfully!")

        st.divider()

        st.subheader("✈ Recommended Airfoil")

        st.markdown(f"# {airfoil['name']}")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Lift Coefficient",
            airfoil["cl"]
        )

        c2.metric(
            "Drag Coefficient",
            airfoil["cd"]
        )

        c3.metric(
            "L/D Ratio",
            airfoil["ld"]
        )

        c4.metric(
            "Stall Speed",
            f"{airfoil['stall']} km/h"
        )

        st.info(airfoil["description"])

        st.divider()

        st.subheader("🤖 AI Confidence")

        score = np.random.randint(94, 100)

        gauge = go.Figure(go.Indicator(

            mode="gauge+number",

            value=score,

            title={"text": "AI Confidence (%)"},

            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "limegreen"},
                "steps": [
                    {"range": [0, 60], "color": "red"},
                    {"range": [60, 85], "color": "orange"},
                    {"range": [85, 100], "color": "green"},
                ]
            }

        ))

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        st.divider()

        st.subheader("📈 Performance Scores")

        p1, p2, p3, p4 = st.columns(4)

        lift_score = round(airfoil["cl"] * 8, 1)
        drag_score = round((0.05 - airfoil["cd"]) * 180, 1)
        endurance = round(airfoil["ld"] / 5, 1)
        stability = round((100 - airfoil["stall"]) / 10, 1)

        p1.metric(
            "Lift",
            f"{lift_score}/10"
        )

        p2.metric(
            "Efficiency",
            f"{drag_score}/10"
        )

        p3.metric(
            "Endurance",
            f"{endurance}/10"
        )

        p4.metric(
            "Stability",
            f"{stability}/10"
        )

        st.divider()

        st.subheader("🪶 Airfoil Shape")

        fig = draw_airfoil()

        st.pyplot(fig)

        st.divider()

        st.subheader("📊 Performance Analysis")

        chart = performance_chart(
            airfoil["cl"],
            airfoil["cd"],
            airfoil["ld"]
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

        st.divider()

        st.subheader("🧮 Aerodynamic Calculations")

        lift = calculate_lift(
            speed,
            airfoil["cl"]
        )

        drag = lift * airfoil["cd"]

        reynolds = (
            (1.225 * (speed / 3.6) * 1.5)
            / 1.81e-5
        )

        a1, a2, a3 = st.columns(3)

        a1.metric(
            "Estimated Lift",
            f"{lift:.2f} N"
        )

        a2.metric(
            "Estimated Drag",
            f"{drag:.2f} N"
        )

        a3.metric(
            "Reynolds Number",
            f"{reynolds:,.0f}"
        )

        st.divider()

        st.subheader("💡 AI Engineering Recommendation")

        st.success(f"""
For a **{aircraft}** performing **{mission}** missions,
the **{airfoil['name']}** provides an excellent balance
between lift, drag, stability and endurance.

This airfoil is expected to deliver high aerodynamic
efficiency while maintaining safe stall characteristics.
""")
# ==========================================================
# ANALYSIS PAGE
# ==========================================================

elif page == "📊 Analysis":

    st.title("📊 Aerodynamic Analysis")

    if st.session_state.airfoil is None:
        st.warning("Generate a design first.")
        st.stop()

    airfoil = st.session_state.airfoil
    speed = st.session_state.speed

    lift = calculate_lift(speed, airfoil["cl"])
    drag = lift * airfoil["cd"]
    ld = lift / drag if drag else 0

    c1, c2, c3 = st.columns(3)

    c1.metric("Lift", f"{lift:.2f} N")
    c2.metric("Drag", f"{drag:.2f} N")
    c3.metric("L/D Ratio", f"{ld:.2f}")

    st.divider()

    st.subheader("Performance Chart")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=["Lift", "Drag", "L/D"],
        y=[lift, drag, ld],
        mode="lines+markers",
        line=dict(width=4)
    ))

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Performance Breakdown")

    values = pd.DataFrame({

        "Metric": [
            "Lift Coefficient",
            "Drag Coefficient",
            "L/D Ratio",
            "Stall Speed"
        ],

        "Value": [
            airfoil["cl"],
            airfoil["cd"],
            airfoil["ld"],
            airfoil["stall"]
        ]

    })

    st.dataframe(values, use_container_width=True)

# ==========================================================
# AIRFOIL EXPLORER
# ==========================================================

elif page == "🪶 Airfoil Explorer":

    st.title("🪶 Airfoil Explorer")

    data = []

    for key, value in AIRFOILS.items():

        data.append({

            "Aircraft": key[0],
            "Mission": key[1],
            "Airfoil": value["name"],
            "Lift": value["cl"],
            "Drag": value["cd"],
            "L/D": value["ld"],
            "Stall": value["stall"]

        })

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    st.divider()

    option = st.selectbox(
        "Compare Airfoil",
        df["Airfoil"]
    )

    row = df[df["Airfoil"] == option].iloc[0]

    st.subheader(option)

    a, b, c, d = st.columns(4)

    a.metric("Lift", row["Lift"])
    b.metric("Drag", row["Drag"])
    c.metric("L/D", row["L/D"])
    d.metric("Stall", row["Stall"])

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Lift", "Drag", "L/D"],
        y=[
            row["Lift"],
            row["Drag"],
            row["L/D"]
        ]
    ))

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# AI ENGINEER
# ==========================================================

elif page == "🤖 AI Engineer":

    st.title("🤖 AI Engineer")

    st.write("Ask AeroMind AI an engineering question.")

    question = st.text_area(
        "Question",
        height=180
    )

    if st.button(
        "Generate Answer",
        use_container_width=True
    ):

        if question.strip() == "":

            st.warning("Enter a question.")

        else:

            with st.spinner("Thinking..."):

                time.sleep(2)

            answer = f"""
### AI Response

**Question**

{question}

**Answer**

Based on aerodynamic principles, the recommended airfoil depends on the aircraft mission.

For surveillance aircraft, prioritize high lift and stability.

For racing aircraft, minimize drag.

For endurance missions, maximize the Lift-to-Drag ratio.

For cargo aircraft, maintain predictable stall characteristics.

This demo version uses a rule-based AI engine. Future versions can integrate OpenAI or Gemini APIs for real engineering assistance.
"""

            st.markdown(answer)

            st.divider()

            st.subheader("Suggested Questions")

            st.info("""
• Which airfoil is best for endurance?

• How does Reynolds Number affect lift?

• What increases drag?

• Explain stall speed.

• Compare NACA 4412 and S1223.

• How can wing loading be reduced?
""")
# ==========================================================
# REPORTS PAGE
# ==========================================================

elif page == "📄 Reports":

    st.title("📄 Engineering Report")

    if st.session_state.airfoil is None:
        st.warning("Generate an aircraft design first.")
        st.stop()

    airfoil = st.session_state.airfoil
    aircraft = st.session_state.aircraft
    mission = st.session_state.mission
    speed = st.session_state.speed

    lift = calculate_lift(speed, airfoil["cl"])
    drag = lift * airfoil["cd"]

    st.subheader("Aircraft Summary")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Aircraft", aircraft)
        st.metric("Mission", mission)
        st.metric("Cruise Speed", f"{speed} km/h")

    with c2:
        st.metric("Recommended Airfoil", airfoil["name"])
        st.metric("Lift", f"{lift:.2f} N")
        st.metric("Drag", f"{drag:.2f} N")

    st.divider()

    report = f"""
===============================
        AEROMIND AI REPORT
===============================

Aircraft Type : {aircraft}

Mission : {mission}

Cruise Speed : {speed} km/h

--------------------------------

Recommended Airfoil

{airfoil["name"]}

Lift Coefficient : {airfoil["cl"]}

Drag Coefficient : {airfoil["cd"]}

Lift / Drag Ratio : {airfoil["ld"]}

Estimated Stall Speed : {airfoil["stall"]} km/h

--------------------------------

Estimated Lift : {lift:.2f} N

Estimated Drag : {drag:.2f} N

--------------------------------

Description

{airfoil["description"]}

--------------------------------

Generated using AeroMind AI
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name="AeroMind_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.text_area(
        "Report Preview",
        report,
        height=450
    )

# ==========================================================
# FOOTER
# ==========================================================

st.sidebar.markdown("---")
st.sidebar.caption("✈ AeroMind AI v3.0")
st.sidebar.caption("Developed with Streamlit")

st.markdown("---")

st.markdown(
    """
<div style="text-align:center;color:gray;">

### AeroMind AI

AI Powered Aircraft Design Platform

Made with ❤️ using Streamlit & Plotly

</div>
""",
unsafe_allow_html=True
)