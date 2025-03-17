import tkinter as tk

BACKGROUND_COLOR = "#FFF6E3"
class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        self.bg = BACKGROUND_COLOR
        super().__init__(parent, bg=self.bg)

        self.controller = controller
        self.create_widgets()
        self.display_widgets()

    def create_widgets(self):
        self.dashboard_label = tk.Label(self, text="Welcome to the Dashboard", font=("Arial", 40, "bold"), fg="#CDC1FF", bg=self.bg)
        self.dashboard_label.pack(pady=20)

        # Add other dashboard widgets here

    def display_widgets(self):
        self.dashboard_label.pack()