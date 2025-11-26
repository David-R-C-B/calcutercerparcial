import customtkinter as ctk
from tkinter import messagebox, ttk
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
        self.generated_steps = [] 
        self.histogram_window = None # Reference to the histogram window
        self._crear_ui()

    def _crear_ui(self):
        # Frame principal para controles
        control_frame = ctk.CTkFrame(self.parent_frame)
        control_frame.pack(padx=10, pady=10, fill="x")
        control_frame.grid_columnconfigure(1, weight=1)

        # Selección de Generador
        ctk.CTkLabel(control_frame, text="Seleccionar Generador:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.generator_var = ctk.StringVar(value="Cuadrados Medios")
        self.generator_combobox = ctk.CTkComboBox(control_frame, variable=self.generator_var,
                                                  values=["Cuadrados Medios", "Productos Medios", "Multiplicador Constante"],
                                                  command=self._actualizar_parametros_ui)
        self.generator_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Frame para parámetros dinámicos
        self.params_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        self.params_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.params_frame.grid_columnconfigure(1, weight=1)

        self._actualizar_parametros_ui() 

        # Cantidad de números a generar
        ctk.CTkLabel(control_frame, text="Cantidad de Números:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.cantidad_entry = ctk.CTkEntry(control_frame)
        self.cantidad_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.cantidad_entry.insert(0, "1000")

        # Checkbutton para mostrar procedimiento
        self.mostrar_procedimiento_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(control_frame, text="Mostrar procedimiento",
                        variable=self.mostrar_procedimiento_var).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Botones de acción
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ctk.CTkButton(button_frame, text="Generar", command=self._generar_numeros).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Ver Histograma", command=self._abrir_histograma).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Limpiar", command=self._limpiar_resultados, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Exportar a CSV", command=self._exportar_resultados).pack(side="left", padx=10)

        # Frame para resultados y gráfica
        results_plot_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        results_plot_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Frame para la lista de números (Izquierda)
        numbers_frame = ctk.CTkFrame(results_plot_frame)
        numbers_frame.pack(side="left", fill="y", padx=5, pady=5) 
        
        ctk.CTkLabel(numbers_frame, text="Números Generados").pack(pady=5)
        
        self.numbers_text = ctk.CTkTextbox(numbers_frame, width=200) 
        self.numbers_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.numbers_text.configure(state="disabled")

        # Frame derecho (Contenedor para Tabla)
        self.right_frame = ctk.CTkFrame(results_plot_frame, fg_color="transparent")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Contenedor para la tabla de procedimiento (Arriba)
        self.procedure_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        # Initially hidden

        # Configurar estilo del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white", 
                        fieldbackground="#2b2b2b", 
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", 
                        background="#343638", 
                        foreground="white", 
                        relief="flat")
        style.map("Treeview.Heading", 
                  background=[('active', '#343638')])

        self.tree = ttk.Treeview(self.procedure_container, show="headings", style="Treeview")
        self.scrollbar = ttk.Scrollbar(self.procedure_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def _actualizar_parametros_ui(self, event=None):
        # Limpiar parámetros anteriores
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        selected_generator = self.generator_var.get()

        if selected_generator == "Cuadrados Medios":
            ctk.CTkLabel(self.params_frame, text="Semilla (X0, par de dígitos):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.semilla_entry = ctk.CTkEntry(self.params_frame)
            self.semilla_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.semilla_entry.insert(0, "5731") 
            self.constante_entry = None 
            self.semilla2_entry = None 
        elif selected_generator == "Productos Medios":
            ctk.CTkLabel(self.params_frame, text="Semilla 1 (X0):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.semilla_entry = ctk.CTkEntry(self.params_frame)
            self.semilla_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.semilla_entry.insert(0, "5015") 

            ctk.CTkLabel(self.params_frame, text="Semilla 2 (X1):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.semilla2_entry = ctk.CTkEntry(self.params_frame)
            self.semilla2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            self.semilla2_entry.insert(0, "5734") 
            self.constante_entry = None 
        elif selected_generator == "Multiplicador Constante":
            ctk.CTkLabel(self.params_frame, text="Semilla (X0):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.semilla_entry = ctk.CTkEntry(self.params_frame)
            self.semilla_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.semilla_entry.insert(0, "12345")

            ctk.CTkLabel(self.params_frame, text="Constante (a):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.constante_entry = ctk.CTkEntry(self.params_frame)
            self.constante_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            self.constante_entry.insert(0, "7143")
            self.semilla2_entry = None 

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
                self.generated_steps = [] 

            self._mostrar_resultados()

        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def _mostrar_resultados(self):
        # Mostrar números en el Text widget
        self.numbers_text.configure(state="normal")
        self.numbers_text.delete(1.0, "end")

        for num in self.generated_numbers:
            self.numbers_text.insert("end", f"{num:.6f}\n")
        
        self.numbers_text.configure(state="disabled")

        # Configurar Tabla de Procedimiento
        self.procedure_container.pack_forget()

        if self.mostrar_procedimiento_var.get() and self.generated_steps:
            # Mostrar tabla arriba
            self.procedure_container.pack(side="top", fill="both", expand=True, pady=5)
            self.tree.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")
            
            # Limpiar tabla anterior
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Definir columnas según generador
            headers = []
            keys = []
            if self.generator_var.get() == "Cuadrados Medios":
                headers = ["i", "Xi", "Yi (Cuadrado)", "Extracción", "Xi+1", "ri"]
                keys = ["i", "Xi", "Yi", "mid", "X_next", "ri"]
            elif self.generator_var.get() == "Productos Medios":
                headers = ["i", "Xi-1", "Xi", "Yi (Producto)", "Extracción", "Xi+1", "ri"]
                keys = ["i", "Xi_prev", "Xi_curr", "Yi", "mid", "X_next", "ri"] 
            elif self.generator_var.get() == "Multiplicador Constante":
                headers = ["i", "Xi", "Yi (Producto)", "Extracción", "Xi+1", "ri"]
                keys = ["i", "Xi", "Yi", "mid", "X_next", "ri"]

            # Configurar columnas
            self.tree["columns"] = headers
            for header in headers:
                self.tree.heading(header, text=header)
                self.tree.column(header, anchor="center", width=100) # Ajustar ancho según necesidad

            # Llenar datos
            for step in self.generated_steps:
                vals = []
                if self.generator_var.get() == "Productos Medios":
                    vals = [step['i'], step['Xi'][0], step['Xi'][1], step['Yi'], step['mid'], step['X_next'], f"{step['ri']:.4f}"]
                else:
                    vals = [step[k] if k != 'ri' else f"{step[k]:.4f}" for k in keys]
                
                self.tree.insert("", "end", values=vals)

    def _abrir_histograma(self):
        if not self.generated_numbers:
            messagebox.showwarning("Advertencia", "No hay números generados para graficar.")
            return

        if self.histogram_window is None or not self.histogram_window.winfo_exists():
            self.histogram_window = ctk.CTkToplevel(self.parent_frame)
            self.histogram_window.title(f"Histograma - {self.generator_var.get()}")
            self.histogram_window.geometry("600x400")
            self.histogram_window.attributes("-topmost", True)
        else:
            self.histogram_window.focus()
            # Clear previous content if reusing window
            for widget in self.histogram_window.winfo_children():
                widget.destroy()

        plot_histograma(self.generated_numbers, f"Histograma de {self.generator_var.get()}", self.histogram_window)

    def _limpiar_resultados(self):
        self.generated_numbers = []
        self.generated_steps = []
        self.numbers_text.configure(state="normal")
        self.numbers_text.delete(1.0, "end")
        self.numbers_text.configure(state="disabled")
        
        self.procedure_container.pack_forget()
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.histogram_window and self.histogram_window.winfo_exists():
            self.histogram_window.destroy()
            self.histogram_window = None

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
