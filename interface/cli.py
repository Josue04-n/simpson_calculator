"""
Autor: [Josue Llumitasig]
Fecha: 2025-06-11
Descripción: Interfaz de línea de comandos (CLI) para calcular integrales definidas
utilizando el método de Simpson 1/3. Permite calcular el área bajo una curva o entre dos curvas.
"""

from core.utils import validar_funcion
from services.plot_service import graficar_area
import numpy as np
from core.simpson import simpson_13
from sympy import symbols, lambdify, sympify

def ingresar_funcion(mensaje="f(x) = "):
    print(f"👉 Ingresa la función {mensaje}")
    entrada = input()
    expr, latex_str, error = validar_funcion(entrada)

    if error:
        print(error)
        return None, None, None

    try:
        f = lambdify(symbols('x'), expr, modules=['numpy'])
        return f, str(expr), latex_str
    except Exception as e:
        print(f"❌ Error al convertir a función evaluable: {e}")
        return None, None, None


def calcular_area_una_funcion():
    f, texto_funcion, latex_funcion  = ingresar_funcion("a integrar (por ejemplo: sqrt(x) - x/2):")
    if f is None:
        return


    try:
        a = float(input("🔢 Límite inferior a: "))
        b = float(input("🔢 Límite superior b: "))
        n = int(input("🔢 Número de subintervalos (par): "))

        resultado = simpson_13(f, a, b, n)
        print(f"\n✅ Resultado:\n∫ {texto_funcion} dx de {a} a {b} ≈ {resultado:.6f}")

        ver = input("¿Deseas visualizar la gráfica? (s/n): ").strip().lower()
        if ver == "s":
            graficar_area(f1=f, a=a, b=b, area_valor=resultado, texto_funcion1=texto_funcion)

    except Exception as e:
        print(f"❌ Error en los datos: {e}")


def calcular_area_entre_dos_funciones():
    f1, texto1, latex1  = ingresar_funcion("superior f(x):")
    f2, texto2, latex2  = ingresar_funcion("inferior g(x):")

    if f1 is None or f2 is None:
        return

    try:
        a = float(input("🔢 Límite inferior a: "))
        b = float(input("🔢 Límite superior b: "))
        n = int(input("🔢 Número de subintervalos (par): "))

        diferencia = lambda x: f1(x) - f2(x)
        resultado = simpson_13(diferencia, a, b, n)
        print(f"\n✅ Resultado:\nÁrea entre {texto1} y {texto2} de {a} a {b} ≈ {resultado:.6f}")

        ver = input("¿Deseas visualizar la gráfica? (s/n): ").strip().lower()
        if ver == "s":
            graficar_area(f1=f1, f2=f2, a=a, b=b, area_valor=resultado,
              texto_funcion1=texto1, texto_funcion2=texto2, latex_funcion=latex1)  



    except Exception as e:
        print(f"❌ Error en los datos: {e}")


def ejecutar_calculadora():
    print("🧮 Calculadora de Integrales con Método de Simpson 1/3")
    print("------------------------------------------------------")

    print("1. Calcular integral de una sola función")
    print("2. Calcular área entre dos funciones")
    opcion = input("Selecciona una opción (1 o 2): ")

    if opcion == "1":
        calcular_area_una_funcion()
    elif opcion == "2":
        calcular_area_entre_dos_funciones()
    else:
        print("❌ Opción inválida.")

if __name__ == "__main__":
    ejecutar_calculadora()
