import streamlit as st
import pandas as pd
import plotly.express as px

from utils.estilo import aplicar_estilo
from utils.carregamento import (
    carregar_estatisticas,
    carregar_escolaridade,
    carregar_horas,
    carregar_idade_renda,
    carregar_tempo_trabalho_renda,
    carregar_escolaridade_ocupacao,
    carregar_escolaridade_carteira,
    carregar_sexo_renda_escolaridade,
    carregar_cor_raca_renda_escolaridade,
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
)

st.set_page_config(page_title="Estatisticas - PNAD", layout="wide")

aplicar_estilo()

st.title("Estatisticas PNAD Contínua")
st.caption(
    "🛈 Nessa seção é possível explorar as estatísticas trimestrais da PNAD Contínua "
    "de forma interativa, aplicando filtros e visualizando gráficos personalizados."
)

df_est = carregar_estatisticas()
df_esc = carregar_escolaridade()
df_hor = carregar_horas()

df_idade = carregar_idade_renda()
df_tempo = carregar_tempo_trabalho_renda()
df_esc_ocup = carregar_escolaridade_ocupacao()
df_esc_cart = carregar_escolaridade_carteira()
df_sexo_esc = carregar_sexo_renda_escolaridade()
df_raca_esc = carregar_cor_raca_renda_escolaridade()

modulos = [
    "Panorama Geral",
    "Ocupados",
    "Carteira Assinada",
    "Servidor Publico",
    "Conta Propria",
    "Empregadores",
    "Escolaridade x Renda",
    "Horas Trabalhadas x Renda",
    "Idade x Renda",
    "Tempo de Trabalho x Renda",
    "Escolaridade x Ocupacao",
    "Escolaridade x Carteira Assinada",
    "Sexo x Renda x Escolaridade",
    "Cor/Raca x Escolaridade x Renda",
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


def filtrar_ano_tri(df, prefixo):
    with st.sidebar:
        ano = filtro_ano_unico(df, prefixo)
        multi = st.checkbox(
            "Comparar vários trimestres",
            value=False,
            key=f"{prefixo}_multi",
        )

        tris_disp = sorted(df[df["Ano"] == ano]["Trimestre"].unique())

        if multi:
            tris_sel = st.multiselect(
                "Trimestres",
                options=tris_disp,
                default=tris_disp,
                key=f"{prefixo}_tris",
            )
            if not tris_sel:
                tris_sel = tris_disp
        else:
            tri = filtro_trimestre_unico(df, ano, prefixo)
            tris_sel = [tri]

    return ano, tris_sel



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
            f"Valores correspondem à média dos trimestres filtrados "
            f"({ano_min} a {ano_max})."
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Populacao Total", formatar_numero(df_f["Total_Pessoas"].mean()))
        c2.metric("Populacao Ponderada", formatar_numero(df_f["Populacao_Ponderada"].mean()))
        c3.metric("Ocupados", formatar_numero(df_f["Ocupados_total"].mean()))
        c4.metric("Ocupados Ponderado", formatar_numero(df_f["Ocupados_Ponderado"].mean()))

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Taxa de Ocupacao", f"{df_f['Taxa_Ocupacao'].mean():.1f}%")
        c6.metric("Renda Media", formatar_moeda(df_f["Renda_Media"].mean()))
        c7.metric("Renda Mediana", formatar_moeda(df_f["Renda_Mediana"].mean()))
        c8.metric("Renda Media Ponderada", formatar_moeda(df_f["Renda_Media_Ponderada"].mean()))

        c9, c10, c11, c12 = st.columns(4)
        c9.metric("Carteira Assinada Ponderada", formatar_numero(df_f["Carteira_Assinada_Ponderado"].mean()))
        c10.metric("Servidor Publico Ponderado", formatar_numero(df_f["Servidor_Publico_Ponderado"].mean()))
        c11.metric("Conta Propria Ponderado", formatar_numero(df_f["Conta_Propria_Ponderado"].mean()))
        c12.metric("Empregadores Ponderado", formatar_numero(df_f["Empregador_Ponderado"].mean()))

        c13, _, _, _ = st.columns(4)
        c13.metric("Horas Medias/Semana", f"{df_f['Horas_Media_Semanal'].mean():.1f}")

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
        series = seletor_series(opcoes, "panorama", padrao="_empilhada")

        fig = grafico_linha(df_f, "Periodo", series, "Evolucao das Series Selecionadas")
        st.plotly_chart(fig, width='stretch')


elif modulo == "Ocupados":
    st.header("Ocupados")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "ocupados")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ocupados Total", formatar_numero(df_f["Ocupados_total"].mean()))
        c2.metric("Renda Total", formatar_moeda(df_f["Ocupados_Renda_Total"].mean()))
        c3.metric("Renda Media", formatar_moeda(df_f["Ocupados_Renda_Media"].mean()))
        c4.metric("Ocupados Ponderado", formatar_numero(df_f["Ocupados_Ponderado"].mean()))

        st.divider()

        opcoes = [
            "Ocupados_total",
            "Ocupados_Renda_Total",
            "Ocupados_Renda_Media",
            "Ocupados_Ponderado",
        ]
        series = seletor_series(opcoes, "ocupados")
        fig = grafico_linha(df_f, "Periodo", series, "Series de Ocupados")
        st.plotly_chart(fig, width='stretch')


