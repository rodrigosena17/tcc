import pandas as pd
import numpy as np
import os

def organizar_pnad(caminho_txt, saida_txt_dir, saida_csv_dir):
    """
    Le o arquivo .txt da PNAD Continua, organiza conforme layout fixo,
    converte para DataFrame e salva versoes organizadas em saida_txt_dir e saida_csv_dir.
    """
    print(f"Lendo arquivo bruto: {caminho_txt}")

    # Definicao do layout fixo (estrutura das colunas)
    layout_data = {
        'variavel': [
            # ---- Parte 1 - Identificacao e Controle ----
            "Ano", "Trimestre", "UF", "Capital", "RM_RIDE", "UPA", "Estrato",
            "V1008", "V1014", "V1016", "V1022", "V1023", "V1027", "V1028",
            "V1029", "V1033", "posest", "posest_sxi",
            # ---- Ocupacao / Renda / Atividade ----
            "V4012", "V4013", "V40132A", "V4015", "V40151", "V401511",
            "V401512", "V4016", "V40161", "V40162", "V40163", "V4017",
            "V40171", "V401711", "V4018", "V40181", "V40182", "V40183",
            "V4019", "V4020", "V4021", "V4022", "V4024", "V4025", "V4026",
            "V4027", "V4028", "V4029", "V4032", "V4033", "V40331", "V403312",
            "V403322", "V4034", "V403412", "V403422", "V4039", "V4039C",
            "V4043", "V4044", "V4045", "V4046", "V4048", "V4050", "V40501",
            "V405012", "V4051", "V40511", "V405112", "V405122", "V405912",
            "V405922", "V4062", "V4062C", "V4063", "V4063A", "V4064", "V4064A"
        ],
        'start': [
            # ---- Parte 1 - Identificacao e Controle ----
            1, 5, 6, 8, 10, 12, 21, 28, 30, 32, 33, 34, 35, 50, 65, 74, 83, 86,
            # ---- Ocupacao / Renda / Atividade ----
            156, 158, 164, 166, 167, 168, 169, 171, 172, 173, 175, 177, 178,
            179, 180, 181, 182, 184, 186, 187, 188, 189, 190, 191, 192, 193,
            194, 195, 196, 197, 198, 200, 210, 220, 223, 233, 241, 244, 258,
            260, 265, 266, 268, 270, 271, 273, 293, 294, 296, 306, 348, 358,
            366, 369, 372, 373, 374, 375
        ],
        'width': [
            # ---- Parte 1 - Identificacao e Controle ----
            4, 1, 2, 2, 2, 9, 7, 2, 2, 1, 1, 1, 15, 15, 9, 9, 3, 3,
            # ---- Ocupacao / Renda / Atividade ----
            1, 5, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 1, 8, 8, 3, 3, 1, 5, 1, 1, 1, 1,
            1, 8, 1, 1, 8, 8, 8, 8, 3, 3, 1, 1, 1, 1
        ]
    }

    layout = pd.DataFrame(layout_data)
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

    # Conversoes numericas e pesos
    for col in df.columns:
        df[col] = pd.to_numeric(df[col].str.strip(), errors='coerce')

    # Normalizacao dos pesos (se vierem em escala inteira)
    if 'V1028' in df.columns and df['V1028'].max(skipna=True) > 1e6:
        df['V1028'] = df['V1028'] / 1e8

    if 'V1027' in df.columns and df['V1027'].max(skipna=True) > 1e6:
        df['V1027'] = df['V1027'] / 1e8

    # Filtro para Pernambuco (UF == 26)
    if "UF" in df.columns:
        df = df[df["UF"] == 26]
        print(f"Filtrado para Pernambuco: {df.shape[0]} linhas restantes.")

    # Salvamento do arquivo organizado (com nomes baseados no txt)
    nome_base = os.path.splitext(os.path.basename(caminho_txt))[0]
    caminho_saida_txt = os.path.join(saida_txt_dir, f"{nome_base}_organizado.txt")
    caminho_saida_csv = os.path.join(saida_csv_dir, f"{nome_base}_organizado.csv")

    # Salva em formato TXT (tabulado) e CSV
    df.to_csv(caminho_saida_txt, sep="\t", index=False)
    print(f"Arquivo organizado salvo em: {caminho_saida_txt}")

    df.to_csv(caminho_saida_csv, sep=",", index=False)
    print(f"Arquivo CSV salvo em: {caminho_saida_csv}")

    # Retorna os caminhos por se algum log externo precisar
    return caminho_saida_txt, caminho_saida_csv