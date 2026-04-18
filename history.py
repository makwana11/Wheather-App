"""
history.py - Search History & Error Handling Module
Student 3 Responsibility: Save/load search history, manage errors gracefully
"""

import json
import os
from datetime import datetime

HISTORY_FILE = "search_history.json"
MAX_HISTORY  = 10


def save_search(city: str, temp: int, description: str):
    """Save a city search to history file."""
    history = load_history()
    entry = {
        "city":        city,
        "temp":        temp,
        "description": description,
        "searched_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
    }
    history = [h for h in history if h["city"].lower() != city.lower()]
    history.insert(0, entry)
    history = history[:MAX_HISTORY]
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save history: {e}")


def load_history() -> list:
    """Load search history from file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def clear_history():
    """Delete all saved search history."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)


def format_error(error: Exception) -> str:
    """Convert exception into a user-friendly message."""
    msg = str(error)
    if "API Key" in msg:
        return "Invalid API Key!\nGet your free key at:\nopenweathermap.org/api"
    if "not found" in msg:
        return "City not found!\nPlease check the city name and try again."
    if "internet" in msg.lower() or "network" in msg.lower():
        return "No Internet Connection!\nPlease check your network."
    return f"Something went wrong:\n{msg}"
