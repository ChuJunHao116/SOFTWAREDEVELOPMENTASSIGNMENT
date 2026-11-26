import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from component import DatePicker, save_data

BLUE_MAIN = "#8ec5fc"
BLUE_LIGHT = "#d6ecff"
WHITE_BG = "#ffffff"
BLACK = "#000000"

def show_skills_page(content_frame, profile, data):
    # Get user's skills list
    skills = profile["skills_log"]

    # Setup main screen
    main = tk.Frame(content_frame, bg=WHITE_BG)
    main.pack(fill="both", expand=True, padx=10, pady=10)

    title_frame = tk.Frame(main, bg=WHITE_BG)
    title_frame.pack(fill="x", pady=(0, 10))

    t = tk.Label(title_frame, text="📚 Skills & Certifications Log",
                 font=("Arial", 16, "bold"), bg=WHITE_BG, fg=BLACK)
    t.pack(anchor="w")

    ttk.Separator(main, orient="horizontal").pack(fill="x", pady=5)

    ctn = tk.Frame(main, bg=WHITE_BG)
    ctn.pack(fill="both", expand=True)

    # --- Left Side: Input Form ---
    left = tk.Frame(ctn, bg=WHITE_BG, bd=2, relief="solid")
    left.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)

    form = tk.Frame(left, bg=WHITE_BG)
    form.pack(fill="x", padx=15, pady=15)

    # Name Input
    tk.Label(form, text="Skill/Course Name:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=0, column=0, sticky="w", padx=5, pady=8)
    name_entry = tk.Entry(form, font=("Arial", 11), bd=2, relief="solid", width=35)
    name_entry.grid(row=0, column=1, sticky="we", padx=5, pady=8)

    # Type Dropdown
    tk.Label(form, text="Type:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=1, column=0, sticky="w", padx=5, pady=8)
    type_var = tk.StringVar(value="Course")
    type_combo = ttk.Combobox(form, textvariable=type_var,
                              values=["Course", "Certification", "Workshop", "Skill", "Project"],
                              state="readonly", width=35)
    type_combo.grid(row=1, column=1, sticky="we", padx=5, pady=8)

    # Date Input
    tk.Label(form, text="Completion Date:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=2, column=0, sticky="w", padx=5, pady=8)

    dp_frame = tk.Frame(form, bg=WHITE_BG)
    dp_frame.grid(row=2, column=1, sticky="w", padx=5, pady=8)

    date_picker = DatePicker(dp_frame, datetime.now().strftime("%Y-%m-%d"))
    date_picker.pack(anchor="w")

    # Provider Input (e.g., Coursera)
    tk.Label(form, text="Provider/Platform:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=3, column=0, sticky="w", padx=5, pady=8)
    provider_entry = tk.Entry(form, font=("Arial", 11), bd=2, relief="solid", width=35)
    provider_entry.grid(row=3, column=1, sticky="we", padx=5, pady=8)

    # Description Input
    tk.Label(form, text="Description/Notes:", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).grid(row=4, column=0, sticky="nw", padx=5, pady=8)
    desc_text = tk.Text(form, font=("Arial", 10), height=3, width=35, bd=2, relief="solid")
    desc_text.grid(row=4, column=1, sticky="we", padx=5, pady=8)

    # Function to Add new Skill
    def add_skill():
        nm = name_entry.get().strip()
        tp = type_var.get()
        pv = provider_entry.get().strip()
        ds = desc_text.get("1.0", "end").strip()

        if not nm:
            messagebox.showerror("Error", "Please fill in Skill/Course Name")
            return

        ok, err = date_picker.validate_date()
        if not ok:
            messagebox.showerror("Error", err)
            return

        d = date_picker.get_date()

        # Check future date
        try:
            dt = datetime.strptime(d, "%Y-%m-%d")
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if dt > today:
                messagebox.showerror("Error", "Completion Date cannot be in the future")
                return
        except:
            messagebox.showerror("Error", "Invalid date format")
            return

        new_id = max([x["id"] for x in skills], default=0) + 1

        skills.append({
            "id": new_id,
            "name": nm,
            "type": tp,
            "completion_date": d,
            "provider": pv,
            "description": ds,
            "added_date": datetime.now().strftime("%Y-%m-%d")
        })

        save_data(data)
        refresh()
        
        # Clear form
        name_entry.delete(0, "end")
        provider_entry.delete(0, "end")
        desc_text.delete("1.0", "end")
        date_picker.set_date(datetime.now().strftime("%Y-%m-%d"))
        messagebox.showinfo("Success", "Skill/Certification added successfully!")

    btn_frame = tk.Frame(form, bg=WHITE_BG)
    btn_frame.grid(row=5, column=0, columnspan=2, pady=20, sticky="e")

    add_btn = tk.Button(btn_frame, text="Add Skill", font=("Arial", 11, "bold"),
                        bg=BLUE_MAIN, fg=BLACK, bd=2, relief="solid",
                        command=add_skill)
    add_btn.pack(side="right", padx=5)

    # --- Right Side: Skills List ---
    right = tk.Frame(ctn, bg=WHITE_BG, bd=2, relief="solid")
    right.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=5)

    header = tk.Frame(right, bg=WHITE_BG)
    header.pack(fill="x", padx=10, pady=10)

    tk.Label(header, text="My Skills & Certifications:",
             font=("Arial", 12, "bold"), bg=WHITE_BG, fg=BLACK).pack(side="left")

    lst_container = tk.Frame(right, bg=WHITE_BG)
    lst_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    lst = tk.Listbox(lst_container, font=("Arial", 11), bd=2, relief="solid",
                     selectbackground=BLUE_LIGHT, selectforeground=BLACK,
                     highlightthickness=0, selectmode="single")
    lst.pack(side="left", fill="both", expand=True)

    sb = tk.Scrollbar(lst_container, orient="vertical", command=lst.yview)
    sb.pack(side="left", fill="y")
    lst.config(yscrollcommand=sb.set)

    ctrl = tk.Frame(right, bg=WHITE_BG)
    ctrl.pack(fill="x", padx=10, pady=(0, 10))

    # Function to update the list display
    def refresh():
        lst.delete(0, "end")
        for s in sorted(skills, key=lambda x: x["completion_date"], reverse=True):
            # Choose an icon based on type
            symbol = "📚" if s["type"] == "Course" else (
                "📜" if s["type"] == "Certification" else
                "🛠️" if s["type"] == "Skill" else
                "📂" if s["type"] == "Project" else "🔹"
            )
            line = f"{symbol} {s['completion_date']:12} {s['type'][:15]:15} {s['name'][:25]:25} {s.get('provider','')[:15]:15}"
            lst.insert("end", line)

    # Function to delete selected item
    def delete_skill():
        sel = lst.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a Skill/Certification record")
            return

        if not messagebox.askyesno("Delete Record", "Are you sure you want to delete this Skill/Certification record?"):
            return

        txt = lst.get(sel[0])
        for i, s in enumerate(skills):
            if s["name"] in txt and s["completion_date"] in txt:
                del skills[i]
                save_data(data)
                refresh()
                messagebox.showinfo("Success", "Skill/Certification record deleted successfully!")
                return

    del_btn = tk.Button(ctrl, text="Delete Record", font=("Arial", 11),
                        bg=WHITE_BG, fg="red", bd=2, relief="solid",
                        command=delete_skill, width=15)
    del_btn.pack(side="left", padx=5)

    refresh()