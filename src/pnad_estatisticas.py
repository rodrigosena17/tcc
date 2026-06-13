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

    renda_escolaridade = []

    renda_horas_semanais = []

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

        df_escolaridade = (
            df.groupby("V3009A")["V403312"]
            .sum()
            .reset_index()
        )

        df_escolaridade["Ano"] = ano
        df_escolaridade["Trimestre"] = trimestre

        df_escolaridade = df_escolaridade.rename(
            columns={
                "V3009A": "Escolaridade",
                "V403312": "Renda_Total"
            }
        )

        renda_escolaridade.append(
            df_escolaridade
        )

        df_ocupados = df[df["V4001"] == 1]

        df_carteira_assinada = df[df["V4029"] == 1]

        df_servidor_publico = df[df["V4028"] == 1]

        df_conta_propria = df[df["V4012"] == 6]

        df_empregador = df[df["V4012"] == 5]

        total_pessoas = len(df)

        populacao_ponderada = (
            df["V1028"].sum()
            if "V1028" in df.columns
            else None
        )

        df_horas = (
            df.groupby("V4039")["V403312"]
            .sum()
            .reset_index()
        )

        df_horas["Ano"] = ano
        df_horas["Trimestre"] = trimestre

        df_horas = df_horas.rename(
            columns={
                "V4039": "Horas_Semanais",
                "V403312": "Renda_Total"
            }
        )

        renda_horas_semanais.append(
            df_horas
        )

        ocupados_total = len(df_ocupados)
        ocupados_renda_total = df_ocupados["V403312"].sum()
        ocupados_renda_media = df_ocupados["V403312"].mean()

        carteira_assinada_total = len(df_carteira_assinada)
        carteira_assinada_renda_total = df_carteira_assinada["V403312"].sum() 
        carteira_assinada_renda_media = df_carteira_assinada["V403312"].mean() 

        servidor_publico_total = len(df_servidor_publico)
        servidor_publico_renda_total = df_servidor_publico["V403312"].sum() 
        servidor_publico_renda_media = df_servidor_publico["V403312"].mean()
    
        conta_propria_total = len(df_conta_propria)
        conta_propria_renda_total = df_conta_propria["V403312"].sum()
        conta_propria_renda_media = df_conta_propria["V403312"].mean()

        empregador_total = len(df_empregador)
        empregador_renda_total = df_empregador["V403312"].sum()
        empregador_renda_media = df_empregador["V403312"].mean()

        taxa_ocupacao = (
            (ocupados_total / total_pessoas) * 100
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
            "Ocupados_total": ocupados_total,
            "Taxa_Ocupacao": taxa_ocupacao,
            "Ocupados_Renda_Total": ocupados_renda_total,
            "Ocupados_Renda_Media": ocupados_renda_media,
            "Carteira_Assinada_Total": carteira_assinada_total,
            "Carteira_Assinada_Renda_Total": carteira_assinada_renda_total,
            "Carteira_Assinada_Renda_Media": carteira_assinada_renda_media,
            "Servidor_Publico_Total": servidor_publico_total,
            "Servidor_Publico_Renda_Total": servidor_publico_renda_total,
            "Servidor_Publico_Renda_Media": servidor_publico_renda_media,
            "Conta_Propria_Total": conta_propria_total,
            "Conta_Propria_Renda_Total": conta_propria_renda_total,
            "Conta_Propria_Renda_Media": conta_propria_renda_media,
            "Empregador_Total": empregador_total,
            "Empregador_Renda_Total": empregador_renda_total,
            "Empregador_Renda_Media": empregador_renda_media,
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

    renda_escolaridade_df = pd.concat(
        renda_escolaridade,
        ignore_index=True
    )

    renda_horas_semanais_df = pd.concat(
        renda_horas_semanais,
        ignore_index=True
    )

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

        caminho_escolaridade = os.path.join(
            pasta_resultados,
            f"{ano}_renda_escolaridade.csv"
        )

        renda_escolaridade_df[renda_escolaridade_df["Ano"] == ano].to_csv(
            caminho_escolaridade,
            index=False
        )

        caminho_horas_semanais = os.path.join(
            pasta_resultados,
            f"{ano}_renda_horas_semanais.csv"
        )

        renda_horas_semanais_df[renda_horas_semanais_df["Ano"] == ano].to_csv(
            caminho_horas_semanais,
            index=False
        )

        arquivos_por_ano[ano] = caminho_ano


    return {
        "por_ano": arquivos_por_ano,
        "tabela_resultados": resultados_df
    }