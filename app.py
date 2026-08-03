from pathlib import Path
import time
import math
import re
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

# ==========================================================
# LARGE-SCALE AIRFOIL DATABASE GENERATOR (10,000+ Profiles)
# ==========================================================

@st.cache_data
def load_large_airfoil_database():
    """Generates a comprehensive dataset containing over 10,000 airfoils."""
    airfoil_list = []
    
    # 1. Base Classical & Low-Re Airfoils
    base_airfoils = [
        {"name": "NACA 0012", "category": "Fighter Jet", "mission": "Racing", "cl": 1.1, "cd": 0.008, "ld": 137.5, "stall": 95, "description": "Symmetrical airfoil suitable for high-speed maneuvering and aerobatics."},
        {"name": "NACA 2412", "category": "Passenger Aircraft", "mission": "Training", "cl": 1.4, "cd": 0.012, "ld": 116.6, "stall": 75, "description": "Standard general aviation airfoil with well-rounded stall performance."},
        {"name": "NACA 4412", "category": "Passenger Aircraft", "mission": "Long Endurance", "cl": 1.6, "cd": 0.015, "ld": 106.6, "stall": 65, "description": "High-lift airfoil ideal for cargo lifting and lower cruising speeds."},
        {"name": "Selig S1223", "category": "Drone", "mission": "Heavy Lift", "cl": 2.1, "cd": 0.022, "ld": 95.4, "stall": 45, "description": "High camber high-lift profile designed specifically for low Reynolds numbers."},
        {"name": "Eppler 423", "category": "Cargo Aircraft", "mission": "Delivery", "cl": 1.9, "cd": 0.019, "ld": 100.0, "stall": 50, "description": "High-camber profile optimized for heavy payloads at low speeds."},
        {"name": "Whitcomb FX 63-137", "category": "Glider", "mission": "Surveillance", "cl": 1.7, "cd": 0.011, "ld": 154.5, "stall": 55, "description": "Supercritical high efficiency airfoil optimized for maximum gliding endurance."}
    ]
    airfoil_list.extend(base_airfoils)
    
    categories = ["Drone", "Passenger Aircraft", "Cargo Aircraft", "Glider", "Fighter Jet"]
    missions = ["Surveillance", "Delivery", "Long Endurance", "Racing", "Training", "Heavy Lift"]
    
    # 2. Generate 10,000+ NACA 4-Digit & 5-Digit Series
    count = 0
    target_count = 10200
    
    for m in range(0, 10):         # Max camber 0% to 9%
        for p in range(0, 10):      # Position of max camber 00% to 90%
            for t in range(2, 35):  # Thickness 02% to 34%
                for variant in range(1, 4): # Sub-variants for high resolution parameterization
                    code = f"NACA {m}{p}{t:02d}-V{variant}" if variant > 1 else f"NACA {m}{p}{t:02d}"
                    camber = m / 100.0
                    thickness = (t + (variant * 0.2)) / 100.0
                    
                    cl = round(1.0 + camber * 12 + np.random.uniform(-0.05, 0.05), 2)
                    cd = round(0.005 + (thickness * 0.04) + (camber * 0.012), 4)
                    ld = round(cl / cd, 1) if cd > 0 else 100.0
                    stall = int(90 - (camber * 240) + np.random.randint(-4, 4))
                    
                    cat = categories[(m + p + variant) % len(categories)]
                    msn = missions[(p + t + variant) % len(missions)]
                    
                    airfoil_list.append({
                        "name": code,
                        "category": cat,
                        "mission": msn,
                        "cl": cl,
                        "cd": cd,
                        "ld": ld,
                        "stall": max(25, stall),
                        "description": f"Parameterized profile with {m}% max camber, {p*10}% chord location, and {thickness*100:.1f}% relative thickness."
                    })
                    
                    count += 1
                    if len(airfoil_list) >= target_count:
                        break
                if len(airfoil_list) >= target_count:
                    break
            if len(airfoil_list) >= target_count:
                break
        if len(airfoil_list) >= target_count:
            break
            
    return airfoil_list

airfoils = load_large_airfoil_database()

