import customtkinter as ctk
from gui.cellular_automata_subtab import CellularAutomataSubTab
from gui.game_of_life_subtab import GameOfLifeSubTab
from gui.covid_simulation_subtab import CovidSimulationSubTab

class AutomataMainTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self._crear_ui()

    def _crear_ui(self):
        self.automata_tabview = ctk.CTkTabview(self.parent_frame)
        self.automata_tabview.pack(expand=True, fill="both", padx=5, pady=5)

        self.automata_tabview.add("Autómatas 1D/2D")
        self.automata_tabview.add("Juego de la Vida")
        self.automata_tabview.add("Simulación COVID")

        # Sub-tab for general 1D/2D Cellular Automata
        self.ca_frame = self.automata_tabview.tab("Autómatas 1D/2D")
        CellularAutomataSubTab(self.ca_frame)

        # Sub-tab for Game of Life
        self.gol_frame = self.automata_tabview.tab("Juego de la Vida")
        GameOfLifeSubTab(self.gol_frame)
        
        # Sub-tab for COVID Simulation
        self.covid_frame = self.automata_tabview.tab("Simulación COVID")
        CovidSimulationSubTab(self.covid_frame)
