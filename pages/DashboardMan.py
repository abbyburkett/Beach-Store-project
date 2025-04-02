import tkinter as tk
from tkinter import ttk
from logics import dashboard_functions
from pages.DashboardEmp import DashboardEmployee
from tkinter import messagebox

BACKGROUND_COLOR = "#FFF6E3"
SIDE_BAR_COLOR = "pink"
MAIN_CONTENT_COLOR = "green"

SIDEBAR_TEXT_COLOR = "black"

class DashboardManager(DashboardEmployee):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.is_manager = True

        # self.location_list = ["Aloha", "Olaho", "Olaola"]
        # self.selected_location = tk.StringVar()
        # self.selected_location.set(self.location_list[0])

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

        # Details and Data Section
        container_frame = tk.Frame(self.manage_employees_page)
        container_frame.pack(fill="both", expand=True)

        detail_frame = tk.LabelFrame(container_frame, text="Enter Details", font=("Helvetica", 16, "bold"))
        detail_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        data_frame = tk.LabelFrame(container_frame, text="Employee Data", font=("Helvetica", 16, "bold"))
        data_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        container_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_columnconfigure(1, weight=10)
        container_frame.grid_rowconfigure(0, weight=1)

        # Username
        self.username_label = tk.Label(detail_frame, text="Username", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.username_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

        self.username_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.username_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="w")

        # First Name
        self.fname_label = tk.Label(detail_frame, text="First Name", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.fname_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")

        self.fname_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.fname_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="w")

        # Last Name
        self.lname_label = tk.Label(detail_frame, text="Last Name", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.lname_label.grid(row=4, column=0, padx=5, pady=(5, 0), sticky="w")

        self.lname_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.lname_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="w")

        # Password
        self.password_label = tk.Label(detail_frame, text="Password", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.password_label.grid(row=6, column=0, padx=5, pady=(5, 0), sticky="w")

        self.password_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.password_entry.grid(row=7, column=0, padx=5, pady=(0, 10), sticky="w")

        # Pay Rate
        self.pay_rate_label = tk.Label(detail_frame, text="Pay Rate", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.pay_rate_label.grid(row=8, column=0, padx=5, pady=(5, 0), sticky="w")

        self.pay_rate_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.pay_rate_entry.grid(row=9, column=0, padx=5, pady=(0, 10), sticky="w")

        #Buttons
        buttons_frame = tk.Frame(detail_frame, bg=BACKGROUND_COLOR)
        buttons_frame.grid(row=10, column=0, columnspan=2, pady=2)

        self.add_employee_btn = tk.Button(buttons_frame, text="Add", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.create_employee)
        self.add_employee_btn.pack(side="left", padx=2)

        self.update_employee_btn = tk.Button(buttons_frame, text="Update", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.update_employee)
        self.update_employee_btn.pack(side="left", padx=2) 

        self.delete_employee_btn = tk.Button(buttons_frame, text="Delete", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command = self.delete_employee)
        self.delete_employee_btn.pack(side="left", padx=2)

        #Data Views
        self.data_view = ttk.Treeview(data_frame, columns=("UserName", "First Name", "Last Name", "Role", "Pay Rate"), show="headings", height=10)
        self.data_view.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.data_view.heading("UserName", text="Username")
        self.data_view.heading("First Name", text="First Name")
        self.data_view.heading("Last Name", text="Last Name")
        self.data_view.heading("Role", text="Role")
        self.data_view.heading("Pay Rate", text="Pay Rate")

        self.data_view.column("UserName", width=100)
        self.data_view.column("First Name", width=100)
        self.data_view.column("Last Name", width=100)
        self.data_view.column("Role", width=80)
        self.data_view.column("Pay Rate", width=100)

        self.data_view.bind('<<TreeviewSelect>>', self.on_employee_select)

        employee_data = dashboard_functions.get_all_Emp_data()
        
        for item in self.data_view.get_children():
            self.data_view.delete(item)

        for emp in employee_data:
            self.data_view.insert("", "end", values=emp)

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
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        try:
            pay_rate = float(self.pay_rate_entry.get())

        except ValueError:
            messagebox.showerror("Invalid Input", "Error: Pay rate must be a valid number.")
            print("Error: Pay rate must be a valid number.")

        
        success = dashboard_functions.createEmployee(username, password, fname, lname, pay_rate)

        if success:
            messagebox.showinfo("Success", "Employee successfully registered!")
        else:
            messagebox.showerror("Registration Failed", "Error: Could not register employee.")

    def update_employee(self):
        selected_item = self.data_view.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an employee to update.")
            return

        employee_username = self.data_view.item(selected_item)["values"][0]
        
        new_fname = self.fname_entry.get()
        new_lname = self.lname_entry.get()
        
        try:
            new_pay_rate = float(self.pay_rate_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Pay rate must be a valid number.")
            return

        result = messagebox.askyesno("Update Employee", f"Are you sure you want to update employee {employee_username}?")
        if result:
            if dashboard_functions.update_employee_in_db(employee_username, new_fname, new_lname, new_pay_rate):
                self.data_view.item(selected_item, values=(employee_username, new_fname, new_lname, "Employee", new_pay_rate))
                messagebox.showinfo("Success", "Employee updated successfully.")
            else:
                messagebox.showerror("Error", "Failed to update employee.")

    def delete_employee(self):
        selected_item = self.data_view.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an employee to delete.")
            return

        employee_username = self.data_view.item(selected_item)["values"][0]
        
        # Confirm deletion
        result = messagebox.askyesno("Delete Employee", f"Are you sure you want to delete employee {employee_username}?")
        if result:
            if dashboard_functions.delete_employee_from_db(employee_username):
                self.data_view.delete(selected_item)
                messagebox.showinfo("Success", "Employee deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete employee.")

    def on_employee_select(self, event):
        selected_item = self.data_view.selection()
    
        if selected_item:
            employee_data = self.data_view.item(selected_item)["values"]

            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, employee_data[0])  # Username

            self.fname_entry.delete(0, tk.END)
            self.fname_entry.insert(0, employee_data[1])  # First Name

            self.lname_entry.delete(0, tk.END)
            self.lname_entry.insert(0, employee_data[2])  # Last Name

            self.pay_rate_entry.delete(0, tk.END)
            self.pay_rate_entry.insert(0, employee_data[4])  # Pay Rate