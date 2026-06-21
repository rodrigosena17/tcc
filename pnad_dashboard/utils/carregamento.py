import os
import pandas as pd
import streamlit as st

DIR_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def _criar_periodo(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Ano" in df.columns:
        df["Ano"] = pd.to_numeric(df["Ano"], errors="coerce").astype("Int64")
    if "Trimestre" in df.columns:
        df["Trimestre"] = pd.to_numeric(df["Trimestre"], errors="coerce").astype("Int64")

    df = df[df["Ano"].notna() & df["Trimestre"].notna()].copy()
    df["Ano"] = df["Ano"].astype(int)
    df["Trimestre"] = df["Trimestre"].astype(int)
    df["Periodo"] = df["Ano"].astype(str) + "T" + df["Trimestre"].astype(str)

    return df.sort_values(["Ano", "Trimestre"])


def _ler_empilhado_por_padrao(padrao: str) -> pd.DataFrame:
    arquivos = sorted(PASTA_DADOS.glob(padrao))

    if not arquivos:
        return pd.DataFrame()

    dfs = []
    for arq in arquivos:
        try:
            df = pd.read_csv(arq)
            df.columns = df.columns.str.strip()
            dfs.append(df)
        except Exception as e:
            st.warning(f"Erro ao ler {arq.name}: {e}")

    if not dfs:
        return pd.DataFrame()

    df_final = pd.concat(dfs, ignore_index=True)
    df_final = _criar_periodo(df_final)

    return df_final


def _to_numeric_cols(df: pd.DataFrame, exceto=None) -> pd.DataFrame:
    df = df.copy()
    exceto = exceto or []
    for col in df.columns:
        if col not in exceto:
            df[col] = pd.to_numeric(df[col], errors="ignore")
    return df


@st.cache_data
def carregar_estatisticas():
    df = _ler_empilhado_por_padrao("*_estatisticas.csv")
    return _to_numeric_cols(df)


@st.cache_data
def carregar_escolaridade():
    df = _ler_empilhado_por_padrao("*_renda_escolaridade.csv")
    df = _to_numeric_cols(df, exceto=["Escolaridade_Desc"])
    df = adicionar_escolaridade_desc(df)
    return df


@st.cache_data
def carregar_horas():
    df = _ler_empilhado_por_padrao("*_renda_horas_semanais.csv")
    return _to_numeric_cols(df)


@st.cache_data
def carregar_idade_renda():
    df = _ler_empilhado_por_padrao("*_idade_renda.csv")
    return _to_numeric_cols(df)


@st.cache_data
def carregar_tempo_trabalho_renda():
    df = _ler_empilhado_por_padrao("*_tempo_trabalho_renda.csv")
    return _to_numeric_cols(df)


@st.cache_data
def carregar_escolaridade_ocupacao():
    df = _ler_empilhado_por_padrao("*_escolaridade_ocupacao.csv")
    df = _to_numeric_cols(df, exceto=["Escolaridade_Desc"])
    df = adicionar_escolaridade_desc(df)
    return df


@st.cache_data
def carregar_escolaridade_carteira():
    df = _ler_empilhado_por_padrao("*_escolaridade_carteira.csv")
    df = _to_numeric_cols(df, exceto=["Escolaridade_Desc"])
    df = adicionar_escolaridade_desc(df)
    return df


@st.cache_data
def carregar_sexo_renda_escolaridade():
    df = _ler_empilhado_por_padrao("*_sexo_renda_escolaridade.csv")
    df = _to_numeric_cols(df, exceto=["Sexo_Desc", "Escolaridade_Desc"])
    df = adicionar_escolaridade_desc(df)
    df = adicionar_sexo_desc(df)
    return df


@st.cache_data
def carregar_cor_raca_renda_escolaridade():
    df = _ler_empilhado_por_padrao("*_cor_raca_renda_escolaridade.csv")
    df = _to_numeric_cols(df, exceto=["Cor_Raca_Desc", "Escolaridade_Desc"])
    df = adicionar_escolaridade_desc(df)
    df = adicionar_cor_raca_desc(df)
    return df


def adicionar_escolaridade_desc(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "Escolaridade_Desc" in df.columns:
        return df

    mapa = {
        1: "Sem instrução e menos de 1 ano",
        2: "Fundamental incompleto",
        3: "Fundamental completo",
        4: "Médio incompleto",
        5: "Médio completo",
        6: "Superior incompleto",
        7: "Superior completo",
        8: "Pós-graduação",
    }

    if "Escolaridade" in df.columns:
        df["Escolaridade_Num"] = pd.to_numeric(df["Escolaridade"], errors="coerce")
        df["Escolaridade_Desc"] = df["Escolaridade_Num"].map(mapa).fillna(
            df["Escolaridade"].astype(str)
        )

    return df


def adicionar_sexo_desc(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    mapa = {
        1: "Homem",
        2: "Mulher",
    }

    if "Sexo" in df.columns:
        df["Sexo_Num"] = pd.to_numeric(df["Sexo"], errors="coerce")
        df["Sexo_Desc"] = df["Sexo_Num"].map(mapa).fillna(df["Sexo"].astype(str))

    return df


def adicionar_cor_raca_desc(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    mapa = {
        1: "Branca",
        2: "Preta",
        3: "Amarela",
        4: "Parda",
        5: "Indígena",
        9: "Ignorado",
    }

    if "Cor_Raca" in df.columns:
        df["Cor_Raca_Num"] = pd.to_numeric(df["Cor_Raca"], errors="coerce")
        df["Cor_Raca_Desc"] = df["Cor_Raca_Num"].map(mapa).fillna(
            df["Cor_Raca"].astype(str)
        )

    return df
