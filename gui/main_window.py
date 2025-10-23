import tkinter as tk
from tkinter import ttk
from gui.generators_tab import GeneratorsTab
from gui.tests_tab import TestsTab
from gui.automata_main_tab import AutomataMainTab
from gui.distributions_tab import DistributionsTab



class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Simulación y Modelación")
        self.geometry("1000x700")

        self.generators_tab_instance = None # To store the instance

        self._crear_pestañas()

    def _crear_pestañas(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Pestaña de Generadores
        self.generators_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.generators_frame, text="Generadores")
        self.generators_tab_instance = GeneratorsTab(self.generators_frame) # Store the instance

        # Pestaña de Pruebas
        self.tests_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tests_frame, text="Pruebas")
        TestsTab(self.tests_frame)

        # Pestaña de Autómatas / Juego de la Vida
        self.automata_gol_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.automata_gol_frame, text="Autómatas / Juego de la Vida")
        AutomataMainTab(self.automata_gol_frame) # Inicializar la pestaña principal de Autómatas

        # Pestaña de Distribuciones
        self.distributions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.distributions_frame, text="Distribuciones")
        DistributionsTab(self.distributions_frame, get_prng_callback=self.get_prng_numbers_from_generators_tab)

    def get_prng_numbers_from_generators_tab(self):
        if self.generators_tab_instance:
            return self.generators_tab_instance.generated_numbers
        return []


