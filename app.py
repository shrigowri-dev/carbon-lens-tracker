# app.py — Carbon Lens Tracker (Full Version with Auto Transport Tracking)
import streamlit as st
import plotly.express as px
import pandas as pd
from model import calculate_carbon, get_recommendations
from transport_tracker import calculate_distance, calculate_transport_emission, EMISSION_FACTORS

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Carbon Lens Tracker", page_icon="🌍", layout="wide")

st.title("🌍 Carbon Lens Tracker")
st.subheader("AI-Based Personal Carbon Footprint Estimator — India Edition")
st.markdown("---")

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("ℹ️ About Carbon Lens")
    st.info("Track your carbon footprint across Transport, Energy, Food, Water, Shopping and Waste!")
    st.markdown("### 🎯 Benchmarks")
    st.metric("🇮🇳 India Average", "1,800 kg/year")
    st.metric("🌍 Global Average", "4,000 kg/year")
    st.metric("🎯 Paris Target", "2,300 kg/year")
    st.markdown("*Source: World Bank, Global Carbon Project*")

# ─── INPUT TABS ───────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚗 Transport", "⚡ Energy", "🍽️ Food", "💧 Water", "🛍️ Shopping", "🗑️ Waste"
])

# ─── TRANSPORT TAB ────────────────────────────────────────────────────────────
with tab1:
    st.header("🚗 Transport Tracker")
    st.caption("Enter your route and we'll automatically calculate the distance!")

    # Auto distance calculator
    st.subheader("📍 Auto Distance Calculator")
    col1, col2 = st.columns(2)
    with col1:
        from_location = st.text_input("📍 From Location", placeholder="e.g. Coimbatore Railway Station")
    with col2:
        to_location = st.text_input("📍 To Location", placeholder="e.g. Karunya University")

    vehicle_type = st.selectbox("🚗 Vehicle Type", list(EMISSION_FACTORS.keys()))
    trips_per_day = st.slider("How many trips per day?", 1, 10, 2)

    # Initialize session state for transport
    if "transport_emission" not in st.session_state:
        st.session_state.transport_emission = 0
    if "calculated_distance" not in st.session_state:
        st.session_state.calculated_distance = 0

    if st.button("📍 Calculate Distance & Emission"):
        if from_location and to_location:
            with st.spinner("Finding locations on map... please wait"):
                distance, error = calculate_distance(from_location, to_location)

            if error:
                st.error(f"❌ {error} — Please try a more specific location name")
            else:
                emission = calculate_transport_emission(distance, vehicle_type, trips_per_day)
                st.session_state.transport_emission = emission
                st.session_state.calculated_distance = distance

                st.success(f"✅ Distance calculated successfully!")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📏 Distance", f"{distance} km")
                with col2:
                    st.metric("🔄 Daily Trips", f"{trips_per_day} trips")
                with col3:
                    st.metric("💨 Annual Emission", f"{emission} kg CO₂/year")
        else:
            st.warning("⚠️ Please enter both From and To locations!")

    # Show current transport emission
    if st.session_state.transport_emission > 0:
        st.info(f"✅ Transport emission saved: **{st.session_state.transport_emission} kg CO₂/year** for {st.session_state.calculated_distance} km route")

    # Manual override
    st.markdown("---")
    st.subheader("✈️ Additional Transport (Manual)")
    st.caption("For flights and other transport not covered above")
    col1, col2 = st.columns(2)
    with col1:
        domestic_flights = st.number_input("Domestic flights per year", 0, 50, 0)
        domestic_flight_hrs = st.slider("Avg hours per domestic flight", 1, 5, 2)
    with col2:
        international_flights = st.number_input("International flights per year", 0, 20, 0)
        international_flight_hrs = st.slider("Avg hours per international flight", 1, 20, 8)

# ─── ENERGY TAB ───────────────────────────────────────────────────────────────
with tab2:
    st.header("⚡ Home Energy")
    st.caption("Enter your monthly energy consumption")
    col1, col2 = st.columns(2)
    with col1:
        electricity_kwh = st.slider("Monthly electricity units (kWh)", 0, 1000, 100)
        lpg_cylinders = st.slider("LPG cylinders per month", 0, 10, 1)
    with col2:
        png_scm = st.slider("Piped gas per month (SCM)", 0, 50, 0)
        generator_ltrs = st.slider("Generator diesel per month (litres)", 0, 50, 0)

# ─── FOOD TAB ─────────────────────────────────────────────────────────────────
with tab3:
    st.header("🍽️ Food & Diet")
    st.caption("Enter your average weekly food consumption")
    col1, col2 = st.columns(2)
    with col1:
        beef_mutton_meals = st.slider("Beef/Mutton meals per week", 0, 21, 2)
        chicken_meals = st.slider("Chicken meals per week", 0, 21, 3)
        fish_meals = st.slider("Fish meals per week", 0, 21, 2)
        eggs_per_day = st.slider("Eggs per day", 0, 10, 1)
    with col2:
        veg_meals = st.slider("Vegetarian meals per week", 0, 21, 10)
        dairy_litres = st.slider("Dairy per week (litres)", 0, 10, 2)
        food_waste_kg = st.slider("Food wasted per week (kg)", 0, 10, 1)

# ─── WATER TAB ────────────────────────────────────────────────────────────────
with tab4:
    st.header("💧 Water Usage")
    st.caption("Enter your daily water consumption")
    col1, col2 = st.columns(2)
    with col1:
        water_litres = st.slider("Daily water usage (litres)", 0, 500, 100)
        shower_mins = st.slider("Daily hot shower (minutes)", 0, 60, 10)
    with col2:
        washing_cycles = st.slider("Washing machine cycles per week", 0, 14, 3)

