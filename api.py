"""
api.py - API Integration Module
Student 1 Responsibility: Fetch weather data from OpenWeatherMap API
"""

import urllib.request
import urllib.parse
import json
import os

# ✅ Put your API key here (get free key from https://openweathermap.org/api)
API_KEY = "71f22deb50d955ee051232b28e7275d7"
BASE_URL = "https://api.openweathermap.org/data/2.5"


def fetch_current_weather(city: str) -> dict:
    """
    Fetch current weather data for a given city.
    Returns a dictionary with weather info or raises an error.
    """
    params = urllib.parse.urlencode({
        "q": city,
        "appid": API_KEY,
        "units": "metric"   # Change to 'imperial' for Fahrenheit
    })
    url = f"{BASE_URL}/weather?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise Exception("❌ Invalid API Key. Get a free key at openweathermap.org")
        elif e.code == 404:
            raise Exception(f"❌ City '{city}' not found. Check the spelling.")
        else:
            raise Exception(f"❌ HTTP Error: {e.code}")
    except urllib.error.URLError:
        raise Exception("❌ No internet connection. Please check your network.")


def fetch_forecast(city: str) -> dict:
    """
    Fetch 5-day / 3-hour forecast for a given city.
    """
    params = urllib.parse.urlencode({
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 5   # 5 forecast entries (every 3 hours)
    })
    url = f"{BASE_URL}/forecast?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise Exception("❌ Invalid API Key.")
        elif e.code == 404:
            raise Exception(f"❌ City '{city}' not found.")
        else:
            raise Exception(f"❌ HTTP Error: {e.code}")
    except urllib.error.URLError:
        raise Exception("❌ No internet connection.")
