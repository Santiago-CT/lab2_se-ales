# system_design.py

import numpy as np

def check_stability(params: dict) -> bool:
    """
    Verifica si el sistema es estable según la condición derivada.
    Un sistema discreto es estable si sus polos tienen una magnitud menor a 1.
    Para este sistema, la condición de estabilidad es d + |k| < 0.
    """
    d = params.get('d', 0)
    k = params.get('k', 0)
    return d + abs(k) < 0

def generate_signals(params: dict, n_points: int) -> tuple:
    """
    Genera el vector de tiempo, la señal de entrada x(n) y la señal
    de salida teórica y(n) para comparación.
    """
    # Parámetros para las señales
    a = params.get('a', 1.0)
    b = params.get('b', 0.01)
    c = params.get('c', 1.0)
    d = params.get('d', -0.1)
    k = params.get('k', 0.05)

    # Vector de tiempo (tiempo discreto n)
    n = np.arange(n_points)

    # Señal de entrada: x(n) = a * e^(b*n) * u(n)
    x_n = a * np.exp(b * n)

    # Señal de salida teórica: y(n) = c * e^(d*n) * cosh(k*n) * u(n)
    y_theoretical_n = c * np.exp(d * n) * np.cosh(k * n)
    
    return n, x_n, y_theoretical_n

def process_system(x_n: np.ndarray, params: dict) -> np.ndarray:
    """
    Procesa la señal de entrada x(n) a través del sistema discreto para
    obtener la salida real y(n) usando la ecuación en diferencias recursiva.
    """
    # Parámetros del sistema
    a = params.get('a', 1.0)
    b = params.get('b', 0.01)
    c = params.get('c', 1.0)
    d = params.get('d', -0.1)
    k_param = params.get('k', 0.05)
    
    # Pre-cálculo de constantes para la ecuación en diferencias
    K = c / a
    exp_b = np.exp(b)
    exp_d = np.exp(d)
    exp_2d = np.exp(2 * d)
    cosh_k = np.cosh(k_param)

    # Coeficientes de la ecuación en diferencias:
    # y(n) = C1*y(n-1) - C2*y(n-2) + K*[x(n) - C3*x(n-1) + C4*x(n-2)]
    C1 = 2 * exp_d * cosh_k
    C2 = exp_2d
    C3 = exp_b + exp_d * cosh_k
    C4 = np.exp(b + d) * cosh_k

    # Inicializar el vector de salida con ceros
    y_n = np.zeros_like(x_n)
    
    # Manejar condiciones iniciales (n=0, n=1) ya que el sistema depende de valores pasados
    # Para n=0, todos los valores pasados (en n=-1, -2) son cero
    if len(y_n) > 0:
        y_n[0] = K * x_n[0]
    
    # Para n=1, los valores en n=-1 son cero
    if len(y_n) > 1:
        y_n[1] = C1 * y_n[0] + K * (x_n[1] - C3 * x_n[0])

    # Aplicar la fórmula recursiva para el resto de los puntos
    for n in range(2, len(x_n)):
        term_y = C1 * y_n[n-1] - C2 * y_n[n-2]
        term_x = K * (x_n[n] - C3 * x_n[n-1] + C4 * x_n[n-2])
        y_n[n] = term_y + term_x
        
    return y_n