# ─── SHOPPING TAB ─────────────────────────────────────────────────────────────
with tab5:
    st.header("🛍️ Shopping & Lifestyle")
    st.caption("Enter your monthly/yearly shopping habits")
    col1, col2 = st.columns(2)
    with col1:
        clothing_items = st.slider("Clothing items per month", 0, 20, 2)
        electronics_items = st.number_input("Electronics per year", 0, 20, 1)
    with col2:
        online_orders = st.slider("Online orders per week", 0, 30, 3)

# ─── WASTE TAB ────────────────────────────────────────────────────────────────
with tab6:
    st.header("🗑️ Waste Management")
    st.caption("Enter your weekly waste habits")
    col1, col2 = st.columns(2)
    with col1:
        landfill_kg = st.slider("Waste to landfill per week (kg)", 0, 20, 5)
        recycled_kg = st.slider("Waste recycled per week (kg)", 0, 20, 2)
    with col2:
        composting_kg = st.slider("Waste composted per week (kg)", 0, 10, 1)

# ─── CALCULATE BUTTON ─────────────────────────────────────────────────────────
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    calculate = st.button("🔍 Calculate My Full Carbon Footprint", use_container_width=True)

if calculate:
    # Use auto-calculated transport if available, else calculate from manual
    if st.session_state.transport_emission > 0:
        transport_override = st.session_state.transport_emission
    else:
        transport_override = None

    total, breakdown = calculate_carbon(
        "Petrol", 0 if transport_override else 10,
        0, 0, 0, 0,
        domestic_flights, domestic_flight_hrs,
        international_flights, international_flight_hrs,
        electricity_kwh, lpg_cylinders, png_scm, generator_ltrs,
        beef_mutton_meals, chicken_meals, fish_meals,
        eggs_per_day, veg_meals, dairy_litres, food_waste_kg,
        water_litres, shower_mins, washing_cycles,
        clothing_items, electronics_items, online_orders,
        landfill_kg, recycled_kg, composting_kg
    )

    # Add auto transport emission if calculated
    if transport_override:
        total = total + transport_override
        breakdown["🚗 Transport"] = transport_override

    st.markdown("---")
    st.header("📊 Your Results")

    # ─── METRIC CARDS ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 Your Footprint", f"{total:,.0f} kg/year")
    with col2:
        india_diff = round(total - 1800, 2)
        st.metric("vs 🇮🇳 India Avg", f"{abs(india_diff):,.0f} kg",
                  delta=f"{'above' if india_diff > 0 else 'below'}",
                  delta_color="inverse")
    with col3:
        global_diff = round(total - 4000, 2)
        st.metric("vs 🌍 Global Avg", f"{abs(global_diff):,.0f} kg",
                  delta=f"{'above' if global_diff > 0 else 'below'}",
                  delta_color="inverse")
    with col4:
        trees_needed = int(total / 22)
        st.metric("🌳 Trees to Offset", f"{trees_needed} trees/year")

    # ─── STATUS ───────────────────────────────────────────────────────────────
    if total < 1800:
        st.success("🟢 Excellent! You are below India's average. You're a climate champion!")
        st.balloons()
    elif total < 2300:
        st.success("🟡 Good! You are within the Paris Agreement target of 2,300 kg/year!")
    elif total < 4000:
        st.warning("🟠 Above India's average but below global average. Room to improve!")
    else:
        st.error("🔴 Above the global average. Check recommendations below!")

    # ─── CHARTS ───────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Emission Breakdown")
        df = pd.DataFrame({
            "Category": list(breakdown.keys()),
            "CO₂ (kg/year)": list(breakdown.values())
        })
        fig = px.pie(df, values="CO₂ (kg/year)", names="Category",
                     title="Where your emissions come from",
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📈 Category Wise Emissions")
        fig2 = px.bar(df, x="Category", y="CO₂ (kg/year)",
                      title="Emissions by Category",
                      color="CO₂ (kg/year)",
                      color_continuous_scale="reds")
        fig2.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig2, use_container_width=True)

    # ─── BENCHMARK COMPARISON ─────────────────────────────────────────────────
    st.subheader("🌍 How You Compare to World Benchmarks")
    compare_df = pd.DataFrame({
        "": ["You", "🇮🇳 India Avg", "🌍 Global Avg", "🎯 Paris Target"],
        "CO₂ (kg/year)": [total, 1800, 4000, 2300]
    })
    fig3 = px.bar(compare_df, x="", y="CO₂ (kg/year)",
                  title="Your Footprint vs World Benchmarks",
                  color="CO₂ (kg/year)",
                  color_continuous_scale="RdYlGn_r")
    st.plotly_chart(fig3, use_container_width=True)

    # ─── RECOMMENDATIONS ──────────────────────────────────────────────────────
    st.markdown("---")
    st.header("💡 Personalized Recommendations")
    recommendations = get_recommendations(breakdown, total)
    for rec in recommendations:
        st.success(rec)

    # ─── SAVINGS ──────────────────────────────────────────────────────────────
    st.markdown("---")
    st.header("💰 Potential Savings If You Act Now")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🚌 Switch transport mode\n\n**Save up to 600 kg CO₂/year**")
    with col2:
        st.info("☀️ Install solar panels\n\n**Save up to 800 kg CO₂/year**")
    with col3:
        st.info("🥗 Reduce meat consumption\n\n**Save up to 300 kg CO₂/year**")

    st.markdown("---")
    st.caption("🌍 Carbon Lens | AURELION 2026 Smart Cities Hackathon | Data: EPA, World Bank, IPCC")