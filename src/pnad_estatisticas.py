import os
import re
import pandas as pd
from typing import Dict, List, Any

def _extrair_ano_trimestre_do_nome(nome_arquivo: str):
    """
    Tenta extrair ano e trimestre a partir do nome do arquivo.
    Suporta nomes como:
      - PNADC_012024_organizado.csv  -> trimestre 01 -> 1 ; ano 2024
      - PNAD_02-2023_organizado.csv  -> trimestre 02 -> 2 ; ano 2023
      - PNADC_1T2024_organizado.csv  -> trimestre 1  ; ano 2024
      - 2023_T3_organizado.csv
    Retorna (ano:int|pd.NA, trimestre:int|pd.NA)
    """
    ano = pd.NA
    trimestre = pd.NA
    base = os.path.splitext(os.path.basename(nome_arquivo))[0]

    # 1) padrão PNADC_012024 (dois dígitos para trimestre + 4 para ano)
    m = re.search(r'[_\-\.](?P<tr>\d{2})(?P<yr>20\d{2}|19\d{2})', base)
    if m:
        try:
            trimestre = int(m.group('tr').lstrip('0')) if m.group('tr').lstrip('0') != '' else int(m.group('tr'))
        except:
            trimestre = pd.NA
        try:
            ano = int(m.group('yr'))
        except:
            ano = pd.NA
        return ano, trimestre

    # 2) padrão _T1_ ou _1T / _1_tri / _01-2024 etc
    m2 = re.search(r'(?:(T|t)[-_\.]?(?P<tr1>[1-4]))|(?P<tr2>[1-4])(?:[Tt]ri|[_\- ]tri)?[_\-\.]?(?P<yr2>20\d{2}|19\d{2})', base)
    if m2:
        tr = m2.group('tr1') or m2.group('tr2')
        try:
            trimestre = int(tr)
        except:
            trimestre = pd.NA
        yr = m2.group('yr2')
        if yr:
            try:
                ano = int(yr)
            except:
                ano = pd.NA
        # se ano não foi capturado aqui, tentaremos abaixo
    # 3) busca isolada de ano (4 dígitos)
    if pd.isna(ano):
        m_ano = re.search(r'(19|20)\d{2}', base)
        if m_ano:
            try:
                ano = int(m_ano.group(0))
            except:
                ano = pd.NA

    return ano, trimestre


