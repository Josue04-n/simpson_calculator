'''
GRAFICA PROTOTIPO 1
Autor: Josue Llumitasig
Fecha: 2025-06-11
Descripción: Servicio para graficar funciones y mostrar el área bajo la curva usando matplotlib.


import numpy as np
import matplotlib.pyplot as plt

def graficar_area_bajo_funcion(f, a, b, puntos=1000):
    x = np.linspace(a, b, puntos)
    y = f(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label='f(x)', color='green')
    plt.fill_between(x, y, color='orange', alpha=0.4, label='Área bajo la curva')
    
    plt.title('Área bajo la curva de f(x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.legend()
    plt.grid(True)
    plt.show()
    '''
    
'''GRAFICA PROTOTIPO 2

import numpy as np
import matplotlib.pyplot as plt

def graficar_area_bajo_funcion_v2(f, a, b, area_valor=None, texto_funcion="f(x)", puntos=1000):
    x = np.linspace(a, b, puntos)
    y = f(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=texto_funcion, color='green', linewidth=2)
    plt.fill_between(x, y, color='orange', alpha=0.4, label='Área bajo la curva')

    # Líneas verticales en a y b
    plt.axvline(a, color='red', linestyle='--', label=f"x = {a}")
    plt.axvline(b, color='blue', linestyle='--', label=f"x = {b}")

    # Mostrar área numérica si se pasa
    if area_valor is not None:
        plt.text((a + b) / 2, max(y) * 0.7, f"Área ≈ {area_valor:.4f}", fontsize=12, bbox=dict(facecolor='white', edgecolor='black'))

    plt.title(f"Área bajo la curva {texto_funcion} en [{a}, {b}]")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()

   '''
'''PROTOTIPO 3'''
"""
Autor: [Tu Nombre]
Fecha: 2025-06-11
Descripción: Servicio para graficar el área bajo una curva o entre dos curvas usando matplotlib.
Incluye visualización de límites, valor del área y opción para guardar como imagen.
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

    # Límites de integración
    plt.axvline(a, color='red', linestyle='--', label=f"x = {a}")
    plt.axvline(b, color='purple', linestyle='--', label=f"x = {b}")

    # Valor del área en el gráfico
    if area_valor is not None:
        plt.text((a + b) / 2, max(y1) * 0.7, f"Área ≈ {area_valor:.4f}", fontsize=12,
                 bbox=dict(facecolor='white', edgecolor='black'))

    plt.title("Visualización de Área")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()

    if guardar_como:
        plt.savefig(guardar_como, dpi=300)
        print(f"✅ Imagen guardada como: {guardar_como}")

    plt.show()
