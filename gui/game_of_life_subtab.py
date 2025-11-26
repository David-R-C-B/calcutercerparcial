import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

from cellular_automata.game_of_life import GameOfLife

class GameOfLifeSubTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.game_of_life = None
        self.simulation_running = False
        self.after_id = None
        self.manual_mode_active = False
        self._crear_ui()

    def _crear_ui(self):
        control_frame = ctk.CTkFrame(self.parent_frame)
        control_frame.pack(padx=10, pady=10, fill="x")
        control_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(control_frame, text="Configuración Juego de la Vida", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(control_frame, text="Filas:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.rows_entry = ctk.CTkEntry(control_frame)
        self.rows_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.rows_entry.insert(0, "50")

        ctk.CTkLabel(control_frame, text="Columnas:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.cols_entry = ctk.CTkEntry(control_frame)
        self.cols_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.cols_entry.insert(0, "50")

        ctk.CTkLabel(control_frame, text="Velocidad (ms/paso):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.speed_entry = ctk.CTkEntry(control_frame)
        self.speed_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.speed_entry.insert(0, "100")

        self.manual_mode_var = ctk.BooleanVar(value=False)
        self.manual_mode_checkbutton = ctk.CTkCheckBox(control_frame, text="Modo Manual (clic para editar)",
                                                            variable=self.manual_mode_var, command=self._toggle_manual_mode)
        self.manual_mode_checkbutton.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        self.start_button = ctk.CTkButton(button_frame, text="Iniciar", command=self._start_simulation)
        self.start_button.pack(side="left", padx=5)
        self.pause_button = ctk.CTkButton(button_frame, text="Pausar", command=self._pause_simulation)
        self.pause_button.pack(side="left", padx=5)
        self.next_step_button = ctk.CTkButton(button_frame, text="Siguiente Paso", command=self._next_step)
        self.next_step_button.pack(side="left", padx=5)
        self.clear_button = ctk.CTkButton(button_frame, text="Limpiar", command=self._clear_simulation, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clear_button.pack(side="left", padx=5)
        self.random_button = ctk.CTkButton(button_frame, text="Aleatorio", command=self._initialize_random_grid)
        self.random_button.pack(side="left", padx=5)

        self.plot_frame = ctk.CTkFrame(self.parent_frame)
        self.plot_frame.pack(padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(self.plot_frame, text="Visualización Juego de la Vida").pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100, facecolor="#2b2b2b") 
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="top", fill="both", expand=1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_aspect('equal', adjustable='box')
        self.im = None

        # Set axes background and text colors
        self.ax.set_facecolor("#2b2b2b")
        self.ax.tick_params(axis='x', colors='#e0e0e0')
        self.ax.tick_params(axis='y', colors='#e0e0e0')
        self.ax.xaxis.label.set_color('#e0e0e0')
        self.ax.yaxis.label.set_color('#e0e0e0')
        self.ax.title.set_color('#e0e0e0')

        self.canvas.mpl_connect('button_press_event', self._on_click)

    def _toggle_manual_mode(self):
        self.manual_mode_active = self.manual_mode_var.get()
        if self.manual_mode_active:
            self._pause_simulation() 
            self.rows_entry.configure(state="disabled")
            self.cols_entry.configure(state="disabled")
            self.random_button.configure(state="disabled")
            self._initialize_manual_grid() 
        else:
            self.rows_entry.configure(state="normal")
            self.cols_entry.configure(state="normal")
            self.random_button.configure(state="normal")

    def _initialize_manual_grid(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.game_of_life = GameOfLife(rows, cols, initial_state=np.zeros((rows, cols), dtype=int)) 
            self._draw_grid()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
            self.manual_mode_var.set(False)
            self.rows_entry.configure(state="normal")
            self.cols_entry.configure(state="normal")
            self.random_button.configure(state="normal")

    def _initialize_random_grid(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.game_of_life = GameOfLife(rows, cols) 
            self._draw_grid()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))

    def _on_click(self, event):
        if self.manual_mode_active and self.game_of_life and event.inaxes == self.ax:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < self.game_of_life.cols and 0 <= y < self.game_of_life.rows:
                current_state = self.game_of_life.grid[y, x]
                self.game_of_life.grid[y, x] = 1 - current_state
                self._draw_grid()

    def _start_simulation(self):
        self._pause_simulation() 
        self.simulation_running = True

        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            if self.game_of_life is None or self.game_of_life.rows != rows or self.game_of_life.cols != cols:
                self.game_of_life = GameOfLife(rows, cols)
            
            self._draw_grid()
            self._update_simulation()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
            self._pause_simulation()
            return

        self._disable_controls()

    def _pause_simulation(self):
        self.simulation_running = False
        if self.after_id:
            self.parent_frame.after_cancel(self.after_id)
            self.after_id = None
        self._enable_controls()

    def _next_step(self):
        if not self.simulation_running and self.game_of_life:
            self.game_of_life.next_generation()
            self._draw_grid()

    def _clear_simulation(self):
        self._pause_simulation()
        self.manual_mode_var.set(False)
        self.manual_mode_active = False
        self.game_of_life = None
        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
        self.rows_entry.configure(state="normal")
        self.cols_entry.configure(state="normal")
        self.random_button.configure(state="normal")
        self._enable_controls() 

    def _update_simulation(self):
        if self.simulation_running and self.game_of_life:
            self.game_of_life.next_generation()
            self._draw_grid()
            try:
                speed_ms = int(self.speed_entry.get())
            except ValueError:
                speed_ms = 100
            self.after_id = self.parent_frame.after(speed_ms, self._update_simulation)

    def _draw_grid(self):
        if self.game_of_life:
            grid = self.game_of_life.get_grid()
            self.ax.clear()
            self.ax.imshow(grid, cmap='Greens', vmin=0, vmax=1, extent=[0, self.game_of_life.cols, self.game_of_life.rows, 0]) 
            
            self.ax.set_xticks(np.arange(0, self.game_of_life.cols + 1), minor=True)
            self.ax.set_yticks(np.arange(0, self.game_of_life.rows + 1), minor=True)
            self.ax.grid(which='minor', color='#33334d', linestyle='-', linewidth=0.5) 
            self.ax.tick_params(which='minor', size=0)

            self.ax.set_title("Juego de la Vida", color='#e0e0e0')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.canvas.draw()

    def _disable_controls(self):
        self.rows_entry.configure(state="disabled")
        self.cols_entry.configure(state="disabled")
        self.speed_entry.configure(state="disabled")
        self.manual_mode_checkbutton.configure(state="disabled")
        self.start_button.configure(state="disabled")
        self.next_step_button.configure(state="disabled")
        self.random_button.configure(state="disabled")

    def _enable_controls(self):
        self.rows_entry.configure(state="normal")
        self.cols_entry.configure(state="normal")
        self.speed_entry.configure(state="normal")
        self.manual_mode_checkbutton.configure(state="normal")
        self.start_button.configure(state="normal")
        self.next_step_button.configure(state="normal")
        self.random_button.configure(state="normal")
