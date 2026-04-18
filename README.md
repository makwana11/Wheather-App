# 🌦️ Python Weather App

A command-line Weather App for 4 students — each student owns one module.

---

## 📁 Project Structure

```
weather_app/
│
├── main.py          ← Entry point (run this)
├── config.py        ← ⚠️ Add your API key here
├── api.py           ← Student 1: API integration
├── parser.py        ← Student 2: Data parsing
├── display.py       ← Student 3: Display & formatting
├── history.py       ← Student 4: Search history & validation
├── ui.py            ← Menu & interaction loop
├── requirements.txt ← Dependencies
└── README.md        ← This file
```

---

## ⚙️ Setup Instructions

### Step 1 — Get a Free API Key
1. Go to 👉 https://openweathermap.org/api
2. Click **Sign Up** and create a free account
3. After login, go to **API Keys** tab
4. Copy your default key (or generate a new one)
5. ⏳ Wait ~10 minutes for the key to activate

### Step 2 — Add API Key to config.py
Open `config.py` and replace the placeholder:

```python
# Before
API_KEY = "YOUR_API_KEY_HERE"

# After (example)
API_KEY = "a1b2c3d4e5f6789abc123def456"
```

### Step 3 — Install Python
Make sure Python 3.10 or higher is installed:
```bash
python --version
```
Download from: https://www.python.org/downloads/

### Step 4 — Install Dependencies
Open a terminal in the `weather_app` folder and run:

```bash
pip install -r requirements.txt
```

### Step 5 — Run the App
```bash
python main.py
```

---

## 🖥️ How to Use

| Menu Option | Description |
|---|---|
| 1 | View current weather for any city |
| 2 | View 5-day forecast |
| 3 | View your search history |
| 4 | Clear search history |
| 5 | Re-fetch weather for last searched city |
| 0 | Exit |

---

## 👥 Student Roles

| Student | File | Responsibility |
|---|---|---|
| Student 1 | `api.py` | API calls to OpenWeatherMap |
| Student 2 | `parser.py` | Parse & process API response |
| Student 3 | `display.py` | Format & display output |
| Student 4 | `history.py` | Save history & validate input |

---

## 🔧 Common Errors

| Error | Fix |
|---|---|
| `Invalid API key` | Check config.py — wait 10 min after signup |
| `City not found` | Check spelling or try "London,UK" format |
| `No internet connection` | Check your network |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |

---

## 💡 Possible Enhancements
- Add a Tkinter GUI (Student 3 extension)
- Add unit toggle °C / °F
- Add air quality index (AQI) API
- Deploy as a web app using Flask