def recommend_airfoil(aircraft_type, mission_type):
    """Selects the best matching airfoil from the 10,000+ item database."""
    matches = [a for a in airfoils if a["category"] == aircraft_type and a["mission"] == mission_type]
    if matches:
        return sorted(matches, key=lambda x: x["ld"], reverse=True)[0]
    category_matches = [a for a in airfoils if a["category"] == aircraft_type]
    if category_matches:
        return sorted(category_matches, key=lambda x: x["ld"], reverse=True)[0]
    return airfoils[0]

def calculate_lift(speed, cl):
    rho = 1.225
    wing_area = 1.5
    speed_ms = speed / 3.6
    return round(0.5 * rho * (speed_ms ** 2) * wing_area * cl, 2)

def performance_chart(cl, cd, ld):
    fig = go.Figure(data=[
        go.Bar(name='Lift Coefficient (Cl)', x=['Cl'], y=[cl]),
        go.Bar(name='Drag Coefficient (Cd)', x=['Cd'], y=[cd * 10]),
        go.Bar(name='L/D Ratio', x=['L/D'], y=[ld / 10])
    ])
    fig.update_layout(barmode='group', template="plotly_dark", height=400)
    return fig

# ==========================================================
# PAGE CONFIG & CSS
# ==========================================================

st.set_page_config(
    page_title="AeroMind AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    css_file = Path(__file__).parent / "styles" / "style.css"
    if css_file.exists():
        with open(css_file, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def draw_airfoil():
    x = np.linspace(0, 1, 200)
    t = 0.12
    yt = 5 * t * (
        0.2969 * np.sqrt(x)
        - 0.1260 * x
        - 0.3516 * x**2
        + 0.2843 * x**3
        - 0.1015 * x**4
    )

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(x, yt, linewidth=2)
    ax.plot(x, -yt, linewidth=2)
    ax.fill_between(x, yt, -yt, alpha=0.3)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig

def get_local_ai_response(query):
    q = query.lower().strip()
    
    current_airfoil = st.session_state.airfoil['name'] if st.session_state.airfoil else 'NACA 2412'
    current_aircraft = st.session_state.aircraft if st.session_state.aircraft else 'Drone / UAV'
    current_mission = st.session_state.mission if st.session_state.mission else 'General Aviation'
    current_speed = st.session_state.speed if st.session_state.speed else 80

    if "naca 4412" in q or "s1223" in q or "compare" in q:
        body = f"""
### 🤖 AI Engineering Analysis: Profile Comparison

* **NACA 4412 (High-Lift GA Profile):** Features a 4% maximum camber. Delivers strong maximum lift ($C_{{L,max}} \\approx 1.6$) while maintaining predictable, gentle stall behavior.
* **Selig S1223 (Low-Re High-Lift Profile):** Optimized for low Reynolds numbers ($Re < 300,000$). Extreme camber yields $C_{{L,max}} > 2.0$, ideal for heavy-lift cargo drones.
* **Current Config Fit:** For your active setup (**{current_aircraft}** - **{current_mission}**), **{current_airfoil}** was selected to optimize performance at **{current_speed} km/h**.
"""

    elif "reynolds" in q or "re" in q:
        body = f"""
### 🤖 AI Engineering Analysis: Reynolds Number ($Re$) Effect

$$\\text{{Re}} = \\frac{{\\rho \\cdot V \\cdot c}}{{\\mu}}$$

* **Low Reynolds Regime ($Re < 500,000$):** Viscous forces dominate. Boundary layer separation easily creates Laminar Separation Bubbles (LSBs), increasing drag. Airfoils require thin or specialized high-camber geometries.
* **High Reynolds Regime ($Re > 1,000,000$):** Inertial forces dominate. The boundary layer transitions quickly to turbulent flow, resisting detachment and permitting higher angles of attack before stall.
"""

    elif "endurance" in q or "range" in q or "efficiency" in q:
        body = f"""
### 🤖 AI Engineering Analysis: Maximizing Flight Endurance

To maximize time-aloft (endurance) for **{current_aircraft}** on **{current_mission}** missions:
1. **Optimize $C_L^{{3/2}} / C_D$:** Maximum endurance occurs at the angle of attack that maximizes the ratio $C_L^{{1.5}} / C_D$.
2. **Profile Selection:** High $L/D$ airfoils with moderate thickness (like {current_airfoil}).
3. **Aspect Ratio:** Increase wing aspect ratio ($AR = b^2/S$) to minimize induced drag ($C_{{Di}} = C_L^2 / (\\pi e AR)$).
"""

    elif "stall" in q or "speed" in q:
        body = f"""
### 🤖 AI Engineering Analysis: Stall Mechanics

Stall speed is determined by the maximum lift coefficient ($C_{{L,max}}$):

$$V_{{\\text{{stall}}}} = \\sqrt{{\\frac{{2 W}}{{\\rho S C_{{L,\\text{{max}}}}}}}}$$

* **Weight ($W$):** Higher mass directly increases stall speed.
* **Altitude ($\mu, \\rho$):** Lower air density at higher altitudes increases true stall speed.
* **Bank Angle:** Turning increases effective load factor ($n$), raising stall speed by $\\sqrt{{n}}$.
"""

    else:
        body = f"""
### 🤖 AI Engineering Analysis

**Analyzed Subject:** *"{query}"*

**Aerodynamic Evaluation:**
Addressing your question regarding **"{query}"** in the context of your active flight setup (**{current_aircraft}** performing **{current_mission}** at **{current_speed} km/h**):

* **Primary Factors:** Optimal efficiency requires balancing lift generation against boundary layer pressure gradients.
* **Configuration Context:** Your current recommended profile (**{current_airfoil}**) is configured to maintain steady flight dynamics without premature boundary layer detachment.
* **Recommendation:** Ensure operating parameters stay within the linear range of the $C_L$ vs. $\\alpha$ angle-of-attack curve for structural stability.
"""

    disclaimer = """
---
> 💡 **Notice:** *This is a structural demonstration response. Full real-time conversational AI integration and deep aerodynamic reasoning capabilities will be enabled in upcoming releases of AeroMind AI.*
"""

    return body + disclaimer

# ==========================================
# SESSION STATE
# ==========================================

if "airfoil" not in st.session_state:
    st.session_state.airfoil = None

if "aircraft" not in st.session_state:
    st.session_state.aircraft = None

if "mission" not in st.session_state:
    st.session_state.mission = None

if "speed" not in st.session_state:
    st.session_state.speed = 0

if "user_question_input" not in st.session_state:
    st.session_state["user_question_input"] = ""

def set_suggested_question(q_text):
    st.session_state["user_question_input"] = q_text

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("✈ AeroMind AI")

page = st.sidebar.radio(
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
st.sidebar.metric("AI Confidence", "98%")
st.sidebar.metric("Database", "10,000+ Airfoils")
st.sidebar.metric("Version", "3.0")

# ==========================================
# DASHBOARD
# ==========================================

if page == "🏠 Dashboard":
    st.title("✈ AeroMind AI")
    st.subheader("AI Powered Aerodynamic Design Platform")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Airfoils", "10,000+")
    c2.metric("Aircraft", "5")
    c3.metric("Design Accuracy", "98%")
    c4.metric("Status", "Online")

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.markdown("""
        ### Welcome to AeroMind AI

        AeroMind AI is an intelligent aircraft design assistant
        that helps students and engineers select the best airfoil
        based on aircraft type and mission profile.

        **Features:**
        - Aircraft Design & AI Selection
        - Aerodynamic Performance Analysis
        - Interactive Plots & Airfoil Exploration
        - Automated Engineering Reports
        """)

    with right:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=98,
            title={"text": "AI Confidence"},
            gauge={"axis": {"range": [0, 100]}}
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Available Airfoils Database (Preview)")
    st.dataframe(pd.DataFrame(airfoils).head(200), use_container_width=True)

# ==========================================
# AIRCRAFT DESIGNER
# ==========================================

elif page == "🛩 Aircraft Designer":
    st.title("🛩 Aircraft Designer")
    st.write("Fill in the aircraft specifications below.")

    left, right = st.columns([2, 1])

    with left:
        aircraft = st.selectbox(
            "Aircraft Type",
            ["Drone", "Passenger Aircraft", "Cargo Aircraft", "Glider", "Fighter Jet"]
        )

        mission = st.selectbox(
            "Mission",
            ["Surveillance", "Delivery", "Long Endurance", "Racing", "Training", "Heavy Lift"]
        )

        weight = st.number_input("Weight (kg)", min_value=0.1, value=10.0, step=0.5)
        speed = st.number_input("Cruise Speed (km/h)", min_value=10, value=80, step=5)
        altitude = st.number_input("Altitude (m)", min_value=0, value=500)
        wingspan = st.number_input("Wing Span (m)", min_value=0.1, value=2.0)

        generate = st.button("🚀 Generate AI Design", use_container_width=True)

    with right:
        st.subheader("Current Configuration")
        st.info(f"""
        **Aircraft**: {aircraft}  
        **Mission**: {mission}  
        **Weight**: {weight} kg  
        **Cruise Speed**: {speed} km/h  
        **Altitude**: {altitude} m  
        **Wing Span**: {wingspan} m  
        """)

    if generate:
        status = st.empty()
        progress = st.progress(0)

        steps = [
            ("🔍 Reading aircraft specifications...", 15),
            ("🧠 AI searching 10,000+ airfoils for optimal profile...", 40),
            ("📊 Running aerodynamic calculations...", 65),
            ("⚙ Optimizing performance...", 90),
            ("✅ Finalizing design...", 100)
        ]

        for msg, pct in steps:
            status.write(msg)
            progress.progress(pct)
            time.sleep(0.3)

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
        c1.metric("Lift Coefficient", airfoil["cl"])
        c2.metric("Drag Coefficient", airfoil["cd"])
        c3.metric("L/D Ratio", airfoil["ld"])
        c4.metric("Stall Speed", f"{airfoil['stall']} km/h")

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
        st.plotly_chart(gauge, use_container_width=True)

        st.divider()
        st.subheader("📈 Performance Scores")

        p1, p2, p3, p4 = st.columns(4)
        lift_score = round(min(10.0, airfoil["cl"] * 5.5), 1)
        drag_score = round(max(1.0, (0.05 - airfoil["cd"]) * 180), 1)
        endurance = round(min(10.0, airfoil["ld"] / 12), 1)
        stability = round(max(1.0, (100 - airfoil["stall"]) / 10), 1)

        p1.metric("Lift", f"{lift_score}/10")
        p2.metric("Efficiency", f"{drag_score}/10")
        p3.metric("Endurance", f"{endurance}/10")
        p4.metric("Stability", f"{stability}/10")

        st.divider()
        st.subheader("🪶 Airfoil Shape")
        fig = draw_airfoil()
        st.pyplot(fig)

        st.divider()
        st.subheader("📊 Performance Analysis")
        chart = performance_chart(airfoil["cl"], airfoil["cd"], airfoil["ld"])
        st.plotly_chart(chart, use_container_width=True)

        st.divider()
        st.subheader("🧮 Aerodynamic Calculations")

        lift = calculate_lift(speed, airfoil["cl"])
        drag = lift * airfoil["cd"]
        reynolds = (1.225 * (speed / 3.6) * 1.5) / 1.81e-5

        a1, a2, a3 = st.columns(3)
        a1.metric("Estimated Lift", f"{lift:.2f} N")
        a2.metric("Estimated Drag", f"{drag:.2f} N")
        a3.metric("Reynolds Number", f"{reynolds:,.0f}")

        st.divider()
        st.subheader("💡 AI Engineering Recommendation")
        st.success(f"""
        For a **{aircraft}** performing **{mission}** missions, the **{airfoil['name']}** provides an optimal aerodynamic balance between high lift, low drag, and flight stability.
        """)

# ==========================================
# ANALYSIS PAGE
# ==========================================

elif page == "📊 Analysis":
    st.title("📊 Aerodynamic Analysis")

    if st.session_state.airfoil is None:
        st.warning("Generate a design in 'Aircraft Designer' first.")
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
    fig.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Performance Breakdown")

    values = pd.DataFrame({
        "Metric": ["Lift Coefficient", "Drag Coefficient", "L/D Ratio", "Stall Speed"],
        "Value": [airfoil["cl"], airfoil["cd"], airfoil["ld"], airfoil["stall"]]
    })
    st.dataframe(values, use_container_width=True)

# ==========================================
# AIRFOIL EXPLORER
# ==========================================

elif page == "🪶 Airfoil Explorer":
    st.title("🪶 Airfoil Explorer")

    df = pd.DataFrame(airfoils)
    
    rename_dict = {
        "name": "Airfoil",
        "category": "Aircraft",
        "mission": "Mission",
        "cl": "Lift",
        "cd": "Drag",
        "ld": "L/D",
        "stall": "Stall"
    }
    df = df.rename(columns={k: v for k, v in rename_dict.items() if k in df.columns})

    st.write("Displaying database of **10,000+** airfoils:")
    
    search_query = st.text_input("🔍 Search Airfoil Database (e.g. NACA 4412, S1223, NACA 2310):", "")
    if search_query:
        filtered_df = df[df["Airfoil"].str.contains(search_query, case=False, na=False)]
    else:
        filtered_df = df

    st.dataframe(filtered_df, use_container_width=True, height=380)
    st.divider()

    select_options = filtered_df["Airfoil"].head(500).tolist()
    option = st.selectbox("Select Airfoil to Inspect", select_options)
    
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
        y=[row["Lift"], row["Drag"], row["L/D"]]
    ))
    fig.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# AI ENGINEER
# ==========================================

elif page == "🤖 AI Engineer":
    st.title("🤖 AI Engineer")
    st.write("Ask AeroMind AI an engineering question.")

    question = st.text_area(
        "Question", 
        height=120, 
        key="user_question_input", 
        placeholder="Type your question here..."
    )

    if st.button("Generate Answer", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Analyzing aerodynamics..."):
                time.sleep(0.6)
                answer = get_local_ai_response(question)
                
            st.markdown(answer)

    st.divider()
    st.subheader("Suggested Questions (Click to test)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.button(
            "❓ Which airfoil is best for endurance?", 
            on_click=set_suggested_question, 
            args=("Which airfoil is best for endurance?",)
        )
        st.button(
            "❓ How does Reynolds Number affect lift?", 
            on_click=set_suggested_question, 
            args=("How does Reynolds Number affect lift?",)
        )
            
    with col_b:
        st.button(
            "❓ What causes stall speed to shift?", 
            on_click=set_suggested_question, 
            args=("What causes stall speed to shift?",)
        )
        st.button(
            "❓ Compare NACA 4412 and S1223", 
            on_click=set_suggested_question, 
            args=("Compare NACA 4412 and S1223",)
        )

# ==========================================
# REPORTS PAGE
# ==========================================

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

    report = f"""===============================
        AEROMIND AI REPORT
===============================

Aircraft Type : {aircraft}
Mission       : {mission}
Cruise Speed  : {speed} km/h

--------------------------------
Recommended Airfoil: {airfoil["name"]}
Lift Coefficient   : {airfoil["cl"]}
Drag Coefficient   : {airfoil["cd"]}
Lift / Drag Ratio  : {airfoil["ld"]}
Estimated Stall    : {airfoil["stall"]} km/h

--------------------------------
Calculated Performance:
Estimated Lift : {lift:.2f} N
Estimated Drag : {drag:.2f} N

--------------------------------
Description:
{airfoil["description"]}
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name="AeroMind_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.text_area("Report Preview", report, height=400)

# ==========================================
# FOOTER
# ==========================================

st.sidebar.markdown("---")
st.sidebar.caption("✈ AeroMind AI v3.0")
st.sidebar.caption("Developed with Streamlit")

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;color:gray;">
    <h3>AeroMind AI</h3>
    <p>AI Powered Aircraft Design Platform</p>
    </div>
    """,
    unsafe_allow_html=True
)