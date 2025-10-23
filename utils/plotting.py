import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

def plot_histograma(datos: list[float], titulo: str, parent_frame: tk.Frame):
    """
    Genera y muestra un histograma de los datos en un frame de Tkinter.

    Args:
        datos (list[float]): Lista de números a graficar.
        titulo (str): Título del histograma.
        parent_frame (tk.Frame): El frame de Tkinter donde se incrustará el gráfico.
    """
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Use the cyberpunk colors
    bg_dark = "#1a1a2e"
    fg_light = "#e0e0e0"
    accent_neon_green = "#00ff41"
    border_color = "#33334d"

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100, facecolor=bg_dark) # Set figure facecolor
    ax.hist(datos, bins=10, edgecolor=fg_light, alpha=0.7, color=accent_neon_green) # Set bar colors
    ax.set_title(titulo, color=fg_light) # Set title color
    ax.set_xlabel("Valor", color=fg_light) # Set xlabel color
    ax.set_ylabel("Frecuencia", color=fg_light) # Set ylabel color
    ax.set_facecolor(bg_dark) # Set axes facecolor
    ax.tick_params(axis='x', colors=fg_light) # Set x-axis tick color
    ax.tick_params(axis='y', colors=fg_light) # Set y-axis tick color
    ax.grid(True, linestyle='--', alpha=0.6, color=border_color)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()