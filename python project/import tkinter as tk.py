import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CondoManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Condominium A - Maintenance Management System")
        self.root.geometry("700x500")

        # Use ttk Notebook for a Tabbed Interface
        # This organizes the "Add" and "Search/Manage" requirements neatly.
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Create two main frames (Tabs)
        self.frame_report = ttk.Frame(self.notebook, width=680, height=480)
        self.frame_manage = ttk.Frame(self.notebook, width=680, height=480)

        self.frame_report.pack(fill='both', expand=True)
        self.frame_manage.pack(fill='both', expand=True)

        # Add tabs to notebook
        self.notebook.add(self.frame_report, text='Report New Incident')
        self.notebook.add(self.frame_manage, text='Search & Manage Incidents')

        # ==========================================
        # TAB 1: REPORT INCIDENT (Requirement: Add requests)
        # ==========================================
        tk.Label(self.frame_report, text="Report New Maintenance Issue", font=("Arial", 16, "bold")).pack(pady=15)

        # Form Layout
        form_frame = tk.Frame(self.frame_report)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Incident Type (e.g., Leaky Pipe):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_type = tk.Entry(form_frame, width=40)
        self.entry_type.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Location (e.g., Gym Lvl 1):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_loc = tk.Entry(form_frame, width=40)
        self.entry_loc.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Description:").grid(row=2, column=0, sticky="nw", pady=5)
        self.text_desc = tk.Text(form_frame, width=30, height=5)
        self.text_desc.grid(row=2, column=1, pady=5)

        # Submit Button
        btn_submit = tk.Button(self.frame_report, text="Submit Report", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_submit.pack(pady=20)

        # ==========================================
        # TAB 2: MANAGE INCIDENTS (Requirement: Search, Assign, Update)
        # ==========================================
        tk.Label(self.frame_manage, text="Maintenance Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(self.frame_manage)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search Request:").pack(side=tk.LEFT, padx=5)
        tk.Entry(search_frame, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search").pack(side=tk.LEFT)

        # List of Incidents (Treeview)
        cols = ('ID', 'Type', 'Location', 'Status', 'Assigned Vendor')
        tree = ttk.Treeview(self.frame_manage, columns=cols, show='headings', height=8)
        
        # Define headings
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Mock Data (To show what it looks like populated)
        tree.insert("", "end", values=("INC-101", "Elevator Fault", "Block A", "Pending", "Unassigned"))
        tree.insert("", "end", values=("INC-102", "Leaky Pipe", "Gym", "In Progress", "Express Plumbing"))
        tree.pack(pady=10)

        # Action Buttons
        btn_frame = tk.Frame(self.frame_manage)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Assign Vendor", width=15, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Update Status", width=15, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Generate Report", width=15, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CondoManagementSystem(root)
    root.mainloop()