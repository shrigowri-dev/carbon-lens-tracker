# model.py — Carbon Lens Tracker
# Emission factors based on EPA, IPCC, and India-specific data

# ─── EMISSION FACTORS (kg CO2 per unit) ───────────────────────────────────────

TRANSPORT_FACTORS = {
    "petrol_car": 0.21,
    "diesel_car": 0.27,
    "motorbike": 0.09,
    "auto_rickshaw": 0.07,
    "bus": 0.03,
    "metro_train": 0.01,
    "bicycle": 0.0,
    "walking": 0.0,
    "flight_domestic": 0.255,
    "flight_international": 0.195,
}

ENERGY_FACTORS = {
    "electricity_kwh": 0.82,
    "lpg_cylinder": 63.0,
    "natural_gas_m3": 2.04,
    "kerosene_litre": 2.54,
    "coal_kg": 2.42,
    "solar_kwh": 0.0,
}

FOOD_FACTORS = {
    "beef_mutton": 3.6,
    "chicken_pork": 1.1,
    "fish_seafood": 1.4,
    "eggs_dairy": 0.8,
    "vegetarian": 0.5,
    "vegan": 0.3,
}

WATER_FACTORS = {
    "water_litre": 0.000298,
    "hot_shower_min": 0.135,
}

WASTE_FACTORS = {
    "waste_kg_week": 0.5,
    "recycling_reduction": 0.3,
}

SHOPPING_FACTORS = {
    "clothing_item": 10.0,
    "electronics_small": 50.0,
    "electronics_large": 300.0,
    "online_order": 0.5,
    "grocery_1000rs": 2.0,
}

INDIA_AVERAGE = 1800
GLOBAL_AVERAGE = 4000
PARIS_TARGET = 1500


def calculate_transport(
    petrol_car_km=0, diesel_car_km=0, motorbike_km=0,
    auto_km=0, bus_km=0, metro_km=0,
    domestic_flight_km=0, international_flight_km=0
):
    daily = (
        petrol_car_km * TRANSPORT_FACTORS["petrol_car"] +
        diesel_car_km * TRANSPORT_FACTORS["diesel_car"] +
        motorbike_km * TRANSPORT_FACTORS["motorbike"] +
        auto_km * TRANSPORT_FACTORS["auto_rickshaw"] +
        bus_km * TRANSPORT_FACTORS["bus"] +
        metro_km * TRANSPORT_FACTORS["metro_train"]
    ) * 365

    flights = (
        domestic_flight_km * TRANSPORT_FACTORS["flight_domestic"] +
        international_flight_km * TRANSPORT_FACTORS["flight_international"]
    )
    return round(daily + flights, 2)


def calculate_energy(
    electricity_kwh=0, lpg_cylinders=0,
    natural_gas_m3=0, kerosene_litre=0,
    coal_kg=0
):
    monthly = (
        electricity_kwh * ENERGY_FACTORS["electricity_kwh"] +
        lpg_cylinders * ENERGY_FACTORS["lpg_cylinder"] +
        natural_gas_m3 * ENERGY_FACTORS["natural_gas_m3"] +
        kerosene_litre * ENERGY_FACTORS["kerosene_litre"] +
        coal_kg * ENERGY_FACTORS["coal_kg"]
    ) * 12
    return round(monthly, 2)


def calculate_food(
    beef_mutton_meals=0, chicken_meals=0, fish_meals=0,
    eggs_dairy_meals=0, vegetarian_meals=0, vegan_meals=0
):
    weekly = (
        beef_mutton_meals * FOOD_FACTORS["beef_mutton"] +
        chicken_meals * FOOD_FACTORS["chicken_pork"] +
        fish_meals * FOOD_FACTORS["fish_seafood"] +
        eggs_dairy_meals * FOOD_FACTORS["eggs_dairy"] +
        vegetarian_meals * FOOD_FACTORS["vegetarian"] +
        vegan_meals * FOOD_FACTORS["vegan"]
    ) * 52
    return round(weekly, 2)


def calculate_water(daily_litres=0, hot_shower_mins=0):
    yearly = (
        daily_litres * WATER_FACTORS["water_litre"] * 365 +
        hot_shower_mins * WATER_FACTORS["hot_shower_min"] * 365
    )
    return round(yearly, 2)


def calculate_waste(waste_kg_week=0, recycling=False):
    yearly = waste_kg_week * WASTE_FACTORS["waste_kg_week"] * 52
    if recycling:
        yearly *= (1 - WASTE_FACTORS["recycling_reduction"])
    return round(yearly, 2)


def calculate_shopping(
    clothing_items=0, small_electronics=0,
    large_electronics=0, online_orders_month=0,
    grocery_1000rs_month=0
):
    yearly = (
        clothing_items * SHOPPING_FACTORS["clothing_item"] +
        small_electronics * SHOPPING_FACTORS["electronics_small"] +
        large_electronics * SHOPPING_FACTORS["electronics_large"] +
        online_orders_month * SHOPPING_FACTORS["online_order"] * 12 +
        grocery_1000rs_month * SHOPPING_FACTORS["grocery_1000rs"] * 12
    )
    return round(yearly, 2)


def get_recommendations(breakdown, total):
    recommendations = []

    if breakdown["Transport"] > 1000:
        recommendations.append("🚌 Switch to public transport or carpool — could save 500+ kg CO₂/year")
    if breakdown["Transport"] > 500:
        recommendations.append("🚲 Use bicycle or walk for short trips under 3 km")
    if breakdown["Transport"] > 2000:
        recommendations.append("✈️ Reduce flights — consider train travel for domestic trips")
    if breakdown["Energy"] > 800:
        recommendations.append("💡 Switch to LED bulbs — saves 150 kg CO₂/year")
    if breakdown["Energy"] > 1000:
        recommendations.append("☀️ Install rooftop solar — reduces electricity emissions by 80%")
    if breakdown["Energy"] > 600:
        recommendations.append("❄️ Set AC to 24°C instead of 18°C — saves 200 kg/year")
    if breakdown["Food"] > 500:
        recommendations.append("🥗 Replace 2 non-veg meals/week with vegetarian — saves 200 kg CO₂/year")
    if breakdown["Food"] > 800:
        recommendations.append("🌱 Try plant-based diet 3 days/week")
    if breakdown["Water"] > 100:
        recommendations.append("🚿 Reduce shower time by 2 minutes — saves 100 kg CO₂/year")
    if breakdown["Waste"] > 50:
        recommendations.append("♻️ Start recycling and composting — reduces waste emissions by 30%")
    if breakdown["Shopping"] > 200:
        recommendations.append("🛍️ Buy less fast fashion — each clothing item = 10 kg CO₂")
    if breakdown["Shopping"] > 300:
        recommendations.append("📦 Consolidate online orders to once a week")
    if total > GLOBAL_AVERAGE:
        recommendations.append("🌳 Plant 10 trees this year to offset ~200 kg CO₂")
    if not recommendations:
        recommendations.append("🎉 You're doing great! Keep maintaining your green lifestyle.")

    return recommendations


def calculate_total(transport, energy, food, water, waste, shopping):
    breakdown = {
        "Transport": transport,
        "Energy": energy,
        "Food": food,
        "Water": water,
        "Waste": waste,
        "Shopping": shopping,
    }
    total = round(sum(breakdown.values()), 2)
    recommendations = get_recommendations(breakdown, total)
    return total, breakdown, recommendations