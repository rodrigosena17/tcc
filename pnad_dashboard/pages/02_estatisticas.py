import streamlit as st
import pandas as pd

from utils.estilo import aplicar_estilo
from utils.carregamento import (
    carregar_estatisticas,
    carregar_escolaridade,
    carregar_horas,
)
from utils.filtros import (
    filtro_anos_trimestres,
    filtro_ano_unico,
    filtro_trimestre_unico,
    seletor_series,
)
from utils.graficos import (
    grafico_linha,
    grafico_barras,
    grafico_dispersao,
)

st.set_page_config(page_title="Estatisticas - PNAD", layout="wide")

aplicar_estilo()

st.title("Estatisticas Interativas")
st.caption("Explore as series temporais e analises por modulo.")

df_est = carregar_estatisticas()
df_esc = carregar_escolaridade()
df_hor = carregar_horas()

modulos = [
    "Panorama Geral",
    "Ocupados",
    "Carteira Assinada",
    "Servidor Publico",
    "Conta Propria",
    "Empregadores",
    "Escolaridade x Renda",
    "Horas Trabalhadas x Renda",
]

modulo = st.sidebar.radio("Modulos", modulos)
st.sidebar.divider()


def formatar_numero(valor):
    try:
        return f"{valor:,.0f}".replace(",", ".")
    except Exception:
        return "-"


def formatar_moeda(valor):
    try:
        return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(
            ".", ","
        ).replace("X", ".")
    except Exception:
        return "-"


# MODULO 1 - PANORAMA GERAL
if modulo == "Panorama Geral":
    st.header("Panorama Geral")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "panorama")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        ano_min = int(df_f["Ano"].min())
        ano_max = int(df_f["Ano"].max())
        st.caption(
            f"Valores correspondem a media dos trimestres filtrados "
            f"({ano_min} a {ano_max})."
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(
            "Populacao Total",
            formatar_numero(df_f["Total_Pessoas"].mean()),
        )
        c2.metric(
            "Populacao Ponderada",
            formatar_numero(df_f["Populacao_Ponderada"].mean()),
        )
        c3.metric(
            "Ocupados",
            formatar_numero(df_f["Ocupados_total"].mean()),
        )
        c4.metric(
            "Ocupados Ponderado",
            formatar_numero(df_f["Ocupados_Ponderado"].mean()),
        )

        c5, c6, c7, c8 = st.columns(4)
        c5.metric(
            "Taxa de Ocupacao",
            f"{df_f['Taxa_Ocupacao'].mean():.1f}%",
        )
        c6.metric(
            "Renda Media",
            formatar_moeda(df_f["Renda_Media"].mean()),
        )
        c7.metric(
            "Renda Mediana",
            formatar_moeda(df_f["Renda_Mediana"].mean()),
        )
        c8.metric(
            "Renda Media Ponderada",
            formatar_moeda(df_f["Renda_Media_Ponderada"].mean()),
        )

        c9, _, _, _ = st.columns(4)
        c9.metric(
            "Horas Medias/Semana",
            f"{df_f['Horas_Media_Semanal'].mean():.1f}",
        )

        st.divider()

        opcoes = [
            "Total_Pessoas",
            "Populacao_Ponderada",
            "Ocupados_total",
            "Ocupados_Ponderado",
            "Taxa_Ocupacao",
            "Renda_Media",
            "Renda_Mediana",
            "Renda_Media_Ponderada",
            "Horas_Media_Semanal",
        ]
        series = seletor_series(opcoes, "panorama", padrao=opcoes[:4])

        fig = grafico_linha(
            df_f, "Periodo", series, "Evolucao das Series Selecionadas"
        )
        st.plotly_chart(fig, use_container_width=True)


# MODULO 2 - OCUPADOS

elif modulo == "Ocupados":
    st.header("Ocupados")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "ocupados")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        ano_min = int(df_f["Ano"].min())
        ano_max = int(df_f["Ano"].max())
        st.caption(
            f"Valores correspondem a media dos trimestres filtrados "
            f"({ano_min} a {ano_max})."
        )

        c1, c2, c3 = st.columns(3)
        c1.metric(
            "Ocupados Total",
            formatar_numero(df_f["Ocupados_total"].mean()),
        )
        c2.metric(
            "Renda Total",
            formatar_moeda(df_f["Ocupados_Renda_Total"].mean()),
        )
        c3.metric(
            "Renda Media",
            formatar_moeda(df_f["Ocupados_Renda_Media"].mean()),
        )

        st.divider()
        opcoes = [
            "Ocupados_total",
            "Ocupados_Renda_Total",
            "Ocupados_Renda_Media",
        ]
        series = seletor_series(opcoes, "ocupados")
        fig = grafico_linha(df_f, "Periodo", series, "Series de Ocupados")
        st.plotly_chart(fig, use_container_width=True)

