import matplotlib.pyplot as plt
import numpy as np

def plot_signals(n: np.ndarray, x_n: np.ndarray, y_theoretical: np.ndarray, y_processed: np.ndarray):
    """
    Creates and displays two plots: one for the input signal and one for
    comparing the theoretical and processed output signals.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=4.0)

    # Plot 1: Input Signal
    ax1.plot(n, x_n, color='dodgerblue', label='x(n)')
    ax1.set_title("Input Signal: $x(n) = a e^{bn} \mu(n)$", fontsize=14)
    ax1.set_xlabel("Sample (n)", fontsize=12)
    ax1.set_ylabel("Amplitude", fontsize=12)
    ax1.legend()
    ax1.grid(True)

    # Plot 2: Output Signals
    ax2.plot(n, y_theoretical, 'r--', label='Theoretical Output y(n)', linewidth=2.5)
    ax2.plot(n, y_processed, 'g-', label='System Output y(n) (Processed)', linewidth=1.5)
    ax2.set_title("Output Signal: $y(n) = c e^{dn} \cosh(kn) \mu(n)$", fontsize=14)
    ax2.set_xlabel("Sample (n)", fontsize=12)
    ax2.set_ylabel("Amplitude", fontsize=12)
    ax2.legend()
    ax2.grid(True)
    
    plt.show()