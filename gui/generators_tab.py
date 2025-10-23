import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from rng_algorithms.cuadrados_medios import generar_cuadrados_medios
from rng_algorithms.productos_medios import generar_productos_medios
from rng_algorithms.multiplicador_constante import generar_multiplicador_constante
from utils.plotting import plot_histograma
from utils.data_exporter import exportar_a_csv

class GeneratorsTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.generated_numbers = []
        self.generated_steps = [] # Para almacenar los pasos
        self._crear_ui()

    def _crear_ui(self):
        # Frame principal para controles
        control_frame = ttk.LabelFrame(self.parent_frame, text="Configuración del Generador")
        control_frame.pack(padx=10, pady=10, fill="x")
        control_frame.columnconfigure(1, weight=1)

        # Selección de Generador
        ttk.Label(control_frame, text="Seleccionar Generador:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.generator_var = tk.StringVar()
        self.generator_combobox = ttk.Combobox(control_frame, textvariable=self.generator_var,
                                               values=["Cuadrados Medios", "Productos Medios", "Multiplicador Constante"],
                                               state="readonly")
        self.generator_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.generator_combobox.set("Cuadrados Medios") # Valor por defecto
        self.generator_combobox.bind("<<ComboboxSelected>>", self._actualizar_parametros_ui)

        # Frame para parámetros dinámicos
        self.params_frame = ttk.Frame(control_frame)
        self.params_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.params_frame.columnconfigure(1, weight=1)

        self._actualizar_parametros_ui() # Cargar UI de parámetros inicial

        # Cantidad de números a generar
        ttk.Label(control_frame, text="Cantidad de Números:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.cantidad_entry = ttk.Entry(control_frame)
        self.cantidad_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.cantidad_entry.insert(0, "1000")

        # Checkbutton para mostrar procedimiento
        self.mostrar_procedimiento_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Mostrar procedimiento",
                        variable=self.mostrar_procedimiento_var).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Botones de acción
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Generar", command=self._generar_numeros).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self._limpiar_resultados).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exportar a CSV", command=self._exportar_resultados).pack(side="left", padx=5)

        # Frame para resultados y gráfica
        results_plot_frame = ttk.Frame(self.parent_frame)
        results_plot_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Frame para la lista de números
        numbers_frame = ttk.LabelFrame(results_plot_frame, text="Números Generados")
        numbers_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.numbers_text = tk.Text(numbers_frame, height=15, state="disabled",
                                    bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff",
                                    selectbackground="#4a90e2", selectforeground="#ffffff")
        self.numbers_text.pack(side="left", fill="both", expand=True)
        numbers_scrollbar = ttk.Scrollbar(numbers_frame, command=self.numbers_text.yview)
        numbers_scrollbar.pack(side="right", fill="y")
        self.numbers_text.config(yscrollcommand=numbers_scrollbar.set)

        # Frame para la gráfica
        self.plot_frame = ttk.LabelFrame(results_plot_frame, text="Histograma")
        self.plot_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def _actualizar_parametros_ui(self, event=None):
        # Limpiar parámetros anteriores
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        selected_generator = self.generator_var.get()

        if selected_generator == "Cuadrados Medios":
            ttk.Label(self.params_frame, text="Semilla (X0, par de dígitos):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.semilla_entry = ttk.Entry(self.params_frame)
            self.semilla_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.semilla_entry.insert(0, "5731") # Ejemplo para Cuadrados Medios
            self.constante_entry = None # No usado
            self.semilla2_entry = None # No usado
        elif selected_generator == "Productos Medios":
            ttk.Label(self.params_frame, text="Semilla 1 (X0):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.semilla_entry = ttk.Entry(self.params_frame)
            self.semilla_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.semilla_entry.insert(0, "5015") # Ejemplo para Productos Medios

            ttk.Label(self.params_frame, text="Semilla 2 (X1):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.semilla2_entry = ttk.Entry(self.params_frame)
            self.semilla2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            self.semilla2_entry.insert(0, "5734") # Ejemplo para Productos Medios
            self.constante_entry = None # No usado
        elif selected_generator == "Multiplicador Constante":
            ttk.Label(self.params_frame, text="Semilla (X0):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.semilla_entry = ttk.Entry(self.params_frame)
            self.semilla_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.semilla_entry.insert(0, "12345")

            ttk.Label(self.params_frame, text="Constante (a):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.constante_entry = ttk.Entry(self.params_frame)
            self.constante_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            self.constante_entry.insert(0, "7143")
            self.semilla2_entry = None # No usado

    def _generar_numeros(self):
        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser un número positivo.")

            selected_generator = self.generator_var.get()
            mostrar_pasos = self.mostrar_procedimiento_var.get()

            self.generated_numbers = []
            self.generated_steps = []

            if selected_generator == "Cuadrados Medios":
                semilla = int(self.semilla_entry.get())
                result = generar_cuadrados_medios(semilla, cantidad, devolver_pasos=mostrar_pasos)
            elif selected_generator == "Productos Medios":
                semilla1 = int(self.semilla_entry.get())
                semilla2 = int(self.semilla2_entry.get())
                result = generar_productos_medios(semilla1, semilla2, cantidad, devolver_pasos=mostrar_pasos)
            elif selected_generator == "Multiplicador Constante":
                semilla = int(self.semilla_entry.get())
                constante = int(self.constante_entry.get())
                result = generar_multiplicador_constante(semilla, constante, cantidad, devolver_pasos=mostrar_pasos)

            if mostrar_pasos:
                self.generated_numbers, self.generated_steps = result
            else:
                self.generated_numbers = result
                self.generated_steps = [] # Asegurarse de que esté vacío si no se piden pasos

            self._mostrar_resultados()

        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def _mostrar_resultados(self):
        # Mostrar números en el Text widget
        self.numbers_text.config(state="normal")
        self.numbers_text.delete(1.0, tk.END)

        for num in self.generated_numbers:
            self.numbers_text.insert(tk.END, f"{num:.6f}\n")
        
        if self.generated_steps:
            self.numbers_text.insert(tk.END, "\n-- Procedimiento --\n")
            if self.generator_var.get() == "Cuadrados Medios":
                self.numbers_text.insert(tk.END, "i   | Xi     | Yi         | mid  | X_next | r\n")
                self.numbers_text.insert(tk.END, "----|--------|------------|------|--------|-----\n")
                for step in self.generated_steps:
                    self.numbers_text.insert(tk.END, f"{step['i']:<3} | {step['Xi']:<6} | {step['Yi']:<10} | {step['mid']:<4} | {step['X_next']:<6} | {step['ri']:.4f}\n")
            elif self.generator_var.get() == "Productos Medios":
                self.numbers_text.insert(tk.END, "i   | Xi_1   | Xi     | Yi         | mid  | X_next | r\n")
                self.numbers_text.insert(tk.END, "----|--------|--------|------------|------|--------|-----\n")
                for step in self.generated_steps:
                    self.numbers_text.insert(tk.END, f"{step['i']:<3} | {step['Xi'][0]:<6} | {step['Xi'][1]:<6} | {step['Yi']:<10} | {step['mid']:<4} | {step['X_next']:<6} | {step['ri']:.4f}\n")
            elif self.generator_var.get() == "Multiplicador Constante":
                self.numbers_text.insert(tk.END, "i   | Xi     | Yi         | mid  | X_next | r\n")
                self.numbers_text.insert(tk.END, "----|--------|------------|------|--------|-----\n")
                for step in self.generated_steps:
                    self.numbers_text.insert(tk.END, f"{step['i']:<3} | {step['Xi']:<6} | {step['Yi']:<10} | {step['mid']:<4} | {step['X_next']:<6} | {step['ri']:.4f}\n")

        self.numbers_text.config(state="disabled")

        # Mostrar histograma
        if self.generated_numbers:
            plot_histograma(self.generated_numbers, f"Histograma de {self.generator_var.get()}", self.plot_frame)
        else:
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            ttk.Label(self.plot_frame, text="No hay datos para graficar.").pack(pady=20)

    def _limpiar_resultados(self):
        self.generated_numbers = []
        self.generated_steps = []
        self.numbers_text.config(state="normal")
        self.numbers_text.delete(1.0, tk.END)
        self.numbers_text.config(state="disabled")
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.plot_frame, text="Histograma").pack(pady=20)

    def _exportar_resultados(self):
        if not self.generated_numbers:
            messagebox.showwarning("Advertencia", "No hay números generados para exportar.")
            return

        try:
            generator_name = self.generator_var.get().replace(" ", "_").lower()
            file_name = f"numeros_{generator_name}"
            ruta_guardada = exportar_a_csv(self.generated_numbers, file_name)
            messagebox.showinfo("Exportación Exitosa", f"Números exportados a {ruta_guardada}")
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudieron exportar los datos: {e}")
