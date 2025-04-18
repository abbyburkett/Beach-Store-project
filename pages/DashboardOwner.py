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
        # Clear previous content
        self.clear_main_content()

        reports_label = tk.Label(self.main_content, text="Owner Reports", font=("Helvetica", 16, "bold"))
        reports_label.pack(pady=10)

        # Dropdown for Month Selection
        month_frame = tk.Frame(self.main_content)
        month_frame.pack(pady=5)

        month_label = tk.Label(month_frame, text="Select Month:", font=("Helvetica", 12))
        month_label.pack(side="left", padx=(0, 5))

        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]

        self.selected_month = tk.StringVar()
        month_dropdown = ttk.Combobox(month_frame, textvariable=self.selected_month, values=months, state="readonly")
        month_dropdown.pack(side="left")

        # Treeview setup
        columns = ("Day", "Date", "Gross Profit", "Expense", "Merchandise", "Payroll")
        self.report_tree = ttk.Treeview(self.main_content, columns=columns, show="headings", height=20)

        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=130, anchor="center")

        self.report_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Load initial data for current month
        self.selected_month.set(datetime.now().strftime('%B'))  # Default to current month
        self.load_reports(self.report_tree)

        # Bind dropdown change
        month_dropdown.bind("<<ComboboxSelected>>", lambda event: self.load_reports(self.report_tree))

    def load_reports(self, tree):
        tree.delete(*tree.get_children())
        cursor = self.db.cursor()

        try:
            month = self.selected_month.get()
            if not month:
                return

            month_number = datetime.strptime(month, "%B").month
            year = datetime.today().year

            first_day = f"{year}-{month_number:02d}-01"
            last_day = f"{year}-{month_number:02d}-{calendar.monthrange(year, month_number)[1]}"

            date_filter = f"WHERE Date BETWEEN '{first_day}' AND '{last_day}'"

            # Get profit
            cursor.execute(f"""
                SELECT Date, SUM(Cash + Credit) 
                FROM Profit 
                {date_filter}
                GROUP BY Date
            """)
            profits = {row[0]: row[1] for row in cursor.fetchall()}

            # Get expenses (and merchandise)
            cursor.execute(f"""
                SELECT Date, SUM(Amount), SUM(CASE WHEN isMerchandise THEN Amount ELSE 0 END)
                FROM Expense 
                {date_filter}
                GROUP BY Date
            """)
            expenses = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

            # Get payroll
            cursor.execute(f"""
                SELECT Date, SUM(e.PayRate) 
                FROM ClockInOut c 
                JOIN Employee e ON c.EmployeeID = e.EmployeeID 
                {date_filter}
                GROUP BY Date
            """)
            payrolls = {row[0]: row[1] for row in cursor.fetchall()}

            all_dates = sorted(set(profits.keys()) | set(expenses.keys()) | set(payrolls.keys()))

            for date in all_dates:
                profit = profits.get(date, 0)
                expense, merch = expenses.get(date, (0, 0))
                payroll = payrolls.get(date, 0)
                day = datetime.strptime(str(date), "%Y-%m-%d").strftime('%A')

                tree.insert("", "end", values=(
                    day, date, round(profit, 2), round(expense, 2), round(merch, 2), round(payroll, 2)
                ))

            cursor.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

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
            columns=("LocationID", "Name", "Address", "ManagerID"),
            show="headings",
            height=10
        )
        self.data_view.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)

        self.data_view.heading("LocationID", text="Location ID")
        self.data_view.heading("Name", text="Name")
        self.data_view.heading("Address", text="Address")
        self.data_view.heading("ManagerID", text="Manager ID")

        self.data_view.column("LocationID", width=100)
        self.data_view.column("Name", width=120)
        self.data_view.column("Address", width=200)
        self.data_view.column("ManagerID", width=100)

        self.data_view.bind("<<TreeviewSelect>>", self.on_location_select)

        location_data = dashboard_functions.get_location_data()
    
        for item in self.data_view.get_children():
            self.data_view.delete(item)
        for loc in location_data:
            # Assuming loc = (LocationID, Name, Address, ManagerID)
            self.data_view.insert("", "end", values=loc)

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
            self.data_view.item(selected[0], values=(location_id, name, address, manager_id))
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

            self.manager_entry.delete(0, tk.END)
            self.manager_entry.insert(0, values[3])


