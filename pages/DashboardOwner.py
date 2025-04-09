import tkinter as tk
from tkinter import ttk
from logics import dashboard_functions
from tkinter import messagebox
from pages.DashboardMan import DashboardManager
import mysql.connector

BACKGROUND_COLOR = "#FFF6E3"
SIDE_BAR_COLOR = "pink"
MAIN_CONTENT_COLOR = "green"

SIDEBAR_TEXT_COLOR = "black"

class Dashboard_Owner(DashboardManager):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.is_owner = True

        # Establish database connection
        self.db = dashboard_functions.create_db_connection()
        if self.db is None:
            messagebox.showerror("Database Error", "Database Error")
        else:
            self.cursor = self.db.cursor()

        self.dashboard_label.config(text=f"Welcome to the Owner Dashboard")

    def create_widgets(self):
        super().create_widgets()

        self.location_indicate = tk.Label(self.side_bar, text="", bg=SIDE_BAR_COLOR)
        self.location_btn = tk.Button(self.side_bar, text="Location", font=("Bold", 15), bd=0, fg=SIDEBAR_TEXT_COLOR, command=lambda: self.indicate(self.location_indicate, self.show_locations))

    def display_widgets(self):
        super().display_widgets()

        self.location_btn.place(x=10, y=350)
        self.location_indicate.place(x=3, y=350, width=5, height=25)

    def hide_indicator(self):
        super().hide_indicator()
        self.location_indicate.config(bg = SIDE_BAR_COLOR)

    def show_reports(self):
        super().show_reports()
        # Clear previous content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        reports_label = tk.Label(self.main_content, text="Owner Reports", font=("Helvetica", 16, "bold"))
        reports_label.pack(pady=10)

        # Example: Show Total Revenue
        revenue_label = tk.Label(self.main_content, text="Total Revenue: $0.00", font=("Helvetica", 12))
        revenue_label.pack()

    def show_locations(self):
        self.locations_page = tk.Frame(self.main_content)
        self.locations_page.pack(fill="both", expand=True)

        self.location_label = tk.Label(self.locations_page, text="Add Location", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        self.location_label.pack(pady=10)

        container_frame = tk.Frame(self.locations_page)
        container_frame.pack(fill="both", expand=True)

        detail_frame = tk.LabelFrame(container_frame, text="Enter Details", font=("Helvetica", 16, "bold"))
        detail_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        data_frame = tk.LabelFrame(container_frame, text="Location Data", font=("Helvetica", 16, "bold"))
        data_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        container_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_columnconfigure(1, weight=10)
        container_frame.grid_rowconfigure(0, weight=1)


        # Location Name
        self.location_name_label = tk.Label(detail_frame, text="Location Name", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.location_name_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

        self.location_name_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.location_name_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="w")

        # Address
        self.address_label = tk.Label(detail_frame, text="Address", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.address_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")

        self.address_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.address_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="w")

        # ManagerID
        self.manager_label = tk.Label(detail_frame, text="Last Name", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.manager_label.grid(row=4, column=0, padx=5, pady=(5, 0), sticky="w")

        self.manager_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.manager_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="w")

        buttons_frame = tk.Frame(detail_frame, bg=BACKGROUND_COLOR)
        buttons_frame.grid(row=12, column=0, columnspan=2, pady=2)

        self.add_location_btn = tk.Button(buttons_frame, text="Add", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.create_employee)
        self.add_location_btn.pack(side="left", padx=2)

        self.update_location_btn = tk.Button(buttons_frame, text="Update", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.update_employee)
        self.update_location_btn.pack(side="left", padx=2) 

        self.delete_location_btn = tk.Button(buttons_frame, text="Delete", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command = self.delete_employee)
        self.delete_location_btn.pack(side="left", padx=2)