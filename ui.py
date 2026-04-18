"""
ui.py - User Interface Module (Tkinter)
Student 4 Responsibility: Build the full GUI using tkinter
"""

import tkinter as tk
from tkinter import messagebox
import threading

from api import fetch_current_weather, fetch_forecast
from parser import parse_current_weather, parse_forecast, get_weather_emoji
from history import save_search, load_history, clear_history, format_error

BG_DARK    = "#0f172a"
BG_CARD    = "#1e293b"
BG_INPUT   = "#334155"
ACCENT     = "#38bdf8"
TEXT_WHITE = "#f1f5f9"
TEXT_GRAY  = "#94a3b8"
TEXT_RED   = "#f87171"


class WeatherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("700x750")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", padx=20, pady=(20, 5))
        tk.Label(header, text="Weather App",
                 font=("Segoe UI", 22, "bold"),
                 bg=BG_DARK, fg=ACCENT).pack(side="left")
        tk.Button(header, text="History",
                  font=("Segoe UI", 10),
                  bg=BG_CARD, fg=TEXT_WHITE,
                  bd=0, padx=10, pady=5, cursor="hand2",
                  command=self._show_history).pack(side="right")

        # Search Bar
        search_frame = tk.Frame(self.root, bg=BG_DARK)
        search_frame.pack(fill="x", padx=20, pady=10)
        self.city_var = tk.StringVar()
        self.entry = tk.Entry(search_frame, textvariable=self.city_var,
                              font=("Segoe UI", 14),
                              bg=BG_INPUT, fg=TEXT_WHITE,
                              insertbackground=TEXT_WHITE, bd=0, relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, ipadx=10)
        self.entry.insert(0, "Enter city name...")
        self.entry.bind("<FocusIn>",  self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._restore_placeholder)
        self.entry.bind("<Return>",   lambda e: self._search())
        self.search_btn = tk.Button(search_frame, text="Search",
                                    font=("Segoe UI", 12, "bold"),
                                    bg=ACCENT, fg=BG_DARK,
                                    bd=0, padx=15, pady=10, cursor="hand2",
                                    command=self._search)
        self.search_btn.pack(side="right", padx=(8, 0))

        # Status
        self.status_var = tk.StringVar(value="Search for a city to see weather")
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Segoe UI", 10),
                 bg=BG_DARK, fg=TEXT_GRAY).pack()

        # Main Card
        self.card = tk.Frame(self.root, bg=BG_CARD)
        self.card.pack(fill="x", padx=20, pady=10)
        self.emoji_lbl   = tk.Label(self.card, text="", font=("Segoe UI", 50), bg=BG_CARD, fg=TEXT_WHITE)
        self.temp_lbl    = tk.Label(self.card, text="", font=("Segoe UI", 48, "bold"), bg=BG_CARD, fg=TEXT_WHITE)
        self.desc_lbl    = tk.Label(self.card, text="", font=("Segoe UI", 14), bg=BG_CARD, fg=TEXT_GRAY)
        self.city_lbl    = tk.Label(self.card, text="", font=("Segoe UI", 18, "bold"), bg=BG_CARD, fg=ACCENT)
        self.updated_lbl = tk.Label(self.card, text="", font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_GRAY)
        self.emoji_lbl.grid(row=0, column=0, rowspan=2, padx=(20, 0), pady=20, sticky="w")
        self.temp_lbl.grid(row=0, column=1, padx=10, pady=(20, 0), sticky="w")
        self.desc_lbl.grid(row=1, column=1, padx=10, sticky="w")
        self.city_lbl.grid(row=0, column=2, padx=20, pady=(20, 0), sticky="e")
        self.updated_lbl.grid(row=1, column=2, padx=20, sticky="e")
        self.card.columnconfigure(1, weight=1)

        # Details Grid
        self.details = tk.Frame(self.root, bg=BG_DARK)
        self.details.pack(fill="x", padx=20, pady=5)
        self._detail_labels = {}
        detail_keys = [
            ("Feels Like", "feels_like"), ("Humidity",   "humidity"),
            ("Wind Speed", "wind_speed"), ("Visibility", "visibility"),
            ("High",       "temp_max"),   ("Low",        "temp_min"),
            ("Sunrise",    "sunrise"),    ("Sunset",     "sunset"),
        ]
        for i, (label, key) in enumerate(detail_keys):
            col = (i % 4) * 2
            row = i // 4
            lf = tk.Frame(self.details, bg=BG_CARD, padx=10, pady=8)
            lf.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            self.details.columnconfigure(col, weight=1)
            tk.Label(lf, text=label, font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")
            val = tk.Label(lf, text="--", font=("Segoe UI", 12, "bold"), bg=BG_CARD, fg=TEXT_WHITE)
            val.pack(anchor="w")
            self._detail_labels[key] = val

        # Forecast
        tk.Label(self.root, text="Upcoming Forecast",
                 font=("Segoe UI", 13, "bold"),
                 bg=BG_DARK, fg=TEXT_WHITE).pack(anchor="w", padx=22, pady=(10, 4))
        self.forecast_frame = tk.Frame(self.root, bg=BG_DARK)
        self.forecast_frame.pack(fill="x", padx=20, pady=(0, 15))

    def _search(self):
        city = self.city_var.get().strip()
        if not city or city == "Enter city name...":
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        self.status_var.set("Fetching weather data...")
        self.search_btn.config(state="disabled")
        threading.Thread(target=self._fetch_data, args=(city,), daemon=True).start()

    def _fetch_data(self, city: str):
        try:
            raw_current  = fetch_current_weather(city)
            raw_forecast = fetch_forecast(city)
            weather   = parse_current_weather(raw_current)
            forecasts = parse_forecast(raw_forecast)
            self.root.after(0, lambda: self._update_ui(weather, forecasts))
        except Exception as e:
            err_msg = format_error(e)
            self.root.after(0, lambda: self._show_error(err_msg))

    def _update_ui(self, w: dict, forecasts: list):
        emoji = get_weather_emoji(w["description"])
        self.emoji_lbl.config(text=emoji)
        self.temp_lbl.config(text=f"{w['temp']}C")
        self.desc_lbl.config(text=w["description"])
        self.city_lbl.config(text=f"{w['city']}, {w['country']}")
        self.updated_lbl.config(text=f"Updated: {w['timestamp']}")
        self._detail_labels["feels_like"].config(text=f"{w['feels_like']}C")
        self._detail_labels["humidity"]  .config(text=f"{w['humidity']}%")
        self._detail_labels["wind_speed"].config(text=f"{w['wind_speed']} km/h")
        self._detail_labels["visibility"].config(text=f"{w['visibility']} km")
        self._detail_labels["temp_max"]  .config(text=f"{w['temp_max']}C")
        self._detail_labels["temp_min"]  .config(text=f"{w['temp_min']}C")
        self._detail_labels["sunrise"]   .config(text=w["sunrise"])
        self._detail_labels["sunset"]    .config(text=w["sunset"])

        for widget in self.forecast_frame.winfo_children():
            widget.destroy()
        for fc in forecasts:
            box = tk.Frame(self.forecast_frame, bg=BG_CARD, padx=10, pady=8)
            box.pack(side="left", expand=True, fill="x", padx=4)
            emo = get_weather_emoji(fc["description"])
            tk.Label(box, text=emo,                   font=("Segoe UI", 18),       bg=BG_CARD).pack()
            tk.Label(box, text=fc["time"],             font=("Segoe UI", 9),        bg=BG_CARD, fg=TEXT_GRAY).pack()
            tk.Label(box, text=f"{fc['temp']}C",      font=("Segoe UI", 13, "bold"),bg=BG_CARD, fg=TEXT_WHITE).pack()
            tk.Label(box, text=f"{fc['humidity']}%",  font=("Segoe UI", 8),        bg=BG_CARD, fg=TEXT_GRAY).pack()

        self.status_var.set(f"Weather data loaded for {w['city']}")
        self.search_btn.config(state="normal")
        save_search(w["city"], w["temp"], w["description"])

    def _show_error(self, message: str):
        self.status_var.set("Error fetching data")
        self.search_btn.config(state="normal")
        messagebox.showerror("Error", message)

    def _show_history(self):
        history = load_history()
        if not history:
            messagebox.showinfo("Search History", "No search history yet!")
            return
        win = tk.Toplevel(self.root)
        win.title("Search History")
        win.geometry("420x450")
        win.configure(bg=BG_DARK)
        win.grab_set()
        tk.Label(win, text="Recent Searches",
                 font=("Segoe UI", 14, "bold"),
                 bg=BG_DARK, fg=ACCENT).pack(pady=(15, 5))
        frame = tk.Frame(win, bg=BG_DARK)
        frame.pack(fill="both", expand=True, padx=15, pady=5)
        for h in history:
            row = tk.Frame(frame, bg=BG_CARD, padx=12, pady=8)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=h["city"],
                     font=("Segoe UI", 12, "bold"),
                     bg=BG_CARD, fg=TEXT_WHITE).pack(side="left")
            tk.Label(row, text=f"  {h['temp']}C  {h['description']}",
                     font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")
            tk.Label(row, text=h["searched_at"],
                     font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_GRAY).pack(side="right")
            row.bind("<Button-1>", lambda e, c=h["city"]: self._load_from_history(c, win))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, c=h["city"]: self._load_from_history(c, win))
        tk.Button(win, text="Clear History", font=("Segoe UI", 10),
                  bg=TEXT_RED, fg="white", bd=0, padx=12, pady=6, cursor="hand2",
                  command=lambda: [clear_history(), win.destroy(),
                                   messagebox.showinfo("Done", "History cleared!")]).pack(pady=10)

    def _load_from_history(self, city: str, win: tk.Toplevel):
        win.destroy()
        self.city_var.set(city)
        self._search()

    def _clear_placeholder(self, event):
        if self.city_var.get() == "Enter city name...":
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_WHITE)

    def _restore_placeholder(self, event):
        if not self.city_var.get():
            self.entry.insert(0, "Enter city name...")
            self.entry.config(fg=TEXT_GRAY)
