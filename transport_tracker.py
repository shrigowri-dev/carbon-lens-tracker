# transport_tracker.py — Auto Distance Calculator using OpenStreetMap (No API Key!)
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time

# Emission factors (kg CO2 per km)
EMISSION_FACTORS = {
    "Car (Petrol)": 0.21,
    "Car (Diesel)": 0.17,
    "Motorbike": 0.09,
    "Auto Rickshaw": 0.10,
    "Public Bus": 0.04,
    "Train": 0.01,
    "Electric Vehicle": 0.02,
    "Bicycle / Walking": 0.0,
}

def get_coordinates(location_name):
    """Convert location name to coordinates using OpenStreetMap"""
    try:
        geolocator = Nominatim(user_agent="carbon_lens_tracker")
        time.sleep(1)  # Required delay for Nominatim free service
        location = geolocator.geocode(location_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        return None

def calculate_distance(from_location, to_location):
    """Calculate distance between two locations in km"""
    from_coords = get_coordinates(from_location)
    if not from_coords:
        return None, f"Could not find location: {from_location}"
    
    to_coords = get_coordinates(to_location)
    if not to_coords:
        return None, f"Could not find location: {to_location}"
    
    distance = geodesic(from_coords, to_coords).kilometers
    return round(distance, 2), None

def calculate_transport_emission(distance_km, vehicle_type, trips_per_day):
    """Calculate annual emission from transport"""
    factor = EMISSION_FACTORS.get(vehicle_type, 0.21)
    annual_emission = distance_km * factor * trips_per_day * 365
    return round(annual_emission, 2)