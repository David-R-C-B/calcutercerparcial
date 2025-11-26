import customtkinter as ctk
from tkinter import messagebox
import numpy as np

from statistical_tests.prueba_medias import realizar_prueba_medias
from statistical_tests.prueba_varianza import realizar_prueba_varianza
from utils.data_exporter import exportar_a_csv

class TestsTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.numbers_to_test = []
        self._crear_ui()

    def _crear_ui(self):
        # Frame principal para controles
        control_frame = ctk.CTkFrame(self.parent_frame)
        control_frame.pack(padx=10, pady=10, fill="x")

        # Selección de Prueba
        ctk.CTkLabel(control_frame, text="Seleccionar Prueba:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.test_var = ctk.StringVar(value="Prueba de Medias")
        self.test_combobox = ctk.CTkComboBox(control_frame, variable=self.test_var,
                                          values=["Prueba de Medias", "Prueba de Varianza"],
                                          state="readonly")
        self.test_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Nivel de Significancia
        ctk.CTkLabel(control_frame, text="Nivel de Significancia (alpha):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.alpha_entry = ctk.CTkEntry(control_frame)
        self.alpha_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.alpha_entry.insert(0, "0.05")

        # Botones de acción
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ctk.CTkButton(button_frame, text="Realizar Prueba", command=self._realizar_prueba).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Limpiar", command=self._limpiar_resultados, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Exportar Resultados", command=self._exportar_resultados).pack(side="left", padx=10)

        # Frame para entrada de números y resultados
        data_results_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        data_results_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Frame para entrada de números
        numbers_input_frame = ctk.CTkFrame(data_results_frame)
        numbers_input_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(numbers_input_frame, text="Números a Probar (uno por línea)").pack(pady=5)
        
        self.numbers_text_input = ctk.CTkTextbox(numbers_input_frame, height=300, width=200)
        self.numbers_text_input.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame para resultados de la prueba
        results_frame = ctk.CTkFrame(data_results_frame)
        results_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(results_frame, text="Resultados de la Prueba").pack(pady=5)
        
        self.results_text = ctk.CTkTextbox(results_frame, height=300, width=300)
        self.results_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.results_text.configure(state="disabled")

    def _realizar_prueba(self):
        try:
            alpha = float(self.alpha_entry.get())
            if not (0 < alpha < 1):
                raise ValueError("El nivel de significancia (alpha) debe ser un valor entre 0 y 1.")

            numbers_str = self.numbers_text_input.get("1.0", "end").strip()
            if not numbers_str:
                raise ValueError("Por favor, introduce números para realizar la prueba.")
            
            # Convertir los números de string a float
            self.numbers_to_test = [float(num.strip()) for num in numbers_str.split('\n') if num.strip()]
            if not self.numbers_to_test:
                raise ValueError("No se pudieron parsear números válidos. Asegúrate de que cada número esté en una línea separada.")

            selected_test = self.test_var.get()
            results = {}

            if selected_test == "Prueba de Medias":
                results = realizar_prueba_medias(self.numbers_to_test, alpha)
            elif selected_test == "Prueba de Varianza":
                results = realizar_prueba_varianza(self.numbers_to_test, alpha)
            
            self._mostrar_resultados(results)

        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def _mostrar_resultados(self, results: dict):
        self.results_text.configure(state="normal")
        self.results_text.delete(1.0, "end")

        if "error" in results:
            self.results_text.insert("end", f"Error: {results['error']}\n")
        else:
            for key, value in results.items():
                if isinstance(value, float):
                    self.results_text.insert("end", f"{key.replace('_', ' ').capitalize()}: {value:.6f}\n")
                elif isinstance(value, tuple):
                     self.results_text.insert("end", f"{key.replace('_', ' ').capitalize()}: {value}\n")
                else:
                    self.results_text.insert("end", f"{key.replace('_', ' ').capitalize()}: {value}\n")
        self.results_text.configure(state="disabled")

    def _limpiar_resultados(self):
        self.numbers_text_input.delete("1.0", "end")
        self.results_text.configure(state="normal")
        self.results_text.delete(1.0, "end")
        self.results_text.configure(state="disabled")
        self.numbers_to_test = []

    def _exportar_resultados(self):
        if not self.numbers_to_test:
            messagebox.showwarning("Advertencia", "No hay números para exportar.")
            return
        if not self.results_text.get("1.0", "end").strip():
            messagebox.showwarning("Advertencia", "No hay resultados de prueba para exportar.")
            return

        try:
            test_name = self.test_var.get().replace(" ", "_").lower()
            file_name = f"resultados_{{test_name}}"
            
            # Exportar los números usados en la prueba
            ruta_numeros = exportar_a_csv(self.numbers_to_test, f"{file_name}_numeros")

            # Exportar los resultados de la prueba como texto
            results_content = self.results_text.get("1.0", "end")
            results_file_path = f"{file_name}_resultados.txt"
            with open(results_file_path, "w", encoding="utf-8") as f:
                f.write(results_content)

            messagebox.showinfo("Exportación Exitosa", f"Números exportados a {ruta_numeros}\nResultados exportados a {results_file_path}")
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudieron exportar los datos: {e}")