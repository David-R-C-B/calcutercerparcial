import customtkinter as ctk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

from distributions.continuous_discrete import (
    uniforme, exponencial, erlang, gamma, normal, weibull,
    uniforme_discreta, bernoulli, binomial, poisson
)

class DistributionsTab:
    def __init__(self, parent_frame, get_prng_callback=None):
        self.parent_frame = parent_frame
        self.generated_numbers = []
        self.get_prng_callback = get_prng_callback 
        self._crear_ui()

    def _crear_ui(self):
        control_frame = ctk.CTkFrame(self.parent_frame)
        control_frame.pack(padx=10, pady=10, fill="x")
        control_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(control_frame, text="Configuración de Distribución", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # Distribution Selection
        ctk.CTkLabel(control_frame, text="Distribución:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.distribution_var = ctk.StringVar(value="Uniforme Continua")
        self.distribution_combobox = ctk.CTkComboBox(control_frame, variable=self.distribution_var,
                                                  values=["Uniforme Continua", "Exponencial", "Erlang", "Gamma", "Normal", "Weibull",
                                                            "Uniforme Discreta", "Bernoulli", "Binomial", "Poisson"],
                                                  command=self._on_distribution_selected)
        self.distribution_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # PRNG Selection
        ctk.CTkLabel(control_frame, text="Fuente PRNG:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.prng_source_choice = ctk.StringVar(value="Interno (numpy.random)")
        self.prng_source_combobox = ctk.CTkComboBox(control_frame, variable=self.prng_source_choice,
                                                 values=["Interno (numpy.random)", "Desde Generadores"],
                                                 state="readonly",
                                                 command=self._on_prng_source_selected)
        self.prng_source_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Parameters Frame
        self.params_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        self.params_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.param_entries = {}
        self._on_distribution_selected(None) 

        # Number of samples
        ctk.CTkLabel(control_frame, text="Cantidad de Números:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.num_samples_entry = ctk.CTkEntry(control_frame)
        self.num_samples_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.num_samples_entry.insert(0, "1000")

        # Buttons
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ctk.CTkButton(button_frame, text="Generar", command=self._generate_numbers).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Limpiar", command=self._clear_results, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Exportar", command=self._export_data).pack(side="left", padx=5)

        # Results Frame
        results_frame = ctk.CTkFrame(self.parent_frame)
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(results_frame, text="Resultados").pack(pady=5)

        # Statistics Display
        stats_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=5, pady=5)
        self.mean_label = ctk.CTkLabel(stats_frame, text="Media Empírica: ")
        self.mean_label.pack(side="left", padx=10)
        self.variance_label = ctk.CTkLabel(stats_frame, text="Varianza Empírica: ")
        self.variance_label.pack(side="left", padx=10)

        # New container frame for plot and numbers
        plot_numbers_container_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        plot_numbers_container_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Plotting Area
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100, facecolor="#2b2b2b") 
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_numbers_container_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.ax.set_title("Histograma de Números Generados", color="#e0e0e0") 
        self.ax.set_xlabel("Valor", color="#e0e0e0") 
        self.ax.set_ylabel("Frecuencia", color="#e0e0e0") 
        self.ax.set_facecolor("#2b2b2b") 
        self.ax.tick_params(axis='x', colors='#e0e0e0') 
        self.ax.tick_params(axis='y', colors='#e0e0e0') 
        self.fig.tight_layout()

        # Text widget to display generated numbers
        self.numbers_text = ctk.CTkTextbox(plot_numbers_container_frame, height=200, width=200)
        self.numbers_text.pack(side="right", fill="y", padx=5, pady=5)

    def _on_distribution_selected(self, event):
        # Clear previous parameter entries
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        dist_type = self.distribution_var.get()
        params = []

        if dist_type == "Uniforme Continua":
            params = [("a", "0"), ("b", "1")]
        elif dist_type == "Exponencial":
            params = [("lambda", "1")]
        elif dist_type == "Erlang":
            params = [("k", "1"), ("lambda", "1")]
        elif dist_type == "Gamma":
            params = [("alpha", "1"), ("beta", "1")]
        elif dist_type == "Normal":
            params = [("mu", "0"), ("sigma", "1")]
        elif dist_type == "Weibull":
            params = [("gamma", "0"), ("beta", "1"), ("alpha", "1")]
        elif dist_type == "Uniforme Discreta":
            params = [("a", "0"), ("b", "10")]
        elif dist_type == "Bernoulli":
            params = [("p", "0.5")]
        elif dist_type == "Binomial":
            params = [("n", "10"), ("p", "0.5")]
        elif dist_type == "Poisson":
            params = [("lambda", "1")]

        for i, (name, default_val) in enumerate(params):
            ctk.CTkLabel(self.params_frame, text=f"{name}:").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            entry = ctk.CTkEntry(self.params_frame)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            entry.insert(0, default_val)
            self.param_entries[name] = entry

    def _on_prng_source_selected(self, event=None):
        if self.prng_source_choice.get() == "Desde Generadores" and not self.get_prng_callback:
            messagebox.showwarning("Advertencia", "No se ha configurado una fuente de números desde la pestaña de Generadores.")
            self.prng_source_choice.set("Interno (numpy.random)")

    def _get_prng_numbers(self, count):
        if self.prng_source_choice.get() == "Desde Generadores":
            if self.get_prng_callback:
                external_numbers = self.get_prng_callback()
                if not external_numbers:
                    messagebox.showwarning("Advertencia", "No hay números generados en la pestaña de Generadores. Usando numpy.random.")
                    self.prng_source_choice.set("Interno (numpy.random)")
                    return np.random.rand(count).tolist()
                else:
                    if len(external_numbers) < count:
                        messagebox.showwarning("Advertencia", f"La pestaña de Generadores tiene {len(external_numbers)} números, se necesitan {count}. Se usarán los disponibles y se complementará con numpy.random.")
                        return external_numbers + np.random.rand(count - len(external_numbers)).tolist()
                    else:
                        return external_numbers[:count]
            else:
                messagebox.showwarning("Advertencia", "Callback de Generadores no disponible. Usando numpy.random.")
                return np.random.rand(count).tolist()
        else: 
            return np.random.rand(count).tolist()

    def _generate_numbers(self):
        try:
            num_samples = int(self.num_samples_entry.get())
            if num_samples <= 0:
                raise ValueError("Cantidad de números debe ser un entero positivo.")

            r_numbers = self._get_prng_numbers(num_samples * 2) 

            dist_type = self.distribution_var.get()
            params = {name: float(entry.get()) if name not in ["k", "n", "a", "b"] else int(entry.get()) for name, entry in self.param_entries.items()}

            if dist_type == "Uniforme Continua":
                self.generated_numbers = uniforme(params["a"], params["b"], r_numbers[:num_samples])
            elif dist_type == "Exponencial":
                self.generated_numbers = exponencial(params["lambda"], r_numbers[:num_samples])
            elif dist_type == "Erlang":
                k_val = params["k"]
                required_r = num_samples * k_val
                if len(r_numbers) < required_r:
                    r_numbers = self._get_prng_numbers(required_r)
                self.generated_numbers = erlang(k_val, params["lambda"], r_numbers[:required_r])
            elif dist_type == "Gamma":
                alpha_val = params["alpha"]
                required_r = num_samples * alpha_val
                if len(r_numbers) < required_r:
                    r_numbers = self._get_prng_numbers(required_r)
                self.generated_numbers = gamma(alpha_val, params["beta"], r_numbers[:required_r])
            elif dist_type == "Normal":
                required_r = num_samples * 2
                if len(r_numbers) < required_r:
                    r_numbers = self._get_prng_numbers(required_r)
                self.generated_numbers = normal(params["mu"], params["sigma"], r_numbers[:required_r])
                self.generated_numbers = self.generated_numbers[:num_samples] 
            elif dist_type == "Weibull":
                self.generated_numbers = weibull(params["gamma"], params["beta"], params["alpha"], r_numbers[:num_samples])
            elif dist_type == "Uniforme Discreta":
                self.generated_numbers = uniforme_discreta(params["a"], params["b"], r_numbers[:num_samples])
            elif dist_type == "Bernoulli":
                self.generated_numbers = bernoulli(params["p"], r_numbers[:num_samples])
            elif dist_type == "Binomial":
                n_val = params["n"]
                required_r = num_samples * n_val
                if len(r_numbers) < required_r:
                    r_numbers = self._get_prng_numbers(required_r)
                self.generated_numbers = binomial(n_val, params["p"], r_numbers[:required_r])
            elif dist_type == "Poisson":
                self.generated_numbers = poisson(params["lambda"], r_numbers)
                self.generated_numbers = self.generated_numbers[:num_samples] 
            else:
                messagebox.showerror("Error", "Distribución no reconocida.")
                return

            if self.generated_numbers:
                self.mean_label.configure(text=f"Media Empírica: {np.mean(self.generated_numbers):.4f}")
                self.variance_label.configure(text=f"Varianza Empírica: {np.var(self.generated_numbers):.4f}")
                self._plot_histogram(self.generated_numbers)

                self.numbers_text.configure(state="normal")
                self.numbers_text.delete("1.0", "end")
                for num in self.generated_numbers:
                    self.numbers_text.insert("end", f"{num:.4f}\n")
                self.numbers_text.configure(state="disabled")
            else:
                self._clear_results()

        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar números: {e}")

    def _plot_histogram(self, data):
        self.ax.clear()
        if data:
            self.ax.hist(data, bins=30, density=True, alpha=0.7, color='#00ff41', edgecolor='#e0e0e0') 
            self.ax.set_title(f"Histograma de {self.distribution_var.get()}", color='#e0e0e0')
            self.ax.set_xlabel("Valor", color='#e0e0e0')
            self.ax.set_ylabel("Frecuencia Normalizada", color='#e0e0e0')
        else:
            self.ax.set_title("Histograma de Números Generados", color='#e0e0e0')
            self.ax.set_xlabel("Valor", color='#e0e0e0')
            self.ax.set_ylabel("Frecuencia", color='#e0e0e0')
        self.fig.tight_layout()
        self.canvas.draw()

    def _clear_results(self):
        self.generated_numbers = []
        self.prng_numbers = []
        self.mean_label.configure(text="Media Empírica: ")
        self.variance_label.configure(text="Varianza Empírica: ")
        self.ax.clear()
        self.ax.set_title("Histograma de Números Generados")
        self.ax.set_xlabel("Valor")
        self.ax.set_ylabel("Frecuencia")
        self.fig.tight_layout()
        self.canvas.draw()

        self.numbers_text.configure(state="normal")
        self.numbers_text.delete("1.0", "end")
        self.numbers_text.configure(state="disabled")

    def _export_data(self):
        if not self.generated_numbers:
            messagebox.showinfo("Exportar Datos", "No hay datos para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")])

        if file_path:
            try:
                df = pd.DataFrame({"Numeros Generados": self.generated_numbers})
                if file_path.endswith(".csv"):
                    df.to_csv(file_path, index=False)
                elif file_path.endswith(".xlsx"):
                    df.to_excel(file_path, index=False)
                messagebox.showinfo("Exportar Datos", f"Datos exportados exitosamente a {file_path}")
            except Exception as e:
                messagebox.showerror("Error de Exportación", f"Ocurrió un error al exportar los datos: {e}")
