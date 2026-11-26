import tkinter as tk
from tkinter import ttk, messagebox
import random
from component import save_data
from datetime import datetime

PINK_MAIN = "#ffc0cb"
BLUE_MAIN = "#8ec5fc"
PINK_LIGHT = "#ffe4f0"
BLUE_LIGHT = "#d6ecff"
WHITE_BG = "#ffffff"
BLACK = "#000000"

def show_interview_page(content_frame, profile, data):
    # Load interview questions
    qas = profile["interview_qas"]

    # Setup main screen
    main = tk.Frame(content_frame, bg=WHITE_BG)
    main.pack(fill="both", expand=True, padx=10, pady=10)

    t_frame = tk.Frame(main, bg=WHITE_BG)
    t_frame.pack(fill="x", pady=(0, 8))
    tk.Label(t_frame, text="💬 Interview Preparation", font=("Arial", 14, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(anchor="w")

    ttk.Separator(main, orient="horizontal").pack(fill="x", pady=3)

    # --- Top Section: Tips and Adding Questions ---
    top = tk.Frame(main, bg=WHITE_BG)
    top.pack(fill="x", pady=8, padx=5)

    # --- Tips Box (Left) ---
    tips_box = tk.Frame(top, bg=WHITE_BG, bd=1, relief="solid")
    tips_box.pack(side="left", fill="both", expand=True, padx=(0, 8))

    tips_in = tk.Frame(tips_box, bg=WHITE_BG)
    tips_in.pack(fill="both", expand=True, padx=8, pady=8)

    tk.Label(tips_in, text="💡 Tips", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(anchor="w", pady=(0, 6))

    # A list of helpful advice strings
    tips = [
        "Research the company and role before interview.",
        "Prepare 2-3 stories showing problem-solving skills.",
        "Practice answering common questions out loud.",
        "Review your projects and be ready to explain them.",
        "Prepare 2-3 questions to ask the interviewer.",
        "Arrive early, test equipment for online interviews.",
        "Be honest about experience, focus on learning.",
        "Highlight achievements with specific results.",
        "Link skills to job requirements.",
        "Thank interviewer for their time."
    ]

    # Pick a random tip to start
    cur = random.randint(0, len(tips) - 1)

    tip_frame = tk.Frame(tips_in, bg=BLUE_LIGHT, bd=1, relief="solid", height=70)
    tip_frame.pack(fill="both", expand=True)
    tip_frame.pack_propagate(False)

    tip_lbl = tk.Label(tip_frame, text=tips[cur], font=("Arial", 9),
                       bg=BLUE_LIGHT, fg=BLACK, wraplength=320,
                       justify="left", padx=8, pady=8)
    tip_lbl.pack(fill="both", expand=True)

    btns = tk.Frame(tips_in, bg=WHITE_BG)
    btns.pack(fill="x", pady=(2, 0))

    # Function to pick a new random tip
    def random_tip():
        nonlocal cur
        new = cur
        while new == cur and len(tips) > 1:
            new = random.randint(0, len(tips) - 1)
        cur = new
        tip_lbl.config(text=tips[cur])

    tk.Button(btns, text="🎲 Random", font=("Arial", 9),
              bg=PINK_MAIN, fg=BLACK, bd=1, relief="solid",
              command=random_tip, width=10).pack(side="left", padx=(0, 5))

    # Function to show the next tip in the list
    def next_tip():
        nonlocal cur
        cur = (cur + 1) % len(tips)
        tip_lbl.config(text=tips[cur])

    tk.Button(btns, text="⏭️ Next", font=("Arial", 9),
              bg=WHITE_BG, fg=BLACK, bd=1, relief="solid",
              command=next_tip, width=8).pack(side="left")

    # --- Add Q&A Box (Right) ---
    qa_box = tk.Frame(top, bg=WHITE_BG, bd=1, relief="solid")
    qa_box.pack(side="right", fill="both", expand=True)

    qa_in = tk.Frame(qa_box, bg=WHITE_BG)
    qa_in.pack(fill="both", expand=True, padx=8, pady=8)

    tk.Label(qa_in, text="➕ Add Q&A", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(anchor="w", pady=(0, 6))

    # Question Input
    qi = tk.Frame(qa_in, bg=WHITE_BG)
    qi.pack(fill="x", pady=(0, 5))
    tk.Label(qi, text="Q:", font=("Arial", 9, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(side="left", padx=(0, 5))
    q_entry = tk.Entry(qi, font=("Arial", 9), bd=1, relief="solid", width=35)
    q_entry.pack(side="left", fill="x", expand=True)

    # Answer Input
    ai = tk.Frame(qa_in, bg=WHITE_BG)
    ai.pack(fill="both", expand=True, pady=(0, 6))
    tk.Label(ai, text="A:", font=("Arial", 9, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(side="left", padx=(0, 5), anchor="n")
    a_text = tk.Text(ai, font=("Arial", 9), bd=1, relief="solid",
                     height=2, width=35)
    a_text.pack(side="left", fill="both", expand=True)

    # Function to save the new Q&A
    def add_qa():
        q = q_entry.get().strip()
        a = a_text.get("1.0", "end").strip()
        if not q:
            messagebox.showerror("Error", "Please enter a question")
            return
        if not a:
            messagebox.showerror("Error", "Please enter an answer")
            return

        nid = max([x["id"] for x in qas], default=0) + 1
        qas.append({
            "id": nid,
            "question": q,
            "answer": a,
            "added_date": datetime.now().strftime("%Y-%m-%d")
        })
        save_data(data)
        refresh()
        q_entry.delete(0, "end")
        a_text.delete("1.0", "end")
        messagebox.showinfo("Success", "Q&A added!")

    tk.Button(qa_in, text="➕ Add", font=("Arial", 9, "bold"),
              bg=PINK_MAIN, fg=BLACK, bd=1, relief="solid",
              command=add_qa, width=8).pack(pady=(4, 0))

    def clear_form():
        q_entry.delete(0, "end")
        a_text.delete("1.0", "end")

    # --- Bottom Section: List of Questions and Answer Reveal ---
    bottom = tk.Frame(main, bg=WHITE_BG)
    bottom.pack(fill="both", expand=True, pady=(5, 0))

    # List of Questions
    qs_box = tk.Frame(bottom, bg=WHITE_BG, bd=1, relief="solid")
    qs_box.pack(fill="both", expand=True, pady=(0, 5))

    qs_in = tk.Frame(qs_box, bg=WHITE_BG)
    qs_in.pack(fill="both", expand=True, padx=8, pady=8)

    tk.Label(qs_in, text="📋 Questions", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(anchor="w", pady=(0, 6))

    qs_list = tk.Listbox(qs_in, font=("Arial", 9), bd=1, relief="solid",
                         bg=WHITE_BG, selectbackground=PINK_LIGHT,
                         selectforeground=BLACK, highlightthickness=0,
                         selectmode="single", activestyle="none", height=4)
    qs_list.pack(fill="both", expand=True, pady=(0, 6))

    sb = tk.Scrollbar(qs_list, orient="vertical", command=qs_list.yview)
    sb.pack(side="right", fill="y")
    qs_list.config(yscrollcommand=sb.set)

    # Answer Reveal Area
    ans_box = tk.Frame(bottom, bg=WHITE_BG, bd=1, relief="solid")
    ans_box.pack(fill="both", expand=True, pady=(5, 0))

    ans_in = tk.Frame(ans_box, bg=WHITE_BG)
    ans_in.pack(fill="both", expand=True, padx=8, pady=8)

    tk.Label(ans_in, text="📝 Answer", font=("Arial", 11, "bold"),
             bg=WHITE_BG, fg=BLACK).pack(anchor="w", pady=(0, 6))

    ans_txt = tk.Text(ans_in, font=("Arial", 9), bg=BLUE_LIGHT,
                      fg=BLACK, bd=1, relief="solid", wrap="word",
                      height=3, state="disabled")
    ans_txt.pack(fill="both", expand=True, pady=(0, 6))

    sb2 = tk.Scrollbar(ans_txt, orient="vertical",
                       command=ans_txt.yview)
    sb2.pack(side="right", fill="y")
    ans_txt.config(yscrollcommand=sb2.set)

    ctrl = tk.Frame(bottom, bg=WHITE_BG)
    ctrl.pack(fill="x", pady=(8, 0))

    def refresh():
        qs_list.delete(0, "end")
        for qa in sorted(qas, key=lambda x: x["id"]):
            qs_list.insert("end", qa["question"])

    # Show the answer when a question is clicked
    def show_ans(e=None):
        sel = qs_list.curselection()
        if not sel:
            return
        i = sel[0]
        if i < len(qas):
            qa = qas[i]
            ans_txt.config(state="normal")
            ans_txt.delete("1.0", "end")
            ans_txt.insert("1.0", qa["answer"])
            ans_txt.config(state="disabled")

    # Delete selected Q&A
    def del_qa():
        sel = qs_list.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a question")
            return
        if not messagebox.askyesno("Delete", "Delete this Q&A?"):
            return
        i = sel[0]
        if i < len(qas):
            del qas[i]
            save_data(data)
            refresh()
            ans_txt.config(state="normal")
            ans_txt.delete("1.0", "end")
            ans_txt.config(state="disabled")

    # Clear all Q&As
    def clear_all():
        if not qas:
            return
        if not messagebox.askyesno("Clear All", "Delete ALL Q&As?"):
            return
        qas.clear()
        save_data(data)
        refresh()
        ans_txt.config(state="normal")
        ans_txt.delete("1.0", "end")
        ans_txt.config(state="disabled")

    qs_list.bind("<<ListboxSelect>>", show_ans)

    # Control Buttons
    tk.Button(ctrl, text="🗑️ Delete", font=("Arial", 9),
              bg=WHITE_BG, fg="red", bd=1, relief="solid",
              command=del_qa, width=10).pack(side="left", padx=(0, 8))
    tk.Button(ctrl, text="🗑️ Clear All", font=("Arial", 9),
              bg=WHITE_BG, fg="orange", bd=1, relief="solid",
              command=clear_all, width=10).pack(side="left")
    tk.Button(ctrl, text="🗑️ Clear Form", font=("Arial", 9),
              bg=WHITE_BG, fg=BLACK, bd=1, relief="solid",
              command=clear_form, width=10).pack(side="right")

    refresh()
    random_tip()