def calcular_estatisticas(base_dir_organizados_csv: str, pasta_resultados: str) -> Dict[str, Any]:
    """
    Varre base_dir_organizados_csv por arquivos '*_organizado.csv', calcula as estatísticas por arquivo
    e salva um CSV por ano em pasta_resultados contendo as linhas (ano, trimestre, arquivo, ocupados_nao_ponderado,
    ocupados_ponderado, renda_total_ponderada).

    Retorna dicionário com caminhos dos arquivos gerados.
    """
    os.makedirs(pasta_resultados, exist_ok=True)

    # Encontrar arquivos *_organizado.csv
    arquivos: List[str] = []
    for root, _, files in os.walk(base_dir_organizados_csv):
        for f in files:
            if f.endswith("_organizado.csv"):
                arquivos.append(os.path.join(root, f))

    if not arquivos:
        print(f"Aviso: nenhum '*_organizado.csv' encontrado em {base_dir_organizados_csv}")
        return {}

    registros = []
    vistos = set()

    # colunas relevantes
    ocupado_col = 'V4012'
    peso_col = 'V1028'
    renda_cols_default = ['V403412', 'V405112']

    for caminho in sorted(arquivos):
        nome_base = os.path.basename(caminho)
        if nome_base in vistos:
            # evita processar mesmo nome duas vezes
            continue
        vistos.add(nome_base)

        # tenta ler o CSV
        try:
            df = pd.read_csv(caminho, low_memory=False)
        except Exception as e:
            print(f"Erro lendo {caminho}: {e} — pulando.")
            continue

        # converte colunas numéricas quando existirem
        if ocupado_col in df.columns:
            df[ocupado_col] = pd.to_numeric(df[ocupado_col], errors='coerce')
        if peso_col in df.columns:
            df[peso_col] = pd.to_numeric(df[peso_col], errors='coerce')
        for rc in renda_cols_default:
            if rc in df.columns:
                df[rc] = pd.to_numeric(df[rc], errors='coerce')

        # extrai ano/trimestre do próprio CSV (colunas) se presentes
        ano = pd.NA
        trimestre = pd.NA
        if 'Ano' in df.columns and df['Ano'].notna().any():
            vals = pd.to_numeric(df['Ano'], errors='coerce').dropna().unique()
            if len(vals) >= 1:
                # pega o primeiro (normalmente único)
                ano = int(vals[0])
        if 'Trimestre' in df.columns and df['Trimestre'].notna().any():
            vals = pd.to_numeric(df['Trimestre'], errors='coerce').dropna().unique()
            if len(vals) >= 1:
                trimestre = int(vals[0])

        # se não obteve, extrai do nome do arquivo (padrão PNADC_012024_organizado.csv)
        if pd.isna(ano) or pd.isna(trimestre):
            ano_n, tri_n = _extrair_ano_trimestre_do_nome(nome_base)
            if pd.isna(ano) and not pd.isna(ano_n):
                ano = ano_n
            if pd.isna(trimestre) and not pd.isna(tri_n):
                trimestre = tri_n

        # cálculos solicitados
        # 1) ocupados não ponderado
        if ocupado_col in df.columns:
            ocupados_nao_ponderado = int((df[ocupado_col] == 1).sum())
        else:
            ocupados_nao_ponderado = pd.NA

        # 2) ocupados ponderado
        if (ocupado_col in df.columns) and (peso_col in df.columns):
            ocupados_ponderado = float(((df[ocupado_col] == 1) * df[peso_col].fillna(0)).sum())
        else:
            ocupados_ponderado = pd.NA

        # 3) renda total ponderada
        renda_cols = [c for c in renda_cols_default if c in df.columns]
        if renda_cols and (peso_col in df.columns):
            renda_total = df[renda_cols].sum(axis=1, skipna=True)
            renda_total_ponderada = float((renda_total * df[peso_col].fillna(0)).sum())
        else:
            renda_total_ponderada = pd.NA

        registros.append({
            "ano": int(ano) if not pd.isna(ano) else pd.NA,
            "trimestre": int(trimestre) if not pd.isna(trimestre) else pd.NA,
            "arquivo": nome_base,
            "ocupados_nao_ponderado": ocupados_nao_ponderado,
            "ocupados_ponderado": ocupados_ponderado,
            "renda_total_ponderada": renda_total_ponderada
        })

    # montar DataFrame e salvar por ano
    resultados_df = pd.DataFrame(registros)

    # ordenar por ano/trimestre quando possível
    if not resultados_df.empty:
        if 'ano' in resultados_df.columns and 'trimestre' in resultados_df.columns:
            resultados_df = resultados_df.sort_values(['ano', 'trimestre'], na_position='last')

    arquivos_por_ano = {}
    anos_detectados = resultados_df['ano'].dropna().unique() if 'ano' in resultados_df.columns else []

    for a in sorted(anos_detectados):
        df_a = resultados_df[resultados_df['ano'] == a].copy()
        caminho_ano = os.path.join(pasta_resultados, f"{int(a)}_estatisticas_trimestrais.csv")
        df_a.to_csv(caminho_ano, index=False)
        arquivos_por_ano[int(a)] = caminho_ano

    # salva também um combinado opcional (todas as linhas)
    caminho_combinado = os.path.join(pasta_resultados, "estatisticas_trimestrais_completo.csv")
    resultados_df.to_csv(caminho_combinado, index=False)

    retorno = {
        "combinado": caminho_combinado,
        "por_ano": arquivos_por_ano,
        "tabela_resultados": resultados_df
    }
    return retorno