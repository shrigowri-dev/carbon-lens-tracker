import streamlit as st
import plotly.express as px
import pandas as pd

# -------------------------------
# Carbon Calculation Function
# -------------------------------
def calculate_carbon(travel_km, electricity_units, diet_type):
    TRAVEL_FACTOR = 0.21       # kg CO2 per km
    ELECTRICITY_FACTOR = 0.82  # kg CO2 per kWh

    DIET = {
        "Vegetarian": 1500,
        "Mixed": 2500,
        "Non-Vegetarian": 3300
    }

    travel_emission = travel_km * TRAVEL_FACTOR * 365 / 7
    electricity_emission = electricity_units * ELECTRICITY_FACTOR * 12
    diet_emission = DIET[diet_type]

    total = travel_emission + electricity_emission + diet_emission

    return travel_emission, electricity_emission, diet_emission, total


# -------------------------------
# Recommendation Engine
# -------------------------------
def recommendations(travel, electricity, diet):
    recs = []

    if travel > 1500:
        recs.append("🚲 Use public transport or carpool to reduce travel emissions.")

    if electricity > 1200:
        recs.append("💡 Reduce AC usage and switch to LED bulbs.")

    if diet > 2500:
        recs.append("🥗 Try plant-based meals twice a week.")

    if not recs:
        recs.append("✅ Excellent! Your carbon footprint is already low.")

    return recs


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Carbon Lens Tracker", layout="centered")

st.title("🌍 Carbon Lens Tracker")
st.write("Measure, visualize, and reduce your carbon footprint")

st.sidebar.header("User Inputs")

travel_km = st.sidebar.slider("🚗 Daily Travel (km)", 0, 100, 10)
electricity_units = st.sidebar.slider("⚡ Monthly Electricity (kWh)", 50, 500, 150)
diet_type = st.sidebar.selectbox(
    "🍽️ Diet Type",
    ["Vegetarian", "Mixed", "Non-Vegetarian"]
)

if st.sidebar.button("Calculate Carbon Footprint"):
    travel, electricity, diet, total = calculate_carbon(
        travel_km, electricity_units, diet_type
    )

    st.subheader("📊 Annual Carbon Footprint (kg CO₂)")
    st.metric("Total Emissions", f"{total:.2f} kg")

    data = pd.DataFrame({
        "Source": ["Travel", "Electricity", "Diet"],
        "Emissions": [travel, electricity, diet]
    })

    fig = px.pie(
        data,
        values="Emissions",
        names="Source",
        title="Emission Breakdown"
    )

    st.plotly_chart(fig)

    st.subheader("🔧 Personalized Recommendations")
    for r in recommendations(travel, electricity, diet):
        st.write(r)

    st.subheader("🏙️ Smart City Comparison")
    city_avg = 4500
    st.write(f"City Average Emissions: **{city_avg} kg CO₂/year**")

    if total < city_avg:
        st.success("🎉 You are below the city average!")
    else:
        st.warning("⚠️ You are above the city average. Small changes matter!")