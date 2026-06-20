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

    idade_renda = []

    tempo_trabalho_renda = []
    
    escolaridade_ocupacao = []
    
    escolaridade_carteira = []
    
    sexo_renda_escolaridade = []
    
    cor_raca_renda_escolaridade = []

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

        # Idade x renda
        
        df_idade = (
            df.groupby("V2009")["V403312"]
            .mean()
            .reset_index()
        )
        
        df_idade["Ano"] = ano
        df_idade["Trimestre"] = trimestre
        
        df_idade = df_idade.rename(
            columns={
                "V2009": "Idade",
                "V403312": "Renda_Media"
            }
        )
        
        idade_renda.append(df_idade)
        
        # Tempo de trabalho x renda
        
        df_tempo = (
            df.groupby("V4040")["V403312"]
            .mean()
            .reset_index()
        )
        
        df_tempo["Ano"] = ano
        df_tempo["Trimestre"] = trimestre
        
        df_tempo = df_tempo.rename(
            columns={
                "V4040": "Tempo_Trabalho",
                "V403312": "Renda_Media"
            }
        )
        
        tempo_trabalho_renda.append(
            df_tempo
        )
        
        
        # Escolaridade x ocupação
        
        df_escolaridade_ocupacao = (
            df.groupby("V3009A")["V4001"]
            .apply(
                lambda x:
                (x == 1).mean() * 100
            )
            .reset_index()
        )
        
        df_escolaridade_ocupacao["Ano"] = ano
        df_escolaridade_ocupacao["Trimestre"] = trimestre
        
        df_escolaridade_ocupacao = (
            df_escolaridade_ocupacao.rename(
                columns={
                    "V3009A": "Escolaridade",
                    "V4001": "Percentual_Ocupados"
                }
            )
        )
        
        escolaridade_ocupacao.append(
            df_escolaridade_ocupacao
        )
        
        
        # Escolaridade x carteira assinada
        
        df_escolaridade_carteira = (
            df.groupby("V3009A")["V4029"]
            .apply(
                lambda x:
                (x == 1).mean() * 100
            )
            .reset_index()
        )
        
        df_escolaridade_carteira["Ano"] = ano
        df_escolaridade_carteira["Trimestre"] = trimestre
        
        df_escolaridade_carteira = (
            df_escolaridade_carteira.rename(
                columns={
                    "V3009A": "Escolaridade",
                    "V4029": "Percentual_Carteira"
                }
            )
        )
        
        escolaridade_carteira.append(
            df_escolaridade_carteira
        )
        
        
        # Sexo x escolaridade x renda
        
        df_sexo = (
            df.groupby(
                ["V2007", "V3009A"]
            )["V403312"]
            .mean()
            .reset_index()
        )
        
        df_sexo["Ano"] = ano
        df_sexo["Trimestre"] = trimestre
        
        df_sexo = df_sexo.rename(
            columns={
                "V2007": "Sexo",
                "V3009A": "Escolaridade",
                "V403312": "Renda_Media"
            }
        )
        
        sexo_renda_escolaridade.append(
            df_sexo
        )
        
        
        # Cor/raça x escolaridade x renda
        
        df_raca = (
            df.groupby(
                ["V2010", "V3009A"]
            )["V403312"]
            .mean()
            .reset_index()
        )
        
        df_raca["Ano"] = ano
        df_raca["Trimestre"] = trimestre
        
        df_raca = df_raca.rename(
            columns={
                "V2010": "Cor_Raca",
                "V3009A": "Escolaridade",
                "V403312": "Renda_Media"
            }
        )
        
        cor_raca_renda_escolaridade.append(
            df_raca
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
        ocupados_ponderado = (
            df_ocupados["V1028"].sum()
            if "V1028" in df_ocupados.columns
            else None
        )
        ocupados_renda_total = df_ocupados["V403312"].sum()
        ocupados_renda_media = df_ocupados["V403312"].mean()

        carteira_assinada_total = len(df_carteira_assinada)
        carteira_assinada_ponderado = (
            df_carteira_assinada["V1028"].sum()
            if "V1028" in df_carteira_assinada.columns
            else None
        )
        carteira_assinada_renda_total = df_carteira_assinada["V403312"].sum() 
        carteira_assinada_renda_media = df_carteira_assinada["V403312"].mean() 

        servidor_publico_total = len(df_servidor_publico)
        servidor_publico_ponderado = (
            df_servidor_publico["V1028"].sum()
            if "V1028" in df_servidor_publico.columns
            else None
        )
        servidor_publico_renda_total = df_servidor_publico["V403312"].sum() 
        servidor_publico_renda_media = df_servidor_publico["V403312"].mean()
    
        conta_propria_total = len(df_conta_propria)
        conta_propria_ponderado = (
            df_conta_propria["V1028"].sum()
            if "V1028" in df_conta_propria.columns
            else None
        )
        conta_propria_renda_total = df_conta_propria["V403312"].sum()
        conta_propria_renda_media = df_conta_propria["V403312"].mean()

        empregador_total = len(df_empregador)
        empregador_ponderado = (
            df_empregador["V1028"].sum()
            if "V1028" in df_empregador.columns
            else None
        )
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

        percentual_conta_propria = (
            (df["V4012"] == 6).mean() * 100
            if "V4012" in df.columns
            else None
        )

        percentual_empregador = (
            (df["V4012"] == 5).mean() * 100
            if "V4012" in df.columns
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
            "Ocupados_Ponderado": ocupados_ponderado,
            "Taxa_Ocupacao": taxa_ocupacao,
            "Ocupados_Renda_Total": ocupados_renda_total,
            "Ocupados_Renda_Media": ocupados_renda_media,
            "Carteira_Assinada_Total": carteira_assinada_total,
            "Carteira_Assinada_Ponderado": carteira_assinada_ponderado,
            "Carteira_Assinada_Renda_Total": carteira_assinada_renda_total,
            "Carteira_Assinada_Renda_Media": carteira_assinada_renda_media,
            "Servidor_Publico_Total": servidor_publico_total,
            "Servidor_Publico_Ponderado": servidor_publico_ponderado,
            "Servidor_Publico_Renda_Total": servidor_publico_renda_total,
            "Servidor_Publico_Renda_Media": servidor_publico_renda_media,
            "Conta_Propria_Total": conta_propria_total,
            "Conta_Propria_Ponderado": conta_propria_ponderado,
            "Conta_Propria_Renda_Total": conta_propria_renda_total,
            "Conta_Propria_Renda_Media": conta_propria_renda_media,
            "Empregador_Total": empregador_total,
            "Empregador_Ponderado": empregador_ponderado,
            "Empregador_Renda_Total": empregador_renda_total,
            "Empregador_Renda_Media": empregador_renda_media,
            "Renda_Media": renda_media,
            "Renda_Mediana": renda_mediana,
            "Renda_Media_Ponderada": renda_media_ponderada,
            "Percentual_Carteira_Assinada": percentual_carteira,
            "Percentual_Servidor_Publico": percentual_servidor,
            "Percentual_Conta_Propria": percentual_conta_propria,
            "Percentual_Empregador": percentual_empregador,
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

    idade_renda_df = pd.concat(
        idade_renda,
        ignore_index=True
    )
    
    tempo_trabalho_renda_df = pd.concat(
        tempo_trabalho_renda,
        ignore_index=True
    )
    
    escolaridade_ocupacao_df = pd.concat(
        escolaridade_ocupacao,
        ignore_index=True
    )
    
    escolaridade_carteira_df = pd.concat(
        escolaridade_carteira,
        ignore_index=True
    )
    
    sexo_renda_escolaridade_df = pd.concat(
        sexo_renda_escolaridade,
        ignore_index=True
    )
    
    cor_raca_renda_escolaridade_df = pd.concat(
        cor_raca_renda_escolaridade,
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

        idade_renda_df[
            idade_renda_df["Ano"] == ano
        ].to_csv(
            os.path.join(
                pasta_resultados,
                f"{ano}_idade_renda.csv"
            ),
            index=False
        )
        
        
        tempo_trabalho_renda_df[
            tempo_trabalho_renda_df["Ano"] == ano
        ].to_csv(
            os.path.join(
                pasta_resultados,
                f"{ano}_tempo_trabalho_renda.csv"
            ),
            index=False
        )
        
        
        escolaridade_ocupacao_df[
            escolaridade_ocupacao_df["Ano"] == ano
        ].to_csv(
            os.path.join(
                pasta_resultados,
                f"{ano}_escolaridade_ocupacao.csv"
            ),
            index=False
        )
        
        
        escolaridade_carteira_df[
            escolaridade_carteira_df["Ano"] == ano
        ].to_csv(
            os.path.join(
                pasta_resultados,
                f"{ano}_escolaridade_carteira.csv"
            ),
            index=False
        )
        
        
        sexo_renda_escolaridade_df[
            sexo_renda_escolaridade_df["Ano"] == ano
        ].to_csv(
            os.path.join(
                pasta_resultados,
                f"{ano}_sexo_renda_escolaridade.csv"
            ),
            index=False
        )
        
        
        cor_raca_renda_escolaridade_df[
            cor_raca_renda_escolaridade_df["Ano"] == ano
        ].to_csv(
            os.path.join(
                pasta_resultados,
                f"{ano}_cor_raca_renda_escolaridade.csv"
            ),
            index=False
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
