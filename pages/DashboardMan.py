import tkinter as tk
from tkinter import ttk
from logics import dashboard_functions
from pages.DashboardEmp import DashboardEmployee
from tkinter import messagebox
import mysql.connector

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

        #Establish database connection
        self.db = dashboard_functions.create_db_connection()
        if self.db is None:
            messagebox.showerror("Database Error", "Database Error")
        else:
            self.cursor = self.db.cursor()

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
        #Clear previous frame if it exists
        for widget in self.main_content.winfo_children():
            widget.destroy()

        self.invoices_page = tk.Frame(self.main_content)
        self.invoices_page.pack(fill="both", expand=True)

        #Title label
        self.invoices_label = tk.Label(self.invoices_page, text="Invoices", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        self.invoices_label.pack(pady=10)

        # Table to display invoices
        self.tree = ttk.Treeview(self.invoices_page, columns=("InvoiceNumber","Date", "Company", "AmountTotal", "AmountPaid", "DueDate", "PaidWay", "Paid"),
                                 show="headings")
        self.tree.heading("InvoiceNumber", text= "Invoice Number")
        self.tree.heading("Date", text="Date Received")
        self.tree.heading("Company", text="Company")
        self.tree.heading("AmountTotal", text="Amount")
        self.tree.heading("AmountPaid", text="Amount Paid")
        self.tree.heading("DueDate", text="Due Date")
        self.tree.heading("PaidWay", text="Paid Way")
        self.tree.heading("Paid", text="Status")


        self.tree.column("InvoiceNumber", width=80)
        self.tree.column("Date", width=80)
        self.tree.column("Company", width=150)
        self.tree.column("AmountTotal", width=80)
        self.tree.column("AmountPaid", width=80)
        self.tree.column("DueDate", width=100)
        self.tree.column("PaidWay", width=80)
        self.tree.column("Paid", width=80)

        self.tree.pack(pady=10)

        #Form to insert new invoice
        self.form_frame = tk.Frame(self.invoices_page)
        self.form_frame.pack(pady=10)

        tk.Label(self.form_frame, text="Company:").grid(row=0, column=0)
        self.company_entry = tk.Entry(self.form_frame)
        self.company_entry.grid(row=0, column=1)

        tk.Label(self.form_frame, text="Amount:").grid(row=0, column=2)
        self.amount_entry = tk.Entry(self.form_frame)
        self.amount_entry.grid(row=0, column=3)

        tk.Label(self.form_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0)
        self.due_date_entry = tk.Entry(self.form_frame)
        self.due_date_entry.grid(row=1, column=1)

        tk.Label(self.form_frame, text="Paid Way:").grid(row=0, column=4)
        self.payway_entry = tk.Entry(self.form_frame)
        self.payway_entry.grid(row=0, column=5)

        tk.Label(self.form_frame, text="Amount Paid:").grid(row=1, column=2)
        self.amount_paid_entry = tk.Entry(self.form_frame)
        self.amount_paid_entry.grid(row=1, column=3)

        #Submit button
        self.submit_button = tk.Button(self.invoices_page, text="Add Invoice", command=self.insert_invoice)
        self.submit_button.pack(pady=5)

        #Load existing invoices
        self.load_invoices()

    def insert_invoice(self):
        company = self.company_entry.get()
        amount = self.amount_entry.get()
        due_date = self.due_date_entry.get()
        payway = self.payway_entry.get()
        amount_paid = self.amount_paid_entry.get()


        if not (company and amount and due_date and payway and amount_paid ):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            #ensure amount is a valid float
            amount = float(amount)
            amount_paid = float(amount_paid)

            cursor = self.db.cursor()
            query = ("INSERT INTO Invoice (Company, AmountTotal, AmountPaid, PaidWay, DueDate)"
                     "VALUES (%s, %s, %s, %s, %s) ")
            cursor.execute(query, (company, amount, amount_paid, payway, due_date))
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Invoice Added", "Invoice Added")
            #Refresh invoice list
            self.load_invoices()
        except Exception as e:
            messagebox.showerror("Error", e)

    def load_invoices(self):
        """Fetch and display invoices from the database."""
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear existing entries

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT InvoiceNumber, Date, Company, AmountTotal, AmountPaid, DueDate, PaidWay, Paid FROM Invoice")
            invoices = cursor.fetchall()
            cursor.close()

            for invoice in invoices:
                invoice_number, date_received, company, amount, amount_paid, due_date, paid_way, status = invoice

                print(f"Date Received: {date_received}")
                amount = float(amount)
                amount_paid = float(amount_paid)

                #Displays date_received as only yy/mm/dd
                date_received = date_received.strftime("%Y-%m-%d")

                #Set the status of the invoice
                if amount_paid >= amount:
                    status = "Paid"
                elif amount_paid < amount:
                    status = "Partially Paid"
                else:
                    status = "Unpaid"

                if amount_paid > amount:
                    messagebox.showerror("Error", "Amount paid can't exceed total amount.")
                    return

                #Insert into treeview, adding the Date received (current date)
                self.tree.insert("", "end", values=(invoice_number, date_received, company, amount, amount_paid, due_date, paid_way, status))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

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

        # Pay Bonus
        self.pay_bonus_label = tk.Label(detail_frame, text="Pay Bonus", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.pay_bonus_label.grid(row=10, column=0, padx=5, pady=(5, 0), sticky="w")

        self.pay_bonus_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.pay_bonus_entry.grid(row=11, column=0, padx=5, pady=(0, 10), sticky="w")

        #Buttons
        buttons_frame = tk.Frame(detail_frame, bg=BACKGROUND_COLOR)
        buttons_frame.grid(row=12, column=0, columnspan=2, pady=2)

        self.add_employee_btn = tk.Button(buttons_frame, text="Add", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.create_employee)
        self.add_employee_btn.pack(side="left", padx=2)

        self.update_employee_btn = tk.Button(buttons_frame, text="Update", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.update_employee)
        self.update_employee_btn.pack(side="left", padx=2) 

        self.delete_employee_btn = tk.Button(buttons_frame, text="Delete", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command = self.delete_employee)
        self.delete_employee_btn.pack(side="left", padx=2)

        #Data Views
        self.data_view = ttk.Treeview(data_frame, columns=("UserName", "First Name", "Last Name", "Role", "Pay Rate", "Pay Bonus"), show="headings", height=10)
        self.data_view.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.data_view.heading("UserName", text="Username")
        self.data_view.heading("First Name", text="First Name")
        self.data_view.heading("Last Name", text="Last Name")
        self.data_view.heading("Role", text="Role")
        self.data_view.heading("Pay Rate", text="Pay Rate")
        self.data_view.heading("Pay Bonus", text="Pay Bonus")

        self.data_view.column("UserName", width=100)
        self.data_view.column("First Name", width=100)
        self.data_view.column("Last Name", width=100)
        self.data_view.column("Role", width=80)
        self.data_view.column("Pay Rate", width=80)
        self.data_view.column("Pay Bonus", width=80)

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
            pay_bonus = float(self.pay_bonus_entry.get())

        except ValueError:
            messagebox.showerror("Invalid Input", "Error: Pay rate must be a valid number.")
            print("Error: Pay rate must be a valid number.")

        
        success = dashboard_functions.create_employee(username, password, fname, lname, pay_rate, pay_bonus)

        if success:
            messagebox.showinfo("Success", "Employee successfully registered!")
            self.show_employees()
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
            new_bonus_rate = float(self.pay_rate_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Pay rate must be a valid number.")
            return

        result = messagebox.askyesno("Update Employee", f"Are you sure you want to update employee {employee_username}?")
        if result:
            if dashboard_functions.update_employee_in_db(employee_username, new_fname, new_lname, new_pay_rate, new_bonus_rate):
                self.data_view.item(selected_item, values=(employee_username, new_fname, new_lname, "Employee", new_pay_rate, new_bonus_rate))
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
