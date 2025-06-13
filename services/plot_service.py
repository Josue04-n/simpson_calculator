'''PROTOTIPO 3'''
"""
Autor: [Josue Llumitasig]
Fecha: 2025-06-11
Descripción: Servicio para graficar el área bajo una curva o entre dos curvas usando matplotlib.
Incluye visualización de límites, valor del área, fórmula en LaTeX y opción para guardar como imagen.
"""

import numpy as np
import matplotlib.pyplot as plt

def graficar_area(
    f1,
    a,
    b,
    area_valor=None,
    texto_funcion1="f(x)",
    f2=None,
    texto_funcion2="",
    guardar_como=None,
    latex_funcion=None,  
    puntos=1000
):
    x = np.linspace(a, b, puntos)
    y1 = f1(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, label=texto_funcion1, color='green', linewidth=2)

    if f2:
        y2 = f2(x)
        plt.plot(x, y2, label=texto_funcion2, color='blue', linestyle='--', linewidth=2)
        plt.fill_between(x, y1, y2, color='orange', alpha=0.4, label='Área entre funciones')
    else:
        plt.fill_between(x, y1, color='orange', alpha=0.4, label='Área bajo la curva')

    # Líneas verticales para los límites de integración
    plt.axvline(a, color='red', linestyle='--', label=f"x = {a}")
    plt.axvline(b, color='purple', linestyle='--', label=f"x = {b}")

    # Mostrar el valor del área
    if area_valor is not None:
        plt.text((a + b) / 2, max(y1) * 0.7, f"Área ≈ {area_valor:.4f}", fontsize=12,
                 bbox=dict(facecolor='white', edgecolor='black'))

    # Mostrar fórmula en LaTeX si está disponible
    if latex_funcion:
        plt.text(a, max(y1) * 1.05, f"${latex_funcion}$", fontsize=16, color='darkgreen')

    plt.title("Visualización de Área")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()

    if guardar_como:
        plt.savefig(guardar_como, dpi=300)
        print(f"✅ Imagen guardada como: {guardar_como}")

    plt.show()
