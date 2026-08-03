import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="AeroMind AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# AIRFOIL DATABASE
# -------------------------------

AIRFOILS = {
    ("Drone", "Surveillance"): {
        "name": "NACA 4412",
        "cl": 1.18,
        "cd": 0.028,
        "ld": 42,
        "stall": 42,
        "desc": "Excellent lift and stability for surveillance drones."
    },
    ("Drone", "Delivery"): {
        "name": "S1223",
        "cl": 1.45,
        "cd": 0.040,
        "ld": 36,
        "stall": 35,
        "desc": "High-lift airfoil suitable for delivery drones."
    },
    ("Glider", "Long Endurance"): {
        "name": "MH32",
        "cl": 0.95,
        "cd": 0.020,
        "ld": 48,
        "stall": 38,
        "desc": "Efficient glider airfoil with low drag."
    },
    ("Cargo Aircraft", "Delivery"): {
        "name": "Clark Y",
        "cl": 1.10,
        "cd": 0.032,
        "ld": 35,
        "stall": 50,
        "desc": "Reliable cargo aircraft airfoil."
    },
    ("Fighter Jet", "Racing"): {
        "name": "NACA 64A204",
        "cl": 0.88,
        "cd": 0.018,
        "ld": 50,
        "stall": 65,
        "desc": "Low drag profile for high-speed aircraft."
    }
}


def recommend_airfoil(aircraft, mission):
    return AIRFOILS.get(
        (aircraft, mission),
        {
            "name": "NACA 2412",
            "cl": 1.02,
            "cd": 0.030,
            "ld": 34,
            "stall": 48,
            "desc": "General-purpose airfoil."
        }
    )


def draw_airfoil():

    x = np.linspace(0, 1, 200)

    t = 0.12

    yt = (
        5
        * t
        * (
            0.2969 * np.sqrt(x)
            - 0.1260 * x
            - 0.3516 * x**2
            + 0.2843 * x**3
            - 0.1015 * x**4
        )
    )

    fig, ax = plt.subplots(figsize=(8, 3))

    ax.plot(x, yt, linewidth=2)

    ax.plot(x, -yt, linewidth=2)

    ax.fill_between(x, yt, -yt, alpha=0.3)

    ax.set_aspect("equal")

    ax.axis("off")

    return fig


def performance_chart(cl, cd, ld):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Lift", "Drag", "L/D"],
            y=[cl, cd, ld],
            text=[cl, cd, ld],
            textposition="outside",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        title="Performance Analysis"
    )

    return fig


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("✈ AeroMind AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🛩 Aircraft Designer",
        "📊 Analysis",
        "🪶 Airfoils",
        "🤖 AI Engineer",
        "📄 Reports",
    ],
)

# -------------------------------
# DASHBOARD
# -------------------------------

if page == "🏠 Dashboard":

    st.title("✈ AeroMind AI")

    st.subheader("AI Powered Aerodynamic Design Platform")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Airfoils", "6")

    c2.metric("Aircraft", "5")

    c3.metric("AI Confidence", "96%")

    c4.metric("Status", "Online")

    st.divider()

    st.markdown(
        """
### Welcome

AeroMind AI helps engineers and students select the best airfoil
for aircraft missions using aerodynamic principles and AI-assisted
recommendations.

Use the navigation menu to start designing.
"""
    )

# -------------------------------
# AIRCRAFT DESIGNER
# -------------------------------

