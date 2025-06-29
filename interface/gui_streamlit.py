from builtins import Exception, abs, dict, float, max
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
from sympy import lambdify, symbols, integrate, latex
from interface.components.keyboard_editor import teclado_visual
from core.functions import area_entre_curvas, longitud_de_arco, superficie_de_revolucion
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

tabs = st.tabs([
    "📥 Ingreso de datos",
    "📊 Ver resultado",
    "📈 Ver gráfica",
    "🛠️ Otras funciones"
])

# ======================
# ✅ TAB 1 - Ingreso de datos
# ======================
with tabs[0]:
    st.subheader("📥 Ingreso de función")

    entrada_key = "entrada_funcion_entrada1"
    editable_key = "editable_input_entrada1"

    if entrada_key not in st.session_state:
        st.session_state[entrada_key] = ""

    valor_actual = st.session_state[entrada_key]
    entrada1 = st.text_input("Función f(x)", value=valor_actual, key=editable_key)

    if entrada1 != st.session_state[entrada_key]:
        st.session_state[entrada_key] = entrada1

    expr, latex_expr, error = validar_funcion(st.session_state[entrada_key])
    if not error:
        st.latex(f"f(x) = {latex_expr}")

    teclado_visual(destino="entrada1")

    a = st.number_input("Límite inferior (a)", value=0.0)
    b = st.number_input("Límite superior (b)", value=4.0)
    n = st.slider("Número de subintervalos (par)", min_value=2, max_value=100, step=2, value=4)

    if st.button("📌 Calcular integral", key="calcular_integral_main"):
        if error:
            st.error(error)
        else:
            try:
                f = lambdify(x, expr, modules=["numpy"])
                resultado = simpson_13(f, a, b, n)

                st.session_state.funcion_str = st.session_state[entrada_key]
                st.session_state.expr = expr
                st.session_state.latex_expr = latex_expr
                st.session_state.resultado = resultado
                st.session_state.a = a
                st.session_state.b = b
                st.session_state.n = n

                st.success("✅ Cálculo realizado. Ve a la pestaña de resultados o gráfica.")
            except Exception as e:
                st.error(f"❌ Error en el cálculo: {e}")

# ======================
# ✅ TAB 2 - Ver resultado
# ======================
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

# ======================
# ✅ TAB 3 - Ver gráfica
# ======================
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

# ======================
# ✅ TAB 4 - Otras funciones
# ======================
with tabs[3]:
    st.subheader("🛠️ Cálculos independientes")

    funcion_opcion = st.selectbox(
        "Selecciona la operación:",
        ("Área entre curvas", "Longitud de arco", "Superficie de revolución")
    )

    colf, colg = st.columns(2)
    with colf:
        if "entrada_funcion_f" not in st.session_state:
            st.session_state["entrada_funcion_f"] = ""
        f_edit = st.text_input("Función f(x)", value=st.session_state["entrada_funcion_f"], key="editable_input_f")

        if f_edit != st.session_state["entrada_funcion_f"]:
            st.session_state["entrada_funcion_f"] = f_edit

        try:
            f_expr, f_latex, f_err = validar_funcion(st.session_state["entrada_funcion_f"])
            st.latex(f"f(x) = {latex(f_expr)}")
        except:
            f_expr = f_latex = f_err = None
            st.warning("⚠️ f(x) inválida")

    if funcion_opcion == "Área entre curvas":
        with colg:
            if "entrada_funcion_g" not in st.session_state:
                st.session_state["entrada_funcion_g"] = ""
            g_edit = st.text_input("Función g(x)", value=st.session_state["entrada_funcion_g"], key="editable_input_g")

            if g_edit != st.session_state["entrada_funcion_g"]:
                st.session_state["entrada_funcion_g"] = g_edit

            try:
                g_expr, g_latex, g_err = validar_funcion(st.session_state["entrada_funcion_g"])
                st.latex(f"g(x) = {latex(g_expr)}")
            except:
                g_expr = g_latex = g_err = None
                st.warning("⚠️ g(x) inválida")
    else:
        g_expr = g_latex = g_err = None

    destino = st.radio("🖱️ ¿Dónde insertar símbolos?", 
                       ["f(x)", "g(x)"] if funcion_opcion == "Área entre curvas" else ["f(x)"], 
                       key="destino_input")
    destino_key = "f" if destino == "f(x)" else "g"
    teclado_visual(destino=destino_key)

    a2 = st.number_input("Límite inferior (a)", value=0.0, key="otras_a")
    b2 = st.number_input("Límite superior (b)", value=4.0, key="otras_b")
    n2 = st.slider("Número de puntos", min_value=10, max_value=1000, step=10, value=200, key="otras_n")

    if st.button("📌 Ejecutar cálculo", key="otras_calcular"):
        if f_err or g_err:
            st.error(f_err or g_err)
        else:
            try:
                f = lambdify(x, f_expr, modules=["numpy"])
                x_vals = np.linspace(a2, b2, n2)

                if funcion_opcion == "Área entre curvas":
                    g = lambdify(x, g_expr, modules=["numpy"])
                    y_vals = np.abs(f(x_vals) - g(x_vals))
                    resultado_otro = np.trapz(y_vals, x_vals)
                    st.latex(f"\\int_{{{a2}}}^{{{b2}}} |{f_latex} - {g_latex}| \\,dx")

                elif funcion_opcion == "Longitud de arco":
                    from scipy.misc import derivative
                    dy_dx = np.array([derivative(f, xi, dx=1e-6) for xi in x_vals])
                    integrando = np.sqrt(1 + dy_dx**2)
                    resultado_otro = np.trapz(integrando, x_vals)
                    st.markdown("$$\\int_a^b \\sqrt{1 + \\left(\\frac{dy}{dx}\\right)^2} dx$$")

                elif funcion_opcion == "Superficie de revolución":
                    from scipy.misc import derivative
                    y_vals = f(x_vals)
                    dy_dx = np.array([derivative(f, xi, dx=1e-6) for xi in x_vals])
                    integrando = 2 * np.pi * np.abs(y_vals) * np.sqrt(1 + dy_dx**2)
                    resultado_otro = np.trapz(integrando, x_vals)
                    st.markdown("$$2\\pi \\int_a^b |f(x)| \\sqrt{1 + \\left(\\frac{dy}{dx}\\right)^2} dx$$")

                st.success(f"📐 Resultado aproximado: {resultado_otro:.6f}")

            except Exception as e:
                st.error(f"❌ Error durante el cálculo: {e}")
