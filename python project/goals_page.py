import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from component import DatePicker, save_data

PINK_MAIN = "#ffc0cb"
BLUE_MAIN = "#8ec5fc"
BLUE_LIGHT = "#d6ecff"
WHITE_BG = "#ffffff"
BLACK = "#000000"

def show_goals_page(content_frame, profile, data, update_today_tasks_callback=None):
    # Load user's career goals
    goals = profile["career_goals"]

    # Setup the main window area
    main = tk.Frame(content_frame, bg=WHITE_BG)
    main.pack(fill="both", expand=True, padx=10, pady=10)

    # Title
    t_frame = tk.Frame(main, bg=WHITE_BG)
    t_frame.pack(fill="x", pady=(0, 10))
    tk.Label(t_frame, text="🎯 Career Goal Tracker",
             font=("Arial", 16, "bold"), bg=WHITE_BG, fg=BLACK).pack(anchor="w")

    ttk.Separator(main, orient="horizontal").pack(fill="x", pady=5)

    # Container for two columns: Form (Left) and List (Right)
    cont = tk.Frame(main, bg=WHITE_BG)
    cont.pack(fill="both", expand=True)

    # --- Left Side: Input Form ---
    left = tk.Frame(cont, bg=WHITE_BG, bd=2, relief="solid")
    left.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)

    form = tk.Frame(left, bg=WHITE_BG)
    form.pack(fill="x", padx=15, pady=15)

    # Goal Title Input
    tk.Label(form, text="Goal Title:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=0, column=0, sticky="w", padx=5, pady=8)
    title_entry = tk.Entry(form, font=("Arial", 11), bd=2,
                           relief="solid", width=35)
    title_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=5, pady=8)

    # Target Date Input
    tk.Label(form, text="Target Date:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=1, column=0, sticky="w", padx=5, pady=8)

    dp_frame = tk.Frame(form, bg=WHITE_BG)
    dp_frame.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=8)

    dp = DatePicker(dp_frame, datetime.now().strftime("%Y-%m-%d"))
    dp.pack(anchor="w")

    # Description Input
    tk.Label(form, text="Description:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=2, column=0, sticky="nw", padx=5, pady=8)
    desc_text = tk.Text(form, font=("Arial", 10), height=4, width=35,
                        bd=2, relief="solid")
    desc_text.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=8)

    # Type Dropdown (Short-term vs Long-term)
    tk.Label(form, text="Type:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=3, column=0, sticky="w", padx=5, pady=8)
    type_var = tk.StringVar(value="Short-term")
    type_combo = ttk.Combobox(form, textvariable=type_var,
                              values=["Short-term", "Long-term"],
                              state="readonly", width=15)
    type_combo.grid(row=3, column=1, sticky="w", padx=5, pady=8)

    # Priority Dropdown (High vs Low)
    tk.Label(form, text="Priority:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=3, column=2, sticky="w", padx=5, pady=8)
    priority_var = tk.StringVar(value="High")
    priority_combo = ttk.Combobox(form, textvariable=priority_var,
                                  values=["High", "Low"],
                                  state="readonly", width=15)
    priority_combo.grid(row=3, column=3, sticky="w", padx=5, pady=8)

    # Variables to track if we are adding a new goal or editing an old one
    edit_mode = False
    editing_id = None

    # --- Function: Add or Save the Goal ---
    def add_or_update():
        nonlocal edit_mode, editing_id

        # Get values from the form
        t = title_entry.get().strip()
        typ = type_var.get()
        dsc = desc_text.get("1.0", "end").strip()
        pr = priority_var.get()

        if not t:
            messagebox.showerror("Error", "Please fill in Goal Title")
            return

        ok, err = dp.validate_date()
        if not ok:
            messagebox.showerror("Error", err)
            return

        d_str = dp.get_date()

        # Ensure goal date isn't in the past
        try:
            dt = datetime.strptime(d_str, "%Y-%m-%d")
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if dt < today:
                messagebox.showerror("Error", "Target Date cannot be in the past")
                return
        except:
            messagebox.showerror("Error", "Invalid date format")
            return

        # If we are editing, update the existing goal
        if edit_mode:
            for g in goals:
                if g["id"] == editing_id:
                    g["title"] = t
                    g["type"] = typ
                    g["target_date"] = d_str
                    g["description"] = dsc
                    g["priority"] = pr
                    break
            add_btn.config(text="Add Goal")
            edit_mode = False
            editing_id = None
            messagebox.showinfo("Success", "Career Goal updated successfully!")
        else:
            # Otherwise, create a new goal
            nid = max([g["id"] for g in goals], default=0) + 1
            goals.append({
                "id": nid,
                "title": t,
                "type": typ,
                "target_date": d_str,
                "description": dsc,
                "priority": pr,
                "status": "Active",
                "created_date": datetime.now().strftime("%Y-%m-%d")
            })
            messagebox.showinfo("Success", "Career Goal added successfully!")

        # Save and refresh
        save_data(data)
        refresh()
        clear()
        if update_today_tasks_callback:
            update_today_tasks_callback()

    # Function to empty the form
    def clear():
        title_entry.delete(0, "end")
        desc_text.delete("1.0", "end")
        type_var.set("Short-term")
        priority_var.set("High")
        dp.set_date(datetime.now().strftime("%Y-%m-%d"))
        add_btn.config(text="Add Goal")

    # Form Buttons
    btns = tk.Frame(form, bg=WHITE_BG)
    btns.grid(row=4, column=0, columnspan=4, pady=20, sticky="e")

    add_btn = tk.Button(btns, text="Add Goal", font=("Arial", 11, "bold"),
                        bg=PINK_MAIN, fg=BLACK, bd=2, relief="solid",
                        command=add_or_update)
    add_btn.pack(side="right", padx=5)

    tk.Button(btns, text="Clear Form", font=("Arial", 11),
              bg=WHITE_BG, fg=BLACK, bd=2, relief="solid",
              command=clear).pack(side="right", padx=5)

    # --- Right Side: Goal List ---
    right = tk.Frame(cont, bg=WHITE_BG, bd=2, relief="solid")
    right.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=5)

    hdr = tk.Frame(right, bg=WHITE_BG)
    hdr.pack(fill="x", padx=10, pady=10)
    tk.Label(hdr, text="My Career Goals:", font=("Arial", 12, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(side="left")

    lst_box = tk.Frame(right, bg=WHITE_BG)
    lst_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    lst = tk.Listbox(lst_box, font=("Arial", 11), bd=2, relief="solid",
                     selectbackground="#4a86e8", selectforeground=WHITE_BG,
                     highlightthickness=0, selectmode="single")
    lst.pack(side="left", fill="both", expand=True)

    sb = tk.Scrollbar(lst_box, orient="vertical", command=lst.yview)
    sb.pack(side="left", fill="y")
    lst.config(yscrollcommand=sb.set)

    ctrl = tk.Frame(right, bg=WHITE_BG)
    ctrl.pack(fill="x", padx=10, pady=(0, 10))

    # --- Function: Update List Display ---
    def refresh():
        lst.delete(0, "end")
        # Sort by Priority, then Date
        for g in sorted(goals, key=lambda x: (x["priority"], x["target_date"])):
            sym = "🔴" if g["priority"] == "High" else "🟡"
            st = "✓" if g["status"] == "Completed" else ""
            t_s = f"{g['type'][:12]:12}"
            d_s = f"{g['target_date']:12}"
            ti = f"{g['title'][:25]:25}"
            lst.insert("end", f"{sym} {st} {t_s} {d_s} {ti}")

    # --- Function: Load selected goal into form for editing ---
    def edit():
        nonlocal edit_mode, editing_id
        sel = lst.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a Career Goal to edit")
            return
        idx = sel[0]
        sorted_list = sorted(goals, key=lambda x: (x["priority"], x["target_date"]))
        item = sorted_list[idx]

        for g in goals:
            if g["id"] == item["id"]:
                title_entry.delete(0, "end")
                title_entry.insert(0, g["title"])
                desc_text.delete("1.0", "end")
                desc_text.insert("1.0", g["description"])
                type_var.set(g["type"])
                priority_var.set(g["priority"])
                dp.set_date(g["target_date"])
                edit_mode = True
                editing_id = g["id"]
                add_btn.config(text="Update Goal")
                break

    # --- Function: Mark as Completed/Active ---
    def toggle():
        sel = lst.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a Career Goal")
            return
        idx = sel[0]
        sorted_list = sorted(goals, key=lambda x: (x["priority"], x["target_date"]))
        item = sorted_list[idx]

        for g in goals:
            if g["id"] == item["id"]:
                g["status"] = "Completed" if g["status"] == "Active" else "Active"
                save_data(data)
                refresh()
                messagebox.showinfo("Success", "Career Goal status updated successfully!")
                if update_today_tasks_callback:
                    update_today_tasks_callback()
                return

    # --- Function: Delete Goal ---
    def delete_goal():
        sel = lst.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a Career Goal")
            return
        if not messagebox.askyesno("Delete Career Goal", "Are you sure you want to delete this Career Goal?"):
            return
        idx = sel[0]
        sorted_list = sorted(goals, key=lambda x: (x["priority"], x["target_date"]))
        item = sorted_list[idx]

        for i, g in enumerate(goals):
            if g["id"] == item["id"]:
                del goals[i]
                save_data(data)
                refresh()
                if edit_mode and editing_id == g["id"]:
                    clear()
                messagebox.showinfo("Success", "Career Goal deleted successfully!")
                if update_today_tasks_callback:
                    update_today_tasks_callback()
                return

    # Action Buttons (Edit, Mark Done, Delete)
    tk.Button(ctrl, text="Edit", font=("Arial", 11),
              bg=BLUE_MAIN, fg=BLACK, bd=2, relief="solid",
              command=edit, width=10).pack(side="left", padx=5)
    tk.Button(ctrl, text="Mark ✓", font=("Arial", 11),
              bg=BLUE_MAIN, fg=BLACK, bd=2, relief="solid",
              command=toggle, width=10).pack(side="left", padx=5)
    tk.Button(ctrl, text="Delete", font=("Arial", 11),
              bg=WHITE_BG, fg="red", bd=2, relief="solid",
              command=delete_goal, width=10).pack(side="left", padx=5)

    refresh()