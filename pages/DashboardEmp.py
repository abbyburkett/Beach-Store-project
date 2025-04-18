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
        # self.user_id = self.controller.user_id
        self.today = controller.today
        self.create_widgets()
        self.display_widgets()


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
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def handleLogout(self):
        print("Handle Logout")
        self.controller.show_Login()
    
    def show_home_page(self):
        self.home_page = tk.Frame(self.main_content)
        self.home_page.pack(fill="both", expand=True)

        self.input_label = tk.Label(self.home_page, text = "Enter current register balance: ", bg = SIDE_BAR_COLOR)
        self.input_label.pack(pady=(20, 5))

        self.input_balance_in = tk.Entry(self.home_page, font=("Arial", 16), width=30)
        self.input_balance_in.pack(pady=(20, 5))

        self.clock_in = tk.Button(self.home_page, text="Clock In", font=("Bold", 36), bd=0, command=self.handle_clock_in)
        self.clock_in.pack(pady=10)
        
        pay_label = tk.Label(self.home_page, text = "Pay Table", fg = MAIN_CONTENT_COLOR)
        pay_label.pack(pady=10)
        
        columns = ("WeekRange", "PayAmount", "GrossBonus", "GrossPaid")
        self.pay_table = ttk.Treeview(self.home_page, columns=columns, show="headings")

        for col in columns:
            self.pay_table.heading(col, text=col)
            self.pay_table.column(col, anchor="center")

        data = dashboard_functions.get_pay_data(self.user_id)

        for row in data:
            self.pay_table.insert("", "end", values=row)

        scrollbar = ttk.Scrollbar(self.home_page, orient="vertical", command=self.pay_table.yview)
        self.pay_table.configure(yscrollcommand=scrollbar.set)

        self.pay_table.pack(side="left", fill="both", expand=True)
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

            separator = tk.Label(self.profile_page, text="--------------------------------------", font=("Helvetica", 12, "italic"))
            separator.pack(anchor="w", padx=20, pady=5)

    def show_close_out(self):
        self.close_out_page = tk.Frame(self.main_content)
        self.close_out_page.pack(fill="both", expand=True)

        container_frame = tk.Frame(self.close_out_page)
        container_frame.pack(fill="both", expand=True)
        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_columnconfigure(1, weight=1)

        left_frame = tk.LabelFrame(container_frame, text="Left", font=("Helvetica", 16, "bold"))
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        right_frame = tk.LabelFrame(container_frame, text="right", font=("Helvetica", 16, "bold"))
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Expense on the Left
        row = 0
        tk.Label(left_frame, text="Date (YYYY-MM-DD):").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.expense_date = tk.Entry(left_frame)
        self.expense_date.grid(row=row, column=1, sticky="ew", padx=10)
        self.expense_date.insert(0, self.today)
        
        row += 1
        tk.Label(left_frame, text="Amount:").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.expense_amount = tk.Entry(left_frame)
        self.expense_amount.grid(row=row, column=1, sticky="ew", padx=10)

        row += 1
        tk.Label(left_frame, text="Expense Type:").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.expense_type = tk.Entry(left_frame)
        self.expense_type.grid(row=row, column=1, sticky="ew", padx=10)

        row += 1
        tk.Label(left_frame, text="Is Merchandise?").grid(row=row, column=0, sticky="w", padx=10, pady=2)
        self.is_merch = tk.BooleanVar()
        self.is_merch.trace_add("write", lambda *args: self.toggle_merchandise_fields())
        tk.Checkbutton(left_frame, variable=self.is_merch).grid(row=row, column=1, sticky="w", padx=10)

        row += 1
        self.merch_label = tk.Label(left_frame, text="Merchandise Type:")
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
        self.cash_entry = tk.Entry(right_frame)
        self.cash_entry.grid(row=row, column=1, sticky="ew", padx=20)

        row += 1
        tk.Label(right_frame, text="Credit:").grid(row=row, column=0, sticky="w", padx=20, pady=2)
        self.credit_entry = tk.Entry(right_frame)
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
            balance = float(self.input_balance_in.get())
            success = dashboard_functions.clock_in(self.user_id, self.today, self.location, balance)

            if success:
                tk.messagebox.showinfo("Clock In", "Clock In completed successfully!")
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
