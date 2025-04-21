import tkinter as tk
from tkinter import messagebox
from logics import login_functions

BACKGROUND_COLOR = "#FFF6E3"

class Login(tk.Frame):
    def __init__(self, parent, controller):
        self.bg = BACKGROUND_COLOR

        location_data = login_functions.get_location_list()
        if not location_data:
            messagebox.showinfo("No Locations", "No locations available in the system.")
            return

        self.location_list = [location[1] for location in location_data]
        self.location_id = [location[0] for location in location_data]

        self.selected_location = tk.StringVar()
        self.selected_location.set(self.location_list[0])

        super().__init__(parent, bg=self.bg)
        self.controller = controller
        self.create_widgets()
        self.display_widgets()

    def create_widgets(self):    
        self.frame = tk.Frame(self, background=self.bg)

        self.login_label = tk.Label(self.frame, text = "Login", font=("Arial", 40, "bold"), fg = "#CDC1FF", bg = self.bg)
        self.username_label = tk.Label(self.frame, text = "Username", font=("Arial", 25, "bold"), fg = "#CDC1FF", bg = self.bg, bd = 0)
        self.username_entry = tk.Entry(self.frame, font = ("Arial", 25, "bold"), bg = "white", fg = "black")
        self.password_label = tk.Label(self.frame, text = "Password", font=("Arial", 25, "bold"), fg = "#CDC1FF", bg = self.bg, bd = 0)
        self.password_entry = tk.Entry(self.frame, font = ("Arial", 25, "bold"), bg = "white", fg = "black", show = "*")
        self.location_menu = tk.OptionMenu(self.frame, self.selected_location, *self.location_list)
        self.location_menu.config(fg = "#FFCCEA", bg = self.bg, bd = 0, highlightthickness = 0, relief = "flat", width = 40)
        self.login_button = tk.Button(self.frame, text = "Login", fg = "#FFCCEA", bg = self.bg, bd = 0, highlightthickness = 0, relief = "flat", command = self.login_submit)

    def display_widgets(self):
        self.frame.pack()

        self.login_label.grid(row = 0, column = 0, columnspan = 2, sticky = "news", pady = 25)
        self.username_label.grid(row = 1, column = 0)
        self.username_entry.grid(row = 1, column = 1, pady = 10)
        self.password_label.grid(row = 2, column = 0)
        self.password_entry.grid(row = 2, column = 1, pady = 10)
        self.location_menu.grid(row = 3, column = 0, columnspan = 2, pady = 10)
        self.login_button.grid(row = 4, column = 0, columnspan = 2, pady = 25)

    def login_submit(self):
        
        username = self.username_entry.get()
        password = self.password_entry.get()
        location = self.selected_location.get()

        if location:
            self.controller.set_location(self.location_id[self.location_list.index(location)])
        
        results = login_functions.check_credentials(username, password)
        if results[0]:
            print(f"Login successful for {username}")

            if results[2] == "Manager":
                self.controller.show_dashboardMan(results[1])
            elif results[2] == "Employee":
                self.controller.show_dashboardEmp(results[1])
            elif results[2] == "Owner":
                self.controller.show_dashboardOwner(results[1])

            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

        else:
            print("Invalid credentials, please try again.")