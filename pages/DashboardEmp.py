import tkinter as tk
from tkinter import ttk
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
        self.today = "2025-03-17"
        self.user_id = 101

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

        self.clock_in = tk.Button(self.home_page, text="Clock In", font=("Bold", 36), bd=0)
        self.clock_in.pack(pady=10)

        self.pay_label = tk.Label(self.home_page, text = "Pay Table", fg = MAIN_CONTENT_COLOR)
        self.pay_label.pack(pady=10)

        columns = ("PayAmount", "BonusPercentage", "GrossBonus", "GrossPaid")
        self.pay_table = ttk.Treeview(self.home_page, columns=columns, show="headings")

        for col in columns:
            self.pay_table.heading(col, text=col)
            self.pay_table.column(col, anchor="center")

        data = dashboard_functions.getPayData(self.user_id, columns)

        for row in data:
            self.pay_table.insert("", "end", values=row)

        scrollbar = ttk.Scrollbar(self.home_page, orient="vertical", command=self.pay_table.yview)
        self.pay_table.configure(yscrollcommand=scrollbar.set)

        self.pay_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_profile(self):

        self.profile_page = tk.Frame(self.main_content)
        self.profile_page.pack(fill="both", expand=True)

        self.profile_label = tk.Label(self.profile_page, text="Profile Page", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        self.profile_label.pack(pady=10)

        user_data = dashboard_functions.getUserProfileData(self.user_id) or []

        if not user_data:
            report_label = tk.Label(self.profile_page, text="No profile data found", fg="red", font=("Helvetica", 12))
            report_label.pack(pady=10)
        else:
            user = user_data[0]

            report_label = tk.Label(self.profile_page, text=f"EmployeeID: {user[0]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"First Name: {user[1]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"Last Name: {user[2]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"Pin Password: {user[3]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"Username: {user[4]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.profile_page, text=f"Role: {user[5]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            separator = tk.Label(self.profile_page, text="--------------------------------------", font=("Helvetica", 12, "italic"))
            separator.pack(anchor="w", padx=20, pady=5)

    def show_close_out(self):
        self.close_out = tk.Frame(self.main_content)
        self.close_out.pack(fill="both", expand=True)

        self.close_out_label = tk.Label(self.close_out, text=f"Close Out Report - {self.today}", fg=MAIN_CONTENT_COLOR, font=("Helvetica", 16, "bold"))
        self.close_out_label.pack(pady=10)

        data = dashboard_functions.getCloseOutData(101, ["EmployeeID", "BeforeBal", "AfterBal", "Cash", "Credit", "GrossRevenue", "Date"], self.today) or []

        if not data:
            report_label = tk.Label(self.close_out, text="No data found for this date", fg="red", font=("Helvetica", 12))
            report_label.pack(pady=10)
        else:
            row = data[0]

            report_label = tk.Label(self.close_out, text=f"EmployeeID: {row[0]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.close_out, text=f"BeforeBal: {row[1]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.close_out, text=f"AfterBal: {row[2]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.close_out, text=f"Cash: {row[3]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.close_out, text=f"Credit: {row[4]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.close_out, text=f"GrossRevenue: {row[5]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            report_label = tk.Label(self.close_out, text=f"Date: {row[6]}", font=("Helvetica", 12))
            report_label.pack(anchor="w", padx=20, pady=5)

            separator = tk.Label(self.close_out, text="--------------------------------------", font=("Helvetica", 12, "italic"))
            separator.pack(anchor="w", padx=20, pady=5)

        self.clock_out = tk.Button(self.close_out, text="Clock Out", font=("Bold", 36), bd=0)
        self.clock_out.pack(pady=10)