from builtins import enumerate, len, str
import streamlit as st
from sympy import sympify, latex

def insertar_simbolo(simbolo: str):
    if "entrada_funcion" not in st.session_state:
        st.session_state.entrada_funcion = ""
    st.session_state.entrada_funcion += simbolo

def teclado_editor():
    if "entrada_funcion" not in st.session_state:
        st.session_state.entrada_funcion = ""

    st.markdown("## ✏️ Editor Visual de Funciones")

    # Entrada fluida editable con teclado físico
    entrada_temporal = st.text_input(
        "Función (puedes escribirla o usar el teclado visual):", 
        value=st.session_state.get("entrada_funcion", ""),
        key="editable_input"
    )
    if entrada_temporal != st.session_state.entrada_funcion:
        st.session_state.entrada_funcion = entrada_temporal

    # Vista LaTeX de la función ingresada
    try:
        expr = sympify(st.session_state.entrada_funcion)
        st.latex(f"f(x) = {latex(expr)}")
    except:
        st.warning("⚠️ La expresión es inválida. Revisa los paréntesis, operadores o símbolos.")

    st.markdown("### 🎛️ Teclado Matemático Visual")

    tabs = st.tabs(["🔢 Números", "📊 Álgebra", "📐 Trigonometría", "📘 Extras"])

    # TAB 1: Números y operadores
    with tabs[0]:
        st.markdown("#### 🔢 Números y operadores")
        filas = [
            [("7", "7"), ("8", "8"), ("9", "9"), ("+", "+")],
            [("4", "4"), ("5", "5"), ("6", "6"), ("−", "-")],
            [("1", "1"), ("2", "2"), ("3", "3"), ("×", "*")],
            [("0", "0"), (".", "."), ("÷", "/"), ("^", "**")]
        ]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, (label, insert) in enumerate(fila):
                if cols[i].button(label):
                    insertar_simbolo(insert)

    # TAB 2: Álgebra
    with tabs[1]:
        st.markdown("#### 📊 Álgebra básica")
        filas = [
            [("x", "x"), ("(", "("), (")", ")"), ("π", "pi")],
            [("√x", "sqrt(x)"), ("x²", "x**2"), ("1/x", "1/x"), ("|x|", "Abs(x)")]
        ]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, (label, insert) in enumerate(fila):
                if cols[i].button(label):
                    insertar_simbolo(insert)

    # TAB 3: Trigonometría
    with tabs[2]:
        st.markdown("#### 📐 Funciones trigonométricas")
        filas = [
            [("sin", "sin(x)"), ("cos", "cos(x)"), ("tan", "tan(x)")],
            [("arcsin", "asin(x)"), ("arccos", "acos(x)"), ("arctan", "atan(x)")],
            [("sec", "sec(x)"), ("csc", "csc(x)"), ("cot", "cot(x)")]
        ]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, (label, insert) in enumerate(fila):
                if cols[i].button(label):
                    insertar_simbolo(insert)

    # TAB 4: Extras
    with tabs[3]:
        st.markdown("#### 📘 Funciones adicionales")
        filas = [
            [("log", "log(x)"), ("eˣ", "exp(x)")]
        ]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, (label, insert) in enumerate(fila):
                if cols[i].button(label):
                    insertar_simbolo(insert)

    # Controles finales
    col1, col2 = st.columns(2)
    if col1.button("↩️ Borrar último"):
        st.session_state.entrada_funcion = st.session_state.entrada_funcion[:-1]
    if col2.button("🗑️ Limpiar todo"):
        st.session_state.entrada_funcion = ""

    return st.session_state.entrada_funcion
