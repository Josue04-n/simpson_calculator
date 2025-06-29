import streamlit as st

def insertar_simbolo(simbolo: str, destino: str):
    key = f"entrada_funcion_{destino}"
    if key not in st.session_state:
        st.session_state[key] = ""
    st.session_state[key] += simbolo

def teclado_visual(destino: str):
    st.markdown("### 🎛️ Teclado Matemático Visual")

    tabs = st.tabs(["🔢 Números", "📊 Álgebra", "📐 Trigonometría", "📘 Extras"])

    # TAB 1: Números y operadores
    with tabs[0]:
        filas = [
            [("7", "7"), ("8", "8"), ("9", "9"), ("+", "+")],
            [("4", "4"), ("5", "5"), ("6", "6"), ("−", "-")],
            [("1", "1"), ("2", "2"), ("3", "3"), ("×", "*")],
            [("0", "0"), (".", "."), ("÷", "/"), ("^", "**")]
        ]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, (label, insert) in enumerate(fila):
                if cols[i].button(label, key=f"{destino}_num_{label}"):
                    insertar_simbolo(insert, destino)

    # TAB 2: Álgebra
    with tabs[1]:
        filas = [
            [("x", "x"), ("(", "("), (")", ")"), ("π", "pi")],
            [("√x", "sqrt(x)"), ("x²", "x**2"), ("1/x", "1/x"), ("|x|", "Abs(x)")]
        ]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, (label, insert) in enumerate(fila):
                if cols[i].button(label, key=f"{destino}_alg_{label}"):
                    insertar_simbolo(insert, destino)

    # TAB 3: Trigonometría
    with tabs[2]:
        filas = [
            [("sin", "sin(x)"), ("cos", "cos(x)"), ("tan", "tan(x)")],
            [("arcsin", "asin(x)"), ("arccos", "acos(x)"), ("arctan", "atan(x)")],
            [("sec", "sec(x)"), ("csc", "csc(x)"), ("cot", "cot(x)")]
        ]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, (label, insert) in enumerate(fila):
                if cols[i].button(label, key=f"{destino}_trig_{label}"):
                    insertar_simbolo(insert, destino)

    # TAB 4: Extras
    with tabs[3]:
        filas = [[("log", "log(x)"), ("eˣ", "exp(x)")]]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, (label, insert) in enumerate(fila):
                if cols[i].button(label, key=f"{destino}_extra_{label}"):
                    insertar_simbolo(insert, destino)
