import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

from cellular_automata.automata_1d_2d import Automata1D, Automata2D

class CellularAutomataSubTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.automata_1d = None
        self.automata_2d = None
        self.simulation_running = False
        self.after_id = None
        self.manual_mode_active = False 
        self.current_automata_type = "1D" 
        self._crear_ui()

    def _crear_ui(self):
        # Tabview para 1D y 2D
        self.automata_tabview = ctk.CTkTabview(self.parent_frame)
        self.automata_tabview.pack(expand=True, fill="both")

        self.automata_tabview.add("Autómata 1D")
        self.automata_tabview.add("Autómata 2D")

        # Configurar comando para cambio de pestaña
        self.automata_tabview.configure(command=self._on_tab_change)

        self.frame_1d = self.automata_tabview.tab("Autómata 1D")
        self.frame_2d = self.automata_tabview.tab("Autómata 2D")

        self._crear_ui_1d(self.frame_1d)
        self._crear_ui_2d(self.frame_2d)

        # Initialize with the default automata type and clear
        self._on_tab_change() 

    def _on_tab_change(self):
        self._pause_simulation() 
        self._clear_simulation() 

        selected_tab_text = self.automata_tabview.get()
        if selected_tab_text == "Autómata 1D":
            self.current_automata_type = "1D"
            if hasattr(self, 'manual_mode_2d_var'):
                self.manual_mode_2d_var.set(False)
        elif selected_tab_text == "Autómata 2D":
            self.current_automata_type = "2D"
            if hasattr(self, 'manual_mode_1d_var'):
                self.manual_mode_1d_var.set(False)
        
        self.manual_mode_active = (self.manual_mode_1d_var.get() if self.current_automata_type == "1D" else self.manual_mode_2d_var.get())

    def _crear_ui_1d(self, parent_frame):
        # 1D Controls
        control_frame = ctk.CTkFrame(parent_frame)
        control_frame.pack(padx=10, pady=10, fill="x")
        control_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(control_frame, text="Configuración Autómata 1D", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(control_frame, text="Tamaño (celdas):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.size_1d_entry = ctk.CTkEntry(control_frame)
        self.size_1d_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.size_1d_entry.insert(0, "101")

        ctk.CTkLabel(control_frame, text="Regla (0-255):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.rule_1d_entry = ctk.CTkEntry(control_frame)
        self.rule_1d_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.rule_1d_entry.insert(0, "30")

        ctk.CTkLabel(control_frame, text="Velocidad (ms/paso):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.speed_1d_entry = ctk.CTkEntry(control_frame)
        self.speed_1d_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.speed_1d_entry.insert(0, "100")

        self.manual_mode_1d_var = ctk.BooleanVar(value=False)
        self.manual_mode_1d_checkbutton = ctk.CTkCheckBox(control_frame, text="Modo Manual (clic para editar)",
                                                            variable=self.manual_mode_1d_var, command=self._toggle_manual_mode_1d)
        self.manual_mode_1d_checkbutton.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        self.start_1d_button = ctk.CTkButton(button_frame, text="Iniciar", command=self._start_simulation)
        self.start_1d_button.pack(side="left", padx=5)
        self.pause_1d_button = ctk.CTkButton(button_frame, text="Pausar", command=self._pause_simulation)
        self.pause_1d_button.pack(side="left", padx=5)
        self.next_step_1d_button = ctk.CTkButton(button_frame, text="Siguiente Paso", command=self._next_step)
        self.next_step_1d_button.pack(side="left", padx=5)
        self.clear_1d_button = ctk.CTkButton(button_frame, text="Limpiar", command=self._clear_simulation, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clear_1d_button.pack(side="left", padx=5)

        # 1D Visualization
        self.plot_frame_1d = ctk.CTkFrame(parent_frame)
        self.plot_frame_1d.pack(padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(self.plot_frame_1d, text="Visualización Autómata 1D").pack(pady=5)

        self.fig_1d, self.ax_1d = plt.subplots(figsize=(6, 6), dpi=100, facecolor="#2b2b2b") 
        self.canvas_1d = FigureCanvasTkAgg(self.fig_1d, master=self.plot_frame_1d)
        self.canvas_widget_1d = self.canvas_1d.get_tk_widget()
        self.canvas_widget_1d.pack(side="top", fill="both", expand=1)
        self.ax_1d.set_xticks([])
        self.ax_1d.set_yticks([])
        self.im_1d = None

        # Set axes background and text colors
        self.ax_1d.set_facecolor("#2b2b2b")
        self.ax_1d.tick_params(axis='x', colors='#e0e0e0')
        self.ax_1d.tick_params(axis='y', colors='#e0e0e0')
        self.ax_1d.xaxis.label.set_color('#e0e0e0')
        self.ax_1d.yaxis.label.set_color('#e0e0e0')
        self.ax_1d.title.set_color('#e0e0e0')

        self.canvas_1d.mpl_connect('button_press_event', self._on_click_1d)

    def _crear_ui_2d(self, parent_frame):
        # 2D Controls
        control_frame = ctk.CTkFrame(parent_frame)
        control_frame.pack(padx=10, pady=10, fill="x")
        control_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(control_frame, text="Configuración Autómata 2D", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(control_frame, text="Filas:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.rows_2d_entry = ctk.CTkEntry(control_frame)
        self.rows_2d_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.rows_2d_entry.insert(0, "30")

        ctk.CTkLabel(control_frame, text="Columnas:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.cols_2d_entry = ctk.CTkEntry(control_frame)
        self.cols_2d_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.cols_2d_entry.insert(0, "30")

        ctk.CTkLabel(control_frame, text="Reglas Nacimiento (ej. 3):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.birth_rules_2d_entry = ctk.CTkEntry(control_frame)
        self.birth_rules_2d_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.birth_rules_2d_entry.insert(0, "3")

        ctk.CTkLabel(control_frame, text="Reglas Supervivencia (ej. 23):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.survival_rules_2d_entry = ctk.CTkEntry(control_frame)
        self.survival_rules_2d_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.survival_rules_2d_entry.insert(0, "23")

        ctk.CTkLabel(control_frame, text="Velocidad (ms/paso):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.speed_2d_entry = ctk.CTkEntry(control_frame)
        self.speed_2d_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        self.speed_2d_entry.insert(0, "200")

        self.manual_mode_2d_var = ctk.BooleanVar(value=False)
        self.manual_mode_2d_checkbutton = ctk.CTkCheckBox(control_frame, text="Modo Manual (clic para editar)",
                                                            variable=self.manual_mode_2d_var, command=self._toggle_manual_mode_2d)
        self.manual_mode_2d_checkbutton.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        self.start_2d_button = ctk.CTkButton(button_frame, text="Iniciar", command=self._start_simulation)
        self.start_2d_button.pack(side="left", padx=5)
        self.pause_2d_button = ctk.CTkButton(button_frame, text="Pausar", command=self._pause_simulation)
        self.pause_2d_button.pack(side="left", padx=5)
        self.next_step_2d_button = ctk.CTkButton(button_frame, text="Siguiente Paso", command=self._next_step)
        self.next_step_2d_button.pack(side="left", padx=5)
        self.clear_2d_button = ctk.CTkButton(button_frame, text="Limpiar", command=self._clear_simulation, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clear_2d_button.pack(side="left", padx=5)

        # 2D Visualization
        self.plot_frame_2d = ctk.CTkFrame(parent_frame)
        self.plot_frame_2d.pack(padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(self.plot_frame_2d, text="Visualización Autómata 2D").pack(pady=5)

        self.fig_2d, self.ax_2d = plt.subplots(figsize=(6, 6), dpi=100, facecolor="#2b2b2b") 
        self.canvas_2d = FigureCanvasTkAgg(self.fig_2d, master=self.plot_frame_2d)
        self.canvas_widget_2d = self.canvas_2d.get_tk_widget()
        self.canvas_widget_2d.pack(side="top", fill="both", expand=1)
        self.ax_2d.set_xticks([])
        self.ax_2d.set_yticks([])
        self.ax_2d.set_aspect('equal', adjustable='box')
        self.im_2d = None

        # Set axes background and text colors
        self.ax_2d.set_facecolor("#2b2b2b")
        self.ax_2d.tick_params(axis='x', colors='#e0e0e0')
        self.ax_2d.tick_params(axis='y', colors='#e0e0e0')
        self.ax_2d.xaxis.label.set_color('#e0e0e0')
        self.ax_2d.yaxis.label.set_color('#e0e0e0')
        self.ax_2d.title.set_color('#e0e0e0')

        self.canvas_2d.mpl_connect('button_press_event', self._on_click_2d)

    def _toggle_manual_mode_1d(self):
        self.manual_mode_active = self.manual_mode_1d_var.get()
        if self.manual_mode_active:
            self._pause_simulation() 
            self.rule_1d_entry.configure(state="disabled")
            self.size_1d_entry.configure(state="disabled")
            self._initialize_manual_grid_1d() 
        else:
            self.rule_1d_entry.configure(state="normal")
            self.size_1d_entry.configure(state="normal")

    def _initialize_manual_grid_1d(self):
        try:
            size = int(self.size_1d_entry.get())
            self.automata_1d = Automata1D(size, rule_number=0, initial_state=np.zeros(size, dtype=int)) 
            self._draw_grid_1d()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
            self.manual_mode_1d_var.set(False)
            self.rule_1d_entry.configure(state="normal")
            self.size_1d_entry.configure(state="normal")

    def _on_click_1d(self, event):
        if self.current_automata_type == "1D" and self.manual_mode_active and self.automata_1d and event.inaxes == self.ax_1d:
            x = int(event.xdata)
            if 0 <= x < self.automata_1d.size:
                if not self.automata_1d.history:
                    self.automata_1d.history.append(np.zeros(self.automata_1d.size, dtype=int))
                
                current_state = self.automata_1d.history[0][x]
                self.automata_1d.history[0][x] = 1 - current_state
                self.automata_1d.current_state = self.automata_1d.history[0].copy()
                self._draw_grid_1d()

    def _toggle_manual_mode_2d(self):
        self.manual_mode_active = self.manual_mode_2d_var.get()
        if self.manual_mode_active:
            self._pause_simulation() 
            self.rows_2d_entry.configure(state="disabled")
            self.cols_2d_entry.configure(state="disabled")
            self.birth_rules_2d_entry.configure(state="disabled")
            self.survival_rules_2d_entry.configure(state="disabled")
            self._initialize_manual_grid_2d() 
        else:
            self.rows_2d_entry.configure(state="normal")
            self.cols_2d_entry.configure(state="normal")
            self.birth_rules_2d_entry.configure(state="normal")
            self.survival_rules_2d_entry.configure(state="normal")

    def _initialize_manual_grid_2d(self):
        try:
            rows = int(self.rows_2d_entry.get())
            cols = int(self.cols_2d_entry.get())
            self.automata_2d = Automata2D(rows, cols, birth_rules=[3], survival_rules=[2,3], initial_state=np.zeros((rows, cols), dtype=int)) 
            self._draw_grid_2d()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
            self.manual_mode_2d_var.set(False)
            self.rows_2d_entry.configure(state="normal")
            self.cols_2d_entry.configure(state="normal")
            self.birth_rules_2d_entry.configure(state="normal")
            self.survival_rules_2d_entry.configure(state="normal")

    def _on_click_2d(self, event):
        if self.current_automata_type == "2D" and self.manual_mode_active and self.automata_2d and event.inaxes == self.ax_2d:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < self.automata_2d.cols and 0 <= y < self.automata_2d.rows:
                current_state = self.automata_2d.grid[y, x]
                self.automata_2d.grid[y, x] = 1 - current_state
                self._draw_grid_2d()

    def _start_simulation(self):
        self._pause_simulation() 
        self.simulation_running = True

        if self.current_automata_type == "1D":
            try:
                size = int(self.size_1d_entry.get())
                rule = int(self.rule_1d_entry.get())
                if self.manual_mode_1d_var.get():
                    if self.automata_1d is None or self.automata_1d.size != size:
                        self.automata_1d = Automata1D(size, rule, initial_state=np.zeros(size, dtype=int))
                    self.automata_1d.rule_number = rule 
                    self.automata_1d.rule_set = self.automata_1d._get_rule_set(rule)
                    self.automata_1d.current_state = self.automata_1d.history[0].copy()
                    self.automata_1d.history = [self.automata_1d.current_state.copy()]
                else:
                    initial_state = np.random.randint(0, 2, size)
                    self.automata_1d = Automata1D(size, rule, initial_state=initial_state)
                self._draw_grid_1d()
                self._update_simulation_1d()
            except ValueError as e:
                messagebox.showerror("Error de Entrada", str(e))
                self._pause_simulation()
                return
        elif self.current_automata_type == "2D":
            try:
                rows = int(self.rows_2d_entry.get())
                cols = int(self.cols_2d_entry.get())
                birth_rules_str = self.birth_rules_2d_entry.get()
                survival_rules_str = self.survival_rules_2d_entry.get()
                birth_rules = [int(r.strip()) for r in birth_rules_str.split(',') if r.strip()]
                survival_rules = [int(r.strip()) for r in survival_rules_str.split(',') if r.strip()]

                if self.manual_mode_2d_var.get():
                    if self.automata_2d is None or self.automata_2d.rows != rows or self.automata_2d.cols != cols:
                        self.automata_2d = Automata2D(rows, cols, birth_rules, survival_rules, initial_state=np.zeros((rows, cols), dtype=int))
                    self.automata_2d.birth_rules = set(birth_rules)
                    self.automata_2d.survival_rules = set(survival_rules)
                else:
                    initial_state = np.random.randint(0, 2, (rows, cols))
                    self.automata_2d = Automata2D(rows, cols, birth_rules, survival_rules, initial_state=initial_state)
                self._draw_grid_2d()
                self._update_simulation_2d()
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
        if not self.simulation_running:
            if self.current_automata_type == "1D" and self.automata_1d:
                self.automata_1d.next_generation()
                self._draw_grid_1d()
            elif self.current_automata_type == "2D" and self.automata_2d:
                self.automata_2d.next_generation()
                self._draw_grid_2d()

    def _clear_simulation(self):
        self._pause_simulation()
        if hasattr(self, 'manual_mode_1d_var'):
            self.manual_mode_1d_var.set(False)
        if hasattr(self, 'manual_mode_2d_var'):
            self.manual_mode_2d_var.set(False)
        self.manual_mode_active = False 

        if self.current_automata_type == "1D":
            self.automata_1d = None
            self.ax_1d.clear()
            self.ax_1d.set_xticks([])
            self.ax_1d.set_yticks([])
            self.canvas_1d.draw()
            self.size_1d_entry.configure(state="normal")
            self.rule_1d_entry.configure(state="normal")
            self.manual_mode_1d_checkbutton.configure(state="normal")
        elif self.current_automata_type == "2D":
            self.automata_2d = None
            self.ax_2d.clear()
            self.ax_2d.set_xticks([])
            self.ax_2d.set_yticks([])
            self.canvas_2d.draw()
            self.rows_2d_entry.configure(state="normal")
            self.cols_2d_entry.configure(state="normal")
            self.birth_rules_2d_entry.configure(state="normal")
            self.survival_rules_2d_entry.configure(state="normal")
            self.manual_mode_2d_checkbutton.configure(state="normal")

        self._enable_controls() 

    def _update_simulation_1d(self):
        if self.simulation_running and self.automata_1d:
            self.automata_1d.next_generation()
            self._draw_grid_1d()
            try:
                speed_ms = int(self.speed_1d_entry.get())
            except ValueError:
                speed_ms = 100
            self.after_id = self.parent_frame.after(speed_ms, self._update_simulation_1d)

    def _update_simulation_2d(self):
        if self.simulation_running and self.automata_2d:
            self.automata_2d.next_generation()
            self._draw_grid_2d()
            try:
                speed_ms = int(self.speed_2d_entry.get())
            except ValueError:
                speed_ms = 200
            self.after_id = self.parent_frame.after(speed_ms, self._update_simulation_2d)

    def _draw_grid_1d(self):
        if self.automata_1d:
            history_grid = np.vstack(self.automata_1d.history)
            self.ax_1d.clear()
            self.ax_1d.imshow(history_grid, cmap='binary', vmin=0, vmax=1, extent=[0, self.automata_1d.size, len(self.automata_1d.history), 0])
            
            self.ax_1d.set_xticks(np.arange(0, self.automata_1d.size + 1), minor=True)
            self.ax_1d.set_yticks(np.arange(0, len(self.automata_1d.history) + 1), minor=True)
            self.ax_1d.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
            self.ax_1d.tick_params(which='minor', size=0)

            self.ax_1d.set_title(f"Regla {self.automata_1d.rule_number}")
            self.ax_1d.set_xticks([])
            self.ax_1d.set_yticks([])
            self.canvas_1d.draw()

    def _draw_grid_2d(self):
        if self.automata_2d:
            grid = self.automata_2d.get_grid()
            self.ax_2d.clear()
            self.ax_2d.imshow(grid, cmap='binary', vmin=0, vmax=1, extent=[0, self.automata_2d.cols, self.automata_2d.rows, 0])
            
            self.ax_2d.set_xticks(np.arange(0, self.automata_2d.cols + 1), minor=True)
            self.ax_2d.set_yticks(np.arange(0, self.automata_2d.rows + 1), minor=True)
            self.ax_2d.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
            self.ax_2d.tick_params(which='minor', size=0)

            self.ax_2d.set_title(f"Reglas B:{list(self.automata_2d.birth_rules)}/S:{list(self.automata_2d.survival_rules)}")
            self.ax_2d.set_xticks([])
            self.ax_2d.set_yticks([])
            self.canvas_2d.draw()

    def _disable_controls(self):
        if self.current_automata_type == "1D":
            self.size_1d_entry.configure(state="disabled")
            self.rule_1d_entry.configure(state="disabled")
            self.manual_mode_1d_checkbutton.configure(state="disabled")
        elif self.current_automata_type == "2D":
            self.rows_2d_entry.configure(state="disabled")
            self.cols_2d_entry.configure(state="disabled")
            self.birth_rules_2d_entry.configure(state="disabled")
            self.survival_rules_2d_entry.configure(state="disabled")
            self.manual_mode_2d_checkbutton.configure(state="disabled")

        self.start_1d_button.configure(state="disabled")
        self.next_step_1d_button.configure(state="disabled")
        self.start_2d_button.configure(state="disabled")
        self.next_step_2d_button.configure(state="disabled")

    def _enable_controls(self):
        if self.current_automata_type == "1D":
            self.size_1d_entry.configure(state="normal")
            self.rule_1d_entry.configure(state="normal")
            self.manual_mode_1d_checkbutton.configure(state="normal")
        elif self.current_automata_type == "2D":
            self.rows_2d_entry.configure(state="normal")
            self.cols_2d_entry.configure(state="normal")
            self.birth_rules_2d_entry.configure(state="normal")
            self.survival_rules_2d_entry.configure(state="normal")
            self.manual_mode_2d_checkbutton.configure(state="normal")

        self.start_1d_button.configure(state="normal")
        self.next_step_1d_button.configure(state="normal")
        self.start_2d_button.configure(state="normal")
        self.next_step_2d_button.configure(state="normal")