# MODULO 3 - CARTEIRA ASSINADA

elif modulo == "Carteira Assinada":
    st.header("Carteira Assinada")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "carteira")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        ano_min = int(df_f["Ano"].min())
        ano_max = int(df_f["Ano"].max())
        st.caption(
            f"Valores correspondem a media dos trimestres filtrados "
            f"({ano_min} a {ano_max})."
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(
            "Total",
            formatar_numero(df_f["Carteira_Assinada_Total"].mean()),
        )
        c2.metric(
            "Renda Total",
            formatar_moeda(df_f["Carteira_Assinada_Renda_Total"].mean()),
        )
        c3.metric(
            "Renda Media",
            formatar_moeda(df_f["Carteira_Assinada_Renda_Media"].mean()),
        )
        c4.metric(
            "Percentual",
            f"{df_f['Percentual_Carteira_Assinada'].mean():.1f}%",
        )

        st.divider()
        opcoes = [
            "Carteira_Assinada_Total",
            "Carteira_Assinada_Renda_Total",
            "Carteira_Assinada_Renda_Media",
            "Percentual_Carteira_Assinada",
        ]
        series = seletor_series(opcoes, "carteira")
        fig = grafico_linha(
            df_f, "Periodo", series, "Series de Carteira Assinada"
        )
        st.plotly_chart(fig, use_container_width=True)


# MODULO 4 - SERVIDOR PUBLICO

elif modulo == "Servidor Publico":
    st.header("Servidor Publico")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "servidor")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        ano_min = int(df_f["Ano"].min())
        ano_max = int(df_f["Ano"].max())
        st.caption(
            f"Valores correspondem a media dos trimestres filtrados "
            f"({ano_min} a {ano_max})."
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(
            "Total",
            formatar_numero(df_f["Servidor_Publico_Total"].mean()),
        )
        c2.metric(
            "Renda Total",
            formatar_moeda(df_f["Servidor_Publico_Renda_Total"].mean()),
        )
        c3.metric(
            "Renda Media",
            formatar_moeda(df_f["Servidor_Publico_Renda_Media"].mean()),
        )
        c4.metric(
            "Percentual",
            f"{df_f['Percentual_Servidor_Publico'].mean():.1f}%",
        )

        st.divider()
        opcoes = [
            "Servidor_Publico_Total",
            "Servidor_Publico_Renda_Total",
            "Servidor_Publico_Renda_Media",
            "Percentual_Servidor_Publico",
        ]
        series = seletor_series(opcoes, "servidor")
        fig = grafico_linha(
            df_f, "Periodo", series, "Series de Servidor Publico"
        )
        st.plotly_chart(fig, use_container_width=True)


# MODULO 5 - CONTA PROPRIA

elif modulo == "Conta Propria":
    st.header("Conta Propria")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "contapropria")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        ano_min = int(df_f["Ano"].min())
        ano_max = int(df_f["Ano"].max())
        st.caption(
            f"Valores correspondem a media dos trimestres filtrados "
            f"({ano_min} a {ano_max})."
        )

        c1, c2, c3 = st.columns(3)
        c1.metric(
            "Total",
            formatar_numero(df_f["Conta_Propria_Total"].mean()),
        )
        c2.metric(
            "Renda Total",
            formatar_moeda(df_f["Conta_Propria_Renda_Total"].mean()),
        )
        c3.metric(
            "Renda Media",
            formatar_moeda(df_f["Conta_Propria_Renda_Media"].mean()),
        )

        st.divider()
        opcoes = [
            "Conta_Propria_Total",
            "Conta_Propria_Renda_Total",
            "Conta_Propria_Renda_Media",
        ]
        series = seletor_series(opcoes, "contapropria")
        fig = grafico_linha(df_f, "Periodo", series, "Series de Conta Propria")
        st.plotly_chart(fig, use_container_width=True)


# MODULO 6 - EMPREGADORES

