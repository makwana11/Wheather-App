"""
main.py - Entry Point
Run: python main.py
"""

import tkinter as tk
from ui import WeatherApp

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
