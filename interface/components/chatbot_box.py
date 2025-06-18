from builtins import Exception
import streamlit as st
from sympy import symbols, lambdify, latex
from core.simpson import simpson_13
from services.ai_assistant import interpretar_instruccion

# Variable simbólica
x = symbols('x')

def mostrar_chatbot():
    st.markdown("## 🧠 Asistente Inteligente")
    st.write("Escribe tu pregunta o instrucción. Ej: *Calcular el área bajo la curva de x^2 entre 1 y 3 usando Simpson*")

    # Inicializar estado del chat
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Entrada del usuario
    user_input = st.text_input("✉️ Tu instrucción", key="chat_input")

    if st.button("💡 Interpretar"):
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })

        resultado = interpretar_instruccion(user_input)

        if resultado.get("exito"):
            try:
                # Generar función y calcular área
                f = lambdify(x, resultado["expr"], modules=["numpy"])
                area = simpson_13(f, resultado["a"], resultado["b"], 4)

                # Guardar en session_state para sincronizar con otras pestañas
                st.session_state.funcion_str = resultado["funcion"]
                st.session_state.expr = resultado["expr"]
                st.session_state.latex_expr = latex(resultado["expr"])
                st.session_state.resultado = area
                st.session_state.a = resultado["a"]
                st.session_state.b = resultado["b"]
                st.session_state.n = 4
                st.session_state.calculado_por_asistente = True

                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": resultado["mensaje"] + f" ✅ Área ≈ {area:.4f}. Puedes ver la gráfica o el resultado."
                })

            except Exception as e:
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"❌ Error al evaluar la función: {e}"
                })

        else:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": resultado.get("mensaje", "❌ No se pudo interpretar la instrucción.")
            })

    # Mostrar historial del chat
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
