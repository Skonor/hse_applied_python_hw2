import math

CALORIES_PER_MINUTE = {
    "running": 10,          # Running at 8 km/h (5 mph)
    "cycling": 8,           # Cycling at 15-20 km/h (9-12 mph)
    "swimming": 7,          # Moderate swimming
    "jumping_rope": 12,     # Jumping rope at moderate pace
    "weight_lifting": 3,    # General weight lifting
    "yoga": 2,              # Hatha yoga
    "basketball": 8,        # Playing basketball
    "soccer": 9,            # Playing soccer
    "tennis": 7,            # Playing singles tennis
    "hiking": 6,            # Hiking with a light pack
    "dancing": 5,           # Moderate-intensity dancing
    "walking": 4,           # Walking at 5 km/h (3 mph)
    "rowing": 7,            # Rowing at moderate effort
    "boxing": 10,           # Sparring or punching bag
    "skiing": 8,            # Cross-country skiing
    "golf": 4,              # Golf, walking and carrying clubs
    "rock_climbing": 11,    # Rock climbing
    "zumba": 7,             # Zumba fitness class
    "pilates": 3,           # Pilates
    "elliptical": 8,        # Elliptical trainer
}

def calculate_calories_norm(weight: int, height: int, age: int):
    calories_norm = math.ceil(10 * weight + 6.25 * height - 5 * age)

    if calories_norm % 10 != 0:
        calories_norm = calories_norm - calories_norm % 10

    return calories_norm
    
def calculate_water_norm(weight: int, minutes_active: int, is_hot: int):
    return weight * 30 + 500 * (minutes_active // 30) + 500 * is_hot