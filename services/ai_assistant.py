from builtins import Exception, float
from sympy import sympify
import re

def interpretar_instruccion(texto):
    try:
        texto = texto.lower().strip()

        # Extraer límites
        limite_pattern = r'entre\s+(.*?)\s+y\s+(.*)'
        limites = re.search(limite_pattern, texto)
        a = sympify(limites.group(1)) if limites else None
        b = sympify(limites.group(2)) if limites else None

        # Extraer función (mejorado: elimina palabras innecesarias)
        funcion_pattern = r'(?:área\s+bajo\s+la\s+curva\s+de|de|la)\s+(.*?)\s+(?:entre|desde)'
        funcion_match = re.search(funcion_pattern, texto)
        funcion_raw = funcion_match.group(1) if funcion_match else None

        if funcion_raw:
            # Limpieza de texto como "curva de x^2" → "x^2"
            funcion = re.sub(r'(curva\s+de\s+)', '', funcion_raw).strip()
            expr = sympify(funcion)
        else:
            return {"exito": False, "mensaje": "❌ No se pudo identificar la función."}

        if expr and a is not None and b is not None:
            return {
                "exito": True,
                "funcion": funcion,
                "expr": expr,
                "a": float(a),
                "b": float(b),
                "mensaje": f"✅ Función reconocida: `{funcion}` con límites `a = {a}`, `b = {b}`."
            }
        else:
            return {"exito": False, "mensaje": "❌ No se pudo interpretar completamente la instrucción."}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error al interpretar: {e}"}
