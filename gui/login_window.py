import customtkinter as ctk
from tkinter import messagebox
from auth.auth_manager import AuthManager
from gui.main_window import MainWindow
from gui.register_window import RegisterWindow

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Inicio de Sesión - Calculadora de Simulación")
        self.geometry("400x500")
        self.resizable(False, False)
        self.attributes("-topmost", True) # Keep on top

        self.auth_manager = AuthManager()
        self._crear_ui()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _crear_ui(self):
        # Título
        ctk.CTkLabel(self, text="Bienvenido", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(40, 20))

        # Usuario
        ctk.CTkLabel(self, text="Usuario:").pack(pady=(10, 5), padx=40, anchor="w")
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Ingrese su usuario")
        self.username_entry.pack(pady=5, padx=40, fill="x")

        # Contraseña
        ctk.CTkLabel(self, text="Contraseña:").pack(pady=(10, 5), padx=40, anchor="w")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Ingrese su contraseña", show="*")
        self.password_entry.pack(pady=5, padx=40, fill="x")

        # Código 2FA
        ctk.CTkLabel(self, text="Código 2FA (Google Authenticator):").pack(pady=(10, 5), padx=40, anchor="w")
        self.totp_entry = ctk.CTkEntry(self, placeholder_text="000000")
        self.totp_entry.pack(pady=5, padx=40, fill="x")

        # Botón Login
        ctk.CTkButton(self, text="Iniciar Sesión", command=self._login).pack(pady=(30, 10), padx=40, fill="x")

        # Botón Registrarse (si no hay usuarios o como opción)
        ctk.CTkButton(self, text="Registrar Nuevo Usuario", command=self._abrir_registro, 
                      fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE")).pack(pady=10, padx=40, fill="x")

    def _login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        totp_code = self.totp_entry.get()

        if not username or not password or not totp_code:
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        success, message = self.auth_manager.verify_login(username, password, totp_code)

        if success:
            self.destroy()
            if hasattr(self.parent, 'set_current_user'):
                self.parent.set_current_user(username)
            self.parent.deiconify() # Show main window
        else:
            messagebox.showerror("Error de Login", message)

    def _abrir_registro(self):
        self.destroy()
        # Call parent to open register window
        if hasattr(self.parent, 'open_register_window'):
            self.parent.open_register_window()

    def _on_close(self):
        self.destroy()
        self.parent.destroy() # Close app if login is closed
