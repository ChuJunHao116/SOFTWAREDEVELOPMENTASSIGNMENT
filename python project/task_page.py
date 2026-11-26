import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from component import DatePicker, save_data

PINK_MAIN = "#ffc0cb"
BLUE_MAIN = "#8ec5fc"
BLUE_LIGHT = "#d6ecff"
WHITE_BG = "#ffffff"
BLACK = "#000000"

# --- Popup Window for "Today's Tasks" ---
# This shows a specific list of what needs to be done TODAY
def show_today_tasks_detail_popup(root, today_tasks):
    if not today_tasks:
        messagebox.showinfo("Today's Tasks", "Great! All tasks for today are completed!")
        return

    # Create a new window on top of the main one
    pop = tk.Toplevel(root)
    pop.title("Today's Tasks")
    pop.geometry("500x400")
    pop.configure(bg=WHITE_BG)
    pop.resizable(False, False)

    t = tk.Label(pop, text="📅 Today's Tasks", font=("Arial", 14, "bold"),
                 bg=WHITE_BG, fg=BLACK)
    t.pack(pady=10)

    # Scrollable area for tasks
    f = tk.Frame(pop, bg=WHITE_BG)
    f.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    c = tk.Canvas(f, bg=WHITE_BG, highlightthickness=0)
    sb = tk.Scrollbar(f, orient="vertical", command=c.yview)
    inner = tk.Frame(c, bg=WHITE_BG)

    inner.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
    c.create_window((0, 0), window=inner, anchor="nw")
    c.configure(yscrollcommand=sb.set)

    c.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    # List the tasks
    for i, tsk in enumerate(today_tasks, 1):
        tf = tk.Frame(inner, bg=WHITE_BG, bd=1, relief="solid")
        tf.pack(fill="x", pady=5, padx=5)

        d = tk.Label(tf, text=f"{i}. {tsk['description']}", font=("Arial", 11),
                     bg=WHITE_BG, fg=BLACK, anchor="w", justify="left")
        d.pack(fill="x", padx=10, pady=5)

        df = tk.Frame(tf, bg=WHITE_BG)
        df.pack(fill="x", padx=10, pady=(0, 5))

        if tsk["repeat_type"] == "specific":
            dt = f"Date: {tsk['date']}"
        else:
            dt = f"Repeats: Every {tsk['date']}"

        tk.Label(df, text=dt, font=("Arial", 9), bg=WHITE_BG, fg="gray").pack(side="left", padx=(0, 15))
        tk.Label(df, text=f"Time: {tsk['time_estimate']}h", font=("Arial", 9), bg=WHITE_BG, fg="gray").pack(side="left")

        if tsk["category"] != "None":
            gf = tk.Frame(tf, bg=WHITE_BG)
            gf.pack(fill="x", padx=10, pady=(0, 5))
            tk.Label(gf, text=f"Related Goal: {tsk['category']}", font=("Arial", 9),
                     bg=WHITE_BG, fg="blue").pack(anchor="w")


