import customtkinter as ctk
from gui.generators_tab import GeneratorsTab
from gui.tests_tab import TestsTab
from gui.automata_main_tab import AutomataMainTab
from gui.distributions_tab import DistributionsTab
from auth.auth_manager import AuthManager
# Import classes inside methods to avoid circular imports if needed, or use string references if possible.
# But here we need to import them. To avoid circular import, we will import inside methods.

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Simulación y Modelación")
        self.geometry("1100x800")
        self.current_user = "Invitado"
        
        # Configurar grid layout
        self.grid_rowconfigure(0, weight=0) # Header row (fixed height)
        self.grid_rowconfigure(1, weight=1) # Content row (expandable)
        self.grid_columnconfigure(0, weight=1)

        # Header Frame
        self.header_frame = ctk.CTkFrame(self, height=50, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        # Title in Header
        self.header_label = ctk.CTkLabel(self.header_frame, text="Calculadora de Simulación", font=ctk.CTkFont(size=20, weight="bold"))
        self.header_label.pack(side="left", padx=20, pady=10)
        
        # Profile Button in Header
        self.profile_btn = ctk.CTkButton(self.header_frame, text="Perfil", width=100, command=self.open_profile_card)
        self.profile_btn.pack(side="right", padx=20, pady=10)

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view.add("Generadores")
        self.tab_view.add("Pruebas")
        self.tab_view.add("Autómatas / Juego de la Vida")
        self.tab_view.add("Distribuciones")

        self.generators_tab = GeneratorsTab(self.tab_view.tab("Generadores"))
        self.tests_tab = TestsTab(self.tab_view.tab("Pruebas"))
        self.automata_tab = AutomataMainTab(self.tab_view.tab("Autómatas / Juego de la Vida"))
        self.distributions_tab = DistributionsTab(self.tab_view.tab("Distribuciones"), self.generators_tab)

        # Authentication Logic
        self.auth_manager = AuthManager()
        self.withdraw() # Hide main window initially
        self.check_authentication()

    def set_current_user(self, username):
        self.current_user = username
        self.profile_btn.configure(text=f"Perfil: {username}")
        
        # Load and apply user theme
        user_theme = self.auth_manager.get_user_theme(username)
        ctk.set_default_color_theme(user_theme)

    def open_profile_card(self):
        # Create a Toplevel window as a card
        card = ctk.CTkToplevel(self)
        card.title("Perfil de Usuario")
        card.geometry("350x350")
        card.resizable(False, False)
        card.attributes("-topmost", True)
        
        # Center the card relative to the main window
        x = self.winfo_x() + self.winfo_width() - 370
        y = self.winfo_y() + 60
        card.geometry(f"+{x}+{y}")

        # Title
        ctk.CTkLabel(card, text="Información del Usuario", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))
        
        # User Info Frame
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=20)
        
        ctk.CTkLabel(info_frame, text="Usuario:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"{self.current_user}", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 10))
        
        # Separator
        ctk.CTkFrame(card, height=2, fg_color="gray50").pack(fill="x", padx=20, pady=10)
        
        # Theme Selection
        ctk.CTkLabel(card, text="Tema de la Aplicación:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        
        current_theme = self.auth_manager.get_user_theme(self.current_user)
        theme_var = ctk.StringVar(value=current_theme)
        theme_combo = ctk.CTkComboBox(card, variable=theme_var, values=["blue", "green", "dark-blue"])
        theme_combo.pack(fill="x", padx=20, pady=10)
        
        def save_theme():
            new_theme = theme_var.get()
            if self.auth_manager.set_user_theme(self.current_user, new_theme):
                try:
                    ctk.set_default_color_theme(new_theme)
                    # Note: Changing theme at runtime might not update all existing widgets perfectly without a restart
                    # or complex recursion, but it sets the default for new ones.
                    from tkinter import messagebox
                    messagebox.showinfo("Tema Guardado", "Preferencia guardada. Reinicie para aplicar cambios completos.")
                except Exception as e:
                    print(f"Error applying theme: {e}")
            card.destroy()

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(btn_frame, text="Guardar", command=save_theme, fg_color="green").pack(side="left", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text="Cerrar", command=card.destroy, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE")).pack(side="right", expand=True, padx=(5, 0))

    def check_authentication(self):
        if self.auth_manager.has_users():
            self.open_login_window()
        else:
            self.open_register_window()

    def open_login_window(self):
        from gui.login_window import LoginWindow
        LoginWindow(self)

    def open_register_window(self):
        from gui.register_window import RegisterWindow
        RegisterWindow(self)
