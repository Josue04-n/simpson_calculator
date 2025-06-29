import numpy as np
from scipy.integrate import simpson
from scipy.misc import derivative

# --- ÁREA ENTRE CURVAS ---
def area_entre_curvas(f, g, a, b, n):
    x = np.linspace(a, b, n)
    y = np.abs(f(x) - g(x))
    return simpson(y, x)


# --- LONGITUD DE ARCO ---
def longitud_de_arco(f, a, b, n):
    x = np.linspace(a, b, n)
    dy_dx = np.array([derivative(f, xi, dx=1e-6) for xi in x])
    integrando = np.sqrt(1 + dy_dx**2)
    return simpson(integrando, x)


# --- SUPERFICIE DE REVOLUCIÓN ---
def superficie_de_revolucion(f, a, b, eje='x', n=1000):
    x = np.linspace(a, b, n)
    y = f(x)
    dy_dx = np.array([derivative(f, xi, dx=1e-6) for xi in x])
    integrando = 2 * np.pi * np.abs(y) * np.sqrt(1 + dy_dx**2)
    return simpson(integrando, x)
