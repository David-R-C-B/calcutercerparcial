import customtkinter as ctk
from tkinter import messagebox
from auth.auth_manager import AuthManager

class ProfileTab(ctk.CTkFrame):
    def __init__(self, parent_frame, username):
        super().__init__(parent_frame)
        self.username = username
        self.auth_manager = AuthManager()
        self.pack(fill="both", expand=True)
        
        self._crear_ui()

    def _crear_ui(self):
        # Título
        ctk.CTkLabel(self, text="Perfil de Usuario", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)

        # Información del Usuario
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(info_frame, text=f"Usuario: {self.username}", font=ctk.CTkFont(size=16)).pack(pady=20)

        # Selección de Tema
        theme_frame = ctk.CTkFrame(self)
        theme_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(theme_frame, text="Tema de la Aplicación:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 10))
        
        current_theme = self.auth_manager.get_user_theme(self.username)
        self.theme_var = ctk.StringVar(value=current_theme)
        
        self.theme_combo = ctk.CTkComboBox(theme_frame, variable=self.theme_var, 
                                           values=["blue", "green", "dark-blue"])
        self.theme_combo.pack(pady=10)

        # Botón Guardar
        ctk.CTkButton(self, text="Guardar Preferencias", command=self._guardar_preferencias).pack(pady=30)
        
        ctk.CTkLabel(self, text="Nota: Algunos cambios pueden requerir reiniciar la aplicación.", 
                     text_color="gray").pack(pady=10)

    def _guardar_preferencias(self):
        new_theme = self.theme_var.get()
        if self.auth_manager.set_user_theme(self.username, new_theme):
            messagebox.showinfo("Éxito", "Preferencias guardadas correctamente.\nReinicie la aplicación para ver todos los cambios.")
            # Intentar aplicar el tema inmediatamente (aunque CTk recomienda hacerlo al inicio)
            try:
                ctk.set_default_color_theme(new_theme)
            except Exception:
                pass # Puede fallar si ya se han creado widgets, pero vale la pena intentar
        else:
            messagebox.showerror("Error", "No se pudieron guardar las preferencias.")
