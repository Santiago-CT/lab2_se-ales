# app.py

import tkinter as tk
from tkinter import ttk, messagebox
import system_design
import visualization

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Sistema Discreto (Lab 1)")
        self.geometry("380x380")

        # --- Frame de Parámetros ---
        param_frame = ttk.LabelFrame(self, text="Parámetros del Sistema y la Señal")
        param_frame.pack(padx=10, pady=10, fill="x")
        
        # Valores estables por defecto
        self.params = {
            'a': tk.StringVar(value="1.0"),
            'b': tk.StringVar(value="0.01"),
            'c': tk.StringVar(value="1.5"),
            'd': tk.StringVar(value="-0.1"),
            'k': tk.StringVar(value="0.05"),
            'n_points': tk.StringVar(value="150")
        }
        
        # Crear campos de entrada
        self.create_entry(param_frame, "a (ganancia entrada):", self.params['a'], 0)
        self.create_entry(param_frame, "b (exponente entrada):", self.params['b'], 1)
        self.create_entry(param_frame, "c (ganancia salida):", self.params['c'], 2)
        self.create_entry(param_frame, "d (exponente salida):", self.params['d'], 3)
        self.create_entry(param_frame, "k (factor cosh):", self.params['k'], 4)
        self.create_entry(param_frame, "N (puntos):", self.params['n_points'], 5)

        # --- Información de Estabilidad ---
        stability_label = ttk.Label(
            self, 
            text="Condición de Estabilidad: d + |k| < 0", 
            font=("Helvetica", 10, "italic")
        )
        stability_label.pack(pady=(5, 10))
        
        # --- Botón de Ejecución ---
        run_button = ttk.Button(self, text="Ejecutar Simulación", command=self.run_simulation)
        run_button.pack(pady=10, ipadx=10, ipady=5)

    def create_entry(self, parent, text, var, row):
        label = ttk.Label(parent, text=text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry = ttk.Entry(parent, textvariable=var, width=15)
        entry.grid(row=row, column=1, padx=5, pady=5)

    def run_simulation(self):
        try:
            # Convertir variables string a float/int
            float_params = {key: float(val.get()) for key, val in self.params.items() if key != 'n_points'}
            n_points = int(self.params['n_points'].get())
        except ValueError:
            messagebox.showerror("Entrada Inválida", "Por favor, ingrese números válidos para todos los parámetros.")
            return

        # 1. Verificar la estabilidad del sistema
        if not system_design.check_stability(float_params):
            messagebox.showwarning(
                "Advertencia de Estabilidad",
                f"El sistema es INESTABLE con los parámetros actuales (d={float_params['d']}, k={float_params['k']}).\n"
                "Por favor, asegúrese de que d + |k| < 0."
            )
            return

        # 2. Generar las señales
        n, x_n, y_theoretical = system_design.generate_signals(float_params, n_points)
        
        # 3. Procesar la entrada a través del sistema
        y_processed = system_design.process_system(x_n, float_params)
        
        # 4. Graficar los resultados
        visualization.plot_signals(n, x_n, y_theoretical, y_processed)

if __name__ == "__main__":
    app = App()
    app.mainloop()