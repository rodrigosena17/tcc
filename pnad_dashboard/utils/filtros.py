import streamlit as st


def filtro_anos_trimestres(df, chave):
    anos = sorted(df["Ano"].unique())
    trimestres = sorted(df["Trimestre"].unique())

    col1, col2 = st.columns(2)

    with col1:
        intervalo = st.select_slider(
            "Intervalo de anos",
            options=anos,
            value=(anos[0], anos[-1]),
            key=f"anos_{chave}",
        )

    with col2:
        tris = st.multiselect(
            "Trimestres",
            options=trimestres,
            default=trimestres,
            key=f"tri_{chave}",
        )

    if not tris:
        tris = trimestres

    ano_min, ano_max = intervalo
    filtrado = df[
        (df["Ano"] >= ano_min)
        & (df["Ano"] <= ano_max)
        & (df["Trimestre"].isin(tris))
    ].copy()

    return filtrado


def filtro_ano_unico(df, chave):
    anos = sorted(df["Ano"].unique())
    ano = st.selectbox("Ano", options=anos, index=0, key=f"ano_un_{chave}")
    return ano


def filtro_trimestre_unico(df, ano, chave):
    tris = sorted(df[df["Ano"] == ano]["Trimestre"].unique())
    tri = st.selectbox(
        "Trimestre", options=tris, index=0, key=f"tri_un_{chave}"
    )
    return tri


def seletor_series(opcoes, chave, padrao=None):
    if padrao is None:
        padrao = opcoes
    selecionadas = st.multiselect(
        "Series temporais",
        options=opcoes,
        default=padrao,
        key=f"series_{chave}",
    )
    return selecionadas if selecionadas else opcoes