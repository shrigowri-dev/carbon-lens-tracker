import streamlit as st
import plotly.express as px
import pandas as pd
from model import calculate_carbon

# --- PAGE CONFIG ---
st.set_page_config(page_title="Carbon Lens", page_icon="🌍", layout="centered")

st.title("🌍 Carbon Lens Tracker")
st.subheader("Estimate your personal carbon footprint")

# --- USER INPUTS ---
st.header("🚗 Transport")
car_km = st.slider("Daily km by car", 0, 100, 10)
bike_km = st.slider("Daily km by motorbike", 0, 100, 5)
flight_hours = st.slider("Total flight hours this year", 0, 100, 2)

st.header("⚡ Home Energy")
electricity_kwh = st.slider("Monthly electricity units (kWh)", 0, 500, 100)
lpg_cylinders = st.slider("LPG cylinders per month", 0, 5, 1)

st.header("🍽️ Food")
beef_meals = st.slider("Non-veg meals per week", 0, 21, 5)
veg_meals = st.slider("Vegetarian meals per week", 0, 21, 10)

st.header("🛍️ Lifestyle")
shopping_monthly = st.slider("Monthly shopping spend (₹1000s)", 0, 50, 5)

# --- CALCULATE ---
if st.button("Calculate My Carbon Footprint 🔍"):
    total, breakdown = calculate_carbon(
        car_km, bike_km, flight_hours,
        electricity_kwh, lpg_cylinders,
        beef_meals, veg_meals, shopping_monthly
    )
    
    # --- RESULT ---
    st.success(f"Your annual carbon footprint: **{total} kg CO₂/year**")
    
    # India average is ~1800 kg, global average ~4000 kg
    if total < 1800:
        st.balloons()
        st.info("🟢 You're below India's average! Great job.")
    elif total < 4000:
        st.warning("🟡 You're above India's average but below global average.")
    else:
        st.error("🔴 You're above the global average. Check recommendations!")
    
    # --- PIE CHART ---
    st.subheader("📊 Your Emission Breakdown")
    df = pd.DataFrame({
        "Category": list(breakdown.keys()),
        "CO2 (kg)": list(breakdown.values())
    })
    fig = px.pie(df, values="CO2 (kg)", names="Category", 
                 title="Where your emissions come from",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)
    
    # --- BAR CHART ---
    fig2 = px.bar(df, x="Category", y="CO2 (kg)", 
                  title="Emission by Category",
                  color="CO2 (kg)", color_continuous_scale="reds")
    st.plotly_chart(fig2)
    
    # --- COMPARISON ---
    st.subheader("📈 How you compare")
    compare_df = pd.DataFrame({
        "": ["You", "India Avg", "Global Avg"],
        "CO2 (kg/year)": [total, 1800, 4000]
    })
    fig3 = px.bar(compare_df, x="", y="CO2 (kg/year)", 
                  color="", title="Your footprint vs averages")
    st.plotly_chart(fig3)