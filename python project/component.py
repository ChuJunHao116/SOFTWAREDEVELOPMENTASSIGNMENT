import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import json

WHITE_BG = "#ffffff"
BLACK = "#000000"

# Find out where this file is located on the computer so we can save data nearby
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

# --- Data Management Functions ---

# Check if the save file exists; if not, create a blank one
def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        tmp = {"users": [], "profiles": {}}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tmp, f, ensure_ascii=False, indent=4)

# Load the saved data from the file into the program
def load_data():
    ensure_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        d = json.load(f)

    # Make sure the data has the correct structure (users and profiles)
    if "users" not in d:
        d["users"] = []
    if "profiles" not in d:
        d["profiles"] = {}

    save_data(d)
    return d

# Write the current program data back to the file (Save)
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Ensure a specific user has all the necessary profile lists (goals, skills, etc.)
def ensure_profile(data, username):
    if "profiles" not in data:
        data["profiles"] = {}
    if username not in data["profiles"]:
        data["profiles"][username] = {
            "career_goals": [],
            "skills_log": [],
            "daily_tasks": [],
            "achievements": [],
            "interview_qas": []
        }

# --- Custom Menu Tool ---
# This creates the small menu that pops up when you hover over the username
class HoverMenu(tk.Menu):
    def __init__(self, parent, app):
        super().__init__(parent, tearoff=0)
        self.app = app
        # Add the Log Out and Exit options
        self.add_command(label="Log Out", command=self.logout)
        self.add_separator()
        self.add_command(label="Exit System (Delete All Data)", command=self.exit_system)

    def logout(self):
        # Ask for confirmation before logging out
        if messagebox.askyesno("Log Out", "Do you want to log out?"):
            self.app.current_user = None
            self.app.show_auth_page()

    def exit_system(self):
        # DANGER: This deletes the data file and closes the app
        if messagebox.askyesno("Exit System", "This will delete all saved data. Are you sure?"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            self.app.root.quit()

# --- Custom Calendar Tool (DatePicker) ---
# This creates a widget with Year, Month, and Day spinners
class DatePicker:
    def __init__(self, parent, default_date=None):
        self.frame = tk.Frame(parent, bg=WHITE_BG)

        # Create the Year spinner
        tk.Label(self.frame, text="Year:", font=("Arial", 11), bg=WHITE_BG, fg=BLACK).pack(side="left", padx=(0, 5))
        now = datetime.now()
        self.year_var = tk.StringVar(value=str(now.year))
        self.year_spin = tk.Spinbox(self.frame, from_=now.year - 10, to=now.year + 10,
                                    textvariable=self.year_var, width=5, font=("Arial", 11))
        self.year_spin.pack(side="left", padx=(0, 10))

        # Create the Month spinner
        tk.Label(self.frame, text="Month:", font=("Arial", 11), bg=WHITE_BG, fg=BLACK).pack(side="left", padx=(0, 5))
        self.month_var = tk.StringVar(value=str(now.month))
        self.month_spin = tk.Spinbox(self.frame, from_=1, to=12,
                                     textvariable=self.month_var, width=3, font=("Arial", 11))
        self.month_spin.pack(side="left", padx=(0, 10))

        # Create the Day spinner
        tk.Label(self.frame, text="Day:", font=("Arial", 11), bg=WHITE_BG, fg=BLACK).pack(side="left", padx=(0, 5))
        self.day_var = tk.StringVar(value=str(now.day))
        self.day_spin = tk.Spinbox(self.frame, from_=1, to=31,
                                   textvariable=self.day_var, width=3, font=("Arial", 11))
        self.day_spin.pack(side="left")

        # If a date was provided, set the spinners to that date
        if default_date:
            self.set_date(default_date)

    # Helper functions to place the widget on screen
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    # Get the selected date as a string (e.g., "2023-12-25")
    def get_date(self):
        try:
            y = int(self.year_var.get())
            m = int(self.month_var.get())
            d = int(self.day_var.get())
            return f"{y:04d}-{m:02d}-{d:02d}"
        except:
            return ""

    # Set the spinners to show a specific date string
    def set_date(self, s):
        try:
            t = datetime.strptime(s, "%Y-%m-%d")
            self.year_var.set(str(t.year))
            self.month_var.set(str(t.month))
            self.day_var.set(str(t.day))
        except:
            pass

    # Check if the selected date is real (e.g., April has only 30 days)
    def validate_date(self):
        try:
            y = int(self.year_var.get())
            m = int(self.month_var.get())
            d = int(self.day_var.get())

            if m < 1 or m > 12:
                return False, "Month must be between 1 and 12"

            if d < 1 or d > 31:
                return False, "Day must be between 1 and 31"

            # Check 30-day months
            if m in [4, 6, 9, 11] and d > 30:
                return False, f"Day must be between 1 and 30 for month {m}"

            # Check February (considering leap years)
            if m == 2:
                leap = (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
                if leap:
                    if d > 29:
                        return False, "Day must be between 1 and 29 for February in leap year"
                else:
                    if d > 28:
                        return False, "Day must be between 1 and 28 for February"

            return True, ""
        except:
            return False, "Invalid date values"