import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from component import DatePicker, save_data

# --- Design Colors ---
# These variables hold the color codes used throughout the page
PINK_MAIN = "#ffc0cb"
PINK_LIGHT = "#ffe4f0"
BLUE_MAIN = "#8ec5fc"
WHITE_BG = "#ffffff"
BLACK = "#000000"

def show_achievements_page(content_frame, profile, data):
    # Load the list of achievements for the current user
    achievements = profile["achievements"]

    # Create the main background area for this page
    main = tk.Frame(content_frame, bg=WHITE_BG)
    main.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Title Section ---
    t_frame = tk.Frame(main, bg=WHITE_BG)
    t_frame.pack(fill="x", pady=(0, 10))

    # Display the large text title at the top
    t = tk.Label(t_frame, text="🏆 Achievement Summary",
                 font=("Arial", 16, "bold"), bg=WHITE_BG, fg=BLACK)
    t.pack(anchor="w")

    # Draw a horizontal line to separate the title
    ttk.Separator(main, orient="horizontal").pack(fill="x", pady=5)

    # --- Statistics Box ---
    # This creates the pink box at the top that shows the user's total stats
    stats = tk.Frame(main, bg=PINK_LIGHT, bd=2, relief="solid")
    stats.pack(fill="x", padx=10, pady=10)

    # Calculate the numbers to display (counting the lists)
    cg = len(profile["career_goals"])
    cg_done = sum(1 for g in profile["career_goals"] if g.get("status") == "Completed")
    sl = len(profile["skills_log"])
    ts = len(profile["daily_tasks"])
    ts_done = sum(1 for tsk in profile["daily_tasks"] if tsk.get("completed"))
    total = len(achievements)

    # Place the calculated numbers into the pink box
    tk.Label(stats, text=f"🎯 Career Goals: {cg} (Completed: {cg_done})",
             font=("Arial", 11), bg=PINK_LIGHT, fg=BLACK).grid(row=0, column=0, sticky="w", padx=10, pady=3)
    tk.Label(stats, text=f"📚 Skills/Certifications: {sl}",
             font=("Arial", 11), bg=PINK_LIGHT, fg=BLACK).grid(row=0, column=1, sticky="w", padx=10, pady=3)
    tk.Label(stats, text=f"📅 Daily Tasks: {ts} (Completed: {ts_done})",
             font=("Arial", 11), bg=PINK_LIGHT, fg=BLACK).grid(row=1, column=0, sticky="w", padx=10, pady=3)
    tk.Label(stats, text=f"🏆 Achievements: {total}",
             font=("Arial", 11), bg=PINK_LIGHT, fg=BLACK).grid(row=1, column=1, sticky="w", padx=10, pady=3)

    # --- Main Content Area ---
    cont = tk.Frame(main, bg=WHITE_BG)
    cont.pack(fill="both", expand=True, pady=10)

    # --- Left Side: Input Form ---
    left = tk.Frame(cont, bg=WHITE_BG, bd=2, relief="solid")
    left.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)

    form = tk.Frame(left, bg=WHITE_BG)
    form.pack(fill="x", padx=15, pady=15)

    tk.Label(form, text="Add Achievement", font=("Arial", 12, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

    # Entry box for the Achievement Title
    tk.Label(form, text="Achievement Title:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=1, column=0, sticky="w", padx=5, pady=8)
    title_entry = tk.Entry(form, font=("Arial", 11), bd=2, relief="solid", width=35)
    title_entry.grid(row=1, column=1, sticky="we", padx=5, pady=8)

    # Date picker for when the achievement happened
    tk.Label(form, text="Date:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=2, column=0, sticky="w", padx=5, pady=8)

    dp_frame = tk.Frame(form, bg=WHITE_BG)
    dp_frame.grid(row=2, column=1, sticky="w", padx=5, pady=8)

    # Use our custom DatePicker tool
    dp = DatePicker(dp_frame, datetime.now().strftime("%Y-%m-%d"))
    dp.pack(anchor="w")

    # Entry box for Category
    tk.Label(form, text="Category:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=3, column=0, sticky="w", padx=5, pady=8)
    category_entry = tk.Entry(form, font=("Arial", 11), bd=2, relief="solid", width=35)
    category_entry.grid(row=3, column=1, sticky="we", padx=5, pady=8)

    # Larger text box for Description
    tk.Label(form, text="Description:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=4, column=0, sticky="nw", padx=5, pady=8)
    desc_text = tk.Text(form, font=("Arial", 10), bd=2, relief="solid", height=4, width=35)
    desc_text.grid(row=4, column=1, sticky="we", padx=5, pady=8)

    # --- Function: Save the new achievement ---
    def add_ach():
        # Get the text the user typed
        ttl = title_entry.get().strip()
        cat = category_entry.get().strip()
        dsc = desc_text.get("1.0", "end").strip()

        # Check if the user forgot to type a title or category
        if not ttl:
            messagebox.showerror("Error", "Please enter Achievement Title")
            return
        if not cat:
            messagebox.showerror("Error", "Please enter Category")
            return

        # Check if the date is valid (e.g., not February 30th)
        ok, err = dp.validate_date()
        if not ok:
            messagebox.showerror("Error", err)
            return

        d = dp.get_date()

        # Ensure the date isn't in the future
        try:
            dt = datetime.strptime(d, "%Y-%m-%d")
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if dt > today:
                messagebox.showerror("Error", "Achievement Date cannot be in the future")
                return
        except:
            messagebox.showerror("Error", "Invalid date format")
            return

        # Create a unique ID for this new item
        new_id = max([a["id"] for a in achievements], default=0) + 1

        # Add the new achievement to the list
        achievements.append({
            "id": new_id,
            "title": ttl,
            "date": d,
            "category": cat,
            "description": dsc,
            "added_date": datetime.now().strftime("%Y-%m-%d")
        })

        # Save to the computer file and update the screen
        save_data(data)
        refresh()
        
        # Clear the form boxes for the next entry
        title_entry.delete(0, "end")
        category_entry.delete(0, "end")
        desc_text.delete("1.0", "end")
        dp.set_date(datetime.now().strftime("%Y-%m-%d"))
        messagebox.showinfo("Success", "Achievement added successfully!")

    # The "Add Achievement" Button
    btns = tk.Frame(form, bg=WHITE_BG)
    btns.grid(row=5, column=0, columnspan=2, pady=20, sticky="e")

    tk.Button(btns, text="Add Achievement", font=("Arial", 11, "bold"),
              bg=PINK_MAIN, fg=BLACK, bd=2, relief="solid",
              command=add_ach).pack(side="right", padx=5)

    # --- Right Side: List of Achievements ---
    right = tk.Frame(cont, bg=WHITE_BG, bd=2, relief="solid")
    right.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=5)

    hdr = tk.Frame(right, bg=WHITE_BG)
    hdr.pack(fill="x", padx=10, pady=10)

    tk.Label(hdr, text="My Achievements:", font=("Arial", 12, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(side="left")

    # Create the listbox to display items
    list_box = tk.Frame(right, bg=WHITE_BG)
    list_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    lst = tk.Listbox(list_box, font=("Arial", 11), bd=2, relief="solid",
                     selectbackground=BLUE_MAIN, selectforeground=BLACK,
                     highlightthickness=0, selectmode="single")
    lst.pack(side="left", fill="both", expand=True)

    # Add a scrollbar in case there are many achievements
    sb = tk.Scrollbar(list_box, orient="vertical", command=lst.yview)
    sb.pack(side="left", fill="y")
    lst.config(yscrollcommand=sb.set)

    ctrl = tk.Frame(right, bg=WHITE_BG)
    ctrl.pack(fill="x", padx=10, pady=(0, 10))

    # --- Function: Update the list on the screen ---
    def refresh():
        lst.delete(0, "end")
        # Sort so the newest achievements appear first
        for a in sorted(achievements, key=lambda x: x["date"], reverse=True):
            line = f"{a['date']}  {a['title'][:40]:40}"
            lst.insert("end", line)

    # --- Function: Delete an achievement ---
    def delete_ach():
        sel = lst.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select an Achievement")
            return

        # Confirm before deleting
        if not messagebox.askyesno("Delete Achievement", "Are you sure you want to delete this Achievement?"):
            return

        txt = lst.get(sel[0])
        for i, a in enumerate(achievements):
            if a["title"] in txt and a["date"] in txt:
                del achievements[i]
                save_data(data) # Save the new list (without the deleted item)
                refresh()
                messagebox.showinfo("Success", "Achievement deleted successfully!")
                return

    # The Delete Button
    tk.Button(ctrl, text="Delete Achievement", font=("Arial", 11),
              bg=WHITE_BG, fg="red", bd=2, relief="solid",
              command=delete_ach, width=20).pack(side="left", padx=5)

    # Show the list when the page loads
    refresh()