import plotly.express as px
import plotly.graph_objects as go

PALETA = [
    "#7ba05b",  # verde medio
    "#1d5631",  # verde escuro
    "#a52828",  # vermelho destaque
    "#5a8a3c",  # verde folha
    "#c9a227",  # dourado
    "#3c6e47",  # verde musgo
    "#8c6d3f",  # marrom claro
    "#d68c45",  # laranja terroso
]

LAYOUT_BASE = dict(
    template="plotly_white",
    font=dict(family="Segoe UI, sans-serif", color="#000000"),
    title_font=dict(size=18, color="#1d5631"),
    margin=dict(l=40, r=20, t=70, b=60),
    hovermode="x unified",
    paper_bgcolor="#f5f2e3",
    plot_bgcolor="#f5f2e3",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        font=dict(color="#000000"),
    ),
)


def _aplicar_estilo_eixos(fig, xaxis_title=None, yaxis_title=None):
    fig.update_xaxes(
        title=xaxis_title,
        gridcolor="#e3ddc4",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
        linecolor="#000000",
    )
    fig.update_yaxes(
        title=yaxis_title,
        gridcolor="#e3ddc4",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
        linecolor="#000000",
    )
    return fig


def grafico_linha(df, x, ys, titulo, rotulo_y="Valor"):
    if isinstance(ys, str):
        ys = [ys]

    fig = go.Figure()

    for i, y in enumerate(ys):
        fig.add_trace(
            go.Scatter(
                x=df[x],
                y=df[y],
                mode="lines+markers",
                name=y.replace("_", " "),
                line=dict(color=PALETA[i % len(PALETA)], width=2.5),
                marker=dict(size=6),
            )
        )

    fig.update_layout(
        title=titulo,
        xaxis_title=x,
        yaxis_title=rotulo_y,
        **LAYOUT_BASE,
    )

    fig = _aplicar_estilo_eixos(fig, xaxis_title=x, yaxis_title=rotulo_y)

    return fig


def grafico_barras(df, x, y, titulo, cor=None, orientacao="v"):
    if orientacao == "h":
        fig = px.bar(
            df,
            x=y,
            y=x,
            color=cor,
            orientation="h",
            color_discrete_sequence=PALETA,
        )
        x_title = y.replace("_", " ")
        y_title = x.replace("_", " ")
    else:
        fig = px.bar(
            df,
            x=x,
            y=y,
            color=cor,
            color_discrete_sequence=PALETA,
        )
        x_title = x.replace("_", " ")
        y_title = y.replace("_", " ")

    fig.update_traces(marker_line_width=0)

    fig.update_layout(
        title=titulo,
        **LAYOUT_BASE,
    )

    if orientacao != "h":
        fig.update_xaxes(tickangle=35)

    fig = _aplicar_estilo_eixos(fig, xaxis_title=x_title, yaxis_title=y_title)

    return fig


def grafico_dispersao(df, x, y, titulo, cor=None):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=cor,
        color_discrete_sequence=PALETA,
        opacity=0.75,
    )

    fig.update_traces(
        marker=dict(
            size=9,
            line=dict(width=0.5, color="#ffffff"),
        )
    )

    fig.update_layout(
        title=titulo,
        **LAYOUT_BASE,
    )

    fig = _aplicar_estilo_eixos(
        fig,
        xaxis_title=x.replace("_", " "),
        yaxis_title=y.replace("_", " "),
    )

    return fig
