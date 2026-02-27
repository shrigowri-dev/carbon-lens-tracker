# app.py — Carbon Lens Tracker (Beautiful Frontend Version)
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from model import calculate_carbon, get_recommendations
from transport_tracker import calculate_distance, calculate_transport_emission, EMISSION_FACTORS
import requests
import json
from gtts import gTTS
import io
import base64

# ─── FEATHERLESS AI ───────────────────────────────────────────────────────────
def get_ai_recommendations(breakdown, total):
    """Get AI-powered recommendations from Featherless AI"""
    try:
        api_key = st.secrets["FEATHERLESS_API_KEY"]
        
        top_category = max(breakdown, key=breakdown.get)
        
        prompt = f"""You are a carbon footprint expert for India. A user has the following annual carbon emissions:

Total: {total} kg CO2/year
Transport: {breakdown.get('🚗 Transport', 0)} kg
Energy: {breakdown.get('⚡ Energy', 0)} kg
Food: {breakdown.get('🍽️ Food', 0)} kg
Water: {breakdown.get('💧 Water', 0)} kg
Shopping: {breakdown.get('🛍️ Shopping', 0)} kg
Waste: {breakdown.get('🗑️ Waste', 0)} kg

India average: 1800 kg/year. Global average: 4000 kg/year.
Their highest emission category is: {top_category}

Give exactly 5 specific, actionable recommendations for an Indian user to reduce their carbon footprint.
Focus on the highest emission category first.
Each recommendation should be practical, India-specific, and include estimated CO2 savings.
Format each as a single line starting with an emoji."""

        response = requests.post(
            "https://api.featherless.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/Llama-3.3-70B-Instruct",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.7
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_text = result["choices"][0]["message"]["content"]
            lines = [line.strip() for line in ai_text.strip().split("\n") if line.strip()]
            return lines, True
        else:
            return get_recommendations(breakdown, total), False
            
    except Exception as e:
        return get_recommendations(breakdown, total), False

# ─── TAMIL TRANSLATIONS ──────────────────────────────────────────────────────
TAMIL = {
    "title": "கார்பன் லென்ஸ் டிராக்கர்",
    "subtitle": "இந்தியாவிற்கான AI அடிப்படையிலான கார்பன் கால்சுவட்டு மதிப்பீட்டாளர்",
    "calculate": "என் கார்பன் கால்சுவட்டை கணக்கிடு",
    "transport": "போக்குவரத்து",
    "energy": "ஆற்றல்",
    "food": "உணவு",
    "water": "நீர்",
    "shopping": "கடை",
    "waste": "கழிவு",
    "your_footprint": "உங்கள் கார்பன் அளவு",
    "trees": "மரங்கள் நடவேண்டும்",
    "hear_summary": "தமிழில் கேளுங்கள்",
    "india_avg": "இந்தியா சராசரி",
    "global_avg": "உலக சராசரி",
    "paris": "பாரிஸ் இலக்கு",
    "recommendations": "பரிந்துரைகள்",
    "low": "நல்லது! இந்தியா சராசரிக்கு கீழே உள்ளீர்கள்!",
    "medium": "பரவாயில்லை! பாரிஸ் ஒப்பந்த இலக்கில் உள்ளீர்கள்!",
    "high": "கவலை! இந்தியா சராசரிக்கு மேலே உள்ளீர்கள்!",
    "very_high": "அபாயம்! உலக சராசரிக்கு மேலே உள்ளீர்கள்!",
}

# ─── FULL TEXT DICTIONARY ────────────────────────────────────────────────────
TEXT = {
    "en": {
        "page_title": "Carbon Lens Tracker",
        "hero_title": "🌍 CARBON LENS",
        "hero_sub": "AI-Based Personal Carbon Footprint Estimator",
        "hero_tag": "TRACK • ANALYZE • REDUCE",
        "india_avg": "🇮🇳 India Average: 1,800 kg/year",
        "global_avg": "🌍 Global Average: 4,000 kg/year",
        "paris": "🎯 Paris Target: 2,300 kg/year",
        "benchmarks": "📊 BENCHMARKS",
        "india_metric": "1,800 kg/year",
        "global_metric": "4,000 kg/year",
        "paris_metric": "2,300 kg/year",
        "powered": "⚡ POWERED BY",
        "tab1": "🚗 Transport", "tab2": "⚡ Energy", "tab3": "🍽️ Food",
        "tab4": "💧 Water", "tab5": "🛍️ Shopping", "tab6": "🗑️ Waste",
        "transport_title": "🚗 Transport Tracker",
        "from_loc": "📍 From Location", "to_loc": "📍 To Location",
        "vehicle": "🚗 Vehicle Type", "trips": "Daily trips (one way)",
        "calc_btn": "📍 Calculate Distance & Emission",
        "energy_title": "⚡ Home Energy",
        "food_title": "🍽️ Food & Diet",
        "water_title": "💧 Water Usage",
        "shop_title": "🛍️ Shopping & Lifestyle",
        "waste_title": "🗑️ Waste Management",
        "calculate": "🔍 CALCULATE MY CARBON FOOTPRINT",
        "your_fp": "YOUR ANNUAL CARBON FOOTPRINT",
        "kg_year": "kg CO₂ / year",
        "status_low": "🟢 CLIMATE CHAMPION — Below India's Average!",
        "status_med": "🟡 WITHIN PARIS TARGET — Well Done!",
        "status_high": "🟠 ABOVE INDIA AVERAGE — Room to Improve!",
        "status_vhigh": "🔴 ABOVE GLOBAL AVERAGE — Take Action Now!",
        "your_fp_metric": "🌍 Your Footprint",
        "vs_india": "vs 🇮🇳 India",
        "vs_global": "vs 🌍 Global",
        "trees": "🌳 Trees to Offset",
        "meter": "🌡️ CARBON INTENSITY METER",
        "low_label": "🟢 Low (0-1800)",
        "med_label": "🟡 Medium (1800-4000)",
        "high_label": "🔴 High (4000+)",
        "recommendations": "💡 AI-POWERED RECOMMENDATIONS",
        "savings": "💰 POTENTIAL ANNUAL SAVINGS",
        "hear": "🔊 HEAR YOUR CARBON SUMMARY",
        "voice_ok": "✅ Voice summary generated!",
        "footer1": "🌍 CARBON LENS TRACKER",
        "footer2": "Built for AURELION 2026 Smart Cities Hackathon",
        "above": "above", "below": "below",
        "flights": T["flights"],
        "domestic_flights": T["domestic_flights"],
        "domestic_hrs": T["domestic_hrs"],
        "intl_flights": T["intl_flights"],
        "intl_hrs": T["intl_hrs"],
        "electricity": T["electricity"],
        "lpg": T["lpg"],
        "png": T["png"],
        "generator": T["generator"],
        "beef": T["beef"],
        "chicken": T["chicken"],
        "fish": T["fish"],
        "eggs": T["eggs"],
        "veg": T["veg"],
        "dairy": T["dairy"],
        "food_waste": T["food_waste"],
        "water": T["water"],
        "shower": T["shower"],
        "washing": T["washing"],
        "clothing": T["clothing"],
        "electronics": T["electronics"],
        "online": T["online"],
        "landfill": T["landfill"],
        "recycled": T["recycled"],
        "composting": T["composting"],
        "source": "Source: World Bank, Global Carbon Project",
        "powered_by": "⚡ POWERED BY",
        "featherless_badge": T["featherless_badge"],
        "ai_proof": T["ai_proof"],
        "switch_transport": T["switch_transport"],
        "install_solar": T["install_solar"],
        "reduce_meat": T["reduce_meat"],
        "co2_saved": T["co2_saved"],
    },
    "ta": {
        "page_title": "கார்பன் லென்ஸ் டிராக்கர்",
        "hero_title": "🌍 கார்பன் லென்ஸ்",
        "hero_sub": "இந்தியாவிற்கான AI கார்பன் கால்சுவட்டு கணக்கீட்டாளர்",
        "hero_tag": "கண்காணி • பகுப்பாய்வு • குறை",
        "india_avg": "🇮🇳 இந்தியா சராசரி: 1,800 கி.கி/ஆண்டு",
        "global_avg": "🌍 உலக சராசரி: 4,000 கி.கி/ஆண்டு",
        "paris": "🎯 பாரிஸ் இலக்கு: 2,300 கி.கி/ஆண்டு",
        "benchmarks": "📊 அளவீடுகள்",
        "india_metric": "1,800 கி.கி/ஆண்டு",
        "global_metric": "4,000 கி.கி/ஆண்டு",
        "paris_metric": "2,300 கி.கி/ஆண்டு",
        "powered": "⚡ இயக்கப்படுகிறது",
        "tab1": "🚗 போக்குவரத்து", "tab2": "⚡ ஆற்றல்", "tab3": "🍽️ உணவு",
        "tab4": "💧 நீர்", "tab5": "🛍️ கடை", "tab6": "🗑️ கழிவு",
        "transport_title": "🚗 போக்குவரத்து கண்காணிப்பு",
        "from_loc": "📍 தொடக்க இடம்", "to_loc": "📍 இலக்கு இடம்",
        "vehicle": "🚗 வாகன வகை", "trips": "தினசரி பயணங்கள்",
        "calc_btn": "📍 தூரம் மற்றும் உமிழ்வு கணக்கிடு",
        "energy_title": "⚡ வீட்டு ஆற்றல்",
        "food_title": "🍽️ உணவு & உணவுமுறை",
        "water_title": "💧 நீர் பயன்பாடு",
        "shop_title": "🛍️ கடை & வாழ்க்கை முறை",
        "waste_title": "🗑️ கழிவு மேலாண்மை",
        "calculate": "🔍 என் கார்பன் கால்சுவட்டை கணக்கிடு",
        "your_fp": "உங்கள் வருடாந்திர கார்பன் கால்சுவடு",
        "kg_year": "கி.கி CO₂ / ஆண்டு",
        "status_low": "🟢 சிறந்தது! இந்தியா சராசரிக்கு கீழே உள்ளீர்கள்!",
        "status_med": "🟡 நல்லது! பாரிஸ் ஒப்பந்த இலக்கில் உள்ளீர்கள்!",
        "status_high": "🟠 கவலை! இந்தியா சராசரிக்கு மேலே உள்ளீர்கள்!",
        "status_vhigh": "🔴 அபாயம்! உலக சராசரிக்கு மேலே உள்ளீர்கள்!",
        "your_fp_metric": "🌍 உங்கள் கால்சுவடு",
        "vs_india": "vs 🇮🇳 இந்தியா",
        "vs_global": "vs 🌍 உலகம்",
        "trees": "🌳 நடவேண்டிய மரங்கள்",
        "meter": "🌡️ கார்பன் தீவிரம்",
        "low_label": "🟢 குறைவு (0-1800)",
        "med_label": "🟡 நடுத்தரம் (1800-4000)",
        "high_label": "🔴 அதிகம் (4000+)",
        "recommendations": "💡 AI பரிந்துரைகள்",
        "savings": "💰 சாத்தியமான சேமிப்பு",
        "hear": "🔊 தமிழில் கேளுங்கள்",
        "voice_ok": "✅ குரல் வெற்றிகரமாக உருவாக்கப்பட்டது!",
        "footer1": "🌍 கார்பன் லென்ஸ் டிராக்கர்",
        "footer2": "AURELION 2026 ஸ்மார்ட் சிட்டீஸ் ஹேக்கத்தானுக்காக உருவாக்கப்பட்டது",
        "above": "மேலே", "below": "கீழே",
        "flights": "✈️ விமான பயணங்கள் (கைமுறை)",
        "domestic_flights": "✈️ உள்நாட்டு விமானங்கள் (ஆண்டுக்கு)",
        "domestic_hrs": "⏱️ சராசரி மணிநேரம் (உள்நாட்டு)",
        "intl_flights": "🌍 சர்வதேச விமானங்கள் (ஆண்டுக்கு)",
        "intl_hrs": "⏱️ சராசரி மணிநேரம் (சர்வதேச)",
        "electricity": "⚡ மாதாந்திர மின்சாரம் (kWh)",
        "lpg": "🔥 LPG சிலிண்டர்கள் (மாதம்)",
        "png": "🔥 குழாய் வாயு (SCM/மாதம்)",
        "generator": "⛽ ஜெனரேட்டர் டீசல் (லிட்டர்/மாதம்)",
        "beef": "🐄 மாட்டிறைச்சி உணவுகள் (வாரம்)",
        "chicken": "🍗 கோழி உணவுகள் (வாரம்)",
        "fish": "🐟 மீன் உணவுகள் (வாரம்)",
        "eggs": "🥚 முட்டைகள் (நாள்)",
        "veg": "🥗 சைவ உணவுகள் (வாரம்)",
        "dairy": "🥛 பால் பொருட்கள் (லிட்டர்/வாரம்)",
        "food_waste": "🗑️ உணவு கழிவு (கிலோ/வாரம்)",
        "water": "💧 தினசரி நீர் பயன்பாடு (லிட்டர்)",
        "shower": "🚿 சூடான குளியல் (நிமிடங்கள்/நாள்)",
        "washing": "👕 வாஷிங் மெஷின் (சுழற்சி/வாரம்)",
        "clothing": "👗 ஆடைகள் (மாதம்)",
        "electronics": "📱 மின்னணு சாதனங்கள் (ஆண்டு)",
        "online": "📦 ஆன்லைன் ஆர்டர்கள் (வாரம்)",
        "landfill": "🗑️ கழிவு தொட்டி (கிலோ/வாரம்)",
        "recycled": "♻️ மறுசுழற்சி (கிலோ/வாரம்)",
        "composting": "🌱 உரமாக்கல் (கிலோ/வாரம்)",
        "source": "ஆதாரம்: உலக வங்கி, உலகளாவிய கார்பன் திட்டம்",
        "powered_by": "⚡ இயக்கப்படுகிறது",
        "featherless_badge": "⚡ FEATHERLESS AI — Llama 3.3 70B மூலம் இயக்கப்படுகிறது",
        "ai_proof": "📊 FEATHERLESS AI க்கு அனுப்பப்பட்ட தரவு:",
        "switch_transport": "போக்குவரத்து மாற்றுங்கள்",
        "install_solar": "சோலார் பேனல் பொருத்துங்கள்",
        "reduce_meat": "இறைச்சி குறையுங்கள்",
        "co2_saved": "ஆண்டுக்கு CO₂ சேமிப்பு",
    }
}

# ─── GTTS VOICE (FREE - NO API KEY) ─────────────────────────────────────────
def generate_voice_summary(total, breakdown, lang="en"):
    """Generate voice summary using gTTS — free, no API key needed"""
    try:
        top_category = max(breakdown, key=breakdown.get)
        top_value = breakdown[top_category]
        top_name = top_category.replace("🚗","").replace("⚡","").replace("🍽️","").replace("💧","").replace("🛍️","").replace("🗑️","").strip()

        if lang == "ta":
            text = f"""உங்கள் வருடாந்திர கார்பன் கால்சுவடு {int(total)} கிலோகிராம் CO2 ஆகும்.
            உங்கள் மிக அதிக உமிழ்வு பிரிவு {top_name} ஆகும், இது {int(top_value)} கிலோகிராம்.
            உங்கள் கார்பன் கால்சுவட்டை சமன் செய்ய ஆண்டுக்கு {int(total/22)} மரங்கள் நடவேண்டும்.
            கீழே உள்ள பரிந்துரைகளை பின்பற்றுங்கள்!"""
        else:
            text = f"""Your annual carbon footprint is {int(total)} kilograms of CO2 per year.
            Your highest emission source is {top_name} at {int(top_value)} kilograms per year.
            To offset your footprint, you need to plant {int(total/22)} trees every year.
            Check the recommendations below to reduce your carbon footprint!"""

        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.read(), True
    except Exception as e:
        return str(e), False

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Carbon Lens Tracker", page_icon="🌍", layout="wide")

# ─── LANGUAGE SELECTOR ───────────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# Define T early so it's available everywhere
T = TEXT[st.session_state.get("lang", "en")]

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

# ─── LANGUAGE SHORTCUT ───────────────────────────────────────────────────────
T = TEXT[st.session_state.get("lang", "en")]

# ─── HERO BANNER ──────────────────────────────────────────────────────────────
st.markdown(f"""
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
    '>{T["hero_title"]}</h1>
    <p style='color: #80cfd8; font-size: 18px; margin: 10px 0 5px 0; font-family: Exo 2, sans-serif;'>
        {T["hero_sub"]}
    </p>
    <p style='
        color: #00e5ff;
        font-size: 13px;
        letter-spacing: 6px;
        text-transform: uppercase;
        font-family: Orbitron, sans-serif;
        margin: 0;
    '>{T["hero_tag"]}</p>
    <div style='
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 20px;
        flex-wrap: wrap;
    '>
        <span style='background: #00ff8822; border: 1px solid #00ff8844; border-radius: 20px; padding: 6px 16px; color: #00ff88; font-size: 13px; font-family: Exo 2, sans-serif;'>{T["india_avg"]}</span>
        <span style='background: #00e5ff22; border: 1px solid #00e5ff44; border-radius: 20px; padding: 6px 16px; color: #00e5ff; font-size: 13px; font-family: Exo 2, sans-serif;'>{T["global_avg"]}</span>
        <span style='background: #ffaa0022; border: 1px solid #ffaa0044; border-radius: 20px; padding: 6px 16px; color: #ffaa00; font-size: 13px; font-family: Exo 2, sans-serif;'>{T["paris"]}</span>
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
    st.markdown("<p style='color: #00ff88; font-family: Orbitron, sans-serif; font-size: 13px;'>🌐 LANGUAGE / மொழி</p>", unsafe_allow_html=True)
    lang_choice = st.radio("", ["🇬🇧 English", "🇮🇳 தமிழ்"], horizontal=True, label_visibility="collapsed")
    st.session_state.lang = "ta" if "தமிழ்" in lang_choice else "en"
    T = TEXT[st.session_state.lang]
    st.markdown("---")
    st.markdown(f"<p style='color: #00ff88; font-family: Orbitron, sans-serif; font-size: 13px;'>{T['benchmarks']}</p>", unsafe_allow_html=True)
    st.metric(T["india_avg"], T["india_metric"])
    st.metric(T["global_avg"], T["global_metric"])
    st.metric(T["paris"], T["paris_metric"])
    st.markdown(f"<p style='color: #80cfd850; font-size: 11px;'>{T['source']}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<p style='color: #00ff88; font-family: Orbitron, sans-serif; font-size: 13px;'>{T['powered_by']}</p>", unsafe_allow_html=True)
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
    T["tab1"], T["tab2"], T["tab3"], T["tab4"], T["tab5"], T["tab6"]
])

# ─── TRANSPORT TAB ────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f"<h3>{T['transport_title']}</h3>", unsafe_allow_html=True)



    # Use session state to persist text input values
    if "from_location" not in st.session_state:
        st.session_state.from_location = ""
    if "to_location" not in st.session_state:
        st.session_state.to_location = ""
    if "transport_emission" not in st.session_state:
        st.session_state.transport_emission = 0
    if "calculated_distance" not in st.session_state:
        st.session_state.calculated_distance = 0

    col1, col2 = st.columns(2)
    with col1:
        from_location = st.text_input(T["from_loc"], placeholder="e.g. Coimbatore Railway Station", key="from_loc")
    with col2:
        to_location = st.text_input(T["to_loc"], placeholder="e.g. Karunya University", key="to_loc")

    col1, col2 = st.columns(2)
    with col1:
        vehicle_type = st.selectbox(T["vehicle"], list(EMISSION_FACTORS.keys()))
    with col2:
        trips_per_day = st.slider(T["trips"], 1, 10, 2)

    if st.button(T["calc_btn"]):
        from_val = st.session_state.get("from_loc", "")
        to_val = st.session_state.get("to_loc", "")
        if from_val and to_val:
            from_location = from_val
            to_location = to_val
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
    st.markdown(f"<p style='color: #80cfd8; font-family: Orbitron, sans-serif; font-size: 12px;'>{T['flights']}</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        domestic_flights = st.number_input("Domestic flights per year", 0, 50, 0)
        domestic_flight_hrs = st.slider("Avg hours per domestic flight", 1, 5, 2)
    with col2:
        international_flights = st.number_input("International flights per year", 0, 20, 0)
        international_flight_hrs = st.slider("Avg hours per international flight", 1, 20, 8)

# ─── ENERGY TAB ───────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f"<h3>{T['energy_title']}</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #ffaa0011; border: 1px solid #ffaa0033; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #ffaa00; font-size: 13px; margin: 0;'>💡 India's electricity grid emits 0.82 kg CO₂ per unit (kWh) — one of the highest in the world due to coal dependency.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        electricity_kwh = st.slider(T["electricity"], 0, 1000, 0)
        lpg_cylinders = st.slider(T["lpg"], 0, 10, 0)
    with col2:
        png_scm = st.slider("🏭 Piped gas per month (SCM)", 0, 50, 0)
        generator_ltrs = st.slider("⛽ Generator diesel per month (L)", 0, 50, 0)

# ─── FOOD TAB ─────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"<h3>{T['food_title']}</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #00ff8811; border: 1px solid #00ff8833; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #00ff88; font-size: 13px; margin: 0;'>🥗 Switching from non-veg to vegetarian meals 2 days/week can save up to 300 kg CO₂/year!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        beef_mutton_meals = st.slider(T["beef"], 0, 21, 0)
        chicken_meals = st.slider(T["chicken"], 0, 21, 0)
        fish_meals = st.slider(T["fish"], 0, 21, 0)
        eggs_per_day = st.slider(T["eggs"], 0, 10, 0)
    with col2:
        veg_meals = st.slider(T["veg"], 0, 21, 0)
        dairy_litres = st.slider(T["dairy"], 0, 10, 0)
        food_waste_kg = st.slider(T["food_waste"], 0, 10, 0)

# ─── WATER TAB ────────────────────────────────────────────────────────────────
with tab4:
    st.markdown(f"<h3>{T['water_title']}</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #00e5ff11; border: 1px solid #00e5ff33; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #00e5ff; font-size: 13px; margin: 0;'>💧 Heating water for showers is one of the biggest hidden sources of home carbon emissions!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        water_litres = st.slider(T["water"], 0, 500, 0)
        shower_mins = st.slider(T["shower"], 0, 60, 0)
    with col2:
        washing_cycles = st.slider(T["washing"], 0, 14, 0)

# ─── SHOPPING TAB ─────────────────────────────────────────────────────────────
with tab5:
    st.markdown(f"<h3>{T['shop_title']}</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #ff444411; border: 1px solid #ff444433; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #ff8888; font-size: 13px; margin: 0;'>👗 The fashion industry accounts for 10% of global carbon emissions. Every clothing item = 10 kg CO₂!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        clothing_items = st.slider(T["clothing"], 0, 20, 0)
        electronics_items = st.number_input(T["electronics"], 0, 20, 0)
    with col2:
        online_orders = st.slider(T["online"], 0, 30, 0)

# ─── WASTE TAB ────────────────────────────────────────────────────────────────
with tab6:
    st.markdown(f"<h3>{T['waste_title']}</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: #00ff8811; border: 1px solid #00ff8833; border-radius: 12px; padding: 12px; margin-bottom: 20px;'>
        <p style='color: #00ff88; font-size: 13px; margin: 0;'>♻️ Composting and recycling actually REDUCES your carbon footprint — they have negative emission values!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        landfill_kg = st.slider(T["landfill"], 0, 20, 0)
        recycled_kg = st.slider(T["recycled"], 0, 20, 0)
    with col2:
        composting_kg = st.slider(T["composting"], 0, 10, 0)

# ─── CALCULATE BUTTON ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    calculate = st.button(T["calculate"], use_container_width=True)

# ─── RESULTS ──────────────────────────────────────────────────────────────────
if calculate:
    transport_override = st.session_state.transport_emission if st.session_state.transport_emission > 0 else None

    # Pass car_km=0 always — transport handled separately to avoid double counting
    total, breakdown = calculate_carbon(
        "None", 0, 0, 0, 0, 0,
        domestic_flights, domestic_flight_hrs,
        international_flights, international_flight_hrs,
        electricity_kwh, lpg_cylinders, png_scm, generator_ltrs,
        beef_mutton_meals, chicken_meals, fish_meals,
        eggs_per_day, veg_meals, dairy_litres, food_waste_kg,
        water_litres, shower_mins, washing_cycles,
        clothing_items, electronics_items, online_orders,
        landfill_kg, recycled_kg, composting_kg
    )

    # Add transport only from auto-calculator — no double counting
    if transport_override:
        total = round(total + transport_override, 2)
        breakdown["🚗 Transport"] = transport_override
    else:
        breakdown["🚗 Transport"] = 0

    # Save results in session state so voice button works
    st.session_state.results_total = total
    st.session_state.results_breakdown = breakdown
    st.session_state.results_ready = True

# Show results if calculated
if "results_ready" in st.session_state and st.session_state.results_ready:
    total = st.session_state.results_total
    breakdown = st.session_state.results_breakdown

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── RESULT BANNER ────────────────────────────────────────────────────────
    if total < 1800:
        banner_color = "#00ff88"
        banner_bg = "#00ff8811"
        banner_border = "#00ff8844"
        status_text = T['status_low']
    elif total < 2300:
        banner_color = "#00e5ff"
        banner_bg = "#00e5ff11"
        banner_border = "#00e5ff44"
        status_text = T['status_med']
    elif total < 4000:
        banner_color = "#ffaa00"
        banner_bg = "#ffaa0011"
        banner_border = "#ffaa0044"
        status_text = T['status_high']
    else:
        banner_color = "#ff4444"
        banner_bg = "#ff444411"
        banner_border = "#ff444444"
        status_text = T['status_vhigh']

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

    # ─── VOICE SUMMARY ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        voice_lang = st.session_state.get("lang", "en")
        btn_label = T["hear"]
        if st.button(btn_label, use_container_width=True):
            spinner_msg = "🎙️ தமிழில் குரல் உருவாக்குகிறது..." if voice_lang == "ta" else "🎙️ Generating voice summary..."
            with st.spinner(spinner_msg):
                audio_data, success = generate_voice_summary(total, breakdown, voice_lang)
            if success and audio_data:
                st.audio(audio_data, format="audio/mpeg")
                st.success(T["voice_ok"])
            else:
                st.error(f"❌ Error: {audio_data}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── METRIC CARDS ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(T["your_fp_metric"], f"{total:,.0f} kg/yr")
    with col2:
        india_diff = round(total - 1800)
        st.metric(T["vs_india"], f"{abs(india_diff):,} kg",
                  delta=f"{T['above'] if india_diff > 0 else T['below']}",
                  delta_color="inverse")
    with col3:
        global_diff = round(total - 4000)
        st.metric(T["vs_global"], f"{abs(global_diff):,} kg",
                  delta=f"{T['above'] if global_diff > 0 else T['below']}",
                  delta_color="inverse")
    with col4:
        trees_needed = int(total / 22)
        st.metric(T["trees"], f"{trees_needed}/year")

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
    st.markdown("<p style='font-family: Orbitron, sans-serif; color: #00e5ff; font-size: 16px; letter-spacing: 2px;'>💡 AI-POWERED RECOMMENDATIONS</p>", unsafe_allow_html=True)
    
    # Featherless AI badge
    st.markdown("""
    <div style='background: linear-gradient(90deg, #ffaa0022, #00e5ff22); border: 1px solid #ffaa0044;
    border-radius: 8px; padding: 8px 16px; display: inline-block; margin-bottom: 10px;'>
        <span style='color: #ffaa00; font-size: 12px; font-family: Orbitron, sans-serif;'>
        ⚡ POWERED BY FEATHERLESS AI — Llama 3.3 70B
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("🤖 Getting AI-powered recommendations from Featherless AI..."):
        recommendations, is_ai = get_ai_recommendations(breakdown, total)
    
    if is_ai:
        st.success("✅ AI recommendations generated by Featherless AI — Llama 3.3 70B!")
        
        # Show proof of API call
        with st.expander("🔍 View Featherless AI API Call Proof (for judges)"):
            st.markdown("""
            <div style='background: #020b12; border: 1px solid #00ff8844; border-radius: 8px; padding: 16px; font-family: monospace;'>
            <p style='color: #00e5ff; font-size: 12px; margin: 0 0 8px 0;'>📡 API REQUEST SENT TO:</p>
            <p style='color: #00ff88; font-size: 12px; margin: 0 0 12px 0;'>https://api.featherless.ai/v1/chat/completions</p>
            <p style='color: #00e5ff; font-size: 12px; margin: 0 0 8px 0;'>🤖 MODEL USED:</p>
            <p style='color: #00ff88; font-size: 12px; margin: 0 0 12px 0;'>meta-llama/Llama-3.3-70B-Instruct</p>
            <p style='color: #00e5ff; font-size: 12px; margin: 0 0 8px 0;'>📤 DATA SENT:</p>
            <p style='color: #ffaa00; font-size: 12px; margin: 0 0 12px 0;'>User emission breakdown with all 6 categories</p>
            <p style='color: #00e5ff; font-size: 12px; margin: 0 0 8px 0;'>📥 RESPONSE STATUS:</p>
            <p style='color: #00ff88; font-size: 12px; margin: 0;'>✅ 200 OK — AI inference successful</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show actual data sent
            st.markdown("<p style='color: #00e5ff; font-size: 12px; margin-top: 12px;'>📊 ACTUAL EMISSION DATA SENT TO FEATHERLESS AI:</p>", unsafe_allow_html=True)
            for cat, val in breakdown.items():
                st.markdown(f"<p style='color: #80cfd8; font-size: 12px; margin: 2px 0;'>→ {cat}: <span style='color: #00ff88;'>{val:.2f} kg CO₂/year</span></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #ffaa00; font-size: 13px; margin-top: 8px;'>→ Total sent: <b>{total:.2f} kg CO₂/year</b></p>", unsafe_allow_html=True)
    else:
        st.info("ℹ️ Showing smart recommendations")
    
    for rec in recommendations:
        st.success(rec)

    # ─── SAVINGS CARDS ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: Orbitron, sans-serif; color: #00e5ff; font-size: 16px; letter-spacing: 2px;'>💰 POTENTIAL ANNUAL SAVINGS</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    # Calculate actual savings based on user data
    transport_saving = round(breakdown.get("🚗 Transport", 0) * 0.30)  # 30% saving by switching transport
    energy_saving = round(breakdown.get("⚡ Energy", 0) * 0.50)        # 50% saving by solar
    food_saving = round(breakdown.get("🍽️ Food", 0) * 0.40)           # 40% saving by reducing meat

    s1 = (T["switch_transport"], "போக்குவரத்து மாற்றுங்கள்")
    s2 = (T["install_solar"], "சோலார் பேனல் பொருத்துங்கள்")
    s3 = (T["reduce_meat"], "இறைச்சி குறையுங்கள்")
    s4 = (T["co2_saved"], "ஆண்டுக்கு CO₂ சேமிப்பு")
    lang_now = st.session_state.get("lang", "en")
    idx = 1 if lang_now == "ta" else 0

    with col1:
        st.markdown(f"""
        <div style='background: #00e5ff11; border: 1px solid #00e5ff33; border-radius: 12px; padding: 20px; text-align: center;'>
            <p style='font-size: 32px; margin: 0;'>🚌</p>
            <p style='color: #00e5ff; font-family: Orbitron, sans-serif; font-size: 12px;'>{s1[idx]}</p>
            <p style='color: #00ff88; font-size: 22px; font-weight: bold; margin: 5px 0;'>-{transport_saving} kg</p>
            <p style='color: #80cfd8; font-size: 12px;'>{s4[idx]}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background: #ffaa0011; border: 1px solid #ffaa0033; border-radius: 12px; padding: 20px; text-align: center;'>
            <p style='font-size: 32px; margin: 0;'>☀️</p>
            <p style='color: #ffaa00; font-family: Orbitron, sans-serif; font-size: 12px;'>{s2[idx]}</p>
            <p style='color: #00ff88; font-size: 22px; font-weight: bold; margin: 5px 0;'>-{energy_saving} kg</p>
            <p style='color: #80cfd8; font-size: 12px;'>{s4[idx]}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style='background: #00ff8811; border: 1px solid #00ff8833; border-radius: 12px; padding: 20px; text-align: center;'>
            <p style='font-size: 32px; margin: 0;'>🥗</p>
            <p style='color: #00ff88; font-family: Orbitron, sans-serif; font-size: 12px;'>{s3[idx]}</p>
            <p style='color: #00ff88; font-size: 22px; font-weight: bold; margin: 5px 0;'>-{food_saving} kg</p>
            <p style='color: #80cfd8; font-size: 12px;'>{s4[idx]}</p>
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