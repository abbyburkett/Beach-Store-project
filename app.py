import tkinter as tk

from pages import DashboardOwner
from pages.Login import Login
from pages.DashboardEmp import DashboardEmployee
from pages.DashboardMan import DashboardManager
from pages.DashboardOwner import Dashboard_Owner

from logics.Connect_SQL import run_sql_file

# this part of the code is from GeeksforGeeks
class MyApp(tk.Frame):
    def __init__(self, root):
        self.BACKGROUND_COLOR = "#FFF6E3"

        run_sql_file(file_path="Tables.sql")

        super().__init__(
            root,
            bg = self.BACKGROUND_COLOR
        )

        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand = True)
        self.main_frame.columnconfigure(0, weight = 1)
        self.main_frame.rowconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}  
        self.user_id = None

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, DashboardEmployee, DashboardManager, Dashboard_Owner):
  
            frame = F(self.main_frame, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Login)
    
    # to display the current frame passed as
    # parameter

    def set_location(self, location):
        self.location = location

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def show_Login(self):
        self.show_frame(Login)

    def show_dashboardEmp(self, user_id):
        self.user_id = user_id
        self.show_frame(DashboardEmployee)
        self.frames[DashboardEmployee].user_id = self.user_id
    
    def show_dashboardMan(self, user_id):
        self.user_id = user_id
        self.show_frame(DashboardManager)
        self.frames[DashboardManager].user_id = self.user_id

    def show_dashboardOwner(self, user_id):
        self.user_id = user_id
        self.show_frame(Dashboard_Owner)
        self.frames[Dashboard_Owner].user_id = self.user_id

root = tk.Tk()
root.title("Beach Store")
root.geometry("1080x720")
root.resizable(width = False, height = False)

app = MyApp(root)
root.mainloop()