import os
import pandas as pd
import streamlit as st

DIR_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

MAPA_ESCOLARIDADE = {
        1: "Creche",
        2: "Pré-escola",
        3: "Classe de alfabetização (CA)",
        4: "Alfabetização de jovens e adultos",
        5: "Antigo primário (elementar)",
        6: "Antigo ginásio (médio 1º ciclo)",
        7: "Ensino fundamental regular",
        8: "EJA ou supletivo do 1º grau",
        9: "Antigo científico, clássico etc. (médio 2º ciclo)",
        10: "Ensino médio regular",
        11: "EJA ou supletivo do 2º grau",
        12: "Superior - graduação",
        13: "Especialização",
        14: "Mestrado",
        15: "Doutorado",
    }


def carregar_estatisticas():
    caminho = os.path.join(DIR_DADOS, "estatisticas_empilhadas.csv")
    df = pd.read_csv(caminho)
    return _criar_periodo(df)


@st.cache_data
def carregar_escolaridade_ocupacao():
    caminho = os.path.join(
        DIR_DADOS,
        "escolaridade_ocupacao_empilhada.csv"
    )

    df = pd.read_csv(caminho)
    df = _criar_periodo(df)

    df["Escolaridade_Desc"] = (
        df["Escolaridade"]
        .map(MAPA_ESCOLARIDADE)
        .fillna(df["Escolaridade"].astype(str))
    )

    return df

@st.cache_data
def carregar_sexo_renda_escolaridade():
    caminho = os.path.join(
        DIR_DADOS,
        "sexo_renda_escolaridade_empilhada.csv"
    )

    df = pd.read_csv(caminho)
    df = _criar_periodo(df)

    mapa_sexo = {
        1: "Homem",
        2: "Mulher"
    }

    df["Sexo_Desc"] = (
        df["Sexo"]
        .map(mapa_sexo)
        .fillna(df["Sexo"].astype(str))
    )

    df["Escolaridade_Desc"] = (
        df["Escolaridade"]
        .map(MAPA_ESCOLARIDADE)
        .fillna(df["Escolaridade"].astype(str))
    )

    return df

@st.cache_data
def carregar_idade_renda():
    caminho = os.path.join(
        DIR_DADOS,
        "idade_renda_empilhada.csv"
    )

    df = pd.read_csv(caminho)
    df = _criar_periodo(df)

    return df

@st.cache_data
def carregar_tempo_trabalho_renda():
    caminho = os.path.join(
        DIR_DADOS,
        "tempo_trabalho_renda_empilhada.csv"
    )

    df = pd.read_csv(caminho)
    df = _criar_periodo(df)

    return df

@st.cache_data
def carregar_escolaridade_carteira():
    caminho = os.path.join(
        DIR_DADOS,
        "escolaridade_carteira_empilhada.csv"
    )

    df = pd.read_csv(caminho)
    df = _criar_periodo(df)

    df["Escolaridade_Desc"] = (
        df["Escolaridade"]
        .map(MAPA_ESCOLARIDADE)
        .fillna(df["Escolaridade"].astype(str))
    )

    return df

@st.cache_data
def carregar_cor_raca_renda_escolaridade():
    caminho = os.path.join(
        DIR_DADOS,
        "cor_raca_renda_escolaridade_empilhada.csv"
    )

    df = pd.read_csv(caminho)
    df = _criar_periodo(df)

    mapa_raca = {
        1: "Branca",
        2: "Preta",
        3: "Amarela",
        4: "Parda",
        5: "Indigena",
        9: "Ignorado"
    }

    df["Cor_Raca_Desc"] = (
        df["Cor_Raca"]
        .map(mapa_raca)
        .fillna(df["Cor_Raca"].astype(str))
    )

    df["Escolaridade_Desc"] = (
        df["Escolaridade"]
        .map(MAPA_ESCOLARIDADE)
        .fillna(df["Escolaridade"].astype(str))
    )

    return df


@st.cache_data
def carregar_estatisticas():
    caminho = os.path.join(DIR_DADOS, "estatisticas_empilhadas.csv")
    df = pd.read_csv(caminho)
    df = _criar_periodo(df)
    return df


@st.cache_data
def carregar_escolaridade():
    caminho = os.path.join(DIR_DADOS, "renda_escolaridade_empilhada.csv")
    df = pd.read_csv(caminho)
    df = _criar_periodo(df)
    df["Escolaridade_Desc"] = df["Escolaridade"].map(MAPA_ESCOLARIDADE)
    df["Escolaridade_Desc"] = df["Escolaridade_Desc"].fillna(
        df["Escolaridade"].astype(str)
    )
    return df


@st.cache_data
def carregar_horas():
    caminho = os.path.join(DIR_DADOS, "renda_horas_semanais_empilhada.csv")
    df = pd.read_csv(caminho)
    df = _criar_periodo(df)
    return df


def _criar_periodo(df):
    df = df.copy()
    df["Ano"] = df["Ano"].astype(int)
    df["Trimestre"] = df["Trimestre"].astype(int)
    df["Periodo"] = df["Ano"].astype(str) + " T" + df["Trimestre"].astype(str)
    df = df.sort_values(["Ano", "Trimestre"]).reset_index(drop=True)
    return df