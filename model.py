import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# --- EMISSION FACTORS (kg of CO2 per unit) ---
# These are standard values from EPA datasets

FACTORS = {
    "car_km": 0.21,          # per km driven by car
    "bike_km": 0.09,         # per km by motorbike
    "flight_hours": 255.0,   # per hour of flying
    "electricity_kwh": 0.82, # per unit of electricity (India grid)
    "lpg_cylinders": 63.0,   # per LPG cylinder
    "beef_meals": 3.6,       # per beef/mutton meal
    "veg_meals": 0.5,        # per vegetarian meal
    "shopping_monthly": 5.5  # per ₹1000 spent on shopping
}

def calculate_carbon(car_km, bike_km, flight_hours, 
                     electricity_kwh, lpg_cylinders,
                     beef_meals, veg_meals, shopping_monthly):
    """
    Takes user inputs and returns total CO2 in kg/year
    """
    
    transport = (car_km * FACTORS["car_km"] * 365) + \
                (bike_km * FACTORS["bike_km"] * 365) + \
                (flight_hours * FACTORS["flight_hours"])
    
    home_energy = (electricity_kwh * FACTORS["electricity_kwh"] * 12) + \
                  (lpg_cylinders * FACTORS["lpg_cylinders"] * 12)
    
    food = (beef_meals * FACTORS["beef_meals"] * 52) + \
           (veg_meals * FACTORS["veg_meals"] * 52)
    
    lifestyle = shopping_monthly * FACTORS["shopping_monthly"] * 12

    total = transport + home_energy + food + lifestyle
    
    breakdown = {
        "Transport": round(transport, 2),
        "Home Energy": round(home_energy, 2),
        "Food": round(food, 2),
        "Lifestyle": round(lifestyle, 2)
    }
    
    return round(total, 2), breakdown