from gui.main_window import MainWindow
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    app = MainWindow()
    style = ttk.Style(app)
    style.theme_use("clam") # Keep clam as base, then override

    # Define cyberpunk theme colors
    bg_dark = "#1a1a2e"         # Deep dark blue/purple
    fg_light = "#e0e0e0"        # Off-white/light gray for main text
    accent_neon_green = "#00ff41" # Primary accent
    accent_neon_blue = "#00b8ff" # Secondary accent
    accent_neon_pink = "#ff007f" # Tertiary accent/highlight
    border_color = "#33334d"    # Darker blue/purple for borders
    text_bg_dark = "#2a2a4a"    # Slightly lighter deep dark for entry fields
    selection_color = "#00b8ff" # Use neon blue for selection

    # Configure general styles
    style.configure(".", background=bg_dark, foreground=fg_light, bordercolor=border_color)
    style.configure("TFrame", background=bg_dark, foreground=fg_light)
    style.configure("TLabel", background=bg_dark, foreground=fg_light)
    style.configure("TLabelframe", background=bg_dark, foreground=fg_light, bordercolor=border_color)
    style.configure("TLabelframe.Label", background=bg_dark, foreground=fg_light, font=("Consolas", 10, "bold")) # Cyberpunk font
    style.configure("TButton", background=bg_dark, foreground=fg_light, bordercolor=border_color,
                    focusthickness=1, focuscolor=accent_neon_green, font=("Consolas", 10))
    style.map("TButton", background=[("active", accent_neon_blue), ("!disabled", bg_dark)],
                         foreground=[("active", fg_light), ("!disabled", fg_light)])

    style.configure("TEntry", fieldbackground=text_bg_dark, foreground=fg_light, bordercolor=border_color,
                     insertcolor=accent_neon_green, selectbackground=selection_color, selectforeground=fg_light)
    style.configure("TCombobox", fieldbackground=text_bg_dark, foreground=fg_light, bordercolor=border_color,
                     selectbackground=selection_color, selectforeground=fg_light)
    style.map("TCombobox", fieldbackground=[("readonly", text_bg_dark)])

    # Notebook (Tabs) styling
    style.configure("TNotebook", background=bg_dark, bordercolor=border_color)
    style.configure("TNotebook.Tab", background=bg_dark, foreground=fg_light, bordercolor=border_color,
                                     font=("Consolas", 10))
    style.map("TNotebook.Tab", background=[("selected", accent_neon_green)],
                               foreground=[("selected", bg_dark)]) # Dark text on bright tab

    # Scrollbar styling (for Text widgets)
    style.configure("Vertical.TScrollbar", background=bg_dark, troughcolor=bg_dark, bordercolor=border_color,
                                           arrowcolor=fg_light)
    style.map("Vertical.TScrollbar", background=[("active", accent_neon_blue)])

    app.mainloop()