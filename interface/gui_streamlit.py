import streamlit as st
import numpy as np
from sympy import symbols, integrate, lambdify, latex
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.utils import validar_funcion
from core.simpson import simpson_13
from services.plot_service import graficar_area_interactiva
from interface.components.keyboard_editor import teclado_visual
from scipy.misc import derivative

x = symbols("x")
st.set_page_config(layout="wide", page_title="Calculadora Simpson")
# Inicialización segura de variables de estado
for k in ["funcion_str", "expr", "latex_expr", "resultado", "a", "b", "n"]:
    if k not in st.session_state:
        st.session_state[k] = None


# ======================= 🎨 ESTILO PERSONALIZADO ============================
st.markdown("""
    <style>
    .main { background-color: #fff7f0; color: #3e2c1c; font-family: 'Segoe UI'; }
    .stButton>button {
        background-color: #f4a261; color: white; font-weight: bold;
        border-radius: 8px; padding: 8px 16px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 16px; font-weight: 600; color: #3e2c1c;
    }
    </style>
""", unsafe_allow_html=True)

# ======================= 📚 SIDEBAR ========================================
with st.sidebar:
    st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/2487/2487986.png" width="80">
    </div>
    """,
    unsafe_allow_html=True
)
    st.title("📘 Menú principal")
    opcion = st.radio("Navegar a:", [
        "📚 Teoría",
        "✍️ Ingreso de datos",
        "📊 Resultados",
        "📈 Gráfica",
        "🛠️ Otras funciones",
        "🧠 ¿Cuánto aprendiste?"
    ])

# ======================= 📚 TEORÍA =========================================
import tempfile, os, base64
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.animation import PillowWriter

if opcion == "📚 Teoría":
    st.markdown(
    "<h1 style='text-align: center;'>📚 Introducción Teórica</h1>",
    unsafe_allow_html=True
)

    st.markdown("### 🌐 ¿Qué es una Integral Definida?")

    st.markdown("""
    Una **integral definida** es una herramienta fundamental del cálculo que permite calcular el **área bajo la curva** de una función continua entre dos puntos \\( a \\) y \\( b \\).
    """)

    st.latex(r"\int_a^b f(x)\,dx")

    st.markdown("""
    Pero va mucho más allá que solo áreas: se usa para medir **cantidades acumuladas** cuando las tasas de cambio son conocidas.
    """)

    st.markdown("### 🧠 ¿Cómo interpretarla?")

    st.markdown(r"""
    - Si imaginas una función como una curva sobre un gráfico, la integral definida **suma infinitas áreas rectangulares** bajo esa curva para aproximar el total.
    - El área puede ser positiva o negativa, dependiendo de si la función está **encima o debajo del eje x**.
    """)

    st.markdown("### 📊 Ejemplos cotidianos:")
    st.markdown("- 📈 **Velocidad a lo largo del tiempo** → Área = **distancia recorrida**")
    st.markdown("- 🔌 **Potencia a lo largo del tiempo** → Área = **energía total consumida**")
    st.markdown("- 💵 **Tasa de ingresos** → Área = **dinero acumulado**")
    st.markdown("- 🧪 **Flujo de una sustancia** → Área = **masa total transportada**")

    st.markdown("### 🔢 ¿Cómo se calcula?")

    st.markdown(r"""
    Para funciones simples, se puede usar la **antiderivada**:
    """)

    st.latex(r"\int_a^b f(x)\,dx = F(b) - F(a)")

    st.markdown(r"""
    Donde \( F(x) \) es la **primitiva** (o antiderivada) de \( f(x) \).

    Pero en la mayoría de casos, se requiere un método **numérico** para calcularlo con computadoras:
    - 🟠 Método del Rectángulo
    - 🔵 Método del Trapecio
    - 🟢 **Método de Simpson** (más preciso y usado aquí)
    """)


    st.markdown("### 📜 Un poco de historia:")

    st.write("""
    El concepto de integral se remonta a los antiguos griegos con Arquímedes, quien calculaba áreas de segmentos de parábolas. 
    Sin embargo, la forma moderna fue desarrollada por Isaac Newton y Gottfried Leibniz en el siglo XVII. 
    Más tarde, matemáticos como Cauchy y Riemann formalizaron su definición.
    """)

    st.success("💡 En resumen: una integral definida es una herramienta para sumar cantidades variables a lo largo de un intervalo.")



    st.latex(r"\int_a^b f(x) \, dx")

    # 🔁 Animación 1: Área bajo curva
    f = lambda x: np.sin(x)
    a, b = 0, np.pi
    x = np.linspace(a, b, 500)
    y = f(x)

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(x, y, label="f(x) = sin(x)")
    ax1.set_xlim(a, b)
    ax1.set_ylim(0, 1.1)
    ax1.grid(True)
    ax1.set_title("Área bajo la curva")

    fill = ax1.fill_between([], [], [], color='orange', alpha=0.5)
    ani1_frames = np.linspace(a, b, 30)

    def animate_area(i):
        ax1.clear()
        ax1.plot(x, y, 'r', label="f(x) = sin(x)")
        ax1.set_xlim(a, b)
        ax1.set_ylim(0, 1.1)
        ax1.grid(True)
        ax1.set_title("Aproximando área bajo la curva")
        x_fill = x[x <= ani1_frames[i]]
        y_fill = f(x_fill)
        ax1.fill_between(x_fill, y_fill, color='orange', alpha=0.5)
        ax1.legend()

    ani1 = animation.FuncAnimation(fig1, animate_area, frames=len(ani1_frames), interval=80)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmp1:
        ani1.save(tmp1.name, writer=PillowWriter(fps=20))
        with open(tmp1.name, "rb") as f1:
            gif_bytes1 = f1.read()
        b64_1 = base64.b64encode(gif_bytes1).decode()
    os.remove(tmp1.name)

    st.markdown("#### 🔸 Visualización de área bajo la curva:")
    st.markdown(f"""
    <img src="data:image/gif;base64,{b64_1}" alt="Área bajo la curva" style="width:100%; border-radius:12px;" />
    """, unsafe_allow_html=True)

    # ----------------- Método de Simpson ---------------------
    st.markdown("### 🧠 ¿Cómo funciona el Método de Simpson?")
    st.info("Aproxima el área usando **parábolas** en lugar de trapecios o rectángulos.")
    st.latex(r"""
