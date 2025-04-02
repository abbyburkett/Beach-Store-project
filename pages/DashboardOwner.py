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

    def display_widgets(self):
        super().display_widgets()

    def hide_indicator(self):
        super().hide_indicator()

    def show_invoices(self):
        super().show_invoices()

    def insert_invoice(self):
        super().insert_invoice()

    def load_invoices(self):
        super().load_invoices()

    def show_employees(self):
        super().show_employees()

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

        # Add logic to calculate and update revenue dynamically

    def create_employee(self):
        super().create_employee()

    def update_employee(self):
        super().update_employee()

    def delete_employee(self):
        super().delete_employee()

    def on_employee_select(self, event):
        super().on_employee_select()


