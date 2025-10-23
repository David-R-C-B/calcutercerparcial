import tkinter as tk
from tkinter import ttk

from gui.cellular_automata_subtab import CellularAutomataSubTab
from gui.game_of_life_subtab import GameOfLifeSubTab

class AutomataMainTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self._crear_ui()

    def _crear_ui(self):
        self.automata_notebook = ttk.Notebook(self.parent_frame)
        self.automata_notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # Sub-tab for general 1D/2D Cellular Automata
        self.ca_frame = ttk.Frame(self.automata_notebook)
        self.automata_notebook.add(self.ca_frame, text="Autómatas 1D/2D")
        CellularAutomataSubTab(self.ca_frame)

        # Sub-tab for Game of Life
        self.gol_frame = ttk.Frame(self.automata_notebook)
        self.automata_notebook.add(self.gol_frame, text="Juego de la Vida")
        GameOfLifeSubTab(self.gol_frame)