elif page == "🛩 Aircraft Designer":

    st.title("Aircraft Designer")

    left, right = st.columns([2, 1])

    with left:

        aircraft = st.selectbox(
            "Aircraft Type",
            [
                "Drone",
                "Passenger Aircraft",
                "Cargo Aircraft",
                "Glider",
                "Fighter Jet",
            ],
        )

        mission = st.selectbox(
            "Mission",
            [
                "Surveillance",
                "Delivery",
                "Training",
                "Long Endurance",
                "Racing",
            ],
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.1,
            value=2.0,
        )

        speed = st.number_input(
            "Cruise Speed (km/h)",
            min_value=10,
            value=80,
        )

        altitude = st.number_input(
            "Altitude (m)",
            min_value=0,
            value=500,
        )

        wingspan = st.number_input(
            "Wing Span (m)",
            min_value=0.1,
            value=1.5,
        )

        generate = st.button("🚀 Generate Design")
    with right:

        st.subheader("Current Configuration")

        st.write(f"**Aircraft:** {aircraft}")
        st.write(f"**Mission:** {mission}")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Cruise Speed:** {speed} km/h")
        st.write(f"**Altitude:** {altitude} m")
        st.write(f"**Wing Span:** {wingspan} m")

    if generate:

        with st.spinner("AI is analyzing your aircraft..."):
            time.sleep(2)

        airfoil = recommend_airfoil(aircraft, mission)
        # Save the generated design so other pages can use it
        st.session_state["airfoil"] = airfoil
        st.session_state["speed"] = speed
        st.session_state["aircraft"] = aircraft
        st.session_state["mission"] = mission

        st.success("Design Generated Successfully!")

        st.subheader("Recommended Airfoil")

        st.markdown(f"## ✈ {airfoil['name']}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Lift Coefficient", airfoil["cl"])
        col2.metric("Drag Coefficient", airfoil["cd"])
        col3.metric("L/D Ratio", airfoil["ld"])

        st.metric(
            "Estimated Stall Speed",
            f"{airfoil['stall']} km/h"
        )

        st.info(airfoil["desc"])

        st.divider()

        st.subheader("Airfoil Shape")

        fig = draw_airfoil()

        st.pyplot(fig)

        st.divider()

        st.subheader("Performance Analysis")

        chart = performance_chart(
            airfoil["cl"],
            airfoil["cd"],
            airfoil["ld"]
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

# ----------------------------------------------------
# ANALYSIS PAGE
# ----------------------------------------------------

elif page == "📊 Analysis":

    st.title("📊 Aerodynamic Analysis")

    if "airfoil" not in st.session_state:
        st.warning("Please generate a design from the Aircraft Designer page first.")
        st.stop()

    airfoil = st.session_state["airfoil"]
    speed = st.session_state["speed"]

    lift = 0.5 * 1.225 * (speed ** 2) * airfoil["cl"]

    st.metric("Estimated Lift", f"{lift:.2f}")
    st.metric("Lift Coefficient", airfoil["cl"])
    st.metric("Drag Coefficient", airfoil["cd"])
    st.metric("L/D Ratio", airfoil["ld"])
# ----------------------------------------------------
# AIRFOILS PAGE
# ----------------------------------------------------

elif page == "🪶 Airfoils":

    st.title("🪶 Airfoil Explorer")

    table = pd.DataFrame([
        {
            "Airfoil": v["name"],
            "Lift": v["cl"],
            "Drag": v["cd"],
            "L/D": v["ld"],
            "Description": v["desc"]
        }
        for v in AIRFOILS.values()
    ])

    st.dataframe(
        table,
        use_container_width=True
    )

# ----------------------------------------------------
# AI ENGINEER PAGE
# ----------------------------------------------------

elif page == "🤖 AI Engineer":

    st.title("🤖 AI Engineer")

    question = st.text_area(
        "Ask an engineering question"
    )

    if st.button("Generate Answer"):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            st.success("AI Response")

            st.write(
                f"""
Your Question:

{question}

Demo Response:

Based on the selected aircraft mission,
AeroMind AI recommends choosing an
airfoil that maximizes lift while keeping
drag low.

In future versions this page will connect
to an actual AI model like Gemini or GPT.
"""
            )

# ----------------------------------------------------
# REPORTS PAGE
# ----------------------------------------------------

elif page == "📄 Reports":

    st.title("📄 Engineering Report")

    st.write("""
The final version will generate:

✅ Aircraft Summary

✅ Recommended Airfoil

✅ Lift & Drag Analysis

✅ Performance Charts

✅ PDF Report
""")

    st.download_button(
        "Download Sample Report",
        data="AeroMind AI Report",
        file_name="AeroMind_Report.txt"
    )

st.sidebar.markdown("---")
st.sidebar.caption("AeroMind AI v2.0")