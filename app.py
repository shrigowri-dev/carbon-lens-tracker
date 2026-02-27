# app.py — Carbon Lens Tracker (Beautiful Frontend Version)
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from model import calculate_carbon, get_recommendations
from transport_tracker import calculate_distance, calculate_transport_emission, EMISSION_FACTORS

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Carbon Lens Tracker", page_icon="🌍", layout="wide")

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

/* Main background */
.stApp {
    background: linear-gradient(135deg, #020b12 0%, #061a24 40%, #020b12 100%);
    color: #e0f7fa;
    font-family: 'Exo 2', sans-serif;
}

/* Hide default streamlit header */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020b12, #061a24);
    border-right: 1px solid #00e5ff22;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #020b12;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #00e5ff22;
}
.stTabs [data-baseweb="tab"] {
    color: #80cfd8;
    font-family: 'Exo 2', sans-serif;
    font-weight: 600;
    font-size: 14px;
    border-radius: 8px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #00e5ff22, #00ff8822) !important;
    color: #00ff88 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00e5ff, #00ff88);
    color: #020b12;
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: 14px;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px #00ff8844;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #061a2480, #0a2a3880);
    border: 1px solid #00e5ff22;
    border-radius: 12px;
    padding: 16px;
    backdrop-filter: blur(10px);
}
[data-testid="stMetricLabel"] { color: #80cfd8 !important; }
[data-testid="stMetricValue"] {
    color: #00ff88 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 24px !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] { color: #00e5ff; }
.stSlider label,
.stSlider [data-testid="stWidgetLabel"] p {
    color: #00e5ff !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* ALL widget labels globally */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #00e5ff !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* Selectbox label */
.stSelectbox label { color: #00e5ff !important; font-weight: 600 !important; }

/* Number input label */
.stNumberInput label { color: #00e5ff !important; font-weight: 600 !important; }

/* Text input label */
.stTextInput label { color: #00e5ff !important; font-weight: 600 !important; }

/* Slider value number color */
.stSlider div[data-testid="stThumbValue"],
.stSlider div[aria-label] { color: #00ff88 !important; }

/* General label fix — catches everything */
label { color: #00e5ff !important; font-weight: 600 !important; }

/* Text inputs */
.stTextInput>div>div>input {
    background: #0a2a38;
    border: 1px solid #00e5ff66;
    border-radius: 8px;
    color: #00ff88 !important;
    font-family: 'Exo 2', sans-serif;
    font-size: 16px;
    font-weight: 600;
    caret-color: #00ff88;
}
.stTextInput>div>div>input::placeholder {
    color: #4a8a9a !important;
    opacity: 1;
    font-weight: 400;
    font-style: italic;
}
.stTextInput>div>div>input:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 15px #00ff8844 !important;
    background: #0d3344 !important;
    color: #00ff88 !important;
}
/* Text input label */
.stTextInput label {
    color: #00e5ff !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* Selectbox */
.stSelectbox>div>div {
    background: #061a24;
    border: 1px solid #00e5ff44;
    border-radius: 8px;
    color: #e0f7fa;
}

/* Success/Warning/Error */
.stSuccess {
    background: #00ff8811 !important;
    border-left: 4px solid #00ff88 !important;
    border-radius: 8px !important;
}
.stWarning {
    background: #ffaa0011 !important;
    border-left: 4px solid #ffaa00 !important;
    border-radius: 8px !important;
}
.stError {
    background: #ff444411 !important;
    border-left: 4px solid #ff4444 !important;
    border-radius: 8px !important;
}
.stInfo {
    background: #00e5ff11 !important;
    border-left: 4px solid #00e5ff !important;
    border-radius: 8px !important;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00e5ff !important;
}
h4, h5, h6 { color: #80cfd8 !important; }

/* Divider */
hr { border-color: #00e5ff22 !important; }

/* Number input */
.stNumberInput>div>div>input {
    background: #061a24;
    border: 1px solid #00e5ff44;
    border-radius: 8px;
    color: #e0f7fa;
}

/* Cards */
.metric-card {
    background: linear-gradient(135deg, #061a2480, #0a2a3880);
    border: 1px solid #00e5ff22;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
}

/* Plotly chart background */
.js-plotly-plot { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ─── HERO BANNER ──────────────────────────────────────────────────────────────
st.markdown("""
<div style='
    background: linear-gradient(135deg, #020b12, #061a24, #020b12);
    border: 1px solid #00e5ff33;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
'>
    <div style='
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at 20% 50%, #00e5ff08 0%, transparent 60%),
                    radial-gradient(ellipse at 80% 50%, #00ff8808 0%, transparent 60%);
    '></div>
    <h1 style='
        font-family: Orbitron, sans-serif;
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(90deg, #00e5ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: 4px;
    '>🌍 CARBON LENS</h1>
    <p style='color: #80cfd8; font-size: 18px; margin: 10px 0 5px 0; font-family: Exo 2, sans-serif;'>
        AI-Based Personal Carbon Footprint Estimator
    </p>
    <p style='
        color: #00e5ff;
        font-size: 13px;
        letter-spacing: 6px;
        text-transform: uppercase;
        font-family: Orbitron, sans-serif;
        margin: 0;
    '>TRACK • ANALYZE • REDUCE</p>
    <div style='
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 20px;
        flex-wrap: wrap;
    '>
        <span style='background: #00ff8822; border: 1px solid #00ff8844; border-radius: 20px; padding: 6px 16px; color: #00ff88; font-size: 13px; font-family: Exo 2, sans-serif;'>🇮🇳 India Average: 1,800 kg/year</span>
        <span style='background: #00e5ff22; border: 1px solid #00e5ff44; border-radius: 20px; padding: 6px 16px; color: #00e5ff; font-size: 13px; font-family: Exo 2, sans-serif;'>🌍 Global Average: 4,000 kg/year</span>
        <span style='background: #ffaa0022; border: 1px solid #ffaa0044; border-radius: 20px; padding: 6px 16px; color: #ffaa00; font-size: 13px; font-family: Exo 2, sans-serif;'>🎯 Paris Target: 2,300 kg/year</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <p style='font-family: Orbitron, sans-serif; color: #00e5ff; font-size: 18px; font-weight: 700;'>
            🌍 CARBON LENS
        </p>
        <p style='color: #80cfd8; font-size: 12px;'>Smart Cities Hackathon 2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color: #00ff88; font-family: Orbitron, sans-serif; font-size: 13px;'>📊 BENCHMARKS</p>", unsafe_allow_html=True)
    st.metric("🇮🇳 India Average", "1,800 kg/year")
    st.metric("🌍 Global Average", "4,000 kg/year")
    st.metric("🎯 Paris Target", "2,300 kg/year")
    st.markdown("<p style='color: #80cfd850; font-size: 11px;'>Source: World Bank, Global Carbon Project</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color: #00ff88; font-family: Orbitron, sans-serif; font-size: 13px;'>⚡ POWERED BY</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 12px; color: #80cfd8; line-height: 2;'>
        🐍 Python + Streamlit<br>
        🗺️ OpenStreetMap (Geopy)<br>
        📊 Plotly Charts<br>
        📁 EPA + IPCC Data<br>
        ☁️ Streamlit Cloud
    </div>
    """, unsafe_allow_html=True)

# ─── INPUT TABS ───────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚗 Transport", "⚡ Energy", "🍽️ Food", "💧 Water", "🛍️ Shopping", "🗑️ Waste"
])

# ─── TRANSPORT TAB ────────────────────────────────────────────────────────────
with tab1:
    st.markdown("<h3>🚗 Transport Tracker</h3>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background: #00e5ff11; border: 1px solid #00e5ff33; border-radius: 12px; padding: 16px; margin-bottom: 20px;'>
        <p style='color: #00e5ff; font-family: Orbitron, sans-serif; font-size: 13px; margin: 0;'>📍 AUTO DISTANCE CALCULATOR</p>
        <p style='color: #80cfd8; font-size: 13px; margin: 5px 0 0 0;'>Type any two locations in India — we calculate the distance automatically using OpenStreetMap!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        from_location = st.text_input("📍 From Location", placeholder="e.g. Coimbatore Railway Station")
    with col2:
        to_location = st.text_input("📍 To Location", placeholder="e.g. Karunya University")

    col1, col2 = st.columns(2)
    with col1:
        vehicle_type = st.selectbox("🚗 Vehicle Type", list(EMISSION_FACTORS.keys()))
    with col2:
        trips_per_day = st.slider("Daily trips (one way)", 1, 10, 2)

    if "transport_emission" not in st.session_state:
        st.session_state.transport_emission = 0
    if "calculated_distance" not in st.session_state:
        st.session_state.calculated_distance = 0

    if st.button("📍 Calculate Distance & Emission"):
        if from_location and to_location:
            with st.spinner("🗺️ Finding locations on OpenStreetMap..."):
                distance, error = calculate_distance(from_location, to_location)
            if error:
                st.error(f"❌ {error} — Try a more specific location name")
            else:
                emission = calculate_transport_emission(distance, vehicle_type, trips_per_day)
                st.session_state.transport_emission = emission
                st.session_state.calculated_distance = distance
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📏 Distance", f"{distance} km")
                with col2:
                    st.metric("🔄 Daily Trips", f"{trips_per_day}")
                with col3:
                    st.metric("💨 Annual CO₂", f"{emission} kg")
                st.success(f"✅ Transport emission saved: {emission} kg CO₂/year")
        else:
            st.warning("⚠️ Please enter both locations!")

    if st.session_state.transport_emission > 0:
        st.info(f"✅ Saved: **{st.session_state.transport_emission} kg CO₂/year** for **{st.session_state.calculated_distance} km** route using **{vehicle_type}**")

    st.markdown("---")
    st.markdown("<p style='color: #80cfd8; font-family: Orbitron, sans-serif; font-size: 12px;'>✈️ FLIGHTS (MANUAL)</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        domestic_flights = st.number_input("Domestic flights per year", 0, 50, 0)
        domestic_flight_hrs = st.slider("Avg hours per domestic flight", 1, 5, 2)
    with col2:
        international_flights = st.number_input("International flights per year", 0, 20, 0)
        international_flight_hrs = st.slider("Avg hours per international flight", 1, 20, 8)

# ─── ENERGY TAB ───────────────────────────────────────────────────────────────
with tab2:
    st.markdown("<h3>⚡ Home Energy</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #ffaa0011; border: 1px solid #ffaa0033; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #ffaa00; font-size: 13px; margin: 0;'>💡 India's electricity grid emits 0.82 kg CO₂ per unit (kWh) — one of the highest in the world due to coal dependency.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        electricity_kwh = st.slider("⚡ Monthly electricity (kWh)", 0, 1000, 100)
        lpg_cylinders = st.slider("🔥 LPG cylinders per month", 0, 10, 1)
    with col2:
        png_scm = st.slider("🏭 Piped gas per month (SCM)", 0, 50, 0)
        generator_ltrs = st.slider("⛽ Generator diesel per month (L)", 0, 50, 0)

# ─── FOOD TAB ─────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("<h3>🍽️ Food & Diet</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #00ff8811; border: 1px solid #00ff8833; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #00ff88; font-size: 13px; margin: 0;'>🥗 Switching from non-veg to vegetarian meals 2 days/week can save up to 300 kg CO₂/year!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        beef_mutton_meals = st.slider("🐄 Beef/Mutton meals per week", 0, 21, 2)
        chicken_meals = st.slider("🍗 Chicken meals per week", 0, 21, 3)
        fish_meals = st.slider("🐟 Fish meals per week", 0, 21, 2)
        eggs_per_day = st.slider("🥚 Eggs per day", 0, 10, 1)
    with col2:
        veg_meals = st.slider("🥗 Vegetarian meals per week", 0, 21, 10)
        dairy_litres = st.slider("🥛 Dairy per week (litres)", 0, 10, 2)
        food_waste_kg = st.slider("🗑️ Food wasted per week (kg)", 0, 10, 1)

# ─── WATER TAB ────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("<h3>💧 Water Usage</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #00e5ff11; border: 1px solid #00e5ff33; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #00e5ff; font-size: 13px; margin: 0;'>💧 Heating water for showers is one of the biggest hidden sources of home carbon emissions!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        water_litres = st.slider("💧 Daily water usage (litres)", 0, 500, 100)
        shower_mins = st.slider("🚿 Daily hot shower (minutes)", 0, 60, 10)
    with col2:
        washing_cycles = st.slider("👕 Washing machine cycles/week", 0, 14, 3)

# ─── SHOPPING TAB ─────────────────────────────────────────────────────────────
with tab5:
    st.markdown("<h3>🛍️ Shopping & Lifestyle</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #ff444411; border: 1px solid #ff444433; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #ff8888; font-size: 13px; margin: 0;'>👗 The fashion industry accounts for 10% of global carbon emissions. Every clothing item = 10 kg CO₂!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        clothing_items = st.slider("👗 Clothing items per month", 0, 20, 2)
        electronics_items = st.number_input("📱 Electronics per year", 0, 20, 1)
    with col2:
        online_orders = st.slider("📦 Online orders per week", 0, 30, 3)

# ─── WASTE TAB ────────────────────────────────────────────────────────────────
with tab6:
    st.markdown("<h3>🗑️ Waste Management</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #00ff8811; border: 1px solid #00ff8833; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #00ff88; font-size: 13px; margin: 0;'>♻️ Composting and recycling actually REDUCES your carbon footprint — they have negative emission values!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        landfill_kg = st.slider("🗑️ Waste to landfill/week (kg)", 0, 20, 5)
        recycled_kg = st.slider("♻️ Waste recycled/week (kg)", 0, 20, 2)
    with col2:
        composting_kg = st.slider("🌱 Waste composted/week (kg)", 0, 10, 1)

# ─── CALCULATE BUTTON ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    calculate = st.button("🔍 CALCULATE MY CARBON FOOTPRINT", use_container_width=True)

# ─── RESULTS ──────────────────────────────────────────────────────────────────
if calculate:
    transport_override = st.session_state.transport_emission if st.session_state.transport_emission > 0 else None

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

    if transport_override:
        total = total + transport_override
        breakdown["🚗 Transport"] = transport_override

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── RESULT BANNER ────────────────────────────────────────────────────────
    if total < 1800:
        banner_color = "#00ff88"
        banner_bg = "#00ff8811"
        banner_border = "#00ff8844"
        status_text = "🟢 CLIMATE CHAMPION — Below India's Average!"
    elif total < 2300:
        banner_color = "#00e5ff"
        banner_bg = "#00e5ff11"
        banner_border = "#00e5ff44"
        status_text = "🟡 WITHIN PARIS TARGET — Well Done!"
    elif total < 4000:
        banner_color = "#ffaa00"
        banner_bg = "#ffaa0011"
        banner_border = "#ffaa0044"
        status_text = "🟠 ABOVE INDIA AVERAGE — Room to Improve!"
    else:
        banner_color = "#ff4444"
        banner_bg = "#ff444411"
        banner_border = "#ff444444"
        status_text = "🔴 ABOVE GLOBAL AVERAGE — Take Action Now!"

    st.markdown(f"""
    <div style='
        background: {banner_bg};
        border: 2px solid {banner_border};
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-bottom: 30px;
    '>
        <p style='font-family: Orbitron, sans-serif; color: #80cfd8; font-size: 14px; margin: 0; letter-spacing: 3px;'>YOUR ANNUAL CARBON FOOTPRINT</p>
        <h1 style='font-family: Orbitron, sans-serif; color: {banner_color}; font-size: 64px; margin: 10px 0; font-weight: 900;'>{total:,.0f}</h1>
        <p style='color: #80cfd8; font-size: 20px; margin: 0;'>kg CO₂ / year</p>
        <p style='color: {banner_color}; font-family: Orbitron, sans-serif; font-size: 16px; margin-top: 15px;'>{status_text}</p>
    </div>
    """, unsafe_allow_html=True)

    if total < 1800:
        st.balloons()

    # ─── METRIC CARDS ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 Your Footprint", f"{total:,.0f} kg/yr")
    with col2:
        india_diff = round(total - 1800)
        st.metric("vs 🇮🇳 India", f"{abs(india_diff):,} kg",
                  delta=f"{'above' if india_diff > 0 else 'below'}",
                  delta_color="inverse")
    with col3:
        global_diff = round(total - 4000)
        st.metric("vs 🌍 Global", f"{abs(global_diff):,} kg",
                  delta=f"{'above' if global_diff > 0 else 'below'}",
                  delta_color="inverse")
    with col4:
        trees_needed = int(total / 22)
        st.metric("🌳 Trees to Offset", f"{trees_needed}/year")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── PROGRESS BAR ─────────────────────────────────────────────────────────
    st.markdown("<p style='font-family: Orbitron, sans-serif; color: #00e5ff; font-size: 13px; letter-spacing: 2px;'>🌡️ CARBON INTENSITY METER</p>", unsafe_allow_html=True)
    progress_val = min(int((total / 6000) * 100), 100)
    st.progress(progress_val)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<p style='color: #00ff88; font-size: 11px; text-align: left;'>🟢 Low (0-1800)</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='color: #ffaa00; font-size: 11px; text-align: center;'>🟡 Medium (1800-4000)</p>", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='color: #ff4444; font-size: 11px; text-align: right;'>🔴 High (4000+)</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── CHARTS ───────────────────────────────────────────────────────────────
    df = pd.DataFrame({
        "Category": list(breakdown.keys()),
        "CO₂ (kg/year)": list(breakdown.values())
    })

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, values="CO₂ (kg/year)", names="Category",
                     title="📊 Emission Sources Breakdown",
                     color_discrete_sequence=["#00ff88", "#00e5ff", "#ffaa00", "#ff6b6b", "#a855f7", "#f97316"])
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          textfont=dict(color='white', size=12))
        fig.update_layout(
            paper_bgcolor='#061a24',
            plot_bgcolor='#061a24',
            font=dict(color='#80cfd8'),
            title_font=dict(color='#00e5ff', size=14),
            legend=dict(font=dict(color='#80cfd8'))
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(df, x="Category", y="CO₂ (kg/year)",
                      title="📈 Emissions by Category",
                      color="CO₂ (kg/year)",
                      color_continuous_scale=[[0, "#00ff88"], [0.5, "#ffaa00"], [1, "#ff4444"]])
        fig2.update_layout(
            paper_bgcolor='#061a24',
            plot_bgcolor='#061a24',
            font=dict(color='#80cfd8'),
            title_font=dict(color='#00e5ff', size=14),
            xaxis=dict(gridcolor='rgba(255,255,255,0.07)', tickangle=-30),
            yaxis=dict(gridcolor='rgba(255,255,255,0.07)')
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ─── BENCHMARK CHART ──────────────────────────────────────────────────────
    compare_df = pd.DataFrame({
        "": ["🧑 You", "🇮🇳 India Avg", "🌍 Global Avg", "🎯 Paris Target"],
        "CO₂ (kg/year)": [total, 1800, 4000, 2300],
        "Color": ["#00e5ff", "#00ff88", "#ff4444", "#ffaa00"]
    })
    fig3 = go.Figure(go.Bar(
        x=compare_df[""],
        y=compare_df["CO₂ (kg/year)"],
        marker_color=compare_df["Color"],
        text=compare_df["CO₂ (kg/year)"].apply(lambda x: f"{x:,.0f} kg"),
        textposition='outside',
        textfont=dict(color='white')
    ))
    fig3.update_layout(
        title="🌍 Your Footprint vs World Benchmarks",
        paper_bgcolor='#061a24',
        plot_bgcolor='#061a24',
        font=dict(color='#80cfd8'),
        title_font=dict(color='#00e5ff', size=14),
        xaxis=dict(gridcolor='rgba(255,255,255,0.07)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.07)', title="kg CO₂/year")
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ─── RECOMMENDATIONS ──────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: Orbitron, sans-serif; color: #00e5ff; font-size: 16px; letter-spacing: 2px;'>💡 PERSONALIZED RECOMMENDATIONS</p>", unsafe_allow_html=True)
    recommendations = get_recommendations(breakdown, total)
    for rec in recommendations:
        st.success(rec)

    # ─── SAVINGS CARDS ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: Orbitron, sans-serif; color: #00e5ff; font-size: 16px; letter-spacing: 2px;'>💰 POTENTIAL ANNUAL SAVINGS</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background: #00e5ff11; border: 1px solid #00e5ff33; border-radius: 12px; padding: 20px; text-align: center;'>
            <p style='font-size: 32px; margin: 0;'>🚌</p>
            <p style='color: #00e5ff; font-family: Orbitron, sans-serif; font-size: 12px;'>SWITCH TRANSPORT</p>
            <p style='color: #00ff88; font-size: 22px; font-weight: bold; margin: 5px 0;'>-600 kg</p>
            <p style='color: #80cfd8; font-size: 12px;'>CO₂ saved per year</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background: #ffaa0011; border: 1px solid #ffaa0033; border-radius: 12px; padding: 20px; text-align: center;'>
            <p style='font-size: 32px; margin: 0;'>☀️</p>
            <p style='color: #ffaa00; font-family: Orbitron, sans-serif; font-size: 12px;'>INSTALL SOLAR</p>
            <p style='color: #00ff88; font-size: 22px; font-weight: bold; margin: 5px 0;'>-800 kg</p>
            <p style='color: #80cfd8; font-size: 12px;'>CO₂ saved per year</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background: #00ff8811; border: 1px solid #00ff8833; border-radius: 12px; padding: 20px; text-align: center;'>
            <p style='font-size: 32px; margin: 0;'>🥗</p>
            <p style='color: #00ff88; font-family: Orbitron, sans-serif; font-size: 12px;'>REDUCE MEAT</p>
            <p style='color: #00ff88; font-size: 22px; font-weight: bold; margin: 5px 0;'>-300 kg</p>
            <p style='color: #80cfd8; font-size: 12px;'>CO₂ saved per year</p>
        </div>
        """, unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='
    background: linear-gradient(135deg, #020b12, #061a24);
    border: 1px solid #00e5ff22;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
'>
    <p style='font-family: Orbitron, sans-serif; color: #00e5ff; font-size: 16px; margin: 0; letter-spacing: 3px;'>🌍 CARBON LENS TRACKER</p>
    <p style='color: #80cfd8; font-size: 13px; margin: 8px 0 4px 0;'>Built for AURELION 2026 Smart Cities Hackathon</p>
    <p style='color: #80cfd850; font-size: 11px; margin: 0;'>Data Sources: EPA Emission Factors | World Bank | IPCC Guidelines | OpenStreetMap | Central Electricity Authority of India</p>
</div>
""", unsafe_allow_html=True)