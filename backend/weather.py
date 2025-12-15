import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

def get_weather(city_name):
    api_key = os.getenv("OPENWEATHER_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
        }
        return weather_info
    else:
        return {"error": "City not found or API request failed"}