\int_a^b f(x) \, dx \approx \frac{h}{3} \left[f(x_0) + 4f(x_1) + 2f(x_2) + \ldots + f(x_n)\right]
""")

    st.markdown("#### 🎞️ Ejemplo Visual: Método de Simpson")

    n = 4
    x_vals = np.linspace(a, b, n + 1)
    x_fine = np.linspace(a, b, 400)
    y_fine = f(x_fine)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.set_ylim(-0.2, 1.2)
    ax2.set_xlim(a, b)

    def update_simpson(i):
        ax2.clear()
        ax2.plot(x_fine, y_fine, 'r-', label='f(x)')
        ax2.set_title(f"Subintervalo {i + 1}")
        ax2.set_xlim(a, b)
        ax2.set_ylim(-0.2, 1.2)
        ax2.grid(True)
        xi = x_vals[i:i + 3]
        yi = f(xi)
        xx = np.linspace(xi[0], xi[-1], 100)
        coeffs = np.polyfit(xi, yi, 2)
        yy = np.polyval(coeffs, xx)
        ax2.plot(xx, yy, 'b--')
        ax2.fill_between(xx, yy, alpha=0.3, color='orange')
        ax2.scatter(xi, yi, color='black')
        ax2.legend(loc='upper right')

    ani2 = animation.FuncAnimation(fig2, update_simpson, frames=n // 2, interval=1500)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmp2:
        ani2.save(tmp2.name, writer=PillowWriter(fps=1))
        with open(tmp2.name, "rb") as f2:
            gif_bytes2 = f2.read()
        b64_2 = base64.b64encode(gif_bytes2).decode()
    os.remove(tmp2.name)

    st.markdown(f"""
    <img src="data:image/gif;base64,{b64_2}" alt="Simpson Animation" style="width:100%; border-radius:12px;" />
    """, unsafe_allow_html=True)

    # Contexto y explicación
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📜 Historia y contexto del Método de Simpson")
    st.markdown("<div style='margin-bottom:32px;'></div>", unsafe_allow_html=True)

    st.write("""
