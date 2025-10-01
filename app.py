# app.py

import tkinter as tk
from tkinter import ttk, messagebox
import system_design
import visualization

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Discrete System Simulator (Lab 1)")
        self.geometry("350x380")

        # --- Parameter Frame ---
        param_frame = ttk.LabelFrame(self, text="System and Signal Parameters")
        param_frame.pack(padx=10, pady=10, fill="x")
        
        # Default stable values
        self.params = {
            'a': tk.StringVar(value="1.0"),
            'b': tk.StringVar(value="0.01"),
            'c': tk.StringVar(value="1.5"),
            'd': tk.StringVar(value="-0.1"),
            'k': tk.StringVar(value="0.05"),
            'n_points': tk.StringVar(value="150")
        }
        
        # Create input fields
        self.create_entry(param_frame, "a (input gain):", self.params['a'], 0)
        self.create_entry(param_frame, "b (input exponent):", self.params['b'], 1)
        self.create_entry(param_frame, "c (output gain):", self.params['c'], 2)
        self.create_entry(param_frame, "d (output exponent):", self.params['d'], 3)
        self.create_entry(param_frame, "k (cosh factor):", self.params['k'], 4)
        self.create_entry(param_frame, "N (points):", self.params['n_points'], 5)

        # --- Stability Info ---
        stability_label = ttk.Label(
            self, 
            text="Stability Condition: d + |k| < 0", 
            font=("Helvetica", 10, "italic")
        )
        stability_label.pack(pady=(5, 10))
        
        # --- Run Button ---
        run_button = ttk.Button(self, text="Run Simulation", command=self.run_simulation)
        run_button.pack(pady=10, ipadx=10, ipady=5)

    def create_entry(self, parent, text, var, row):
        label = ttk.Label(parent, text=text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry = ttk.Entry(parent, textvariable=var, width=15)
        entry.grid(row=row, column=1, padx=5, pady=5)

    def run_simulation(self):
        try:
            # Convert string variables to floats/ints
            float_params = {key: float(val.get()) for key, val in self.params.items() if key != 'n_points'}
            n_points = int(self.params['n_points'].get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for all parameters.")
            return

        # 1. Check for system stability
        if not system_design.check_stability(float_params):
            messagebox.showwarning(
                "Stability Warning",
                f"The system is UNSTABLE with the current parameters (d={float_params['d']}, k={float_params['k']}).\n"
                "Please ensure that d + |k| < 0."
            )
            return

        # 2. Generate the signals
        n, x_n, y_theoretical = system_design.generate_signals(float_params, n_points)
        
        # 3. Process the input through the system
        y_processed = system_design.process_system(x_n, float_params)
        
        # 4. Plot the results
        visualization.plot_signals(n, x_n, y_theoretical, y_processed)

if __name__ == "__main__":
    app = App()
    app.mainloop()