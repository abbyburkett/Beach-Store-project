import tkinter as tk
from tkinter import ttk
from logics import dashboard_functions
from tkinter import messagebox
from datetime import datetime
import calendar
from pages.DashboardMan import DashboardManager
import mysql.connector

BACKGROUND_COLOR = "#FFF6E3"
SIDE_BAR_COLOR = "pink"
MAIN_CONTENT_COLOR = "green"

SIDEBAR_TEXT_COLOR = "black"

class DashboardOwner(DashboardManager):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.isEmployee = False
        self.isManager = False
        self.isOwner = True

        self.dashboard_label.config(text=f"Welcome to the Owner Dashboard")

    def create_widgets(self):
        super().create_widgets()

        self.location_indicate = tk.Label(self.side_bar, text="", bg=SIDE_BAR_COLOR)
        self.location_btn = tk.Button(self.side_bar, text="Location", font=("Bold", 15), bd=0, fg=SIDEBAR_TEXT_COLOR, command=lambda: self.indicate(self.location_indicate, self.show_locations))
        self.withdrawal_indicate = tk.Label(self.side_bar, text="", bg=SIDE_BAR_COLOR)
        self.withdrawal_btn = tk.Button(self.side_bar, text="Withdrawal", font=("Bold", 15), bd=0, fg=SIDEBAR_TEXT_COLOR, command=lambda: self.indicate(self.withdrawal_indicate, self.show_withdrawals))

    def display_widgets(self):
        super().display_widgets()

        self.location_btn.place(x=10, y=350)
        self.location_indicate.place(x=3, y=350, width=5, height=25)
        self.withdrawal_btn.place(x=10, y=400)
        self.withdrawal_indicate.place(x=3, y=400, width=5, height=25)

    def hide_indicator(self):
        super().hide_indicator()
        self.location_indicate.config(bg = SIDE_BAR_COLOR)
        self.withdrawal_indicate.config(bg = SIDE_BAR_COLOR)

    def show_employees(self):
        super().show_employees()

        self.create_owner_btn = tk.Button(
            self.buttons_frame,
            text="Create Owner",
            fg=MAIN_CONTENT_COLOR,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=self.create_owner
        )
        self.create_owner_btn.pack(side="left", padx=2)
    
    def create_owner(self):
        username = self.username_entry.get()
        first_name = self.fname_entry.get()
        last_name = self.lname_entry.get()
        password = self.password_entry.get()
        pay_rate = self.pay_rate_entry.get()
        pay_bonus = self.pay_bonus_entry.get()

        # You can also add validation here if needed
        if not all([username, first_name, last_name, password, pay_rate, pay_bonus]):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        success = dashboard_functions.create_employee(
            username=username,
            password=password,
            fname=first_name,
            lname=last_name,
            role="Owner",
            pay_rate=pay_rate,
            pay_bonus=pay_bonus
        )

        if success:
            messagebox.showinfo("Success", "Owner created successfully.")
            self.indicate(self.employees_indicate, self.show_employees)
        else:
            messagebox.showerror("Error", "Failed to create owner.")

    def show_reports(self):
        self.clear_main_content()

        month_frame = tk.Frame(self.main_content)
        month_frame.pack(pady=5)

        month_label = tk.Label(month_frame, text="Select Month:", font=("Helvetica", 12))
        month_label.pack(side="left", padx=(0, 5))

        months = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]

        self.selected_month = tk.StringVar()
        month_dropdown = ttk.Combobox(month_frame, textvariable=self.selected_month, values=months, state="readonly")
        month_dropdown.pack(side="left")

        month_dropdown.bind("<<ComboboxSelected>>", lambda event: self.load_reports())
        super().show_reports()
        # self.load_reports()

    def load_reports(self):
        self.report_tree.delete(*self.report_tree.get_children())
        try:
            month_map = {
                "January": "01", "February": "02", "March": "03", "April": "04",
                "May": "05", "June": "06", "July": "07", "August": "08",
                "September": "09", "October": "10", "November": "11", "December": "12"
            }

            selected_month = self.selected_month.get()
            if not selected_month:
                return

            selected_month_number = month_map[selected_month]
            temp_today = self.today 

            try:
                base_date = datetime.strptime(self.today, "%Y-%m-%d")
                owner_date = base_date.replace(month=int(selected_month_number))
                self.today = owner_date.strftime("%Y-%m-%d")  
                super().load_reports()
            except Exception as e:
                print(f"Date conversion error: {e}")
                return

            self.today = temp_today 

        except Exception as e:
            print("In owner load report:", e)

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
        self.manager_label = tk.Label(detail_frame, text="Manager ID", font=("Arial", 16, "bold"), fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0)
        self.manager_label.grid(row=4, column=0, padx=5, pady=(5, 0), sticky="w")

        self.manager_entry = tk.Entry(detail_frame, font=("Arial", 16, "bold"), bg=MAIN_CONTENT_COLOR, fg="black")
        self.manager_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="w")

        buttons_frame = tk.Frame(detail_frame, bg=BACKGROUND_COLOR)
        buttons_frame.grid(row=12, column=0, columnspan=2, pady=2)

        self.add_location_btn = tk.Button(buttons_frame, text="Add", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.create_location)
        self.add_location_btn.pack(side="left", padx=2)

        self.update_location_btn = tk.Button(buttons_frame, text="Update", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command=self.update_location)
        self.update_location_btn.pack(side="left", padx=2) 

        self.delete_location_btn = tk.Button(buttons_frame, text="Delete", fg=MAIN_CONTENT_COLOR, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="flat", command = self.delete_location)
        self.delete_location_btn.pack(side="left", padx=2)

        # Data View
        self.data_view = ttk.Treeview(
            data_frame,
            columns=("LocationID", "Name", "Address", "ManagerUsername"),
            show="headings",
            height=10
        )
        self.data_view.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)

        self.data_view.heading("LocationID", text="Location ID")
        self.data_view.heading("Name", text="Name")
        self.data_view.heading("Address", text="Address")
        self.data_view.heading("ManagerUsername", text="Manager")

        self.data_view.column("LocationID", width=100)
        self.data_view.column("Name", width=120)
        self.data_view.column("Address", width=200)
        self.data_view.column("ManagerUsername", width=100)

        self.data_view.bind("<<TreeviewSelect>>", self.on_location_select)

        location_data = dashboard_functions.get_location_data()
    
        for item in self.data_view.get_children():
            self.data_view.delete(item)

        for loc in location_data:
            location_id = loc[0]
            name = loc[1]
            address = loc[2]
            manager_username = loc[3]
            manager_id = loc[4]

            self.data_view.insert(
                "", "end",
                values=(location_id, name, address, manager_username),
                tags=(manager_id,) 
            )
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(data_frame, orient="vertical", command=self.data_view.yview)
        tree_scroll_y.grid(row=0, column=1, sticky="ns")

        self.data_view.config(yscrollcommand=tree_scroll_y.set)

        data_frame.grid_rowconfigure(0, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)

    def create_location(self):
        name = self.location_name_entry.get().strip()
        address = self.address_entry.get().strip()
        manager_id = self.manager_entry.get().strip()

        if not name or not address or not manager_id:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        success = dashboard_functions.add_location(name, address, manager_id)
        if success:
            messagebox.showinfo("Success", "Location added successfully.")
            self.indicate(self.location_indicate, self.show_locations)
            self.clear_location_entries()
        else:
            messagebox.showerror("Error", "Failed to add location.")

    def update_location(self):
        selected = self.data_view.selection() 
        if not selected:
            messagebox.showerror("Error", "Please select a location to update.")
            return

        name = self.location_name_entry.get().strip()
        address = self.address_entry.get().strip()
        manager_id = self.manager_entry.get().strip()

        if not name or not address or not manager_id:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        location_id = self.data_view.item(selected[0], "values")[0]
        success = dashboard_functions.update_location(location_id, name, address, manager_id)
        if success:
            self.indicate(self.location_indicate, self.show_locations)
            messagebox.showinfo("Success", "Location updated successfully.")
            self.clear_location_entries()
        else:
            messagebox.showerror("Error", "Failed to update location.")

    def delete_location(self):
        selected = self.data_view.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a location to delete.")
            return

        values = self.data_view.item(selected[0], "values")
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete location: {values[0]}?")
        if confirm:
            success = dashboard_functions.delete_location(values[0])
            if success:
                self.data_view.delete(selected[0])
                messagebox.showinfo("Success", "Location deleted successfully.")
                self.clear_location_entries()
            else:
                messagebox.showerror("Error", "Failed to delete location.")

    def clear_location_entries(self):
        self.location_name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.manager_entry.delete(0, tk.END)
    
    def on_location_select(self, event):
        selected = self.data_view.selection()
            
        if selected:
            values = self.data_view.item(selected[0], "values")
            self.location_name_entry.delete(0, tk.END)
            self.location_name_entry.insert(0, values[1])

            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, values[2])

            manager_id = self.data_view.item(selected[0], "tags")[0]
            
            self.manager_entry.delete(0, tk.END)
            self.manager_entry.insert(0, manager_id)

    def show_withdrawals(self):
        self.clear_main_content()
        withdrawal_frame = tk.Frame(self.main_content)
        withdrawal_frame.pack(pady=5)

        top_frame = tk.Frame(withdrawal_frame)
        top_frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_label = tk.Label(top_frame, text="Withdrawal History", font=("Helvetica", 14, "bold"))
        top_label.pack(pady=(0, 10))

        tree_frame = tk.Frame(top_frame)
        tree_frame.pack(fill="both", expand=True)
        columns = ("Date", "Amount")
        self.withdrawal_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.withdrawal_tree.heading(col, text=col)
            self.withdrawal_tree.column(col, anchor="center", width=150)
        self.withdrawal_tree.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=self.withdrawal_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.withdrawal_tree.configure(yscrollcommand=scrollbar.set)

        self.load_withdrawal_history()

        bottom_frame = tk.Frame(withdrawal_frame)
        bottom_frame.pack(fill="x", padx=10, pady=20)

        profit_label = tk.Label(bottom_frame, text="Available Profit: ", font=("Helvetica", 12))
        profit_label.grid(row=0, column=0, sticky="w")

        self.available_profit_var = tk.StringVar()

        profit_amount = tk.Label(bottom_frame, textvariable=self.available_profit_var, font=("Helvetica", 12, "bold"))
        profit_amount.grid(row=0, column=1, sticky="w", padx=(5, 20))

        profit_value = dashboard_functions.get_profit(self.location)
        self.available_profit_var.set(f"${profit_value:.2f}")

        withdraw_label = tk.Label(bottom_frame, text="Withdraw Amount:", font=("Helvetica", 12))
        withdraw_label.grid(row=1, column=0, sticky="w")

        self.withdraw_entry = tk.Entry(bottom_frame, width=15)
        self.withdraw_entry.grid(row=1, column=1, sticky="w", padx=(5, 20))

        withdraw_button = tk.Button(bottom_frame, text="Withdraw", command=self.make_withdrawal)
        withdraw_button.grid(row=1, column=2, padx=10)
    
    def load_withdrawal_history(self):
        for row in self.withdrawal_tree.get_children():
            self.withdrawal_tree.delete(row)

        withdrawal_data = dashboard_functions.get_withdrawal_data(self.location)

        for date, amount in withdrawal_data:
            self.withdrawal_tree.insert("", "end", values=(date.strftime("%Y-%m-%d"), f"${amount:.2f}"))

    def make_withdrawal(self):
        try:
            amount = float(self.withdraw_entry.get())
            if not amount:
                messagebox.showwarning("Missing Input", "Please enter a withdrawal amount.")
                return
            if amount <= 0:
                messagebox.showerror("Invalid Input", "Please enter a valid positive number.")
                return
            available = float(self.available_profit_var.get().replace('$', ''))
            if amount > available:
                messagebox.showerror("Insufficient Profit", "Withdrawal amount exceeds available profit.")
                return
            
            result = dashboard_functions.insert_withdrawal(self.location, amount)

            if result: 
                messagebox.showinfo("Success", f"Withdrawal of ${amount:.2f} successful.")
                self.withdraw_entry.delete(0, tk.END)
                self.indicate(self.withdrawal_indicate, self.show_withdrawals)

        except Exception as e:
            messagebox.showerror("Error", e)
