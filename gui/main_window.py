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
        
        # Configurar grid layout (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

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
