import aiohttp
import fatsecret

from config import OPEN_WEATHER_API_KEY, FATSECRET_API_KEY, FATSECRET_SECRET

async def get_temperature(city: str):
    params = {
            'q': city,
            'appid': OPEN_WEATHER_API_KEY,
            'units': 'metric'
        }
    url = "http://api.openweathermap.org/data/2.5/weather"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                cur_weather = data['main']['temp']
                return cur_weather
            elif response.status == 401:
                return None

async def get_food_info(name: str):
    fs = fatsecret.Fatsecret(FATSECRET_API_KEY, FATSECRET_SECRET)

    food_results = fs.foods_search(name)

    if not food_results:
        return None
    
    first_food = food_results[0]
    food_id = first_food["food_id"]

    food_detail = fs.food_get_v2(food_id)
    
    serving = food_detail["servings"]["serving"][0]
    food_name = food_detail["food_name"]
    calories = serving.get("calories")
    metric_unit = serving.get("metric_serving_unit")
    metric_serving_amount = serving.get("metric_serving_amount")

    return food_name, calories, metric_serving_amount, metric_unit