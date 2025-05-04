import tkinter as tk
from tkinter import ttk, messagebox
from logics import login_functions

# ---------------------------------------------------------------------------
#  Colors & Fonts
# ---------------------------------------------------------------------------
BACKGROUND_COLOR = "#F5F0E6"      # soft warm beige
ACCENT_COLOR     = "#6C63FF"      # lavender‑indigo accent
TEXT_COLOR       = "#333333"      # charcoal for better readability


class Login(tk.Frame):
    """A modern‑looking login card that preserves all original behaviour."""

    def __init__(self, parent: tk.Widget, controller):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.controller = controller

        # ------------------------------------------------------------------
        #  Fetch locations from DB (fail gracefully if none exist)
        # ------------------------------------------------------------------
        location_data = login_functions.get_location_list()
        if not location_data:
            messagebox.showinfo("No Locations", "No locations available in the system.")
            return

        self.location_list = [loc[1] for loc in location_data]
        self.location_id   = [loc[0] for loc in location_data]
        self.selected_location = tk.StringVar(value=self.location_list[0])

        # ------------------------------------------------------------------
        #  Styling tweaks (only done once per process)
        # ------------------------------------------------------------------
        self._setup_styles()
        self._configure_grid()

        # ------------------------------------------------------------------
        #  Build the widget tree
        # ------------------------------------------------------------------
        self._create_widgets()
        self._layout_widgets()

    # ----------------------------------------------------------------------
    #  UI helpers
    # ----------------------------------------------------------------------
    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")          # neutral base theme
        except tk.TclError:
            pass  # theme already in use / missing – ignore

        style.configure("Card.TFrame",   background="white")
        style.configure("Header.TLabel", font=("Segoe UI", 36, "bold"), foreground=ACCENT_COLOR, background="white")
        style.configure("TLabel",        font=("Segoe UI", 14), foreground=TEXT_COLOR,  background="white")
        style.configure("TEntry",        font=("Segoe UI", 14))
        style.configure("TCombobox",     font=("Segoe UI", 14))
        style.configure("Accent.TButton",font=("Segoe UI", 14, "bold"), foreground="white", background=ACCENT_COLOR, padding=6)
        style.map("Accent.TButton",
                  background=[("active", "#5750d4")],
                  foreground=[("disabled", "#cccccc")])

    def _configure_grid(self):
        # Give the lone column/row stretch so the card sits centred
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _create_widgets(self):
        # Card container ----------------------------------------------------
        self.card = ttk.Frame(self, padding=40, style="Card.TFrame")

        # Header ------------------------------------------------------------
        self.lbl_header   = ttk.Label(self.card, text="Login", style="Header.TLabel")

        # Username ----------------------------------------------------------
        self.lbl_username = ttk.Label(self.card, text="Username:")
        self.ent_username = ttk.Entry(self.card)

        # Password ----------------------------------------------------------
        self.lbl_password = ttk.Label(self.card, text="Password:")
        self.ent_password = ttk.Entry(self.card, show="*")

        # Location selector -------------------------------------------------
        self.lbl_location = ttk.Label(self.card, text="Location:")
        self.cbo_location = ttk.Combobox(self.card,
                                         textvariable=self.selected_location,
                                         values=self.location_list,
                                         state="readonly")

        # Action button -----------------------------------------------------
        self.btn_login    = ttk.Button(self.card, text="Login",
                                       style="Accent.TButton",
                                       command=self._on_submit)

    def _layout_widgets(self):
        """Grid geometry for a clean, responsive card."""
        self.card.grid(row=0, column=0, padx=20, pady=20)
        for i in range(2):
            self.card.grid_columnconfigure(i, weight=1)

        # Row by row -------------------------------------------------------
        self.lbl_header.grid(  row=0, column=0, columnspan=2, pady=(0, 20))
        self.lbl_username.grid(row=1, column=0, sticky="e", pady=5)
        self.ent_username.grid(row=1, column=1, sticky="ew", pady=5)
        self.lbl_password.grid(row=2, column=0, sticky="e", pady=5)
        self.ent_password.grid(row=2, column=1, sticky="ew", pady=5)
        self.lbl_location.grid(row=3, column=0, sticky="e", pady=5)
        self.cbo_location.grid(row=3, column=1, sticky="ew", pady=5)
        self.btn_login.grid(   row=4, column=0, columnspan=2, pady=(20, 0))

    # ----------------------------------------------------------------------
    #  Business logic (unchanged except for messagebox feedback)
    # ----------------------------------------------------------------------
    def _on_submit(self):
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        location = self.selected_location.get()

        if location:
            idx = self.location_list.index(location)
            self.controller.set_location(self.location_id[idx])

        valid, user_id, role = login_functions.check_credentials(username, password)
        if valid:
            # Route to the appropriate dashboard
            match role:
                case "Manager":  self.controller.show_dashboardMan(user_id)
                case "Employee": self.controller.show_dashboardEmp(user_id)
                case "Owner":    self.controller.show_dashboardOwner(user_id)

            # Clear fields for next login
            self.ent_username.delete(0, tk.END)
            self.ent_password.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Credentials", "Incorrect username or password. Please try again.")
