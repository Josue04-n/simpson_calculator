from builtins import dict, max, min
import numpy as np
import plotly.graph_objects as go

def graficar_area_interactiva(
    f1,
    a,
    b,
    area_valor=None,
    texto_funcion1="f(x)",
    latex_funcion="",
    puntos=1000
):
    # Dominios extendidos
    margen_x = (b - a) * 2 if (b - a) > 0 else 10
    x_total = np.linspace(a - margen_x, b + margen_x, puntos)
    y_total = f1(x_total)
    y_total = np.where(np.isfinite(y_total), y_total, np.nan)

    # Dominio del área
    x_fill = np.linspace(a, b, puntos)
    y_fill = f1(x_fill)
    y_fill = np.where(np.isfinite(y_fill), y_fill, np.nan)

    # Asegurar visualización de los 4 cuadrantes
    y_min = np.nanmin(np.concatenate([y_total, y_fill]))
    y_max = np.nanmax(np.concatenate([y_total, y_fill]))
    margen_y = (y_max - y_min) * 0.2 if (y_max - y_min) > 0 else 10
    y_lim_inf = min(0, y_min - margen_y)
    y_lim_sup = max(0, y_max + margen_y)

    fig = go.Figure()

    # Curva completa
    fig.add_trace(go.Scatter(
        x=x_total,
        y=y_total,
        mode='lines',
        name=f"${latex_funcion}$" if latex_funcion else texto_funcion1,
        line=dict(color='green', width=2),
        hovertemplate='x=%{x}<br>f(x)=%{y}<extra></extra>'
    ))

    # Área bajo la curva
    fig.add_trace(go.Scatter(
        x=np.concatenate([[a], x_fill, [b]]),
        y=np.concatenate([[0], y_fill, [0]]),
        fill='toself',
        name="Área bajo la curva",
        fillcolor='rgba(255,165,0,0.4)',
        line=dict(color='orange'),
        hoverinfo='skip'
    ))

    # Valor del área
    if area_valor is not None:
        fig.add_annotation(
            x=(a + b) / 2,
            y=np.nanmax(y_fill) * 0.6,
            text=f"Área ≈ {area_valor:.4f}",
            showarrow=False,
            font=dict(size=14, color="black"),
            bgcolor="white"
        )

    # Título de la función
    if latex_funcion:
        fig.add_annotation(
            xref="paper", yref="paper",
            x=0.01, y=0.99,
            text=f"${latex_funcion}$",
            showarrow=False,
            font=dict(size=18, color="darkgreen")
        )

    # Líneas de a y b
    fig.add_vline(x=a, line=dict(color='red', dash='dot'),
                  annotation_text=f"a = {a}", annotation_position="bottom left")
    fig.add_vline(x=b, line=dict(color='purple', dash='dot'),
                  annotation_text=f"b = {b}", annotation_position="bottom right")

    # Ejes X e Y bien centrados
    fig.add_hline(y=0, line=dict(color='white', width=1))
    fig.add_vline(x=0, line=dict(color='white', width=1))

    # Estilo general
    fig.update_layout(
        title="Visualización Interactiva del Área",
        xaxis_title="x",
        yaxis_title="f(x)",
        hovermode="x unified",
        template="plotly_dark",
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            zeroline=False,
            rangeslider=dict(visible=True),
            title="🖱️ Usa el scroll inferior o arrastra para explorar el dominio"
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            range=[y_lim_inf, y_lim_sup]
        )
    )

    return fig
