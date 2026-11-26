import tkinter as tk
from tkinter import messagebox
from component import save_data, ensure_profile

PINK_MAIN = "#ffc0cb"
BLUE_MAIN = "#8ec5fc"
PINK_LIGHT = "#ffe4f0"
BLUE_LIGHT = "#d6ecff"
WHITE_BG = "#ffffff"
BLACK = "#000000"

# --- Main Authentication Screen (Login or Sign Up?) ---
def show_auth_page(app):
    app.root.configure(bg=PINK_LIGHT)

    outer = tk.Frame(app.root, bg=PINK_LIGHT)
    outer.pack(fill="both", expand=True)

    # Title
    title_frame = tk.Frame(outer, bg=BLUE_LIGHT, bd=2, relief="solid")
    title_frame.pack(pady=40, padx=40, fill="x")

    title_label = tk.Label(title_frame, text="💼 Career & Skills Development Assistant",
                           font=("Arial", 20, "bold"), bg=BLUE_LIGHT, fg=BLACK)
    title_label.pack(pady=15)

    # Buttons to choose Login or Signup
    btn_frame = tk.Frame(outer, bg=PINK_LIGHT)
    btn_frame.pack(pady=40)

    login_btn = tk.Button(btn_frame, text="Log In", font=("Arial", 14, "bold"),
                          bg=BLUE_MAIN, fg=BLACK, bd=2, relief="solid",
                          width=20, height=2, command=app.show_login_page)
    login_btn.pack(pady=20)

    signup_btn = tk.Button(btn_frame, text="Sign Up", font=("Arial", 14, "bold"),
                           bg=PINK_MAIN, fg=BLACK, bd=2, relief="solid",
                           width=20, height=2, command=app.show_signup_page)
    signup_btn.pack(pady=20)


# --- Login Screen ---
def show_login_page(app):
    app.clear_root()
    app.root.configure(bg=PINK_LIGHT)

    outer = tk.Frame(app.root, bg=PINK_LIGHT)
    outer.pack(fill="both", expand=True)

    # Back Button
    back_frame = tk.Frame(outer, bg=PINK_LIGHT)
    back_frame.pack(fill="x", padx=20, pady=10)

    back_btn = tk.Button(back_frame, text="← Back", font=("Arial", 11),
                         bg=WHITE_BG, fg=BLACK, bd=2, relief="solid",
                         command=app.show_auth_page)
    back_btn.pack(side="left")

    # Title
    title_frame = tk.Frame(outer, bg=BLUE_LIGHT, bd=2, relief="solid")
    title_frame.pack(pady=20, padx=40, fill="x")

    title_label = tk.Label(title_frame, text="🔐 Log In", font=("Arial", 18, "bold"),
                           bg=BLUE_LIGHT, fg=BLACK)
    title_label.pack(pady=15)

    # Input Form
    form = tk.Frame(outer, bg=WHITE_BG, bd=2, relief="solid")
    form.pack(pady=20, padx=60, fill="x")

    tk.Label(form, text="Username:", font=("Arial", 12), bg=WHITE_BG, fg=BLACK).pack(pady=(20, 2), padx=20, anchor="w")
    username_entry = tk.Entry(form, font=("Arial", 12), bd=2, relief="solid", width=30)
    username_entry.pack(pady=(0, 10), padx=20, ipadx=5, ipady=3, fill="x")

    tk.Label(form, text="Password:", font=("Arial", 12), bg=WHITE_BG, fg=BLACK).pack(pady=(10, 2), padx=20, anchor="w")
    password_entry = tk.Entry(form, font=("Arial", 12), show="*", bd=2, relief="solid", width=30)
    password_entry.pack(pady=(0, 20), padx=20, ipadx=5, ipady=3, fill="x")

    error_label = tk.Label(form, text="", font=("Arial", 10), bg=WHITE_BG, fg="red")
    error_label.pack(pady=5)

    # Check Username and Password
    def handle_login():
        user = username_entry.get().strip()
        pwd = password_entry.get().strip()

        if not user:
            error_label.config(text="Please enter username")
            return
        if not pwd:
            error_label.config(text="Please enter password")
            return

        # Look for user in the database
        for u in app.data.get("users", []):
            if u.get("username") == user and u.get("password") == pwd:
                ensure_profile(app.data, user) # Make sure they have a profile setup
                app.current_user = user
                app.show_main_page() # Success! Go to main app
                return

        error_label.config(text="Invalid username or password")

    login_btn = tk.Button(form, text="Log In", font=("Arial", 12, "bold"),
                          bg=BLUE_MAIN, fg=BLACK, bd=2, relief="solid",
                          command=handle_login)
    login_btn.pack(pady=20, padx=20, ipadx=20, ipady=5)


