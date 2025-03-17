import tkinter as tk
from pages.Login import Login
from pages.Dashboard import Dashboard

class MyApp(tk.Frame):
    def __init__(self, root):
        self.BACKGROUND_COLOR = "#FFF6E3"

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

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, Dashboard):
  
            frame = F(self.main_frame, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Login)
    
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_dashboard(self):
        self.show_frame(Dashboard)

root = tk.Tk()
root.title("Beach Store")
root.geometry("1080x720")
root.resizable(width = False, height = False)

app = MyApp(root)
root.mainloop()