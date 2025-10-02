import streamlit as st
import math
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Asteroid Impact Simulator", layout="wide")

# -------------------------------
# Portada
# -------------------------------
st.title("Asteroid Impact Simulator")
st.markdown(
    "This interactive simulator models asteroid impact scenarios on Earth using physics-based "
    "calculations and geospatial visualizations. The tool integrates scientific principles for "
    "impact energy, crater formation, and possible deflection strategies."
)
st.divider()

# -------------------------------
# Pestañas principales
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Asteroid Parameters", 
    "Impact Analysis", 
    "Visualizations", 
    "Mitigation Strategies"
])

# -------------------------------
# TAB 1: Asteroid Parameters
# -------------------------------
with tab1:
    st.header("Asteroid Parameters")
    diameter = st.slider("Asteroid Diameter (m)", 10, 2000, 300)
    velocity = st.slider("Impact Velocity (km/s)", 5, 40, 20)
    density = st.slider("Density (kg/m³)", 500, 8000, 3000)

    # Calculations
    radius = diameter / 2
    volume = (4/3) * math.pi * (radius ** 3)
    mass = volume * density
    vel_ms = velocity * 1000
    energy_joules = 0.5 * mass * (vel_ms ** 2)
    energy_megatons = energy_joules / 4.184e15  # 1 Mt TNT = 4.184e15 J

    st.subheader("Basic Calculations")
    st.write(f"Estimated Mass: {mass:,.2e} kg")
    st.write(f"Kinetic Energy: {energy_megatons:,.2f} megatons TNT equivalent")

# -------------------------------
# TAB 2: Impact Analysis
# -------------------------------
with tab2:
    st.header("Impact Consequences")
    if energy_megatons < 100:
        st.success("Regional damage expected")
    elif energy_megatons < 10000:
        st.warning("Severe continental effects likely")
    else:
        st.error("Global catastrophe likely")

    # Pie chart for effects
    values = [
        min(energy_megatons/100, 100), 
        min(energy_megatons/1000, 100), 
        min(energy_megatons/10000, 100)
    ]
    labels = ["Local Effects", "Continental Effects", "Global Effects"]

    fig = px.pie(values=values, names=labels, hole=0.3)
    fig.update_layout(title="Estimated Distribution of Impact Effects")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# TAB 3: Visualizations
# -------------------------------
with tab3:
    st.header("Geospatial and Orbital Visualizations")

    # --- USER INPUT FOR COORDINATES ---
    st.subheader("Impact Location Map")

    impact_lat = st.number_input("Select impact latitude (°)", -90.0, 90.0, 12.1)
    impact_lon = st.number_input("Select impact longitude (°)", -180.0, 180.0, -86.3)

    view_state = pdk.ViewState(latitude=impact_lat, longitude=impact_lon, zoom=5, pitch=45)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"lat": impact_lat, "lon": impact_lon}],
        get_position=["lon", "lat"],
        get_color=[200, 30, 30],
        get_radius=50000,
    )

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/satellite-streets-v12",
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Estimated impact location"}
    )
    st.pydeck_chart(deck)

    # --- ORBITAL SIMULATION ---
    st.subheader("Orbital Simulation (3D)")

    theta = [i for i in range(0, 360)]
    earth_orbit_x = [math.cos(math.radians(t)) for t in theta]
    earth_orbit_y = [math.sin(math.radians(t)) for t in theta]
    asteroid_orbit_x = [1.5*math.cos(math.radians(t)) for t in theta]
    asteroid_orbit_y = [0.7*math.sin(math.radians(t)) for t in theta]

    orbit_fig = go.Figure()

    # Earth orbit
    orbit_fig.add_trace(go.Scatter3d(
        x=earth_orbit_x, y=earth_orbit_y, z=[0]*360,
        mode="lines", name="Earth Orbit", line=dict(color="blue", width=4)
    ))

    # Asteroid orbit
    orbit_fig.add_trace(go.Scatter3d(
        x=asteroid_orbit_x, y=asteroid_orbit_y, z=[0]*360,
        mode="lines", name="Asteroid Orbit", line=dict(color="red", width=4)
    ))

    # Earth marker
    orbit_fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers", name="Earth", marker=dict(size=8, color="green")
    ))

    orbit_fig.update_layout(
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
        margin=dict(l=0, r=0, b=0, t=30),
        height=600
    )

    st.plotly_chart(orbit_fig, use_container_width=True)
    st.markdown("Rotate the 3D plot with your mouse for a virtual reality-like experience of the orbital paths.")

# -------------------------------
# TAB 4: Mitigation
# -------------------------------
with tab4:
    st.header("Mitigation Strategies")
    st.markdown("Test different deflection strategies and evaluate their outcomes.")

    delta_v = st.slider("Applied Deflection Δv (m/s)", 0, 50, 0)
    lead_time = st.slider("Lead Time before Impact (years)", 0, 10, 2)

    if delta_v > 0 and lead_time > 0:
        st.success(f"With Δv = {delta_v} m/s applied {lead_time} years before impact, Earth is saved.")
    else:
        st.error("No deflection applied. The asteroid impacts Earth.")

# -------------------------------
# Conclusion
# -------------------------------
st.divider()
st.header("Conclusion")
st.markdown(
    "This simulator integrates scientific models and interactive visualizations to provide insights "
    "into asteroid impact risks and mitigation strategies. Through maps, orbital models, and physics-based "
    "calculations, it demonstrates how timely interventions can prevent catastrophic events."
)

