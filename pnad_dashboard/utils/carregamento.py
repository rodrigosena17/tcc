import os
import pandas as pd
import streamlit as st

DIR_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

MAPA_ESCOLARIDADE = {
    1: "Sem instrucao",
    2: "Fundamental incompleto",
    3: "Fundamental completo",
    4: "Medio incompleto",
    5: "Medio completo",
    6: "Superior incompleto",
    7: "Superior completo",
    8: "Pos-graduacao",
}


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