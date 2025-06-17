from builtins import dict
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
    # Ampliar margen para ver la función completa
    margen = (b - a) * 2 if (b - a) > 0 else 10
    x_total = np.linspace(a - margen, b + margen, puntos)
    y_total = f1(x_total)
    y_total = np.where(np.isfinite(y_total), y_total, np.nan)

    # Área bajo la curva
    x_fill = np.linspace(a, b, puntos)
    y_fill = f1(x_fill)
    y_fill = np.where(np.isfinite(y_fill), y_fill, np.nan)

    fig = go.Figure()

    # Curva de la función completa
    fig.add_trace(go.Scatter(
        x=x_total,
        y=y_total,
        mode='lines',
        name=f"${latex_funcion}$" if latex_funcion else texto_funcion1,
        line=dict(color='green', width=2),
        hovertemplate='x=%{x}<br>f(x)=%{y}<extra></extra>'
    ))

    # Área sombreada bajo la curva entre a y b
    fig.add_trace(go.Scatter(
        x=np.concatenate([[a], x_fill, [b]]),
        y=np.concatenate([[0], y_fill, [0]]),
        fill='toself',
        name="Área bajo la curva",
        fillcolor='rgba(255,165,0,0.4)',
        line=dict(color='orange'),
        hoverinfo='skip'
    ))

    # Anotación del valor de área
    if area_valor is not None:
        fig.add_annotation(
            x=(a + b) / 2,
            y=np.nanmax(y_fill) * 0.6,
            text=f"Área ≈ {area_valor:.4f}",
            showarrow=False,
            font=dict(size=14, color="black"),
            bgcolor="white"
        )

    # Mostrar fórmula simbólica en esquina superior izquierda
    if latex_funcion:
        fig.add_annotation(
            xref="paper", yref="paper",
            x=0.01, y=0.99,
            text=f"${latex_funcion}$",
            showarrow=False,
            font=dict(size=18, color="darkgreen")
        )

    # Líneas de los límites
    fig.add_vline(x=a, line=dict(color='red', dash='dot'),
                  annotation_text=f"a = {a}", annotation_position="bottom left")
    fig.add_vline(x=b, line=dict(color='purple', dash='dot'),
                  annotation_text=f"b = {b}", annotation_position="bottom right")

    # Configuración interactiva: zoom y scroll
    fig.update_layout(
        title="Visualización Interactiva del Área",
        xaxis_title="x",
        yaxis_title="f(x)",
        hovermode="x unified",
        template="plotly_white",
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            zeroline=True,
            rangeslider=dict(visible=True),  # Zoom con scroll
            title="🖱️ Usa el scroll o arrastra para acercar/alejar"
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            automargin=True,
            rangemode="tozero"
        )
    )

    return fig
