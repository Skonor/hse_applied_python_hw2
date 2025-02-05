import aiohttp

from config import OPEN_WEATHER_API_KEY

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
    pass