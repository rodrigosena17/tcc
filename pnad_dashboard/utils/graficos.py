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
    margin=dict(l=40, r=20, t=60, b=40),
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


def grafico_linha(df, x, ys, titulo, rotulo_y="Valor"):
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
    fig.update_layout(title=titulo, xaxis_title="Periodo", yaxis_title=rotulo_y)
    fig.update_layout(**LAYOUT_BASE)
    fig.update_xaxes(
        gridcolor="#e3ddc4",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
        linecolor="#000000",
    )
    fig.update_yaxes(
        gridcolor="#e3ddc4",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
        linecolor="#000000",
    )
    return fig


def grafico_barras(df, x, y, titulo, cor=None, orientacao="v"):
    fig = px.bar(
        df,
        x=x if orientacao == "v" else y,
        y=y if orientacao == "v" else x,
        color=cor,
        orientation=orientacao,
        color_discrete_sequence=PALETA,
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(title=titulo)
    fig.update_layout(**LAYOUT_BASE)
    fig.update_xaxes(
        gridcolor="#e3ddc4",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
        linecolor="#000000",
    )
    fig.update_yaxes(
        gridcolor="#e3ddc4",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
        linecolor="#000000",
    )
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
    fig.update_traces(marker=dict(size=9, line=dict(width=0.5, color="#ffffff")))
    fig.update_layout(title=titulo)
    fig.update_layout(**LAYOUT_BASE)
    fig.update_xaxes(
        gridcolor="#e3ddc4",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
        linecolor="#000000",
    )
    fig.update_yaxes(
        gridcolor="#e3ddc4",
        zeroline=False,
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
        linecolor="#000000",
    )
    return fig