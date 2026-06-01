import pandas as pd
import numpy as np
import os

def organizar_pnad(caminho_txt, saida_txt_dir, saida_csv_dir):
    """
    Lê o arquivo .txt da PNAD Contínua (Trimestral), organiza conforme layout fixo,
    converte para DataFrame e salva versões organizadas em TXT e CSV.
    """
    print(f"Lendo arquivo bruto: {caminho_txt}")

    # Definição do layout fixo exato baseado no Dicionário Trimestral
    layout_data = {
        'variavel': [
            "Ano", "Trimestre", "UF",
            "V1028",   # Peso do domicílio e das pessoas com calibração
            "V2007",   # Sexo
            "V2009",   # Idade
            "V2010",   # Cor/Raça
            "V3009A",  # Nível educacional
            "V3014",   # Concluiu o curso que frequentou
            "V4001",   # Trabalhou ou estagiou, pelo menos 1 hora
            "V4010",   # Cargo/função
            "V4012",   # Posição no trabalho
            "V4013",   # Principal atividade desse negócio
            "V4028",   # Servidor público
            "V4029",   # Carteira assinada
            "V403312", # Rendimento bruto mensal em reais
            "V4039",   # Horas trabalhadas por semana
            "V4040",   # Quanto tempo de trabalho
            "V4071"    # Providência para conseguir trabalho
        ],
        'start': [
            1, 5, 6,       # Ano, Trimestre, UF [1]
            50,            # V1028 [2]
            95,            # V2007 [3]
            104,           # V2009 [4]
            107,           # V2010 [4]
            125,           # V3009A [5]
            135,           # V3014 [6]
            136,           # V4001 [7]
            152,           # V4010 [8]
            156,           # V4012 [8]
            158,           # V4013 [9]
            194,           # V4028 [10]
            195,           # V4029 [10]
            200,           # V403312 [11]
            241,           # V4039 [12]
            247,           # V4040 [13]
            376            # V4071 [14]
        ],
        'width': [
            4, 1, 2,       # Ano, Trimestre, UF [1]
            15,            # V1028 [2]
            1,             # V2007 [3]
            3,             # V2009 [4]
            1,             # V2010 [4]
            2,             # V3009A [5]
            1,             # V3014 [6]
            1,             # V4001 [7]
            4,             # V4010 [8]
            1,             # V4012 [8]
            5,             # V4013 [9]
            1,             # V4028 [10]
            1,             # V4029 [10]
            8,             # V403312 [11]
            3,             # V4039 [12]
            1,             # V4040 [13]
            1              # V4071 [14]
        ]
    }

    layout = pd.DataFrame(layout_data)
    
    # O read_fwf do pandas requer que as posições tenham base zero (start - 1)
    fwf_cols = list(zip(layout['start'] - 1, layout['start'] - 1 + layout['width']))

    # Leitura do arquivo FWF (fixed-width format)
    df = pd.read_fwf(
        caminho_txt,
        colspecs=fwf_cols,
        names=layout['variavel'],
        dtype=str,
        encoding='latin1'
    )

    print(f"Arquivo carregado: {df.shape[0]} linhas, {df.shape[1]} colunas")

    # Conversões numéricas para evitar erros de tipagem
    for col in df.columns:
        df[col] = pd.to_numeric(df[col].str.strip(), errors='coerce')

    # Normalização dos pesos (se vierem em escala inteira do IBGE)
    if 'V1028' in df.columns and df['V1028'].max(skipna=True) > 1e6:
        df['V1028'] = df['V1028'] / 1e8

    # Filtro para Pernambuco (UF == 26) conforme as bases do seu projeto
    if "UF" in df.columns:
        df = df[df["UF"] == 26]
        print(f"Filtrado para Pernambuco: {df.shape} linhas restantes.")

    # Salvamento do arquivo organizado
    nome_base = os.path.splitext(os.path.basename(caminho_txt))[0]
    
    # Validação e criação dos diretórios, caso não existam (Boa prática)
    os.makedirs(saida_txt_dir, exist_ok=True)
    os.makedirs(saida_csv_dir, exist_ok=True)
    
    caminho_saida_txt = os.path.join(saida_txt_dir, f"{nome_base}_organizado.txt")
    caminho_saida_csv = os.path.join(saida_csv_dir, f"{nome_base}_organizado.csv")

    # Salva em formato TXT (separado por tabulação) e CSV
    df.to_csv(caminho_saida_txt, sep="\t", index=False)
    print(f"Arquivo organizado salvo em: {caminho_saida_txt}")

    df.to_csv(caminho_saida_csv, sep=",", index=False)
    print(f"Arquivo CSV salvo em: {caminho_saida_csv}")

    return caminho_saida_txt, caminho_saida_csv