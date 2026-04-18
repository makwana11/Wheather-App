"""
parser.py - Data Parsing & Processing Module
Student 2 Responsibility: Parse raw API data into clean, usable format
"""

from datetime import datetime


def parse_current_weather(data: dict) -> dict:
    """
    Parse raw OpenWeatherMap current weather JSON into a clean dictionary.
    """
    return {
        "city":        data.get("name", "Unknown"),
        "country":     data.get("sys", {}).get("country", ""),
        "temp":        round(data.get("main", {}).get("temp", 0)),
        "feels_like":  round(data.get("main", {}).get("feels_like", 0)),
        "temp_min":    round(data.get("main", {}).get("temp_min", 0)),
        "temp_max":    round(data.get("main", {}).get("temp_max", 0)),
        "humidity":    data.get("main", {}).get("humidity", 0),
        "pressure":    data.get("main", {}).get("pressure", 0),
        "wind_speed":  round(data.get("wind", {}).get("speed", 0) * 3.6, 1),  # m/s → km/h
        "description": data.get("weather", [{}])[0].get("description", "").title(),
        "icon_code":   data.get("weather", [{}])[0].get("icon", "01d"),
        "visibility":  round(data.get("visibility", 0) / 1000, 1),             # m → km
        "sunrise":     _unix_to_time(data.get("sys", {}).get("sunrise", 0)),
        "sunset":      _unix_to_time(data.get("sys", {}).get("sunset", 0)),
        "timestamp":   datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }


def parse_forecast(data: dict) -> list:
    """
    Parse raw forecast JSON into a list of forecast entries.
    Each entry = one 3-hour slot.
    """
    forecasts = []
    for item in data.get("list", []):
        forecasts.append({
            "time":        item.get("dt_txt", "")[-8:-3],   # "HH:MM"
            "date":        item.get("dt_txt", "")[:10],      # "YYYY-MM-DD"
            "temp":        round(item.get("main", {}).get("temp", 0)),
            "description": item.get("weather", [{}])[0].get("description", "").title(),
            "icon_code":   item.get("weather", [{}])[0].get("icon", "01d"),
            "humidity":    item.get("main", {}).get("humidity", 0),
            "wind_speed":  round(item.get("wind", {}).get("speed", 0) * 3.6, 1),
        })
    return forecasts


def get_weather_emoji(description: str) -> str:
    """
    Return a relevant emoji based on weather description.
    """
    desc = description.lower()
    if "clear" in desc:      return "☀️"
    if "cloud" in desc:      return "☁️"
    if "rain" in desc:       return "🌧️"
    if "drizzle" in desc:    return "🌦️"
    if "thunder" in desc:    return "⛈️"
    if "snow" in desc:       return "❄️"
    if "mist" in desc or "fog" in desc or "haze" in desc: return "🌫️"
    if "wind" in desc:       return "💨"
    return "🌡️"


def _unix_to_time(unix_ts: int) -> str:
    """Convert Unix timestamp to readable time string."""
    try:
        return datetime.fromtimestamp(unix_ts).strftime("%I:%M %p")
    except Exception:
        return "N/A"
