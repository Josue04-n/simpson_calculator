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

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y1, label=texto_funcion1, color='green', linewidth=2)

    if f2:
        y2 = f2(x)
        ax.plot(x, y2, label=texto_funcion2, color='blue', linestyle='--', linewidth=2)
        ax.fill_between(x, y1, y2, color='orange', alpha=0.4, label='Área entre funciones')
    else:
        ax.fill_between(x, y1, color='orange', alpha=0.4, label='Área bajo la curva')

    ax.axvline(a, color='red', linestyle='--', label=f"x = {a}")
    ax.axvline(b, color='purple', linestyle='--', label=f"x = {b}")

    if area_valor is not None:
        ax.text((a + b) / 2, max(y1) * 0.7, f"Área ≈ {area_valor:.4f}", fontsize=12,
                bbox=dict(facecolor='white', edgecolor='black'))

    if latex_funcion:
        ax.text(a, max(y1) * 1.05, f"${latex_funcion}$", fontsize=16, color='darkgreen')

    ax.set_title("Visualización de Área")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()

    if guardar_como:
        fig.savefig(guardar_como, dpi=300)
        print(f"✅ Imagen guardada como: {guardar_como}")

    return fig