# --- Sign Up Screen ---
def show_signup_page(app):
    app.clear_root()
    app.root.configure(bg=PINK_LIGHT)

    outer = tk.Frame(app.root, bg=PINK_LIGHT)
    outer.pack(fill="both", expand=True)

    # Back Button
    back_frame = tk.Frame(outer, bg=PINK_LIGHT)
    back_frame.pack(fill="x", padx=20, pady=10)

    back_btn = tk.Button(back_frame, text="← Back", font=("Arial", 11),
                         bg=WHITE_BG, fg=BLACK, bd=2, relief="solid",
                         command=app.show_auth_page)
    back_btn.pack(side="left")

    # Title
    title_frame = tk.Frame(outer, bg=PINK_MAIN, bd=2, relief="solid")
    title_frame.pack(pady=20, padx=40, fill="x")

    title_label = tk.Label(title_frame, text="📝 Sign Up", font=("Arial", 18, "bold"),
                           bg=PINK_MAIN, fg=BLACK)
    title_label.pack(pady=15)

    # Input Form
    form = tk.Frame(outer, bg=WHITE_BG, bd=2, relief="solid")
    form.pack(pady=20, padx=60, fill="x")

    tk.Label(form, text="Username:", font=("Arial", 12), bg=WHITE_BG, fg=BLACK).pack(pady=(20, 2), padx=20, anchor="w")
    username_entry = tk.Entry(form, font=("Arial", 12), bd=2, relief="solid", width=30)
    username_entry.pack(pady=(0, 10), padx=20, ipadx=5, ipady=3, fill="x")

    tk.Label(form, text="Password:", font=("Arial", 12), bg=WHITE_BG, fg=BLACK).pack(pady=(10, 2), padx=20, anchor="w")
    password_entry = tk.Entry(form, font=("Arial", 12), show="*", bd=2, relief="solid", width=30)
    password_entry.pack(pady=(0, 10), padx=20, ipadx=5, ipady=3, fill="x")

    tk.Label(form, text="Confirm Password:", font=("Arial", 12), bg=WHITE_BG, fg=BLACK).pack(pady=(10, 2), padx=20, anchor="w")
    confirm_entry = tk.Entry(form, font=("Arial", 12), show="*", bd=2, relief="solid", width=30)
    confirm_entry.pack(pady=(0, 20), padx=20, ipadx=5, ipady=3, fill="x")

    error_label = tk.Label(form, text="", font=("Arial", 10), bg=WHITE_BG, fg="red")
    error_label.pack(pady=5)

    # Create the new user
    def handle_signup():
        user = username_entry.get().strip()
        pwd = password_entry.get().strip()
        conf = confirm_entry.get().strip()

        # Validation Checks
        if not user:
            error_label.config(text="Please enter username")
            return
        if not pwd:
            error_label.config(text="Please enter password")
            return
        if not conf:
            error_label.config(text="Please confirm password")
            return
        if pwd != conf:
            error_label.config(text="Passwords do not match")
            return
        if len(pwd) < 4:
            error_label.config(text="Password must be at least 4 characters long")
            return

        # Check if username is taken
        for u in app.data.get("users", []):
            if u.get("username") == user:
                error_label.config(text="Username already exists")
                return

        # Save new user
        app.data.setdefault("users", []).append({"username": user, "password": pwd})
        ensure_profile(app.data, user)
        save_data(app.data)
        messagebox.showinfo("Sign Up Successful", "Account created successfully!")
        app.current_user = user
        app.show_main_page()

    signup_btn = tk.Button(form, text="Create Account", font=("Arial", 12, "bold"),
                           bg=PINK_MAIN, fg=BLACK, bd=2, relief="solid",
                           command=handle_signup)
    signup_btn.pack(pady=20, padx=20, ipadx=20, ipady=5)