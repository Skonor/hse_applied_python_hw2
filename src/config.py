import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Env variable BOT_TOKEN is not set.")


OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

if not OPEN_WEATHER_API_KEY:
    raise ValueError("Env variable OPEN_WEATHER_API_KEY is not set.")

FATSECRET_API_KEY = os.getenv("FATSECRET_API_KEY")

if not OPEN_WEATHER_API_KEY:
    raise ValueError("Env variable FATSECRET_API_KEY is not set.")

FATSECRET_SECRET = os.getenv("FATSECRET_SECRET")

if not FATSECRET_SECRET:
    raise ValueError("Env variable FATSECRET_SECRET is not set.")