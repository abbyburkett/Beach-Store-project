import tkinter as tk
from tkinter import ttk
from logics import dashboard_functions
from pages.DashboardEmp import DashboardEmployee

BACKGROUND_COLOR = "#FFF6E3"
SIDE_BAR_COLOR = "pink"
MAIN_CONTENT_COLOR = "green"

SIDEBAR_TEXT_COLOR = "black"

class DashboardManager(DashboardEmployee):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.is_manager = True

        self.location_list = ["Aloha", "Olaho", "Olaola"]
        self.selected_location = tk.StringVar()
        self.selected_location.set(self.location_list[0])

        self.dashboard_label.config(text=f"Welcome to the Manager Dashboard")
    def create_widgets(self):
        super().create_widgets()

        # Add additional manager-specific sidebar options
        self.invoice_indicate = tk.Label(self.side_bar, text="", bg=SIDE_BAR_COLOR)
        self.invoice_btn = tk.Button(self.side_bar, text="Invoices", font=("Bold", 15), bd=0, fg=SIDEBAR_TEXT_COLOR, command=lambda: self.indicate(self.invoice_indicate, self.show_invoices))

        self.employees_indicate = tk.Label(self.side_bar, text="", bg=SIDE_BAR_COLOR)
        self.employees_btn = tk.Button(self.side_bar, text="Manage Employees", font=("Bold", 15), bd=0, fg=SIDEBAR_TEXT_COLOR, command=lambda: self.indicate(self.employees_indicate, self.show_employees))

        self.report_indicate = tk.Label(self.side_bar, text="", bg=SIDE_BAR_COLOR)
        self.report_btn = tk.Button(self.side_bar, text="Report", font=("Bold", 15), bd=0, fg=SIDEBAR_TEXT_COLOR, command=lambda: self.indicate(self.report_indicate, self.show_reports))

    def display_widgets(self):
        super().display_widgets()

        self.invoice_btn.place(x=10, y=200)
        self.invoice_indicate.place(x=3, y=200, width=5, height=25)

        self.employees_btn.place(x=10, y=250)
        self.employees_indicate.place(x=3, y=250, width=5, height=25)

        self.report_btn.place(x=10, y=300)
        self.report_indicate.place(x=3, y=300, width=5, height=25)
    
    def hide_indicator(self):
        super().hide_indicator()
        self.invoice_indicate.config(bg = SIDE_BAR_COLOR)
        self.employees_indicate.config(bg = SIDE_BAR_COLOR)
        self.report_indicate.config(bg = SIDE_BAR_COLOR)

    def show_invoices(self):
        self.invoices_page = tk.Frame(self.main_content)
        self.invoices_page.pack(fill="both", expand=True)

        self.invoices_label = tk.Label(self.invoices_page, text="Invoices", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        self.invoices_label.pack(pady=10)

    def show_employees(self):
        self.manage_employees_page = tk.Frame(self.main_content)
        self.manage_employees_page.pack(fill="both", expand=True)

        self.manage_employees_label = tk.Label(self.manage_employees_page, text="Manage Employees", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        self.manage_employees_label.pack(pady=10)

        manage_label = tk.Label(self.manage_employees_page, text="Manage your employees here.", font=("Helvetica", 12))
        manage_label.pack(pady=20)

        self.username_label = tk.Label(self.manage_employees_page, text="Username", font=("Arial", 25, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.username_entry = tk.Entry(self.manage_employees_page, font=("Arial", 25, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.password_label = tk.Label(self.manage_employees_page, text="Password", font=("Arial", 25, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.password_entry = tk.Entry(self.manage_employees_page, font=("Arial", 25, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.create_employee_btn = tk.Button(self.manage_employees_page, text="Create Employee", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.create_employee)
        # self.location_menu = tk.OptionMenu(self.manage_employees_page, self.selected_location, *self.location_list)

        self.username_label.pack(pady=10)
        self.username_entry.pack(pady=10)
        self.password_label.pack(pady=10)
        self.password_entry.pack(pady=10)
        # self.location_menu.pack(pady=10)
        self.create_employee_btn.pack(pady=20)   

    def show_reports(self):
        self.reports_page = tk.Frame(self.main_content)
        self.reports_page.pack(fill="both", expand=True)

        self.reports_label = tk.Label(self.reports_page, text="Reports", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        self.reports_label.pack(pady=10)

        report_label = tk.Label(self.reports_page, text="Employee performance reports will be displayed here.", font=("Helvetica", 12))
        report_label.pack(pady=20)

    def create_employee(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # location = self.selected_location.get()

        dashboard_functions.createEmployee(username, password)