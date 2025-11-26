from gui.main_window import MainWindow
from gui.login_window import LoginWindow
from gui.register_window import RegisterWindow
from auth.auth_manager import AuthManager
import customtkinter as ctk

if __name__ == "__main__":
    # Initialize CustomTkinter settings
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = MainWindow()
    app.mainloop()