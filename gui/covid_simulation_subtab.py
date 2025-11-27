import customtkinter as ctk
import tkinter as tk
import random
import copy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class CovidSimulationSubTab(ctk.CTkFrame):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        self.pack(fill="both", expand=True)
        
        # Parameters
        self.rows = 50
        self.cols = 50
        self.cell_size = 10
        self.grid_data = []
        self.running = False
        
        # Rates
        self.infection_rate = 0.3
        self.recovery_rate = 0.1
        self.mortality_rate = 0.02
        self.asymptomatic_prob = 0.2
        self.relapse_rate = 0.01
        
        # States: 0=Susceptible, 1=Infected, 2=Recovered, 3=Dead, 4=Asymptomatic
        self.colors = {
            0: "#4a4a4a", # Gray (Susceptible)
            1: "#ff4444", # Red (Infected)
            2: "#44ff44", # Green (Recovered)
            3: "#000000", # Black (Dead)
            4: "#ffff44"  # Yellow (Asymptomatic)
        }
        
        # Graph Data
        self.history_s = []
        self.history_i = []
        self.history_r = []
        self.history_d = []
        self.history_a = []
        
        self._crear_ui()
        # Delay initial reset to allow layout to settle
        self.after(100, self._reset_grid)

    def _crear_ui(self):
        # Layout: Left Control Panel, Right Canvas & Graph
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Left Panel (Controls) ---
        control_panel = ctk.CTkFrame(self, width=250)
        control_panel.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        control_panel.grid_propagate(False) # Fixed width
        
        # Scrollable frame for controls if needed, but simple frame is okay for now
        scroll = ctk.CTkScrollableFrame(control_panel, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(scroll, text="Configuración COVID-19", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 10))
        
        # Helper to create sliders
        def create_slider(parent, text, attr_name, default, from_=0.0, to=1.0):
            ctk.CTkLabel(parent, text=text).pack(pady=(5, 0))
            slider = ctk.CTkSlider(parent, from_=from_, to=to, command=lambda v: self._update_params())
            slider.set(default)
            slider.pack(pady=(0, 2))
            label = ctk.CTkLabel(parent, text=f"{default:.2f}")
            label.pack()
            setattr(self, f"{attr_name}_slider", slider)
            setattr(self, f"{attr_name}_label", label)

        create_slider(scroll, "Tasa de Infección:", "infection", 0.3)
        create_slider(scroll, "Tasa de Recuperación:", "recovery", 0.1)
        create_slider(scroll, "Tasa de Mortalidad:", "mortality", 0.02)
        create_slider(scroll, "Prob. Asintomático:", "asymptomatic", 0.2)
        create_slider(scroll, "Tasa de Recaída:", "relapse", 0.01)
        
        # Speed Control
        ctk.CTkLabel(scroll, text="Velocidad (ms):").pack(pady=(10, 0))
        self.speed_slider = ctk.CTkSlider(scroll, from_=10, to=500, command=lambda v: self._update_params())
        self.speed_slider.set(100)
        self.speed_slider.pack(pady=(0, 2))
        self.speed_label = ctk.CTkLabel(scroll, text="100")
        self.speed_label.pack()
        
        # Buttons
        self.start_btn = ctk.CTkButton(scroll, text="Iniciar", command=self._toggle_simulation, fg_color="green")
        self.start_btn.pack(pady=(20, 10), padx=10, fill="x")
        
        ctk.CTkButton(scroll, text="Reiniciar", command=self._reset_grid, fg_color="gray").pack(pady=10, padx=10, fill="x")
        
        # Legend
        legend_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        legend_frame.pack(pady=20, padx=5, fill="x")
        ctk.CTkLabel(legend_frame, text="Leyenda:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self._create_legend_item(legend_frame, "Susceptible", "#4a4a4a")
        self._create_legend_item(legend_frame, "Infectado", "#ff4444")
        self._create_legend_item(legend_frame, "Asintomático", "#ffff44")
        self._create_legend_item(legend_frame, "Recuperado", "#44ff44")
        self._create_legend_item(legend_frame, "Fallecido", "#000000")
        
        # Stats
        self.stats_label = ctk.CTkLabel(control_panel, text="S:0 I:0 A:0 R:0 D:0", font=ctk.CTkFont(size=12))
        self.stats_label.pack(side="bottom", pady=10)

        # --- Right Panel (Canvas + Graph) ---
        right_panel = ctk.CTkFrame(self)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_panel.grid_rowconfigure(0, weight=2) # Canvas gets more space
        right_panel.grid_rowconfigure(1, weight=1) # Graph gets less
        right_panel.grid_columnconfigure(0, weight=1)

        # Canvas
        self.canvas = tk.Canvas(right_panel, bg="#2b2b2b", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.canvas.bind("<Configure>", self._on_resize)
        
        # Graph
        self.fig, self.ax = plt.subplots(figsize=(5, 2), dpi=100, facecolor="#2b2b2b")
        self.ax.set_facecolor("#2b2b2b")
        self.ax.tick_params(colors='white', labelsize=8)
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white') 
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.graph_canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

    def _create_legend_item(self, parent, text, color):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=2)
        color_box = ctk.CTkLabel(frame, text="  ", fg_color=color, width=20, corner_radius=5)
        color_box.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(frame, text=text).pack(side="left")

    def _update_params(self):
        self.infection_rate = self.infection_slider.get()
        self.recovery_rate = self.recovery_slider.get()
        self.mortality_rate = self.mortality_slider.get()
        self.asymptomatic_prob = self.asymptomatic_slider.get()
        self.relapse_rate = self.relapse_slider.get()
        
        # Update labels
        self.infection_label.configure(text=f"{self.infection_rate:.2f}")
        self.recovery_label.configure(text=f"{self.recovery_rate:.2f}")
        self.mortality_label.configure(text=f"{self.mortality_rate:.2f}")
        self.asymptomatic_label.configure(text=f"{self.asymptomatic_prob:.2f}")
        self.relapse_label.configure(text=f"{self.relapse_rate:.2f}")
        
        # Update speed label
        if hasattr(self, 'speed_slider'):
            self.speed_label.configure(text=f"{int(self.speed_slider.get())}")

    def _reset_grid(self):
        self.running = False
        self.start_btn.configure(text="Iniciar", fg_color="green")
        
        self.grid_data = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Infect a few random cells
        for _ in range(5):
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            self.grid_data[r][c] = 1 # Start with symptomatic infected
            
        self.history_s, self.history_i, self.history_r, self.history_d, self.history_a = [], [], [], [], []
            
        self._draw_grid()
        self._update_stats()
        self._update_graph()

    def _draw_grid(self):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width < 50: return

        grid_width = self.cols * self.cell_size
        grid_height = self.rows * self.cell_size
        start_x = (canvas_width - grid_width) // 2
        start_y = (canvas_height - grid_height) // 2
        
        for r in range(self.rows):
            for c in range(self.cols):
                state = self.grid_data[r][c]
                color = self.colors[state]
                x1 = start_x + c * self.cell_size
                y1 = start_y + r * self.cell_size
                self.canvas.create_rectangle(x1, y1, x1+self.cell_size, y1+self.cell_size, fill=color, outline="#333333")

    def _toggle_simulation(self):
        if self.running:
            self.running = False
            self.start_btn.configure(text="Continuar", fg_color="green")
        else:
            self.running = True
            self.start_btn.configure(text="Pausar", fg_color="#e6b800")
            self._run_step()

    def _run_step(self):
        if not self.running: return
            
        new_grid = copy.deepcopy(self.grid_data)
        
        for r in range(self.rows):
            for c in range(self.cols):
                state = self.grid_data[r][c]
                
                # Logic for Infected (1) or Asymptomatic (4)
                if state == 1 or state == 4:
                    # Try to infect neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if self.grid_data[nr][nc] == 0: # Susceptible
                                    if random.random() < self.infection_rate:
                                        # Determine if new infection is asymptomatic
                                        if random.random() < self.asymptomatic_prob:
                                            new_grid[nr][nc] = 4
                                        else:
                                            new_grid[nr][nc] = 1
                    
                    # Try to recover or die
                    if random.random() < self.recovery_rate:
                        new_grid[r][c] = 2 # Recovered
                    elif random.random() < self.mortality_rate:
                        new_grid[r][c] = 3 # Dead
                
                # Logic for Recovered (2) -> Relapse
                elif state == 2:
                    if random.random() < self.relapse_rate:
                        new_grid[r][c] = 1 # Relapse to symptomatic

        self.grid_data = new_grid
        self._draw_grid()
        self._update_stats()
        self._update_graph()
        
        delay = int(self.speed_slider.get()) if hasattr(self, 'speed_slider') else 100
        self.after(delay, self._run_step)

    def _update_stats(self):
        s = sum(row.count(0) for row in self.grid_data)
        i = sum(row.count(1) for row in self.grid_data)
        r = sum(row.count(2) for row in self.grid_data)
        d = sum(row.count(3) for row in self.grid_data)
        a = sum(row.count(4) for row in self.grid_data)
        
        self.stats_label.configure(text=f"S:{s} | I:{i} | A:{a} | R:{r} | D:{d}")
        
        self.history_s.append(s)
        self.history_i.append(i)
        self.history_r.append(r)
        self.history_d.append(d)
        self.history_a.append(a)
        
        # Keep graph history manageable
        if len(self.history_s) > 200:
            self.history_s.pop(0)
            self.history_i.pop(0)
            self.history_r.pop(0)
            self.history_d.pop(0)
            self.history_a.pop(0)

    def _update_graph(self):
        self.ax.clear()
        x = range(len(self.history_s))
        self.ax.plot(x, self.history_s, label='S', color='#4a4a4a')
        self.ax.plot(x, self.history_i, label='I', color='#ff4444')
        self.ax.plot(x, self.history_a, label='A', color='#ffff44')
        self.ax.plot(x, self.history_r, label='R', color='#44ff44')
        self.ax.plot(x, self.history_d, label='D', color='white') # White for visibility on dark bg
        
        self.ax.legend(loc='upper right', fontsize='small', facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
        self.graph_canvas.draw()

    def _on_resize(self, event):
        self._draw_grid()