elif modulo == "Carteira Assinada":
    st.header("Carteira Assinada")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "carteira")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total", formatar_numero(df_f["Carteira_Assinada_Total"].mean()))
        c2.metric("Renda Total", formatar_moeda(df_f["Carteira_Assinada_Renda_Total"].mean()))
        c3.metric("Renda Media", formatar_moeda(df_f["Carteira_Assinada_Renda_Media"].mean()))
        c4.metric("Percentual", f"{df_f['Percentual_Carteira_Assinada'].mean():.1f}%")
        c5.metric("Ponderado", formatar_numero(df_f["Carteira_Assinada_Ponderado"].mean()))

        st.divider()

        opcoes = [
            "Carteira_Assinada_Total",
            "Carteira_Assinada_Renda_Total",
            "Carteira_Assinada_Renda_Media",
            "Percentual_Carteira_Assinada",
            "Carteira_Assinada_Ponderado",
        ]
        series = seletor_series(opcoes, "carteira")
        fig = grafico_linha(df_f, "Periodo", series, "Series de Carteira Assinada")
        st.plotly_chart(fig, width='stretch')


elif modulo == "Servidor Publico":
    st.header("Servidor Publico")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "servidor")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total", formatar_numero(df_f["Servidor_Publico_Total"].mean()))
        c2.metric("Renda Total", formatar_moeda(df_f["Servidor_Publico_Renda_Total"].mean()))
        c3.metric("Renda Media", formatar_moeda(df_f["Servidor_Publico_Renda_Media"].mean()))
        c4.metric("Percentual", f"{df_f['Percentual_Servidor_Publico'].mean():.1f}%")
        c5.metric("Ponderado", formatar_numero(df_f["Servidor_Publico_Ponderado"].mean()))

        st.divider()

        opcoes = [
            "Servidor_Publico_Total",
            "Servidor_Publico_Renda_Total",
            "Servidor_Publico_Renda_Media",
            "Percentual_Servidor_Publico",
            "Servidor_Publico_Ponderado",
        ]
        series = seletor_series(opcoes, "servidor")
        fig = grafico_linha(df_f, "Periodo", series, "Series de Servidor Publico")
        st.plotly_chart(fig, width='stretch')


elif modulo == "Conta Propria":
    st.header("Conta Propria")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "contapropria")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total", formatar_numero(df_f["Conta_Propria_Total"].mean()))
        c2.metric("Renda Total", formatar_moeda(df_f["Conta_Propria_Renda_Total"].mean()))
        c3.metric("Renda Media", formatar_moeda(df_f["Conta_Propria_Renda_Media"].mean()))
        c4.metric("Percentual", f"{df_f['Percentual_Conta_Propria'].mean():.1f}%")
        c5.metric("Ponderado", formatar_numero(df_f["Conta_Propria_Ponderado"].mean()))

        st.divider()

        opcoes = [
            "Conta_Propria_Total",
            "Conta_Propria_Renda_Total",
            "Conta_Propria_Renda_Media",
            "Percentual_Conta_Propria",
            "Conta_Propria_Ponderado",
        ]
        series = seletor_series(opcoes, "contapropria")
        fig = grafico_linha(df_f, "Periodo", series, "Series de Conta Propria")
        st.plotly_chart(fig, width='stretch')


elif modulo == "Empregadores":
    st.header("Empregadores")
    st.sidebar.subheader("Filtros")

    with st.sidebar:
        df_f = filtro_anos_trimestres(df_est, "empregadores")

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total", formatar_numero(df_f["Empregador_Total"].mean()))
        c2.metric("Renda Total", formatar_moeda(df_f["Empregador_Renda_Total"].mean()))
        c3.metric("Renda Media", formatar_moeda(df_f["Empregador_Renda_Media"].mean()))
        c4.metric("Percentual", f"{df_f['Percentual_Empregador'].mean():.1f}%")
        c5.metric("Ponderado", formatar_numero(df_f["Empregador_Ponderado"].mean()))

        st.divider()

        opcoes = [
            "Empregador_Total",
            "Empregador_Renda_Total",
            "Empregador_Renda_Media",
            "Percentual_Empregador",
            "Empregador_Ponderado",
        ]
        series = seletor_series(opcoes, "empregadores")
        fig = grafico_linha(df_f, "Periodo", series, "Series de Empregadores")
        st.plotly_chart(fig, width='stretch')



