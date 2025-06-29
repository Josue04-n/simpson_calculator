
from sympy import symbols, sympify, latex, lambdify
from sympy.core.sympify import SympifyError

x = symbols('x')

def validar_funcion(entrada: str):
    try:
        expr = sympify(entrada)
        _ = lambdify(x, expr, modules=['numpy'])  
        latex_str = latex(expr)
        return expr, latex_str, None
    except SympifyError:
        return None, None, "❌ Error: Expresión inválida. Revisa paréntesis, funciones mal escritas (ej: 'ln' en vez de 'log'), etc."
    except NameError as ne:
        return None, None, f"❌ Nombre no reconocido: {str(ne)}"
    except Exception as e:
        mensaje_limpio = str(e).split(":")[-1].strip()
        return None, None, f"❌ Error general: {mensaje_limpio}"
