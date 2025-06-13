"""
Autor: Josue Llumitasig
Fecha: 2025-06-12
Descripción: Funciones auxiliares para validar expresiones simbólicas y convertirlas a LaTeX.
"""

from sympy import symbols, sympify, latex, lambdify
from sympy.core.sympify import SympifyError

x = symbols('x')

def validar_funcion(entrada: str):
    """
    Valida que la entrada sea una función válida de x.
    Retorna:
    - expresión simbólica (SymPy)
    - versión en LaTeX (str)
    - mensaje de error (None si no hay error)
    """
    try:
        expr = sympify(entrada)
        # Probar si la expresión puede convertirse en una función evaluable
        _ = lambdify(x, expr, modules=['numpy'])  # Solo para validar
        latex_str = latex(expr)
        return expr, latex_str, None
    except SympifyError:
        return None, None, "❌ Error: Expresión inválida. Revisa paréntesis, funciones mal escritas (ej: 'ln' en vez de 'log'), etc."
    except NameError as ne:
        return None, None, f"❌ Nombre no reconocido: {str(ne)}"
    except Exception as e:
        mensaje_limpio = str(e).split(":")[-1].strip()
        return None, None, f"❌ Error general: {mensaje_limpio}"
