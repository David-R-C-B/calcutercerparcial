import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import qrcode
from auth.auth_manager import AuthManager

class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Registro - Calculadora de Simulación")
        self.geometry("500x800")
        self.resizable(True, True)
        self.attributes("-topmost", True)

        self.auth_manager = AuthManager()
        self._crear_ui()
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _crear_ui(self):
        # Título
        ctk.CTkLabel(self, text="Crear Nueva Cuenta", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 20))

        # Usuario
        ctk.CTkLabel(self, text="Usuario:").pack(pady=(10, 5), padx=40, anchor="w")
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Elija un usuario")
        self.username_entry.pack(pady=5, padx=40, fill="x")

        # Contraseña
        ctk.CTkLabel(self, text="Contraseña:").pack(pady=(10, 5), padx=40, anchor="w")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Elija una contraseña", show="*")
        self.password_entry.pack(pady=5, padx=40, fill="x")

        # Confirmar Contraseña
        ctk.CTkLabel(self, text="Confirmar Contraseña:").pack(pady=(10, 5), padx=40, anchor="w")
        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Repita la contraseña", show="*")
        self.confirm_password_entry.pack(pady=5, padx=40, fill="x")

        # Frame para QR (inicialmente vacío o oculto)
        self.qr_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.qr_frame.pack(pady=20, fill="both", expand=True)
        self.qr_label = ctk.CTkLabel(self.qr_frame, text="")
        self.qr_label.pack()

        # Botón Registrar
        self.register_btn = ctk.CTkButton(self, text="Registrar y Generar 2FA", command=self._registrar)
        self.register_btn.pack(pady=20, padx=40, fill="x")

        # Botón Volver al Login
        ctk.CTkButton(self, text="Volver al Login", command=self._volver_login, 
                      fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE")).pack(pady=10, padx=40, fill="x")

    def _registrar(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        try:
            # Registrar y obtener URI y secreto
            totp_uri, totp_secret = self.auth_manager.register_user(username, password)
            
            # Generar imagen QR
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(totp_uri)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.convert("RGB") # Convert to standard PIL Image to fix CTkImage error
            
            # Convertir para CTkImage
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
            
            self.qr_label.configure(image=ctk_img, text="")
            
            # Mostrar clave manual también
            if hasattr(self, 'manual_key_label'):
                self.manual_key_label.destroy()
            
            self.manual_key_label = ctk.CTkEntry(self.qr_frame, width=300, justify="center")
            self.manual_key_label.pack(pady=5)
            self.manual_key_label.insert(0, totp_secret)
            self.manual_key_label.configure(state="readonly")
            
            ctk.CTkLabel(self.qr_frame, text="Si no puede escanear, ingrese esta clave manualmente:").pack(pady=(5,0))

            self.register_btn.configure(state="normal", text="Ir a Iniciar Sesión", command=self._volver_login, fg_color="green")
            
            messagebox.showinfo("Registro Exitoso", "Usuario registrado correctamente.\n\n1. ESCANEE el QR o copie la clave.\n2. Haga clic en 'Ir a Iniciar Sesión'.")


        except ValueError as e:
            messagebox.showerror("Error de Registro", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def _volver_login(self):
        self.destroy()
        if hasattr(self.parent, 'open_login_window'):
            self.parent.open_login_window()

    def _on_close(self):
        self.destroy()
        self.parent.destroy() # Close app
