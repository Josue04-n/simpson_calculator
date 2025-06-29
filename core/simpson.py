from builtins import ValueError
import numpy as np

def simpson_13(f, a, b, n):

    if n % 2 != 0:
        raise ValueError("El número de subintervalos (n) debe ser par.")

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)

    suma = y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])
    resultado = (h / 3) * suma

    return resultado
