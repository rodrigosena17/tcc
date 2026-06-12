import os
import pandas as pd
from typing import Dict, Any


def calcular_media_ponderada(valores, pesos):
    dados = pd.DataFrame({
        "valor": valores,
        "peso": pesos
    }).dropna()

    if dados.empty:
        return None

    return (dados["valor"] * dados["peso"]).sum() / dados["peso"].sum()


def calcular_estatisticas(base_dir_organizados_csv: str,
                          pasta_resultados: str) -> Dict[str, Any]:

    os.makedirs(pasta_resultados, exist_ok=True)

    resultados = []

    arquivos = []

    for root, _, files in os.walk(base_dir_organizados_csv):
        for file in files:
            if file.endswith("_organizado.csv"):
                arquivos.append(os.path.join(root, file))

    for caminho in sorted(arquivos):

        try:
            df = pd.read_csv(caminho)
        except Exception as e:
            print(f"Erro ao ler {caminho}: {e}")
            continue

        colunas_numericas = [
            "Ano",
            "Trimestre",
            "V1028",
            "V2009",
            "V3009A",
            "V4001",
            "V4028",
            "V4029",
            "V403312",
            "V4039"
        ]

        for col in colunas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        ano = int(df["Ano"].iloc[0])
        trimestre = int(df["Trimestre"].iloc[0])

        total_pessoas = len(df)

        populacao_ponderada = (
            df["V1028"].sum()
            if "V1028" in df.columns
            else None
        )

        ocupados = (
            (df["V4001"] == 1).sum()
            if "V4001" in df.columns
            else None
        )

        taxa_ocupacao = (
            (ocupados / total_pessoas) * 100
            if total_pessoas > 0
            else None
        )

        renda_media = (
            df["V403312"].mean()
            if "V403312" in df.columns
            else None
        )

        renda_mediana = (
            df["V403312"].median()
            if "V403312" in df.columns
            else None
        )

        renda_media_ponderada = calcular_media_ponderada(
            df["V403312"],
            df["V1028"]
        )

        percentual_carteira = (
            (df["V4029"] == 1).mean() * 100
            if "V4029" in df.columns
            else None
        )

        percentual_servidor = (
            (df["V4028"] == 1).mean() * 100
            if "V4028" in df.columns
            else None
        )

        horas_media = (
            df["V4039"].mean()
            if "V4039" in df.columns
            else None
        )

        resultados.append({
            "Ano": ano,
            "Trimestre": trimestre,
            "Total_Pessoas": total_pessoas,
            "Populacao_Ponderada": populacao_ponderada,
            "Ocupados": ocupados,
            "Taxa_Ocupacao": taxa_ocupacao,
            "Renda_Media": renda_media,
            "Renda_Mediana": renda_mediana,
            "Renda_Media_Ponderada": renda_media_ponderada,
            "Percentual_Carteira_Assinada": percentual_carteira,
            "Percentual_Servidor_Publico": percentual_servidor,
            "Horas_Media_Semanal": horas_media
        })

    resultados_df = pd.DataFrame(resultados)

    resultados_df = resultados_df.sort_values(
        ["Ano", "Trimestre"]
    )

    

    arquivos_por_ano = {}

    for ano in resultados_df["Ano"].unique():

        df_ano = resultados_df[
            resultados_df["Ano"] == ano
        ]

        caminho_ano = os.path.join(
            pasta_resultados,
            f"{ano}_estatisticas.csv"
        )

        df_ano.to_csv(
            caminho_ano,
            index=False
        )

        arquivos_por_ano[ano] = caminho_ano


    return {
        "por_ano": arquivos_por_ano,
        "tabela_resultados": resultados_df
    }