elif modulo == "Escolaridade x Renda":
    st.header("Escolaridade x Renda")
    st.sidebar.subheader("Filtros")

    ano, tris_sel = filtrar_ano_tri(df_esc, "esc")

    df_f = df_esc[
        (df_esc["Ano"] == ano) & (df_esc["Trimestre"].isin(tris_sel))
    ].copy()

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        if len(tris_sel) > 1:
            fig_v = grafico_barras(
                df_f,
                x="Escolaridade_Desc",
                y="Renda_Total",
                titulo="Renda Total (R$) por Escolaridade",
                cor="Trimestre",
            )
            st.plotly_chart(fig_v, width='stretch')
        else:
            agg = (
                df_f.groupby("Escolaridade_Desc")["Renda_Total"]
                .sum()
                .reset_index()
            )

            agg_ord = agg.sort_values("Renda_Total", ascending=True)
            fig_h = grafico_barras(
                agg_ord,
                x="Escolaridade_Desc",
                y="Renda_Total",
                titulo="Renda Total (R$) por Escolaridade",
                orientacao="h",
            )
            st.plotly_chart(fig_h, width='stretch')


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
        fig_linha = grafico_linha(
                df_f,
                "Horas_Semanais",
                ["Renda_Total"],
                "Renda Total (R$)",
                rotulo_y="Renda Total",
            )
        fig_linha.update_layout(xaxis_title="Horas Semanais")
        st.plotly_chart(fig_linha, width='stretch')


elif modulo == "Idade x Renda":
    st.header("Idade x Renda")
    st.sidebar.subheader("Filtros")

    ano, tris_sel = filtrar_ano_tri(df_idade, "idade")

    df_f = df_idade[
        (df_idade["Ano"] == ano) & (df_idade["Trimestre"].isin(tris_sel))
    ].copy()

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        df_f = df_f.sort_values("Idade")

        idade_min = int(df_f["Idade"].min())
        idade_max = int(df_f["Idade"].max())

        faixa = st.slider(
            "Faixa de idade",
            min_value=idade_min,
            max_value=idade_max,
            value=(idade_min, idade_max),
            key="idade_slider",
        )

        df_f = df_f[
            (df_f["Idade"] >= faixa[0]) & (df_f["Idade"] <= faixa[1])
        ].copy()

        if len(tris_sel) > 1:
            fig = px.line(
                df_f,
                x="Idade",
                y="Renda_Media",
                color="Trimestre",
                markers=True
            )
        else:
            fig = grafico_linha(
                df_f.sort_values("Idade"),
                "Idade",
                ["Renda_Media"],
                "Renda Média (R$) por Idade",
                rotulo_y="Renda Média Mensal",
            )

        st.plotly_chart(fig, width='stretch')
        fig.update_layout(xaxis_title="Idade")




elif modulo == "Tempo de Trabalho x Renda":
    st.header("Tempo de Trabalho x Renda (R$)")
    st.sidebar.subheader("Filtros")

    ano, tris_sel = filtrar_ano_tri(df_tempo, "tempo")

    df_f = df_tempo[
        (df_tempo["Ano"] == ano) & (df_tempo["Trimestre"].isin(tris_sel))
    ].copy()

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        if len(tris_sel) > 1:
            fig = grafico_barras(
                df_f,
                x="Tempo_Trabalho_Desc",
                y="Renda_Media",
                titulo="Renda Média (R$) por Tempo de Trabalho",
                cor="Trimestre",
            )
        else:
            fig = grafico_barras(
                df_f,
                x="Tempo_Trabalho_Desc",
                y="Renda_Media",
                titulo="Renda Média (R$) por Tempo de Trabalho",
            )
        fig.update_layout(xaxis_title="Tempo de Trabalho")
        st.plotly_chart(fig, width='stretch')


elif modulo == "Escolaridade x Ocupacao":
    st.header("Escolaridade x Ocupacao")
    st.sidebar.subheader("Filtros")

    ano, tris_sel = filtrar_ano_tri(df_esc_ocup, "escocup")

    df_f = df_esc_ocup[
        (df_esc_ocup["Ano"] == ano)
        & (df_esc_ocup["Trimestre"].isin(tris_sel))
    ].copy()

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        if len(tris_sel) > 1:
            fig_h = grafico_barras(
                df_f,
                x="Escolaridade_Desc",
                y="Percentual_Ocupados",
                titulo="Percentual de Ocupados por Escolaridade",
                cor="Trimestre",
            )
        else:
            agg = (
                df_f.groupby("Escolaridade_Desc")["Percentual_Ocupados"]
                .mean()
                .reset_index()
            )

            fig_h = grafico_barras(
                agg.sort_values("Percentual_Ocupados"),
                x="Escolaridade_Desc",
                y="Percentual_Ocupados",
                titulo="Percentual de Ocupados por Escolaridade",
                orientacao="h",
            )

        st.plotly_chart(fig_h, width='stretch')


