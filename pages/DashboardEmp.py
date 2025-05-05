import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import mysql

from logics import dashboard_functions

BACKGROUND_COLOR = "#FFF6E3"
SIDE_BAR_COLOR = "pink"
MAIN_CONTENT_COLOR = "green"

SIDEBAR_TEXT_COLOR = "black"

# code copy and learn from https://www.youtube.com/watch?v=95tJO7XJlko&t=581s

class DashboardEmployee(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.controller = controller
        self.user_id = None
        self.location = None
        self.today = controller.today
        self.create_widgets()
        self.display_widgets()

        self.isEmployee = True
        self.isManager = False
        self.isOwner = False

        self.clear_main_content()

    def set_user_data(self, user_id, location):
        self.user_id = user_id
        self.location = location
        self.show_home_page()  # Show home page after user data is set

    def create_widgets(self):
        self.dashboard_label = tk.Label(self, text=f"Welcome to the Employee Dashboard", font=("Arial", 40, "bold"), fg="#CDC1FF", bg=BACKGROUND_COLOR)

        self.side_bar = tk.Frame(self, bg = SIDE_BAR_COLOR)

        self.home_indicate = tk.Label(self.side_bar, text = "", bg = SIDE_BAR_COLOR)
        self.home_btn = tk.Button(self.side_bar, text = "Home", font = ("Bold", 15), bd = 0, fg = SIDEBAR_TEXT_COLOR, command = lambda: self.indicate(self.home_indicate, self.show_home_page))

        self.profile_indicate = tk.Label(self.side_bar, text = "", bg = SIDE_BAR_COLOR)
        self.profile_btn = tk.Button(self.side_bar, text = "Profile", font = ("Bold", 15), bd = 0, fg = SIDEBAR_TEXT_COLOR, command = lambda: self.indicate(self.profile_indicate, self.show_profile))

        self.close_out_indicate = tk.Label(self.side_bar, text = "", bg = SIDE_BAR_COLOR)
        self.close_out_btn = tk.Button(self.side_bar, text = "Close Out", font = ("Bold", 15), bd = 0, fg = SIDEBAR_TEXT_COLOR, command = lambda: self.indicate(self.close_out_indicate, self.show_close_out))
        
        self.log_out_indicate = tk.Label(self.side_bar, text = "", bg = SIDE_BAR_COLOR)
        self.log_out_btn = tk.Button(self.side_bar, text = "Log Out", font = ("Bold", 15), bd = 0, fg = SIDEBAR_TEXT_COLOR, command = self.handleLogout)

        self.main_content = tk.Frame(self, bg = MAIN_CONTENT_COLOR )


    def display_widgets(self):
        self.dashboard_label.pack(pady=20)

        self.side_bar.pack(side = tk.LEFT)
        self.side_bar.pack_propagate(False)
        self.side_bar.configure(width = 240, height = 720)

        self.home_btn.place(x = 10, y = 50)
        self.home_indicate.place(x = 3, y = 50, width = 5, height = 25)

        self.profile_btn.place(x = 10, y = 100)
        self.profile_indicate.place(x = 3, y = 100, width = 5, height = 25)

        self.close_out_btn.place(x = 10, y = 150)
        self.close_out_indicate.place(x = 3, y = 150, width = 5, height = 25)

        self.log_out_btn.place(x = 10, y = 500)
        self.log_out_indicate.place(x = 3, y = 500, width = 5, height = 25)

        self.main_content.pack(side = tk.LEFT)
        self.main_content.pack_propagate(False)
        self.main_content.configure(width = 840, height = 720)
    
    def indicate(self, label, show):
        self.hide_indicator()
        label.config(bg = SIDEBAR_TEXT_COLOR)
        self.clear_main_content()
        show()

    def hide_indicator(self):
        self.home_indicate.config(bg = SIDE_BAR_COLOR)
        self.profile_indicate.config(bg = SIDE_BAR_COLOR)
        self.close_out_indicate.config(bg = SIDE_BAR_COLOR)

    def clear_main_content(self):
        # Instead of destroying widgets, just hide them
        for widget in self.main_content.winfo_children():
            widget.pack_forget()
    
    def handleLogout(self):
        print("Handle Logout")
        self.controller.show_Login()
    
    def show_home_page(self):
        # Check if home_page already exists
        if hasattr(self, 'home_page') and self.home_page.winfo_exists():
            # If it exists, just show it
            self.home_page.pack(fill="both", expand=True)
            return

        # Create new home page if it doesn't exist
        self.home_page = tk.Frame(self.main_content)
        self.home_page.pack(fill="both", expand=True)

        self.input_label = tk.Label(self.home_page, text = "Enter current register balance: ", bg = SIDE_BAR_COLOR)
        self.input_label.pack(pady=(20, 5))

        self.input_balance_in = tk.Entry(self.home_page, font=("Arial", 16), width=30)
        self.input_balance_in.pack(pady=(20, 5))
        
        # Add placeholder text
        self.input_balance_in.insert(0, "Enter here:")
        self.input_balance_in.config(fg='grey')
        
        # Bind events for placeholder behavior
        def on_focus_in(event):
            if self.input_balance_in.get() == "Enter here:":
                self.input_balance_in.delete(0, tk.END)
                self.input_balance_in.config(fg='black')
                
        def on_focus_out(event):
            if not self.input_balance_in.get():
                self.input_balance_in.insert(0, "Enter here:")
                self.input_balance_in.config(fg='grey')
                
        self.input_balance_in.bind('<FocusIn>', on_focus_in)
        self.input_balance_in.bind('<FocusOut>', on_focus_out)

        self.clock_in = tk.Button(self.home_page, text="Clock In", font=("Bold", 36), bd=0, command=self.handle_clock_in)
        self.clock_in.pack(pady=10)
        
        clock_label = tk.Label(self.home_page, text="Clock In/Out Record", fg=MAIN_CONTENT_COLOR)
        clock_label.pack(pady=10)

        columns = ("Date", "ClockIn", "ClockOut", "BeforeBal", "AfterBal")
        self.clock_table = ttk.Treeview(self.home_page, columns=columns, show="headings")

        for col in columns:
            self.clock_table.heading(col, text=col)
            self.clock_table.column(col, anchor="center")

        data = dashboard_functions.get_clock_data(self.user_id, self.location)

        for row in data:
            self.clock_table.insert("", "end", values=row)

        scrollbar = ttk.Scrollbar(self.home_page, orient="vertical", command=self.clock_table.yview)
        self.clock_table.configure(yscrollcommand=scrollbar.set)

        self.clock_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        print("The current Employee ID is: ", self.user_id)
    
    def show_profile(self):

        self.profile_page = tk.Frame(self.main_content)
        self.profile_page.pack(fill="both", expand=True)

        profile_label = tk.Label(self.profile_page, text="Profile Page", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        profile_label.pack(pady=10)

        user_data = dashboard_functions.get_user_profile_data(self.user_id) or []

        if not user_data:
            report_label = tk.Label(self.profile_page, text="No profile data found", fg="red", font=("Helvetica", 12))
            report_label.pack(pady=10)
        else:
            user = user_data[0]

            report_label = tk.Label(self.profile_page, text=f"EmployeeID: {self.user_id}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"First Name: {user[0]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"Last Name: {user[1]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"Username: {user[2]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"Role: {user[3]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text="--------------------------------------", font=("Helvetica", 12, "italic"))
            report_label.pack(anchor="w", padx=20, pady=5)

    def show_close_out(self):
        self.close_out_page = tk.Frame(self.main_content)
        self.close_out_page.pack(fill="both", expand=True)

        self.close_out_container_frame = tk.Frame(self.close_out_page)
        self.close_out_container_frame.pack(fill="both", expand=True)
        self.close_out_container_frame.grid_rowconfigure(0, weight=1)
        self.close_out_container_frame.grid_rowconfigure(1, weight=3)
        self.close_out_container_frame.grid_columnconfigure(0, weight=1)
        self.close_out_container_frame.grid_columnconfigure(1, weight=1)

        left_frame = tk.LabelFrame(self.close_out_container_frame, text="Left", font=("Helvetica", 16, "bold"))
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        right_frame = tk.LabelFrame(self.close_out_container_frame, text="right", font=("Helvetica", 16, "bold"))
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Expense on the Left
        row = 0
        tk.Label(left_frame, text="Date (YYYY-MM-DD):").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.expense_date = tk.Entry(left_frame, bg="white", fg="black", bd=2)
        self.expense_date = tk.Entry(left_frame)
        self.expense_date.grid(row=row, column=1, sticky="ew", padx=10)
        self.expense_date.insert(0, self.today)
        self.expense_date.focus_set()
        
        row += 1
        tk.Label(left_frame, text="Amount:").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.expense_amount = tk.Entry(left_frame, bg="white", fg="black", bd=2)
        self.expense_amount = tk.Entry(left_frame)
        self.expense_amount.grid(row=row, column=1, sticky="ew", padx=10)

        row += 1
        tk.Label(left_frame, text="Expense Type:").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.expense_type = tk.Entry(left_frame, bg="white", fg="black", bd=2)
        self.expense_type = tk.Entry(left_frame)
        self.expense_type.grid(row=row, column=1, sticky="ew", padx=10)

        row += 1
        tk.Label(left_frame, text="Is Merchandise?").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.is_merch = tk.BooleanVar()
        self.is_merch.trace_add("write", lambda *args: self.toggle_merchandise_fields())
        tk.Checkbutton(left_frame, variable=self.is_merch).grid(row=row, column=1, sticky="w", padx=10)

        row += 1
        self.merch_label = tk.Label(left_frame, text="Merchandise Type:")
        self.merch_type = tk.Entry(left_frame, bg="white", fg="black", bd=2)
        self.merch_type = tk.Entry(left_frame)
        self.merch_row = row

        row += 1
        expense_btn = tk.Button(left_frame, text="Add Expense", font=("Helvetica", 14, "bold"), command=self.add_expense)
        expense_btn.grid(row=row, column=0, columnspan=2, pady=10)

        # CloseOut on the Right
        before_data = dashboard_functions.get_before_balance(self.user_id, self.today, self.location)

        row = 0
        tk.Label(right_frame, text=f"Close Out Report - {self.today}", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold")).grid(row=row, column=0, columnspan=2, pady=10)

        row += 1
        tk.Label(right_frame, text=f"BeforeBal: {before_data}", font=("Helvetica", 12)).grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=5)

        row += 1
        tk.Label(right_frame, text="Cash:").grid(row=row, column=0, sticky="w", padx=20, pady=2)
        self.cash_entry = tk.Entry(right_frame, bg="white", fg="black", bd=2)
        self.cash_entry = tk.Entry(right_frame)
        self.cash_entry.grid(row=row, column=1, sticky="ew", padx=20)

        row += 1
        tk.Label(right_frame, text="Credit:").grid(row=row, column=0, sticky="w", padx=20, pady=2)
        self.credit_entry = tk.Entry(right_frame, bg="white", fg="black", bd=2)
        self.credit_entry.grid(row=row, column=1, sticky="ew", padx=20)

        # Close Out button
        row += 1
        clock_out_btn = tk.Button(right_frame, text="Close Out", font=("Helvetica", 18, "bold"), command=self.handle_clock_out)
        clock_out_btn.grid(row=row, column=0, columnspan=2, pady=20)
    
    def toggle_merchandise_fields(self):
        if self.is_merch.get():

            self.merch_label.grid(row=self.merch_row, column=0, sticky="w", padx=10, pady=2)
            self.merch_type.grid(row=self.merch_row, column=1, sticky="ew", padx=10)

            self.expense_type.delete(0, tk.END)
            self.expense_type.insert(0, "Merchandise")
            self.expense_type.config(state="disabled")
        else:
            self.merch_label.grid_remove()
            self.merch_type.grid_remove()
            self.expense_type.config(state="normal")
            self.expense_type.delete(0, tk.END)
    
    def add_expense(self):
        date = self.expense_date.get()
        amount = self.expense_amount.get()
        expense_type = self.expense_type.get()
        is_merch = self.is_merch.get()
        merch_type = self.merch_type.get() if is_merch else None

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for Amount.")
            return

        try:
            expense_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            today = datetime.date.today()
            if expense_date > today:
                messagebox.showerror("Invalid Input", "Date cannot be in the future.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Date must be in YYYY-MM-DD format.")
            return

        success = dashboard_functions.add_expense(date, self.location, amount, expense_type, is_merch, merch_type)

        if success:
                tk.messagebox.showinfo("Expense", "Expense added completed successfully!")
        else:
            tk.messagebox.showerror("Expense", "Expense failed")
 
    def handle_clock_in(self):
        try:
            # Check if the input is empty or contains the placeholder
            input_text = self.input_balance_in.get()
            if not input_text or input_text == "Enter here:":
                messagebox.showerror("Invalid Input", "Please enter a valid balance.")
                return
                
            balance = float(input_text)
            success = dashboard_functions.clock_in(self.user_id, self.today, self.location, balance)

            if success:
                tk.messagebox.showinfo("Clock In", "Clock In completed successfully!")
                # Clear the input and restore placeholder
                self.input_balance_in.delete(0, tk.END)
                self.input_balance_in.insert(0, "Enter here:")
                self.input_balance_in.config(fg='grey')
            else:
                tk.messagebox.showerror("Clock In", "Clock In failed")

        except ValueError:
            messagebox.showerror("Invalid Input", "Error: Please check your balance.")
            print("Error: In DashboardEmp, the balance is not valid.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def handle_clock_out(self):
        cash = self.cash_entry.get()
        credit = self.credit_entry.get()

        try:
            cash = float(cash)
            credit = float(credit)
            if cash < 0 or credit < 0: 
                raise ValueError
            
            success = dashboard_functions.clock_out(self.user_id, self.today, self.location)
            success = dashboard_functions.handle_close_out(self.user_id, self.today, self.location, cash, credit)

            if success:
                tk.messagebox.showinfo("Close Out", "Close Out completed successfully!")
                self.cash_entry.delete(0, tk.END)
                self.credit_entry.delete(0, tk.END)
                self.controller.show_Login()
            else:
                tk.messagebox.showerror("Close Out", "Close Out failed")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for Amount.")
            return

    def show_employees(self):
        # Check if employees_page already exists
        if hasattr(self, 'employees_page') and self.employees_page.winfo_exists():
            # If it exists, just show it
            self.employees_page.pack(fill="both", expand=True)
            return

        # Create new employees page if it doesn't exist
        self.employees_page = tk.Frame(self.main_content)
        self.employees_page.pack(fill="both", expand=True)

        self.employees_label = tk.Label(self.employees_page, text="Manage Employees", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        self.employees_label.pack(pady=10)

        container_frame = tk.Frame(self.employees_page)
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

        self.username_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="grey")
        self.username_entry.insert(0, "Enter here:")
        self.username_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="black", relief="solid", bd=1)
        self.username_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="w")
        self.username_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.username_entry))
        self.username_entry.bind('<FocusOut>', lambda e: self._add_placeholder(self.username_entry))

        # First Name
        self.fname_label = tk.Label(detail_frame, text="First Name", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.fname_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")

        self.fname_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="grey")
        self.fname_entry.insert(0, "Enter here:")
        self.fname_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="black", relief="solid", bd=1)
        self.fname_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="w")
        self.fname_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.fname_entry))
        self.fname_entry.bind('<FocusOut>', lambda e: self._add_placeholder(self.fname_entry))

        # Last Name
        self.lname_label = tk.Label(detail_frame, text="Last Name", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.lname_label.grid(row=4, column=0, padx=5, pady=(5, 0), sticky="w")

        self.lname_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="grey")
        self.lname_entry.insert(0, "Enter here:")
        self.lname_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="black", relief="solid", bd=1)
        self.lname_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="w")
        self.lname_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.lname_entry))
        self.lname_entry.bind('<FocusOut>', lambda e: self._add_placeholder(self.lname_entry))

        # Password
        self.password_label = tk.Label(detail_frame, text="Password", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.password_label.grid(row=6, column=0, padx=5, pady=(5, 0), sticky="w")

        self.password_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="grey")
        self.password_entry.insert(0, "Enter here:")
        self.password_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="black", show="*", relief="solid", bd=1)
        self.password_entry.grid(row=7, column=0, padx=5, pady=(0, 10), sticky="w")
        self.password_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.password_entry, is_password=True))
        self.password_entry.bind('<FocusOut>', lambda e: self._add_placeholder(self.password_entry, is_password=True))

        # Pay Rate
        self.pay_rate_label = tk.Label(detail_frame, text="Pay Rate", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.pay_rate_label.grid(row=8, column=0, padx=5, pady=(5, 0), sticky="w")

        self.pay_rate_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="grey")
        self.pay_rate_entry.insert(0, "Enter here:")
        self.pay_rate_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="black", relief="solid", bd=1)
        self.pay_rate_entry.grid(row=9, column=0, padx=5, pady=(0, 10), sticky="w")
        self.pay_rate_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.pay_rate_entry))
        self.pay_rate_entry.bind('<FocusOut>', lambda e: self._add_placeholder(self.pay_rate_entry))

        # Pay Bonus
        self.pay_bonus_label = tk.Label(detail_frame, text="Pay Bonus", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.pay_bonus_label.grid(row=10, column=0, padx=5, pady=(5, 0), sticky="w")

        self.pay_bonus_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="grey")
        self.pay_bonus_entry.insert(0, "Enter here:")
        self.pay_bonus_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg="white", fg="black", relief="solid", bd=1)
        self.pay_bonus_entry.grid(row=11, column=0, padx=5, pady=(0, 10), sticky="w")
        self.pay_bonus_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.pay_bonus_entry))
        self.pay_bonus_entry.bind('<FocusOut>', lambda e: self._add_placeholder(self.pay_bonus_entry))

        buttons_frame = tk.Frame(detail_frame, bg=BACKGROUND_COLOR)
        buttons_frame.grid(row=12, column=0, columnspan=2, pady=2)

        self.create_employee_btn = tk.Button(buttons_frame, text="Create", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.create_employee)
        self.create_employee_btn.pack(side="left", padx=2)

        self.update_employee_btn = tk.Button(buttons_frame, text="Update", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.update_employee)
        self.update_employee_btn.pack(side="left", padx=2)

        self.delete_employee_btn = tk.Button(buttons_frame, text="Delete", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.delete_employee)
        self.delete_employee_btn.pack(side="left", padx=2)

        # Data View
        self.data_view = ttk.Treeview(
            data_frame,
            columns=("EmployeeID", "Username", "First Name", "Last Name", "Role", "Pay Rate", "Pay Bonus"),
            show="headings",
            height=10
        )
        self.data_view.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)

        self.data_view.heading("EmployeeID", text="Employee ID")
        self.data_view.heading("Username", text="Username")
        self.data_view.heading("First Name", text="First Name")
        self.data_view.heading("Last Name", text="Last Name")
        self.data_view.heading("Role", text="Role")
        self.data_view.heading("Pay Rate", text="Pay Rate")
        self.data_view.heading("Pay Bonus", text="Pay Bonus")

        self.data_view.column("EmployeeID", width=100)
        self.data_view.column("Username", width=120)
        self.data_view.column("First Name", width=120)
        self.data_view.column("Last Name", width=120)
        self.data_view.column("Role", width=100)
        self.data_view.column("Pay Rate", width=100)
        self.data_view.column("Pay Bonus", width=100)

        self.data_view.bind("<<TreeviewSelect>>", self.on_employee_select)

        employee_data = dashboard_functions.get_employee_data()
    
        for item in self.data_view.get_children():
            self.data_view.delete(item)

        for emp in employee_data:
            employee_id = emp[0]
            username = emp[1]
            first_name = emp[2]
            last_name = emp[3]
            role = emp[4]
            pay_rate = emp[5]
            pay_bonus = emp[6]

            self.data_view.insert(
                "", "end",
                values=(employee_id, username, first_name, last_name, role, pay_rate, pay_bonus)
            )

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(data_frame, orient="vertical", command=self.data_view.yview)
        tree_scroll_y.grid(row=0, column=1, sticky="ns")

        self.data_view.config(yscrollcommand=tree_scroll_y.set)

        data_frame.grid_rowconfigure(0, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)

    def _clear_placeholder(self, entry, is_password=False):
        if entry.get() == "Enter here:":
            entry.delete(0, tk.END)
            entry.config(fg='black')
            if is_password:
                entry.config(show='*')

    def _add_placeholder(self, entry, is_password=False):
        if not entry.get():
            entry.insert(0, "Enter here:")
            entry.config(fg='grey')
            if is_password:
                entry.config(show='')
