TRANSPORT_FACTORS = {
    "car_petrol_km": 0.21,
    "car_diesel_km": 0.17,
    "bike_km": 0.09,
    "auto_km": 0.10,
    "bus_km": 0.04,
    "train_km": 0.01,
    "flight_domestic_hr": 255.0,
    "flight_international_hr": 195.0,
}
ENERGY_FACTORS = {
    "electricity_kwh": 0.82,
    "lpg_cylinder": 63.0,
    "png_scm": 2.04,
    "generator_ltr": 2.68,
}
FOOD_FACTORS = {
    "beef_mutton_meal": 3.6,
    "chicken_meal": 1.5,
    "fish_meal": 1.2,
    "egg_daily": 0.5,
    "veg_meal": 0.5,
    "dairy_litre": 3.2,
    "food_waste_kg": 2.5,
}
WATER_FACTORS = {
    "water_litre": 0.0003,
    "hot_shower_min": 0.08,
    "washing_machine_cycle": 0.6,
}
SHOPPING_FACTORS = {
    "clothing_item": 10.0,
    "electronics_item": 70.0,
    "online_order": 0.5,
}
WASTE_FACTORS = {
    "landfill_waste_kg": 0.5,
    "recycled_waste_kg": -0.1,
    "composting_kg": -0.05,
}

def calculate_carbon(
    car_type, car_km, bike_km, auto_km, bus_km, train_km,
    domestic_flights, domestic_flight_hrs,
    international_flights, international_flight_hrs,
    electricity_kwh, lpg_cylinders, png_scm, generator_ltrs,
    beef_mutton_meals, chicken_meals, fish_meals,
    eggs_per_day, veg_meals, dairy_litres, food_waste_kg,
    water_litres, shower_mins, washing_cycles,
    clothing_items, electronics_items, online_orders,
    landfill_kg, recycled_kg, composting_kg
):
    if car_type == "Diesel":
        car_factor = TRANSPORT_FACTORS["car_diesel_km"]
    elif car_type == "Petrol":
        car_factor = TRANSPORT_FACTORS["car_petrol_km"]
    else:
        car_factor = 0

    transport = (
        (car_km * car_factor * 365) +
        (bike_km * TRANSPORT_FACTORS["bike_km"] * 365) +
        (auto_km * TRANSPORT_FACTORS["auto_km"] * 365) +
        (bus_km * TRANSPORT_FACTORS["bus_km"] * 365) +
        (train_km * TRANSPORT_FACTORS["train_km"] * 365) +
        (domestic_flights * domestic_flight_hrs * TRANSPORT_FACTORS["flight_domestic_hr"]) +
        (international_flights * international_flight_hrs * TRANSPORT_FACTORS["flight_international_hr"])
    )
    energy = (
        (electricity_kwh * ENERGY_FACTORS["electricity_kwh"] * 12) +
        (lpg_cylinders * ENERGY_FACTORS["lpg_cylinder"] * 12) +
        (png_scm * ENERGY_FACTORS["png_scm"] * 12) +
        (generator_ltrs * ENERGY_FACTORS["generator_ltr"] * 12)
    )
    food = (
        (beef_mutton_meals * FOOD_FACTORS["beef_mutton_meal"] * 52) +
        (chicken_meals * FOOD_FACTORS["chicken_meal"] * 52) +
        (fish_meals * FOOD_FACTORS["fish_meal"] * 52) +
        (eggs_per_day * FOOD_FACTORS["egg_daily"] * 365) +
        (veg_meals * FOOD_FACTORS["veg_meal"] * 52) +
        (dairy_litres * FOOD_FACTORS["dairy_litre"] * 52) +
        (food_waste_kg * FOOD_FACTORS["food_waste_kg"] * 52)
    )
    water = (
        (water_litres * WATER_FACTORS["water_litre"] * 365) +
        (shower_mins * WATER_FACTORS["hot_shower_min"] * 365) +
        (washing_cycles * WATER_FACTORS["washing_machine_cycle"] * 52)
    )
    shopping = (
        (clothing_items * SHOPPING_FACTORS["clothing_item"] * 12) +
        (electronics_items * SHOPPING_FACTORS["electronics_item"]) +
        (online_orders * SHOPPING_FACTORS["online_order"] * 52)
    )
    waste = (
        (landfill_kg * WASTE_FACTORS["landfill_waste_kg"] * 52) +
        (recycled_kg * WASTE_FACTORS["recycled_waste_kg"] * 52) +
        (composting_kg * WASTE_FACTORS["composting_kg"] * 52)
    )

    total = transport + energy + food + water + shopping + waste

    breakdown = {
        "🚗 Transport": round(transport, 2),
        "⚡ Energy": round(energy, 2),
        "🍽️ Food": round(food, 2),
        "💧 Water": round(water, 2),
        "🛍️ Shopping": round(shopping, 2),
        "🗑️ Waste": round(waste, 2),
    }
    return round(total, 2), breakdown


def get_recommendations(breakdown, total):
    recommendations = []
    sorted_categories = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
    top_category = sorted_categories[0][0]

    if "Transport" in top_category:
        recommendations.append("🚌 Switch to public transport or carpool 3 days/week — saves up to 600kg CO₂/year")
        recommendations.append("🚲 Use bicycle or walk for trips under 3km")
        recommendations.append("⚡ Consider switching to an electric vehicle")
    if "Energy" in top_category:
        recommendations.append("💡 Switch all bulbs to LED — saves 100kg CO₂/year")
        recommendations.append("☀️ Install rooftop solar panels — reduces electricity emissions by 70%")
        recommendations.append("❄️ Set AC to 24°C instead of 18°C — saves 200kg CO₂/year")
    if "Food" in top_category:
        recommendations.append("🥗 Replace 2 non-veg meals per week with vegetarian — saves 300kg CO₂/year")
        recommendations.append("🛒 Buy local and seasonal vegetables")
        recommendations.append("♻️ Reduce food waste by planning meals — saves 130kg CO₂/year")
    if "Water" in top_category:
        recommendations.append("🚿 Reduce shower time by 2 minutes — saves 60kg CO₂/year")
        recommendations.append("🌧️ Install rainwater harvesting system")
        recommendations.append("🔧 Fix leaking taps — 1 dripping tap wastes 3000 litres/year")
    if "Shopping" in top_category:
        recommendations.append("👗 Buy second-hand clothing — fashion is 10% of global emissions")
        recommendations.append("📦 Consolidate online orders — fewer deliveries = less emissions")
        recommendations.append("🔋 Repair electronics instead of replacing them")
    if "Waste" in top_category:
        recommendations.append("♻️ Segregate waste — wet and dry separately")
        recommendations.append("🌱 Start composting kitchen waste")
        recommendations.append("🛍️ Carry reusable bags — avoid plastic bags")

    recommendations.append("🌳 Plant 2 trees this year — each absorbs ~22kg CO₂/year")
    recommendations.append("📱 Track monthly using Carbon Lens to measure progress!")
    return recommendations