elif modulo == "Escolaridade x Carteira Assinada":
    st.header("Escolaridade x Carteira Assinada")
    st.sidebar.subheader("Filtros")

    ano, tris_sel = filtrar_ano_tri(df_esc_cart, "esccart")

    df_f = df_esc_cart[
        (df_esc_cart["Ano"] == ano)
        & (df_esc_cart["Trimestre"].isin(tris_sel))
    ].copy()

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        if len(tris_sel) > 1:
            fig = grafico_barras(
                df_f,
                x="Escolaridade_Desc",
                y="Percentual_Carteira",
                titulo="Percentual com Carteira Assinada por Escolaridade",
                cor="Trimestre",
            )
        else:
            agg = (
                df_f.groupby("Escolaridade_Desc")["Percentual_Carteira"]
                .mean()
                .reset_index()
            )

            fig = grafico_barras(
                agg,
                x="Escolaridade_Desc",
                y="Percentual_Carteira",
                titulo="Percentual com Carteira Assinada por Escolaridade",
            )

        st.plotly_chart(fig, width='stretch')



elif modulo == "Sexo x Renda x Escolaridade":
    st.header("Sexo x Renda x Escolaridade")
    st.sidebar.subheader("Filtros")

    ano, tris_sel = filtrar_ano_tri(df_sexo_esc, "sexoesc")

    sexos = sorted(df_sexo_esc["Sexo_Desc"].dropna().unique().tolist())
    with st.sidebar:
        sexo_sel = st.multiselect(
            "Sexo",
            options=sexos,
            default=sexos,
            key="sexoesc_sexo",
        )

    df_f = df_sexo_esc[
        (df_sexo_esc["Ano"] == ano)
        & (df_sexo_esc["Trimestre"].isin(tris_sel))
        & (df_sexo_esc["Sexo_Desc"].isin(sexo_sel))
    ].copy()

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        if len(tris_sel) > 1:
            df_f["Serie"] = (
                df_f["Sexo_Desc"]
                + " - T"
                + df_f["Trimestre"].astype(str)
            )

            fig = grafico_barras(
                df_f,
                x="Escolaridade_Desc",
                y="Renda_Media",
                titulo="Renda Média (R$) por Sexo e Escolaridade",
                cor="Serie",
            )
        else:
            agg = (
                df_f.groupby(["Escolaridade_Desc", "Sexo_Desc"])["Renda_Media"]
                .mean()
                .reset_index()
            )

            fig = grafico_barras(
                agg,
                x="Escolaridade_Desc",
                y="Renda_Media",
                titulo="Renda Média (R$) por Sexo e Escolaridade",
                cor="Sexo_Desc",
            )

        st.plotly_chart(fig, width='stretch')


elif modulo == "Cor/Raca x Escolaridade x Renda":
    st.header("Cor/Raca x Escolaridade x Renda")
    st.sidebar.subheader("Filtros")

    ano, tris_sel = filtrar_ano_tri(df_raca_esc, "racaesc")

    racas = sorted(df_raca_esc["Cor_Raca_Desc"].dropna().unique().tolist())
    with st.sidebar:
        raca_sel = st.multiselect(
            "Cor/Raça",
            options=racas,
            default=racas,
            key="racaesc_raca",
        )

    df_f = df_raca_esc[
        (df_raca_esc["Ano"] == ano)
        & (df_raca_esc["Trimestre"].isin(tris_sel))
        & (df_raca_esc["Cor_Raca_Desc"].isin(raca_sel))
    ].copy()

    if df_f.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
    else:
        if len(tris_sel) > 1:
            df_f["Serie"] = (
                df_f["Cor_Raca_Desc"]
                + " - T"
                + df_f["Trimestre"].astype(str)
            )

            fig_h = grafico_barras(
                df_f,
                x="Escolaridade_Desc",
                y="Renda_Media",
                titulo="Renda Média (R$) por Cor/Raça e Escolaridade",
                cor="Serie",
            )
        else:
            agg = (
                df_f.groupby(
                    ["Escolaridade_Desc", "Cor_Raca_Desc"]
                )["Renda_Media"]
                .mean()
                .reset_index()
            )

            fig_h = grafico_barras(
                agg.sort_values("Renda_Media"),
                x="Escolaridade_Desc",
                y="Renda_Media",
                titulo="Renda Média (R$) por Cor/Raça e Escolaridade",
                cor="Cor_Raca_Desc",
                orientacao="h",
            )

        st.plotly_chart(fig_h, width='stretch')