El **Método de Simpson** fue descrito por el matemático inglés **Thomas Simpson** en el siglo XVIII, 
aunque ya era conocido anteriormente por Newton. Este método pertenece a una familia 
de técnicas numéricas llamadas **reglas de cuadratura**.
""")

    st.latex(r"""
\int_a^b f(x)\,dx \approx \frac{h}{3} \left[ f(x_0) + 4\sum_{\text{impares}} f(x_i) + 2\sum_{\text{pares}} f(x_i) + f(x_n) \right]
""")

    st.latex(r"h = \frac{b - a}{n}")
    st.markdown("- h: longitud del subintervalo")
    st.markdown("- n debe ser **par**")
    st.markdown("- Los \(x_i\) son los puntos del intervalo divididos")

    st.markdown("### ⚙️ Paso a paso:")
    st.markdown("1. Divide el intervalo \\([a, b]\\) en **n subintervalos pares**.")
    st.markdown("2. Calcula los puntos intermedios \\(x_0, x_1, ..., x_n\\).")
    st.markdown("3. Evalúa \\(f(x_i)\\) en cada punto.")
    st.markdown("4. Aplica la fórmula con coeficientes 1, 4, 2,..., 4, 1.")
    st.markdown("5. Obtén una estimación del área.")

    st.markdown("### 🟢 Ventajas")
    st.markdown("- Más preciso que el método del trapecio con la misma cantidad de puntos")
    st.markdown("- Funciona muy bien con funciones suaves")

    st.markdown("### 🔴 Limitaciones")
    st.markdown("- Requiere que el número de subintervalos sea **par**")
    st.markdown("- Si la función es muy irregular o presenta picos, puede perder precisión")

    st.info("✅ El Método de Simpson es ideal para funciones continuas, suaves y cuando se desea alta precisión con pocos puntos.")

# ======================= ✍️ INGRESO DE DATOS ==============================
elif opcion == "✍️ Ingreso de datos":
    
    st.markdown(
    "<h1 style='text-align: center;'>✍️ Ingreso de datos</h1>",
    unsafe_allow_html=True)

    entrada_key = "entrada_funcion_entrada1"
    editable_key = "editable_input_entrada1"
    if entrada_key not in st.session_state:
        st.session_state[entrada_key] = ""

    entrada = st.text_input("f(x) =", value=st.session_state[entrada_key], key=editable_key)
    if entrada != st.session_state[entrada_key]:
        st.session_state[entrada_key] = entrada

    expr, latex_expr, error = validar_funcion(entrada)
    if not error:
        st.latex(f"f(x) = {latex_expr}")
    else:
        st.warning(error)

    teclado_visual(destino="entrada1")

    a = st.number_input("Límite inferior a:", value=0.0)
    b = st.number_input("Límite superior b:", value=4.0)
    n = st.slider("Número de subintervalos (par):", 2, 100, 4, step=2)

    if st.button("📌 Calcular integral"):
        try:
            f = lambdify(x, expr, modules=["numpy"])
            resultado = simpson_13(f, a, b, n)
            st.session_state.update({
                "funcion_str": entrada,
                "expr": expr,
                "latex_expr": latex_expr,
                "resultado": resultado,
                "a": a,
                "b": b,
                "n": n
            })
            st.success("✅ Resultado guardado.")
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

# ======================= 📊 RESULTADOS ====================================
    import plotly.graph_objects as go
elif opcion == "📊 Resultados":
    st.title("📊 Resultado del cálculo")

    if st.session_state.resultado is not None:
        st.markdown("#### 📐 Función evaluada:")

        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st.latex(f"\\int_{{{st.session_state.a}}}^{{{st.session_state.b}}} {st.session_state.latex_expr} \\,dx")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Paneles de resultados
        col1, col2 = st.columns(2)

        col1.markdown(
            f"""
            <div style='background-color:#102841; padding:15px; border-radius:10px; color:white; text-align:center'>
                <b>Aproximación Simpson:</b><br>
                <span style='font-size:22px;'>{st.session_state.resultado:.6f}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        try:
            exacta = float(integrate(st.session_state.expr, (x, st.session_state.a, st.session_state.b)))
            error = abs(exacta - st.session_state.resultado)
            error_rel = 100 * error / abs(exacta)

            col2.markdown(
                f"""
                <div style='background-color:#0d362f; padding:15px; border-radius:10px; color:white; text-align:center'>
                    <b>Exacta:</b><br>
                    <span style='font-size:22px;'>{exacta:.6f}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("")

            c1, c2 = st.columns(2)
            c1.markdown(
                f"""
                <div style='background-color:#4d3e00; padding:15px; border-radius:10px; color:white; text-align:center'>
                    <b>Error absoluto:</b><br>
                    <span style='font-size:20px;'>{error:.6f}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            c2.markdown(
                f"""
                <div style='background-color:#4d2e00; padding:15px; border-radius:10px; color:white; text-align:center'>
                    <b>Error relativo:</b><br>
                    <span style='font-size:20px;'>{error_rel:.2f}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception:
            st.warning("⚠️ No se pudo calcular el valor exacto.")
    else:
        st.info("🔢 Aún no se ha ingresado una función.")

# ======================= 📈 GRÁFICA ========================================
# ======================= 📈 GRÁFICA ========================================
elif opcion == "📈 Gráfica":
    st.markdown("<h1 style='text-align:center; color:white;'>📈 Visualización Gráfica del Cálculo</h1>", unsafe_allow_html=True)

    if "resultado" in st.session_state and st.session_state.resultado is not None:
        try:
            st.markdown("### 📌 Información General")
            with st.container():
                st.markdown(
                    "<div style='background-color:#1e1e2f; padding:20px; border-radius:12px; color:white;'>",
                    unsafe_allow_html=True
                )
                st.markdown("**Función evaluada:**")
                st.latex(f"f(x) = {st.session_state.latex_expr}")
                st.markdown("**Intervalo:**")
                st.latex(f"[{st.session_state.a}, {st.session_state.b}]")
                st.markdown(f"**Subintervalos:** `{st.session_state.n}`")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🖼️ Área aproximada bajo la curva")
            st.markdown("<p style='color:#ccc;'>Interactúa con la gráfica: haz zoom, mueve el eje o inspecciona valores</p>", unsafe_allow_html=True)

            from plotly import graph_objects as go

            a, b = st.session_state.a, st.session_state.b
            f_plot = lambdify(x, st.session_state.expr, modules=["numpy"])

            n_points = 80  # Animación más fluida
            x_anim = np.linspace(a, b, n_points)
            y_anim = f_plot(x_anim)

            # Dominio extendido
            delta = (b - a) * 0.3
            x_full = np.linspace(a - delta, b + delta, 400)
            y_full = f_plot(x_full)

            fig = go.Figure()

            # Curva completa
            fig.add_trace(go.Scatter(
                x=x_full, y=y_full, mode="lines", name="f(x)",
                line=dict(color="green", width=2)
            ))

            # Área inicial vacía
            x_area = np.concatenate([x_anim[:2], x_anim[:2][::-1]])
            y_area = np.concatenate([y_anim[:2], np.zeros(2)])
            fig.add_trace(go.Scatter(
                x=x_area, y=y_area, fill="toself",
                fillcolor="rgba(255,165,0,0.5)",
                line=dict(color="rgba(255,165,0,0)"),
                name="Área bajo f(x)"
            ))

            # Frames animados
            frames = []
            for i in range(3, len(x_anim)):
                x_fill = np.concatenate([x_anim[:i], x_anim[:i][::-1]])
                y_fill = np.concatenate([y_anim[:i], np.zeros(i)])
                frames.append(go.Frame(data=[
                    go.Scatter(x=x_full, y=y_full),
                    go.Scatter(x=x_fill, y=y_fill)
                ]))

            fig.frames = frames

            # Layout con botón de animación
            fig.update_layout(
                updatemenus=[dict(
                    type="buttons", showactive=False,
                    buttons=[dict(label="▶️ Reproducir", method="animate",
                                  args=[None, {"frame": {"duration": 50, "redraw": True},
                                               "fromcurrent": True}])]
                )],
                title="Área bajo la curva f(x)",
                xaxis_title="x",
                yaxis_title="f(x)",
                height=500,
                template="plotly_dark",
                legend=dict(orientation="h", y=-0.25, x=0.3)
            )

            st.plotly_chart(fig, use_container_width=True)
            st.success("✅ Área bajo la curva visualizada con animación.")

        except Exception as e:
            st.error(f"❌ Error al graficar: {e}")
    else:
        st.info("ℹ️ Por favor, calcula primero una integral en la pestaña correspondiente.")


# ======================= 🛠️ OTRAS FUNCIONES ===============================
elif opcion == "🛠️ Otras funciones":
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
            f_expr = f_latex = f_err = "❌ Error en f(x)"
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
                g_expr = g_latex = g_err = "❌ Error en g(x)"
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
    n2 = st.slider("Número de puntos", min_value=10, max_value=100, step=10, value=100, key="otras_n")

    if st.button("📌 Ejecutar cálculo", key="otras_calcular"):
        if f_err or g_err:
            st.error(f_err or g_err)
        else:
            try:
                f = lambdify(x, f_expr, modules=["numpy"])
                x_vals = np.linspace(a2, b2, n2)

                if funcion_opcion == "Área entre curvas":
                    g = lambdify(x, g_expr, modules=["numpy"])
                    y_f = f(x_vals)
                    y_g = g(x_vals)
                    y_area = np.abs(y_f - y_g)
                    resultado_otro = np.trapz(y_area, x_vals)

                    st.latex(f"\\int_{{{a2}}}^{{{b2}}} |{f_latex} - {g_latex}| \\,dx")
                    st.success(f"📐 Área entre curvas: {resultado_otro:.6f}")
                    st.info("🟨 Este cálculo representa el área encerrada entre dos funciones a lo largo del intervalo definido.")

                    # ---------------- GRAFICA CON ANIMACIÓN (Plotly) ----------------
                    import plotly.graph_objects as go

                    # Dominio ampliado para contexto
                    delta = (b2 - a2) * 0.3
                    x_full = np.linspace(a2 - delta, b2 + delta, 400)
                    y_full_f = f(x_full)
                    y_full_g = g(x_full)

                    # Datos para animar el área
                    x_anim = np.linspace(a2, b2, 80)
                    y_f_anim = f(x_anim)
                    y_g_anim = g(x_anim)

                    fig = go.Figure()

                    # Curva f(x)
                    fig.add_trace(go.Scatter(
                        x=x_full, y=y_full_f, mode="lines", name="f(x)",
                        line=dict(color="green", width=2)
                    ))

                    # Curva g(x)
                    fig.add_trace(go.Scatter(
                        x=x_full, y=y_full_g, mode="lines", name="g(x)",
                        line=dict(color="blue", width=2)
                    ))

                    # Área inicial vacía
                    area_x = np.concatenate([x_anim[:2], x_anim[:2][::-1]])
                    area_y = np.concatenate([y_f_anim[:2], y_g_anim[:2][::-1]])
                    fig.add_trace(go.Scatter(
                        x=area_x, y=area_y,
                        fill='toself', fillcolor='rgba(255,165,0,0.5)',
                        line=dict(color="rgba(255,165,0,0)"),
                        name="Área entre curvas"
                    ))

                    # Frames animados (rellenando área)
                    frames = []
                    for i in range(3, len(x_anim)):
                        x_fill = np.concatenate([x_anim[:i], x_anim[:i][::-1]])
                        y_fill = np.concatenate([y_f_anim[:i], y_g_anim[:i][::-1]])
                        frames.append(go.Frame(data=[
                            go.Scatter(x=x_full, y=y_full_f),
                            go.Scatter(x=x_full, y=y_full_g),
                            go.Scatter(x=x_fill, y=y_fill)
                        ]))

                    fig.frames = frames

                    # Layout interactivo con botones
                    fig.update_layout(
                        updatemenus=[dict(
                            type="buttons",
                            showactive=False,
                            buttons=[dict(label="▶️ Reproducir", method="animate",
                                        args=[None, {"frame": {"duration": 60, "redraw": True},
                                                    "fromcurrent": True}])
                            ])],
                        title="Visualización animada del área entre f(x) y g(x)",
                        xaxis_title="x",
                        yaxis_title="y",
                        template="plotly_dark",
                        height=500,
                        legend=dict(orientation="h", y=-0.25, x=0.3)
                    )

                    st.plotly_chart(fig, use_container_width=True)


                elif funcion_opcion == "Longitud de arco":
                    from scipy.misc import derivative
                    dy_dx = np.array([derivative(f, xi, dx=1e-6) for xi in x_vals])
                    integrando = np.sqrt(1 + dy_dx**2)
                    resultado_otro = np.trapz(integrando, x_vals)
                    st.markdown("$$\\int_a^b \\sqrt{1 + \\left(\\frac{dy}{dx}\\right)^2} dx$$")
                    st.success(f"📏 Longitud de arco: {resultado_otro:.6f}")
                    st.info("📈 Esto estima la longitud de la curva definida por f(x) desde a hasta b.")

                elif funcion_opcion == "Superficie de revolución":
                    from scipy.misc import derivative
                    y_vals = f(x_vals)
                    dy_dx = np.array([derivative(f, xi, dx=1e-6) for xi in x_vals])
                    integrando = 2 * np.pi * np.abs(y_vals) * np.sqrt(1 + dy_dx**2)
                    resultado_otro = np.trapz(integrando, x_vals)
                    st.markdown("$$2\\pi \\int_a^b |f(x)| \\sqrt{1 + \\left(\\frac{dy}{dx}\\right)^2} dx$$")
                    st.success(f"🌀 Superficie de revolución: {resultado_otro:.6f}")
                    st.info("🧮 Esta es el área de la superficie generada al girar la curva f(x) alrededor del eje x.")

            except Exception as e:
                st.error(f"❌ Error durante el cálculo: {e}")

# ======================= 🧠 JUEGO DE APRENDIZAJE ==========================               
elif opcion == "🧠 ¿Cuánto aprendiste?":
    st.title("🧠 ¿Cuánto aprendiste?")
    st.markdown("Pon a prueba tus conocimientos sobre integrales definidas y el Método de Simpson.")

    tipo_juego = st.radio("Selecciona el modo de juego:", [
        "🎲 Quiz de opción múltiple",
        "🎯 Verdadero o Falso",
        "🃏 Emparejar conceptos",
        "🖌️ Dibuja el área"
    ], key="modo_quiz")

    if tipo_juego == "🎲 Quiz de opción múltiple":
        preguntas = [
            {"pregunta": "¿Qué representa una integral definida?",
             "opciones": ["La derivada de una función", "El área bajo la curva", "La pendiente de una recta", "Un número complejo"],
             "respuesta": "El área bajo la curva"},
            {"pregunta": "¿Qué método es más preciso para calcular integrales numéricamente?",
             "opciones": ["Método del rectángulo", "Método del trapecio", "Método de Simpson", "Derivación"],
             "respuesta": "Método de Simpson"},
            {"pregunta": "¿Qué condición debe cumplirse para usar el Método de Simpson?",
             "opciones": ["El intervalo debe ser impar", "Debe ser una función lineal", "El número de subintervalos debe ser par", "Debe ser exponencial"],
             "respuesta": "El número de subintervalos debe ser par"}
        ]

        score = 0
        for i, q in enumerate(preguntas):
            st.markdown(f"**Pregunta {i+1}: {q['pregunta']}**")
            seleccion = st.radio("Elige una opción:",
                                 ["🔸 Selecciona una respuesta"] + q["opciones"],
                                 key=f"q{i}")
            if seleccion != "🔸 Selecciona una respuesta":
                if seleccion == q["respuesta"]:
                    st.success("✅ ¡Correcto!")
                    score += 1
                else:
                    st.error(f"❌ Incorrecto. Respuesta correcta: {q['respuesta']}")
            else:
                st.warning("⚠️ Debes seleccionar una respuesta.")
            st.markdown("---")

        st.markdown(f"### 🎉 Puntuación final: **{score} / {len(preguntas)}**")

    elif tipo_juego == "🎯 Verdadero o Falso":
        preguntas_tf = [
            {"texto": "La integral definida puede calcular áreas negativas.", "respuesta": True},
            {"texto": "El Método de Simpson usa trapecios para aproximar el área.", "respuesta": False},
            {"texto": "Newton y Leibniz desarrollaron el cálculo integral.", "respuesta": True},
            {"texto": "El área bajo la curva siempre es positiva.", "respuesta": False}
        ]

        score_tf = 0
        for i, q in enumerate(preguntas_tf):
            st.markdown(f"**{i+1}. {q['texto']}**")
            seleccion = st.radio("Selecciona:",
                                 ["🔸 Selecciona", "Verdadero", "Falso"],
                                 key=f"tf{i}")
            if seleccion == "🔸 Selecciona":
                st.warning("⚠️ Selecciona una respuesta.")
            else:
                es_correcto = (seleccion == "Verdadero") == q["respuesta"]
                if es_correcto:
                    st.success("✅ ¡Correcto!")
                    score_tf += 1
                else:
                    correcto = "Verdadero" if q["respuesta"] else "Falso"
                    st.error(f"❌ Incorrecto. Respuesta correcta: {correcto}")
            st.markdown("---")

        st.markdown(f"### 🧠 Tu puntuación final fue: **{score_tf} / {len(preguntas_tf)}**")

    elif tipo_juego == "🃏 Emparejar conceptos":
        st.subheader("🃏 Emparejar conceptos")
        st.markdown("Empareja mentalmente el concepto con su definición correcta.")

        definiciones = {
            "Área bajo la curva": "Resultado de una integral definida",
            "Método de Simpson": "Aproxima usando parábolas",
            "Newton y Leibniz": "Creadores del cálculo integral",
            "Subintervalos pares": "Requisito para Simpson 1/3",
            "Función continua": "Condición para aplicar integral definida",
        }

        conceptos = list(definiciones.keys())
        definiciones_shuffled = list(definiciones.values())
        np.random.shuffle(definiciones_shuffled)

        respuestas_usuario = []
        aciertos = 0

        for i, concepto in enumerate(conceptos):
            st.markdown(f"🔹 **{concepto}**")
            seleccion = st.selectbox("Selecciona la definición:",
                                     ["🔸 Elige una definición"] + definiciones_shuffled,
                                     key=f"match{i}")
            respuestas_usuario.append((concepto, seleccion))
            st.markdown("---")

        if st.button("✅ Verificar respuestas"):
            for concepto, seleccion in respuestas_usuario:
                if seleccion == "🔸 Elige una definición":
                    st.warning(f"⚠️ No seleccionaste para: {concepto}")
                elif definiciones[concepto] == seleccion:
                    st.success(f"✔️ {concepto} → Correcto")
                    aciertos += 1
                else:
                    st.error(f"❌ {concepto} → Incorrecto. Era: **{definiciones[concepto]}**")
            st.markdown(f"### 🧠 Resultado final: **{aciertos} / {len(definiciones)} aciertos**")

    elif tipo_juego == "🖌️ Dibuja el área":
        st.subheader("🖌️ Dibuja el área")
        st.markdown("Visualiza la curva y predice visualmente el área sombreada.")

        import matplotlib.pyplot as plt
        f = lambda x: np.sin(x)
        a, b = 0, np.pi
        x_vals = np.linspace(a, b, 300)
        y_vals = f(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="f(x) = sin(x)", color='green')
        ax.fill_between(x_vals, y_vals, color='orange', alpha=0.4)
        ax.set_title("Área bajo la curva")
        ax.grid(True)
        st.pyplot(fig)

        area_esperada = 2.0
        estimacion = st.slider("¿Cuál crees que es el área bajo la curva en [0, π]?", min_value=0.0, max_value=4.0, step=0.1)
        if st.button("🔍 Verificar estimación"):
            error = abs(estimacion - area_esperada)
            if error < 0.2:
                st.success("✅ ¡Muy buena estimación!")
            else:
                st.warning(f"📉 Estimación alejada. El área real es aproximadamente {area_esperada:.2f}")
