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
            self.data_view.insert("", "end", values=(name, address, manager_id))
            messagebox.showinfo("Success", "Location added successfully.")
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

        old_values = self.data_view.item(selected[0], "values")
        success = dashboard_functions.update_location(old_values[0], name, address, manager_id)
        if success:
            self.data_view.item(selected[0], values=(name, address, manager_id))
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
    
    def on_location_select(self, event):
        selected = self.data_view.selection()
        if selected:
            values = self.data_view.item(selected[0], "values")
            self.location_name_entry.delete(0, tk.END)
            self.location_name_entry.insert(0, values[0])

            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, values[1])

            self.manager_entry.delete(0, tk.END)
            self.manager_entry.insert(0, values[2])