elif modulo == "Empregadores":
    st.header("Empregadores")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "empregadores")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        ano_min = int(df_f["Ano"].min())
        ano_max = int(df_f["Ano"].max())
        st.caption(
            f"Valores correspondem a media dos trimestres filtrados "
            f"({ano_min} a {ano_max})."
        )

        c1, c2, c3 = st.columns(3)
        c1.metric(
            "Total",
            formatar_numero(df_f["Empregador_Total"].mean()),
        )
        c2.metric(
            "Renda Total",
            formatar_moeda(df_f["Empregador_Renda_Total"].mean()),
        )
        c3.metric(
            "Renda Media",
            formatar_moeda(df_f["Empregador_Renda_Media"].mean()),
        )

        st.divider()
        opcoes = [
            "Empregador_Total",
            "Empregador_Renda_Total",
            "Empregador_Renda_Media",
        ]
        series = seletor_series(opcoes, "empregadores")
        fig = grafico_linha(df_f, "Periodo", series, "Series de Empregadores")
        st.plotly_chart(fig, use_container_width=True)


# MODULO 7 - ESCOLARIDADE x RENDA

elif modulo == "Escolaridade x Renda":
    st.header("Escolaridade x Renda")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        ano = filtro_ano_unico(df_esc, "esc")
        multi = st.checkbox(
            "Comparar varios trimestres", value=False, key="esc_multi"
        )

        tris_disp = sorted(df_esc[df_esc["Ano"] == ano]["Trimestre"].unique())

        if multi:
            tris_sel = st.multiselect(
                "Trimestres",
                options=tris_disp,
                default=tris_disp,
                key="esc_tris",
            )
            if not tris_sel:
                tris_sel = tris_disp
        else:
            tri = filtro_trimestre_unico(df_esc, ano, "esc")
            tris_sel = [tri]

    df_f = df_esc[
        (df_esc["Ano"] == ano) & (df_esc["Trimestre"].isin(tris_sel))
    ].copy()

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        if multi and len(tris_sel) > 1:
            fig_v = grafico_barras(
                df_f,
                x="Escolaridade_Desc",
                y="Renda_Total",
                titulo="Renda Total por Escolaridade (comparacao)",
                cor="Trimestre",
            )
            st.plotly_chart(fig_v, use_container_width=True)
        else:
            agg = (
                df_f.groupby("Escolaridade_Desc")["Renda_Total"]
                .sum()
                .reset_index()
            )

            fig_v = grafico_barras(
                agg,
                x="Escolaridade_Desc",
                y="Renda_Total",
                titulo="Renda Total por Escolaridade",
            )
            st.plotly_chart(fig_v, use_container_width=True)

            agg_ord = agg.sort_values("Renda_Total", ascending=True)
            fig_h = grafico_barras(
                agg_ord,
                x="Escolaridade_Desc",
                y="Renda_Total",
                titulo="Renda Total por Escolaridade (ordenado)",
                orientacao="h",
            )
            st.plotly_chart(fig_h, use_container_width=True)


# MODULO 8 - HORAS TRABALHADAS x RENDA

elif modulo == "Horas Trabalhadas x Renda":
    st.header("Horas Trabalhadas x Renda")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        ano = filtro_ano_unico(df_hor, "hor")
        tri = filtro_trimestre_unico(df_hor, ano, "hor")

        h_min = int(df_hor["Horas_Semanais"].min())
        h_max = int(df_hor["Horas_Semanais"].max())
        faixa = st.slider(
            "Faixa de horas semanais",
            min_value=h_min,
            max_value=h_max,
            value=(h_min, h_max),
            key="hor_slider",
        )

    df_f = df_hor[
        (df_hor["Ano"] == ano)
        & (df_hor["Trimestre"] == tri)
        & (df_hor["Horas_Semanais"] >= faixa[0])
        & (df_hor["Horas_Semanais"] <= faixa[1])
    ].copy()

    df_f = df_f.sort_values("Horas_Semanais")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        st.subheader("Dispersao")
        fig_disp = grafico_dispersao(
            df_f,
            x="Horas_Semanais",
            y="Renda_Total",
            titulo="Renda Total por Horas Semanais",
        )
        st.plotly_chart(fig_disp, use_container_width=True)

        col_a, col_b = st.columns(2)

        with col_a:
            fig_linha = grafico_linha(
                df_f,
                "Horas_Semanais",
                ["Renda_Total"],
                "Renda Total (linha)",
                rotulo_y="Renda Total",
            )
            fig_linha.update_layout(xaxis_title="Horas Semanais")
            st.plotly_chart(fig_linha, use_container_width=True)

        with col_b:
            fig_barra = grafico_barras(
                df_f,
                x="Horas_Semanais",
                y="Renda_Total",
                titulo="Renda Total (barras)",
            )
            st.plotly_chart(fig_barra, use_container_width=True)