# --- Main Tasks Page ---
def show_tasks_page(content_frame, profile, data, update_today_tasks_callback=None):
    tasks = profile["daily_tasks"]
    goals = profile["career_goals"]

    main = tk.Frame(content_frame, bg=WHITE_BG)
    main.pack(fill="both", expand=True, padx=10, pady=10)

    title = tk.Frame(main, bg=WHITE_BG)
    title.pack(fill="x", pady=(0, 10))

    tk.Label(title, text="📅 Task Planner", font=("Arial", 16, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(anchor="w")

    ttk.Separator(main, orient="horizontal").pack(fill="x", pady=5)

    cont = tk.Frame(main, bg=WHITE_BG)
    cont.pack(fill="both", expand=True)

    # --- Left Side: Input Form ---
    left = tk.Frame(cont, bg=WHITE_BG, bd=2, relief="solid")
    left.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)

    form = tk.Frame(left, bg=WHITE_BG)
    form.pack(fill="x", padx=15, pady=15)

    # Description Input
    tk.Label(form, text="Task Description:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=0, column=0, sticky="w", padx=5, pady=8)
    task_entry = tk.Entry(form, font=("Arial", 11), bd=2, relief="solid", width=35)
    task_entry.grid(row=0, column=1, sticky="we", padx=5, pady=8)

    # Schedule Type (One time vs Repeating)
    tk.Label(form, text="Schedule Type:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=1, column=0, sticky="w", padx=5, pady=8)
    date_type_var = tk.StringVar(value="Specific Date")
    date_type_combo = ttk.Combobox(form, textvariable=date_type_var,
                                   values=["Specific Date", "Weekly"], state="readonly", width=35)
    date_type_combo.grid(row=1, column=1, sticky="we", padx=5, pady=8)

    date_frame = tk.Frame(form, bg=WHITE_BG)
    date_frame.grid(row=2, column=1, sticky="w", padx=5, pady=8)

    # Change the date input based on type (Calendar vs "Every Monday")
    def update_date_frame():
        for w in date_frame.winfo_children():
            w.destroy()

        if date_type_var.get() == "Specific Date":
            dp = DatePicker(date_frame, datetime.now().strftime("%Y-%m-%d"))
            dp.pack(anchor="w")
            date_frame.dp = dp
        else:
            tk.Label(date_frame, text="Every:", font=("Arial", 11),
                     bg=WHITE_BG, fg=BLACK).pack(side="left")
            day_var = tk.StringVar(value="Monday")
            day_combo = ttk.Combobox(date_frame, textvariable=day_var,
                                     values=["Monday", "Tuesday", "Wednesday", "Thursday",
                                             "Friday", "Saturday", "Sunday"],
                                     state="readonly", width=15)
            day_combo.pack(side="left", padx=(5, 0))
            date_frame.day_var = day_var

    date_type_combo.bind("<<ComboboxSelected>>", lambda e: update_date_frame())
    update_date_frame()

    tk.Label(form, text="Date/Time:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=2, column=0, sticky="w", padx=5, pady=8)

    # Link to a Career Goal
    tk.Label(form, text="Related Goal:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=3, column=0, sticky="w", padx=5, pady=8)

    category_var = tk.StringVar(value="None")

    def refresh_goals():
        arr = ["None"] + [g["title"] for g in goals if g.get("status") != "Completed"]
        category_combo["values"] = arr

    category_combo = ttk.Combobox(form, textvariable=category_var, state="readonly", width=35)
    category_combo.grid(row=3, column=1, sticky="we", padx=5, pady=8)
    refresh_goals()

    # Time Estimate Input
    tk.Label(form, text="Time Estimate (hours):", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=4, column=0, sticky="w", padx=5, pady=8)
    time_entry = tk.Entry(form, font=("Arial", 11), bd=2, relief="solid", width=35)
    time_entry.grid(row=4, column=1, sticky="we", padx=5, pady=8)

    edit_mode = False
    current_id = None

    # Function: Add or Save Task
    def add_task():
        nonlocal edit_mode, current_id

        desc = task_entry.get().strip()
        cat = category_var.get()
        time_val = time_entry.get().strip()

        if not desc:
            messagebox.showerror("Error", "Please fill in Task Description")
            return

        if date_type_var.get() == "Specific Date":
            if not hasattr(date_frame, "dp"):
                update_date_frame()
            ok, err = date_frame.dp.validate_date()
            if not ok:
                messagebox.showerror("Error", err)
                return
            d = date_frame.dp.get_date()
            r = "specific"
        else:
            if not hasattr(date_frame, "day_var"):
                update_date_frame()
            d = date_frame.day_var.get()
            r = "weekly"

        # Check for duplicate tasks
        dup = None
        if edit_mode:
            for tsk in tasks:
                if tsk["id"] == current_id:
                    continue
                if tsk["description"] == desc and tsk["date"] == d and tsk["repeat_type"] == r:
                    dup = tsk
                    break
        else:
            for tsk in tasks:
                if tsk["description"] == desc and tsk["date"] == d and tsk["repeat_type"] == r:
                    dup = tsk
                    break

        if dup:
            if r == "specific":
                messagebox.showwarning("Warning", f"A task with the same description already exists for {d}")
            else:
                messagebox.showwarning("Warning", f"A task with the same description already exists for every {d}")
            return

        if edit_mode:
            for tsk in tasks:
                if tsk["id"] == current_id:
                    tsk["description"] = desc
                    tsk["date"] = d
                    tsk["repeat_type"] = r
                    tsk["category"] = cat
                    tsk["time_estimate"] = time_val
                    break
            save_data(data)
            refresh()
            clear_form()
            edit_mode = False
            current_id = None
            add_btn.config(text="Add Task")
            messagebox.showinfo("Success", "Task updated successfully!")
        else:
            new_id = max([x["id"] for x in tasks], default=0) + 1
            tasks.append({
                "id": new_id,
                "description": desc,
                "date": d,
                "repeat_type": r,
                "category": cat,
                "time_estimate": time_val,
                "completed": False,
                "created_date": datetime.now().strftime("%Y-%m-%d")
            })
            save_data(data)
            refresh()
            clear_form()
            messagebox.showinfo("Success", "Task added successfully!")

        if update_today_tasks_callback:
            update_today_tasks_callback()

    def clear_form():
        task_entry.delete(0, "end")
        time_entry.delete(0, "end")
        category_var.set("None")
        date_type_var.set("Specific Date")
        update_date_frame()

    # Function: Edit existing task
    def edit_task():
        nonlocal edit_mode, current_id

        sel = tasks_list.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a Task to edit")
            return

        idx = sel[0]
        if idx < len(shown):
            tsk = shown[idx]
            for x in tasks:
                if x["id"] == tsk["id"]:
                    task_entry.delete(0, "end")
                    task_entry.insert(0, x["description"])
                    time_entry.delete(0, "end")
                    time_entry.insert(0, x["time_estimate"])
                    category_var.set(x["category"])

                    if x["repeat_type"] == "specific":
                        date_type_var.set("Specific Date")
                        update_date_frame()
                        date_frame.dp.set_date(x["date"])
                    else:
                        date_type_var.set("Weekly")
                        update_date_frame()
                        date_frame.day_var.set(x["date"])

                    edit_mode = True
                    current_id = x["id"]
                    add_btn.config(text="Update Task")
                    break

    btn_box = tk.Frame(form, bg=WHITE_BG)
    btn_box.grid(row=5, column=0, columnspan=2, pady=20, sticky="e")

    add_btn = tk.Button(btn_box, text="Add Task", font=("Arial", 11, "bold"),
                        bg=PINK_MAIN, fg=BLACK, bd=2, relief="solid",
                        command=add_task)
    add_btn.pack(side="right", padx=5)

    edit_btn = tk.Button(btn_box, text="Edit Selected", font=("Arial", 11),
                         bg=BLUE_MAIN, fg=BLACK, bd=2, relief="solid",
                         command=edit_task)
    edit_btn.pack(side="right", padx=5)

    # --- Right Side: Task List ---
    right = tk.Frame(cont, bg=WHITE_BG, bd=2, relief="solid")
    right.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=5)

    hdr = tk.Frame(right, bg=WHITE_BG)
    hdr.pack(fill="x", padx=10, pady=10)
    tk.Label(hdr, text="All Tasks:", font=("Arial", 12, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(side="left")

    lst_box = tk.Frame(right, bg=WHITE_BG)
    lst_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    tasks_list = tk.Listbox(lst_box, font=("Arial", 11), bd=2, relief="solid",
                            selectbackground=BLUE_LIGHT, selectforeground=BLACK,
                            highlightthickness=0, selectmode="single")
    tasks_list.pack(side="left", fill="both", expand=True)

    sb2 = tk.Scrollbar(lst_box, orient="vertical", command=tasks_list.yview)
    sb2.pack(side="left", fill="y")
    tasks_list.config(yscrollcommand=sb2.set)

    ctrl = tk.Frame(right, bg=WHITE_BG)
    ctrl.pack(fill="x", padx=10, pady=(0, 10))

    shown = []

    # Update list display
    def refresh():
        nonlocal shown
        tasks_list.delete(0, "end")
        shown = []
        for tsk in sorted(tasks, key=lambda x: x["created_date"], reverse=True):
            st = "✓" if tsk["completed"] else "○"
            cs = "🎯" if tsk["category"] != "None" else "📝"
            if tsk["repeat_type"] == "specific":
                ds = tsk["date"]
            else:
                ds = f"Every {tsk['date']}"

            line = f"{st} {cs} {ds[:15]:15} {tsk['description'][:30]:30} ({tsk['time_estimate']}h)"
            tasks_list.insert("end", line)
            shown.append(tsk)

    # Mark as Done
    def mark_done():
        sel = tasks_list.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a Task")
            return

        idx = sel[0]
        if idx < len(shown):
            tsk = shown[idx]
            for x in tasks:
                if x["id"] == tsk["id"]:
                    x["completed"] = True
                    save_data(data)
                    refresh()
                    messagebox.showinfo("Success", "Task marked as completed!")
                    if update_today_tasks_callback:
                        update_today_tasks_callback()
                    return

    # Delete Task
    def delete_task():
        sel = tasks_list.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a Task")
            return

        if not messagebox.askyesno("Delete Task", "Are you sure you want to delete this Task?"):
            return

        idx = sel[0]
        if idx < len(shown):
            tsk = shown[idx]
            for i, x in enumerate(tasks):
                if x["id"] == tsk["id"]:
                    del tasks[i]
                    save_data(data)
                    refresh()

                    if edit_mode and current_id == x["id"]:
                        edit_mode = False
                        current_id = None
                        add_btn.config(text="Add Task")
                        clear_form()

                    messagebox.showinfo("Success", "Task deleted successfully!")
                    if update_today_tasks_callback:
                        update_today_tasks_callback()
                    return

    mark_btn = tk.Button(ctrl, text="Mark Complete", font=("Arial", 11),
                         bg=BLUE_MAIN, fg=BLACK, bd=2, relief="solid",
                         command=mark_done, width=15)
    mark_btn.pack(side="left", padx=5)

    del_btn = tk.Button(ctrl, text="Delete Task", font=("Arial", 11),
                        bg=WHITE_BG, fg="red", bd=2, relief="solid",
                        command=delete_task, width=15)
    del_btn.pack(side="left", padx=5)

    refresh()