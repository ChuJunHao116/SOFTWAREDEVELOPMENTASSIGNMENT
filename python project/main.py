import tkinter as tk
from tkinter import ttk, messagebox
from component import HoverMenu, DatePicker, save_data, load_data, ensure_profile
from login_signin_page import show_auth_page, show_login_page, show_signup_page
from goals_page import show_goals_page
from skill_page import show_skills_page
from task_page import show_tasks_page, show_today_tasks_detail_popup
from achievement_page import show_achievements_page
from interview_page import show_interview_page
from datetime import datetime
import os

PINK_MAIN = "#ffc0cb"
BLUE_MAIN = "#8ec5fc"
PINK_LIGHT = "#ffe4f0"
BLUE_LIGHT = "#d6ecff"
WHITE_BG = "#ffffff"
BLACK = "#000000"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "career_icon.png")

class CareerAssistantApp:
    def __init__(self):
        self.data = load_data()
        self.current_user = None
        self.hover_menu = None

        self.root = tk.Tk()
        self.root.title("Career & Skills Development Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg=PINK_LIGHT)
        self.root.resizable(False, False)
        icon_img = tk.PhotoImage(file=ICON_PATH)
        self.root.iconphoto(False, icon_img)

        self.content_frame = None
        self.nav_buttons = {}
        self.user_label = None
        self.today_label = None

        self.show_auth_page()

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def ensure_profile(self, username):
        ensure_profile(self.data, username)
        save_data(self.data)

    def show_auth_page(self):
        self.current_user = None
        self.clear_root()
        show_auth_page(self)

    def show_login_page(self):
        show_login_page(self)

    def show_signup_page(self):
        show_signup_page(self)

    def get_today_tasks(self):
        if not self.current_user:
            return []
        profile = self.get_profile()
        today = datetime.now().strftime("%Y-%m-%d")
        week = datetime.now().strftime("%A")

        tasks_today = []
        for task in profile["daily_tasks"]:
            if task.get("completed", False):
                continue
            if task["repeat_type"] == "specific":
                if task["date"] == today:
                    tasks_today.append(task)
            elif task["repeat_type"] == "weekly":
                if task["date"] == week:
                    tasks_today.append(task)
        return tasks_today

    def update_today_tasks_label(self):
        if self.today_label:
            tasks = self.get_today_tasks()
            num = len(tasks)
            if num > 0:
                self.today_label.config(text=f"📅 Today: {num} tasks pending", fg="red", cursor="hand2")
            else:
                self.today_label.config(text="📅 Today: All tasks completed!", fg="green", cursor="hand2")

    def show_main_page(self):
        self.clear_root()
        self.root.configure(bg=WHITE_BG)

        main = tk.Frame(self.root, bg=WHITE_BG)
        main.pack(fill="both", expand=True)
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        header = tk.Frame(main, bg=BLUE_LIGHT, bd=2, relief="solid", highlightbackground=BLACK)
        header.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        title = tk.Label(header, text="💼 Career & Skills Development Assistant",
                         font=("Arial", 18, "bold"), bg=BLUE_LIGHT, fg=BLACK)
        title.pack(side="left", padx=10, pady=10)

        today_box = tk.Frame(header, bg=BLUE_LIGHT)
        today_box.pack(side="right", padx=10, pady=5)

        tasks = self.get_today_tasks()
        num = len(tasks)

        self.today_label = tk.Label(
            today_box,
            text=f"📅 Today: {num} tasks pending" if num > 0 else "📅 Today: All tasks completed!",
            font=("Arial", 11),
            bg=BLUE_LIGHT,
            fg="red" if num > 0 else "green",
            cursor="hand2"
        )
        self.today_label.pack(side="right", padx=(0, 10))

        def show_today_popup():
            show_today_tasks_detail_popup(self.root, self.get_today_tasks())

        self.today_label.bind("<Button-1>", lambda e: show_today_popup())

        self.user_label = tk.Label(
            header,
            text=f"👤 User: {self.current_user}",
            font=("Arial", 12),
            bg=BLUE_LIGHT,
            fg=BLACK,
            cursor="hand2"
        )
        self.user_label.pack(side="right", padx=10)

        self.hover_menu = HoverMenu(self.root, self)
        self.user_label.bind("<Enter>", self.show_user_menu)
        self.user_label.bind("<Leave>", self.hide_user_menu)

        self.content_frame = tk.Frame(main, bg=WHITE_BG, bd=2, relief="solid", highlightbackground=BLACK)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 5))

        nav = tk.Frame(main, bg=PINK_LIGHT, bd=2, relief="solid", highlightbackground=BLACK, height=60)
        nav.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.nav_buttons = {}

        def make_btn(text, key, command, bg):
            btn = tk.Button(
                nav,
                text=text,
                font=("Arial", 11, "bold"),
                bg=bg,
                fg=BLACK,
                bd=2,
                relief="solid",
                highlightbackground=BLACK,
                command=lambda k=key, c=command: self.switch_page_and_update(k, c)
            )
            btn.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            self.nav_buttons[key] = btn

        make_btn("🎯 Goal Tracker", "goals", self.show_goals_page, BLUE_MAIN)
        make_btn("📚 Skills Log", "skills", self.show_skills_page, WHITE_BG)
        make_btn("📅 Task Planner", "tasks", self.show_tasks_page, WHITE_BG)
        make_btn("🏆 Achievement Summary", "achievements", self.show_achievements_page, WHITE_BG)
        make_btn("💬 Interview", "interview", self.show_interview_page, WHITE_BG)

        self.switch_page_and_update("goals", self.show_goals_page)

    def switch_page_and_update(self, key, command):
        self.switch_page(key, command)
        self.update_today_tasks_label()

    def show_user_menu(self, event=None):
        try:
            self.hover_menu.tk_popup(self.user_label.winfo_rootx(),
                                     self.user_label.winfo_rooty() + self.user_label.winfo_height())
        finally:
            self.hover_menu.grab_release()

    def hide_user_menu(self, event=None):
        pass

    def switch_page(self, key, command):
        for k, btn in self.nav_buttons.items():
            btn.config(bg=WHITE_BG)
        self.nav_buttons[key].config(bg=BLUE_MAIN)

        for w in self.content_frame.winfo_children():
            w.destroy()
        command()

    def get_profile(self):
        return self.data["profiles"][self.current_user]

    def show_goals_page(self):
        show_goals_page(self.content_frame, self.get_profile(), self.data, self.update_today_tasks_label)

    def show_skills_page(self):
        show_skills_page(self.content_frame, self.get_profile(), self.data)

    def show_tasks_page(self):
        show_tasks_page(self.content_frame, self.get_profile(), self.data, self.update_today_tasks_label)

    def show_achievements_page(self):
        show_achievements_page(self.content_frame, self.get_profile(), self.data)

    def show_interview_page(self):
        show_interview_page(self.content_frame, self.get_profile(), self.data)


if __name__ == "__main__":
    app = CareerAssistantApp()
    app.root.mainloop()
