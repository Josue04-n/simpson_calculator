from builtins import Exception, abs, dict, float, max
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
from sympy import lambdify, symbols, integrate, latex
from interface.components.keyboard_editor import teclado_editor
from core.simpson import simpson_13
from core.utils import validar_funcion
from services.plot_service import graficar_area_interactiva

x = symbols('x')

# Inicializar estado
for key in ["funcion_str", "expr", "latex_expr", "resultado", "a", "b", "n"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Configuración de página
st.set_page_config(page_title="Calculadora de Integrales", layout="wide")
st.markdown("# 🧮 Calculadora de Integrales - Método de Simpson")

tabs = st.tabs(["📥 Ingreso de datos", "📊 Ver resultado", "📈 Ver gráfica"])

# TAB 1 - Entrada
with tabs[0]:
    entrada = teclado_editor()

    a = st.number_input("Límite inferior (a)", value=0.0)
    b = st.number_input("Límite superior (b)", value=4.0)
    n = st.slider("Número de subintervalos (par)", min_value=2, max_value=100, step=2, value=4)

    if st.button("📌 Calcular integral"):
        expr, latex_expr, error = validar_funcion(entrada)
        if error:
            st.error(error)
        else:
            try:
                f = lambdify(x, expr, modules=["numpy"])
                resultado = simpson_13(f, a, b, n)

                st.session_state.funcion_str = entrada
                st.session_state.expr = expr
                st.session_state.latex_expr = latex_expr
                st.session_state.resultado = resultado
                st.session_state.a = a
                st.session_state.b = b
                st.session_state.n = n

                st.success("✅ Cálculo realizado. Ve a la pestaña de resultados o gráfica.")
            except Exception as e:
                st.error(f"❌ Error en el cálculo: {e}")

# TAB 2 - Resultado
with tabs[1]:
    st.subheader("📊 Resultado del cálculo")
    if st.session_state.resultado is not None:
        st.latex(f"\\int_{{{st.session_state.a}}}^{{{st.session_state.b}}} {st.session_state.latex_expr} \\,dx")
        st.info(f"📌 Área aproximada (Simpson): {st.session_state.resultado:.6f}")

        try:
            exacta = float(integrate(st.session_state.expr, (x, st.session_state.a, st.session_state.b)))
            st.success(f"🧮 Área exacta: {exacta:.6f}")
            error = abs(exacta - st.session_state.resultado)
            st.warning(f"📏 Error absoluto: {error:.6f}")
            st.warning(f"📉 Error relativo: {100 * error / exacta:.4f}%")
        except:
            st.warning("⚠️ No se pudo calcular la integral exacta simbólicamente.")
    else:
        st.info("🕐 Calcula primero una integral en la pestaña anterior.")

# TAB 3 - Gráfica
with tabs[2]:
    st.subheader("📈 Visualización gráfica")
    if st.session_state.resultado is not None:
        try:
            f_graf = lambdify(x, st.session_state.expr, modules=["numpy"])
            fig = graficar_area_interactiva(
                f1=f_graf,
                a=st.session_state.a,
                b=st.session_state.b,
                area_valor=st.session_state.resultado,
                texto_funcion1=st.session_state.funcion_str,
                latex_funcion=st.session_state.latex_expr
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error al graficar: {e}")
    else:
        st.info("📥 Calcula una función primero.")
