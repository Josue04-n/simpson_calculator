"""
Autor: [Josue Llumitasig]
Fecha: 2025-06-11
Descripción: Implementación del método de Simpson 1/3 para aproximar integrales definidas.
Este módulo permite calcular el área bajo una curva o entre dos funciones dadas en un intervalo [a, b].
"""

import numpy as np

def simpson_13(f, a, b, n):
    """
    Calcula la integral definida de f(x) en el intervalo [a, b] usando el método de Simpson 1/3.
    
    Parámetros:
    - f: función a integrar (debe aceptar y operar con arreglos de NumPy)
    - a: límite inferior de integración
    - b: límite superior de integración
    - n: número de subintervalos (debe ser par)

    Retorna:
    - Aprox. del valor de la integral
    """
    if n % 2 != 0:
        raise ValueError("El número de subintervalos (n) debe ser par.")

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)

    suma = y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])
    resultado = (h / 3) * suma

    return resultado
