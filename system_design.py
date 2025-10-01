# system_design.py

import numpy as np

def check_stability(params: dict) -> bool:
    """
    Checks if the system is stable based on the derived condition.
    A discrete system is stable if its poles have a magnitude less than 1. 
    For this system, the stability condition is d + |k| < 0.
    """
    d = params.get('d', 0)
    k = params.get('k', 0)
    return d + abs(k) < 0

def generate_signals(params: dict, n_points: int) -> tuple:
    """
    Generates the time vector, the input signal x(n), and the theoretical
    output signal y(n) for comparison.
    """
    # Parameters for the signals
    a = params.get('a', 1.0)
    b = params.get('b', 0.01)
    c = params.get('c', 1.0)
    d = params.get('d', -0.1)
    k = params.get('k', 0.05)

    # Time vector (discrete time n)
    n = np.arange(n_points)

    # Input signal: x(n) = a * e^(b*n) * u(n)
    x_n = a * np.exp(b * n)

    # Theoretical output signal: y(n) = c * e^(d*n) * cosh(k*n) * u(n)
    y_theoretical_n = c * np.exp(d * n) * np.cosh(k * n)
    
    return n, x_n, y_theoretical_n

def process_system(x_n: np.ndarray, params: dict) -> np.ndarray:
    """
    Processes the input signal x(n) through the discrete system to get the
    actual output y(n) using the derived recursive difference equation.
    """
    # System parameters
    a = params.get('a', 1.0)
    b = params.get('b', 0.01)
    c = params.get('c', 1.0)
    d = params.get('d', -0.1)
    k_param = params.get('k', 0.05)
    
    # Pre-calculate constants for the difference equation
    K = c / a
    exp_b = np.exp(b)
    exp_d = np.exp(d)
    exp_2d = np.exp(2 * d)
    cosh_k = np.cosh(k_param)

    # Coefficients from the difference equation:
    # y(n) = C1*y(n-1) - C2*y(n-2) + K*[x(n) - C3*x(n-1) + C4*x(n-2)]
    C1 = 2 * exp_d * cosh_k
    C2 = exp_2d
    C3 = exp_b + exp_d * cosh_k
    C4 = np.exp(b + d) * cosh_k

    # Initialize the output array with zeros
    y_n = np.zeros_like(x_n)
    
    # Handle initial conditions (n=0, n=1) since the system depends on past values
    # For n=0, all past values (at n=-1, -2) are zero
    if len(y_n) > 0:
        y_n[0] = K * x_n[0]
    
    # For n=1, values at n=-1 are zero
    if len(y_n) > 1:
        y_n[1] = C1 * y_n[0] + K * (x_n[1] - C3 * x_n[0])

    # Apply the recursive formula for the rest of the points
    for n in range(2, len(x_n)):
        term_y = C1 * y_n[n-1] - C2 * y_n[n-2]
        term_x = K * (x_n[n] - C3 * x_n[n-1] + C4 * x_n[n-2])
        y_n[n] = term_y + term_x
        
    return y_n